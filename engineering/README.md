# Engineering

Calculation models, design reviews and bench-test protocols. Every model here is meant to be
**re-run with measured values**: assumptions are tagged `VERIFY` in the code.

| Folder | What |
|---|---|
| [`celestial_v2/`](celestial_v2/) | Energy & timing model for the Celestial planetary jump-hour on a Seagull ST36 base. Run `python3 model.py > report.md`. Latest output: [`report.md`](celestial_v2/report.md) |
| [`thesis-review.md`](thesis-review.md) | What the 2019 TalTech thesis got right and what must change |

## Engineering rules of thumb we design to

1. **Budget at the centre arbor, not the mainspring.** The display is driven from the minute/centre arbor (1 rev/h). Torque there ≈ mainspring torque ÷ (centre-wheel turns per barrel turn) × efficiency, about **1-2 N·mm on a 6497/ST36**, roughly 10x less than the mainspring figure.
2. **The display may take ~5 % average / ~10 % peak of that** (design rule, to be confirmed on the timegrapher). That is **tens of µN·m**, which means milligram-scale parts.
3. **Never load the cannon-pinion clutch beyond its slip torque.** It is a friction fit designed to slip for hand-setting.
4. **Jumps must be spring-driven.** Charge a jumper spring slowly over the hour (snail cam), release in < 50 ms. A Geneva driven 1x/hour takes ~25 min to change hour.
5. **Mass is the enemy:** hollow / titanium / aluminium / skeletonised parts, jewel or ruby-roller supports, no dry sliding of rings.
6. **Buy before you make:** movements, jewels, screws, springs, crowns, crystals, gaskets, hands are bought. We make only what makes the watch *ours* (display parts, case, dial, sculptural parts).

## Bench measurements (cheap, do these first, about 1 evening)

Replace the `VERIFY` values in `celestial_v2/model.py` with these:

| # | Measure | How | Gear needed |
|---|---|---|---|
| B1 | **Amplitude vs. added load** at the centre arbor | Timegrapher reading in 6 positions, then add a tiny friction brake / thread + weight on a pulley on the cannon pinion and log amplitude drop per added µN·m. This calibrates rule 2. | Timegrapher (Weishi 1900 / 1000 class) |
| B2 | **Cannon-pinion slip torque** | Light lever (e.g. a hand blank) on the cannon pinion, add known weights at a known radius until it slips | Micro scale 0.001 g, lever |
| B3 | **Mainspring torque**, let-down → full wind | Lever on the barrel arbor or crown with weights, or a cheap torque gauge | Same |
| B4 | **Barrel turns from let-down to full** | Count ratchet-wheel turns | None |
| B5 | **Power reserve** | Full wind, timegrapher or log until stop | None |

## Next engineering steps (Celestial v2)

- [ ] Order 2-3 Seagull ST3600 (about €30-50 each, see `suppliers/`) and run B1-B5
- [ ] Re-run model with measured values; fix allowable-load rule
- [ ] Choose snail-cam / jumper layout (study existing jump-hour modules: Dubois-Dépraz jump hour, Chinese 8215 jump-hour/wandering-hour modules as cheap teardown references)
- [ ] Re-dimension to a ~44 mm case: spheres Ø3-3.5 mm, module height budget ≤ 4 mm above the movement
- [ ] Gear train redesign with watch-standard profiles (NIHS 20-25 cycloidal) and small modules (m 0.08-0.2), using bought wheels/pinions where possible
- [ ] Proof of concept: 2:1 resin print (micro-SLA) running on the ST36, then 1:1 metal
