#!/usr/bin/env python3
"""
Celestial v2 - first-order energy & timing model on a Seagull ST36 (ETA/Unitas 6497 clone) base.

Purpose
-------
Replace the 2019 thesis "friction = mu*m*g" estimate with a model that asks the
question that actually decides feasibility:

    Can the base movement drive this display without (a) slipping the cannon-pinion
    clutch and (b) robbing the escapement of so much torque that amplitude collapses?

Everything is SI internally (kg, m, N, N*m, s). Output is printed as g, mm, N*mm, ms.

IMPORTANT: every number tagged VERIFY in PARAMS is an assumption, not a measured value.
The model is built so that you replace those with bench measurements (see README.md,
"Bench measurements") and re-run. Run:  python3 model.py > report.md
Standard library only.
"""

import math
from dataclasses import dataclass, field

G = 9.81  # m/s^2

DENSITY = {  # kg/m^3
    "brass": 8500.0,
    "titanium_gr5": 4430.0,
    "aluminium_7075": 2810.0,
    "zirconia": 6050.0,
    "pa12_print": 1010.0,
    "silver925": 10400.0,
}

# --------------------------------------------------------------------------------------
# Base movement parameters (Seagull ST3600 / ETA 6497 class)
# --------------------------------------------------------------------------------------
MOVEMENT = {
    "name": "Seagull ST3600 (ETA/Unitas 6497-1 clone)",
    "diameter_mm": 36.6,          # 16.5 lignes
    "height_mm": 4.5,
    "beat_rate_vph": 18000,       # 2.5 Hz
    "power_reserve_h": 44.0,      # VERIFY: Seagull spec sheets quote ~40-46 h
    "barrel_turns_full_wind": 6.0,  # VERIFY: count crown->barrel turns from let-down to full
    "barrel_torque_Nmm": {        # VERIFY: measure with a mainspring torque gauge or
        "low": 8.0,               #         lever + weights on the barrel arbor
        "nominal": 12.0,
        "high": 16.0,
    },
    "train_efficiency_to_center": 0.85,  # barrel->center wheel mesh efficiency (2 meshes)
    # Design rule (VERIFY on timegrapher): extra average load on the centre arbor
    # should stay below this fraction of the torque arriving there, peak below the 2nd.
    "allowable_avg_fraction": 0.05,
    "allowable_peak_fraction": 0.10,
    # Cannon pinion friction clutch slip torque. VERIFY: measure (see README).
    "cannon_pinion_slip_Nmm": 0.25,
}


def center_wheel_torque_Nmm(barrel_torque_Nmm: float) -> float:
    """Torque arriving at the centre (minute) arbor, which turns once per hour."""
    ratio = MOVEMENT["power_reserve_h"] / MOVEMENT["barrel_turns_full_wind"]  # centre turns per barrel turn
    return barrel_torque_Nmm / ratio * MOVEMENT["train_efficiency_to_center"]


# --------------------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------------------
def sphere_mass(d_mm: float, material: str, wall_mm: float | None = None) -> float:
    r = d_mm / 2 / 1000
    v = 4 / 3 * math.pi * r**3
    if wall_mm is not None:
        ri = max(r - wall_mm / 1000, 0.0)
        v -= 4 / 3 * math.pi * ri**3
    return v * DENSITY[material]


def sphere_inertia_own_axis(m: float, d_mm: float, hollow: bool) -> float:
    r = d_mm / 2 / 1000
    return (2 / 3 if hollow else 2 / 5) * m * r**2  # thin shell ~ 2/3 m r^2 (upper bound)


def annulus_mass(od_mm: float, id_mm: float, t_mm: float, material: str, fill: float = 1.0) -> float:
    a = math.pi / 4 * ((od_mm / 1000) ** 2 - (id_mm / 1000) ** 2)
    return a * (t_mm / 1000) * DENSITY[material] * fill


def annulus_inertia(m: float, od_mm: float, id_mm: float) -> float:
    return 0.5 * m * ((od_mm / 2000) ** 2 + (id_mm / 2000) ** 2)


# --------------------------------------------------------------------------------------
# Mechanisms
# --------------------------------------------------------------------------------------
def geneva_engagement(n_slots: int, driver_period_s: float):
    """External Geneva: driver engaged for (180 - 360/n) deg of each revolution."""
    engaged_deg = 180.0 - 360.0 / n_slots
    return engaged_deg, engaged_deg / 360.0 * driver_period_s


@dataclass
class Design:
    name: str
    hour_mode: str                 # "geneva_continuous" or "snail_jump"
    sphere_d_mm: float
    sphere_material: str
    sphere_wall_mm: float | None   # None = solid
    drive_disc_od_mm: float        # rotating hour-drive disc/sector carrier
    drive_disc_id_mm: float
    drive_disc_t_mm: float
    drive_disc_material: str
    drive_disc_fill: float         # 1.0 solid, <1 skeletonised
    minute_ring_od_mm: float
    minute_ring_id_mm: float
    minute_ring_t_mm: float
    minute_ring_material: str
    minute_ring_fill: float
    minute_ring_support: str       # "sliding_dry" | "sliding_lubricated" | "ruby_rollers"
    pivot_r_mm: float              # effective pivot / post radius of the hour drive
    pivot_mu: float
    jump_time_ms: float = 40.0     # target duration of the hour jump (snail mode)
    sphere_ratio: float = 6.0      # sphere rotation / drive rotation (30 deg step -> 180 deg flip)
    spheres_moving: int = 2
    gear_eff_display: float = 0.90 # efficiency of the display gearing (bevel + spurs)
    cam_eff: float = 0.70          # snail/jumper energy efficiency
    spring_safety: float = 1.5
    notes: list = field(default_factory=list)


RING_SUPPORT_MU = {"sliding_dry": 0.35, "sliding_lubricated": 0.15, "ruby_rollers": 0.02}


def analyse(d: Design):
    out = {}
    # masses
    m_s = sphere_mass(d.sphere_d_mm, d.sphere_material, d.sphere_wall_mm)
    m_disc = annulus_mass(d.drive_disc_od_mm, d.drive_disc_id_mm, d.drive_disc_t_mm, d.drive_disc_material, d.drive_disc_fill)
    m_ring = annulus_mass(d.minute_ring_od_mm, d.minute_ring_id_mm, d.minute_ring_t_mm, d.minute_ring_material, d.minute_ring_fill)
    out["sphere_mass_g"] = m_s * 1000
    out["all_spheres_g"] = 12 * m_s * 1000
    out["drive_disc_g"] = m_disc * 1000
    out["minute_ring_g"] = m_ring * 1000

    # --- minute ring: continuous load, 1 rev/h, driven 1:1 from centre arbor
    mu_ring = RING_SUPPORT_MU[d.minute_ring_support]
    r_ring = (d.minute_ring_od_mm + d.minute_ring_id_mm) / 4 / 1000
    t_ring = mu_ring * m_ring * G * r_ring / d.gear_eff_display ** 3  # 3 meshes in the transfer train
    out["minute_ring_load_Nmm"] = t_ring * 1000

    # --- hour display
    theta = 2 * math.pi / 12
    j_disc = annulus_inertia(m_disc, d.drive_disc_od_mm, d.drive_disc_id_mm)
    j_sph = sphere_inertia_own_axis(m_s, d.sphere_d_mm, d.sphere_wall_mm is not None)
    j_total = j_disc + d.spheres_moving * j_sph * d.sphere_ratio**2
    # friction torque on the hour drive (dial-up worst case: full weight on the pivot)
    t_fric = d.pivot_mu * (m_disc + 0) * G * (d.pivot_r_mm / 1000)
    t_fric += d.spheres_moving * d.pivot_mu * m_s * G * 0.0003 * d.sphere_ratio  # sphere pivots r~0.3mm, reflected
    out["hour_inertia_gmm2"] = j_total * 1e9
    out["hour_friction_Nmm"] = t_fric * 1000

    if d.hour_mode == "geneva_continuous":
        eng_deg, eng_s = geneva_engagement(12, 3600.0)
        out["hour_change_duration"] = f"{eng_s/60:.0f} min (Geneva engaged {eng_deg:.0f} deg of each hour)"
        # Geneva kinematic peak ratio (driven/driver angular speed) for n=12 at mid-engagement
        n = 12
        a = math.sin(math.pi / n)          # crank radius / centre distance
        peak_ratio = a / (1 - a)            # omega_wheel / omega_driver at the line of centres
        t_wheel = t_fric / d.gear_eff_display
        # torque on the driver = wheel torque * (omega_wheel/omega_driver)
        avg = t_wheel * (theta / (2 * math.pi))   # work conservation over one driver turn
        peak = t_wheel * peak_ratio
        out["avg_load_Nmm"] = (t_ring + avg) * 1000
        out["peak_load_Nmm"] = (t_ring + peak) * 1000
        out["note"] = "slow ~25 min transition; low torque but spheres half-turned for long periods"
    else:  # snail_jump
        t_jump = d.jump_time_ms / 1000
        t_acc = 2 * theta * j_total / t_jump**2           # constant-torque acceleration over theta
        t_drive = (t_acc + t_fric) / d.gear_eff_display
        e_jump = t_drive * theta                           # J, energy released per hour
        e_spring = e_jump * d.spring_safety
        avg = e_spring / (2 * math.pi) / d.cam_eff         # snail rotates once per hour
        peak = avg * 1.6                                   # non-linear jumper spring + snail profile
        out["hour_change_duration"] = f"{d.jump_time_ms:.0f} ms jump (spring charged over the hour)"
        out["jump_energy_uJ"] = e_spring * 1e6
        out["avg_load_Nmm"] = (t_ring + avg) * 1000
        out["peak_load_Nmm"] = (t_ring + peak) * 1000
        out["note"] = "instant jump; energy taken smoothly over the hour"
    return out


def verdict(load_avg, load_peak, barrel_Nmm):
    tc = center_wheel_torque_Nmm(barrel_Nmm)
    ok_avg = load_avg <= MOVEMENT["allowable_avg_fraction"] * tc
    ok_peak = load_peak <= MOVEMENT["allowable_peak_fraction"] * tc
    ok_clutch = load_peak <= MOVEMENT["cannon_pinion_slip_Nmm"] / 1.5
    return tc, ok_avg, ok_peak, ok_clutch


# --------------------------------------------------------------------------------------
# Scenarios
# --------------------------------------------------------------------------------------
V1_THESIS = Design(
    name="v1 - 2019 thesis geometry (brass, Geneva, 6 mm solid spheres)",
    hour_mode="geneva_continuous",
    sphere_d_mm=6.0, sphere_material="brass", sphere_wall_mm=None,
    drive_disc_od_mm=27.0, drive_disc_id_mm=3.0, drive_disc_t_mm=1.6, drive_disc_material="brass", drive_disc_fill=1.0,
    minute_ring_od_mm=50.0, minute_ring_id_mm=43.0, minute_ring_t_mm=0.8, minute_ring_material="brass", minute_ring_fill=1.0,
    minute_ring_support="sliding_dry", pivot_r_mm=1.5, pivot_mu=0.35,
)

V2_JUMP_BRASS = Design(
    name="v2a - snail jump-hour, same brass parts",
    hour_mode="snail_jump",
    sphere_d_mm=6.0, sphere_material="brass", sphere_wall_mm=None,
    drive_disc_od_mm=27.0, drive_disc_id_mm=3.0, drive_disc_t_mm=1.6, drive_disc_material="brass", drive_disc_fill=1.0,
    minute_ring_od_mm=50.0, minute_ring_id_mm=43.0, minute_ring_t_mm=0.8, minute_ring_material="brass", minute_ring_fill=1.0,
    minute_ring_support="sliding_lubricated", pivot_r_mm=0.5, pivot_mu=0.15,
)

V2_LIGHT = Design(
    name="v2b - snail jump-hour, wrist-sized & lightweight (proposal)",
    hour_mode="snail_jump",
    sphere_d_mm=3.2, sphere_material="titanium_gr5", sphere_wall_mm=0.35,
    drive_disc_od_mm=20.0, drive_disc_id_mm=2.0, drive_disc_t_mm=0.6, drive_disc_material="titanium_gr5", drive_disc_fill=0.45,
    minute_ring_od_mm=40.0, minute_ring_id_mm=36.0, minute_ring_t_mm=0.4, minute_ring_material="aluminium_7075", minute_ring_fill=0.8,
    minute_ring_support="ruby_rollers", pivot_r_mm=0.15, pivot_mu=0.15,
    notes=["Ti spheres hollow 0.35 mm wall, could be cast silver shells instead (heavier: re-run)",
           "drive disc skeletonised to 45% material", "minute ring on 3 ruby rollers"],
)

V2_LIGHT_SILVER = Design(
    name="v2c - as v2b but cast silver-alloy spheres (family casting)",
    hour_mode="snail_jump",
    sphere_d_mm=3.2, sphere_material="silver925", sphere_wall_mm=0.35,
    drive_disc_od_mm=20.0, drive_disc_id_mm=2.0, drive_disc_t_mm=0.6, drive_disc_material="titanium_gr5", drive_disc_fill=0.45,
    minute_ring_od_mm=40.0, minute_ring_id_mm=36.0, minute_ring_t_mm=0.4, minute_ring_material="aluminium_7075", minute_ring_fill=0.8,
    minute_ring_support="ruby_rollers", pivot_r_mm=0.15, pivot_mu=0.15,
    notes=["hollow lost-wax cast shells - wall thickness 0.35 mm is at the limit of casting; may need 0.5 mm (re-run)"],
)

SCENARIOS = [V1_THESIS, V2_JUMP_BRASS, V2_LIGHT, V2_LIGHT_SILVER]


def main():
    print("# Celestial v2 - energy & timing report\n")
    print("_Generated by `engineering/celestial_v2/model.py`. First-order model; values tagged VERIFY are assumptions._\n")
    print(f"**Base movement:** {MOVEMENT['name']} - {MOVEMENT['diameter_mm']} mm, {MOVEMENT['height_mm']} mm, "
          f"{MOVEMENT['beat_rate_vph']} vph, ~{MOVEMENT['power_reserve_h']:.0f} h\n")

    print("## Torque available at the centre (minute) arbor\n")
    print("| Mainspring torque (VERIFY) | Torque at centre arbor | 5 % avg budget | 10 % peak budget |")
    print("|---|---|---|---|")
    for k, v in MOVEMENT["barrel_torque_Nmm"].items():
        tc = center_wheel_torque_Nmm(v)
        print(f"| {k}: {v:.1f} N*mm | {tc:.3f} N*mm | {0.05*tc:.4f} N*mm | {0.10*tc:.4f} N*mm |")
    print(f"\nCannon-pinion clutch slip torque (VERIFY): {MOVEMENT['cannon_pinion_slip_Nmm']} N*mm "
          f"-> allowed peak with SF 1.5: {MOVEMENT['cannon_pinion_slip_Nmm']/1.5:.3f} N*mm\n")
    print("> The 2019 thesis compared its 0.61 N*mm load with the *mainspring* torque (7 N*mm, ETA 2892). "
          "The relevant number is the torque at the centre arbor, roughly an order of magnitude smaller, "
          "of which only a few percent can be spared for the display.\n")

    print("## Scenario results\n")
    print("| Scenario | Spheres (12x) | Drive disc | Minute ring | Hour change | Avg load | Peak load | Avg OK* | Peak OK* | Clutch OK |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    nominal = MOVEMENT["barrel_torque_Nmm"]["nominal"]
    for d in SCENARIOS:
        r = analyse(d)
        tc, ok_a, ok_p, ok_c = verdict(r["avg_load_Nmm"], r["peak_load_Nmm"], nominal)
        yn = lambda b: "yes" if b else "**NO**"
        print(f"| {d.name} | {r['all_spheres_g']:.2f} g | {r['drive_disc_g']:.2f} g | {r['minute_ring_g']:.2f} g "
              f"| {r['hour_change_duration']} | {r['avg_load_Nmm']:.4f} N*mm | {r['peak_load_Nmm']:.4f} N*mm "
              f"| {yn(ok_a)} | {yn(ok_p)} | {yn(ok_c)} |")
    print(f"\n\\* against the nominal mainspring case (centre arbor {center_wheel_torque_Nmm(nominal):.3f} N*mm).\n")

    print("## Details per scenario\n")
    for d in SCENARIOS:
        r = analyse(d)
        print(f"### {d.name}\n")
        print(f"- Sphere: {d.sphere_d_mm} mm {d.sphere_material}{' hollow '+str(d.sphere_wall_mm)+' mm wall' if d.sphere_wall_mm else ' solid'} "
              f"= {r['sphere_mass_g']*1000:.0f} mg each")
        print(f"- Minute ring load ({d.minute_ring_support}): {r['minute_ring_load_Nmm']:.4f} N*mm")
        print(f"- Hour drive friction: {r['hour_friction_Nmm']:.4f} N*mm; reflected inertia {r['hour_inertia_gmm2']:.2f} g*mm^2")
        if "jump_energy_uJ" in r:
            print(f"- Jump energy stored per hour (incl. SF {d.spring_safety}): {r['jump_energy_uJ']:.2f} uJ")
        print(f"- Behaviour: {r['note']}")
        for n in d.notes:
            print(f"- Note: {n}")
        print()

    print("## Sensitivity: which scenarios survive a weak mainspring?\n")
    print("| Scenario | low | nominal | high |")
    print("|---|---|---|---|")
    for d in SCENARIOS:
        r = analyse(d)
        cells = []
        for k, v in MOVEMENT["barrel_torque_Nmm"].items():
            _, a, p, c = verdict(r["avg_load_Nmm"], r["peak_load_Nmm"], v)
            cells.append("pass" if (a and p and c) else "fail")
        print(f"| {d.name} | " + " | ".join(cells) + " |")

    print("\n## Geneva timing reference\n")
    print("| Slots | Engaged angle | Duration if driver turns 1x/hour |")
    print("|---|---|---|")
    for n in (4, 6, 8, 12):
        a, s = geneva_engagement(n, 3600)
        print(f"| {n} | {a:.0f} deg | {s/60:.1f} min |")
    print("\nA Geneva driven once per hour can never give a crisp jump; it needs either a fast driver "
          "with a reduction after it, or (recommended) a snail cam + jumper that stores energy over the hour.\n")


if __name__ == "__main__":
    main()
