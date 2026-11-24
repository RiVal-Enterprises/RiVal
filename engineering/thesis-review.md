# Review: "Käekella erilahenduse arendus" (TalTech BSc, 2019)

Source: Drive folder `1nC5htM5GOIFBuYi-r45ZtDWuperkLSeg` (thesis PDF, 15 part drawings, SolidWorks + STEP files).

## Keep

- The **Celestial concept**: 12 hour-"planets" where only the current hour turns to face the viewer, plus a rocket orbiting as the minute hand. Distinctive, on-brand.
- The **process**: concepts → scored selection → top-down decomposition → CAD → drawings → 2:1 SLS prototype (Formiga P100, PA12) → CNC toolpaths → cost model.
- Bevel-pinion flip of the spheres via a toothed sector (60° sector, 12 teeth, two spheres meshed at a time) is a neat idea and stays.
- The 300° locking band that keeps idle spheres from rotating stays (becomes the jumper/locking ring).

## Change

| Thesis | Problem | v2 |
|---|---|---|
| Geneva (12 slots) driven 1×/h | Driver engaged 150° → hour change takes **~25 min**; spheres half-turned for ~40 % of the time | Snail cam + jumper spring: energy taken smoothly over the hour, **jump < 50 ms** |
| Load 0.61 N·mm compared with **mainspring** torque (7 N·mm, ETA 2892) | Wrong reference: torque at the centre arbor is ~1-2 N·mm and only ~5 % of it can be spared; the cannon-pinion clutch would slip | Budget at the centre arbor (see `celestial_v2/report.md`): v1 load ≈ 0.39 N·mm vs ≈ 0.07 N·mm allowed |
| Friction = μ·m·g with dry μ (steel-steel 0.78) | Not how watches lose energy (lubricated jewelled pivots, mesh losses, impacts) | Pivot-radius friction with lubricated μ, ruby-roller ring support |
| 55 × 20 mm, module 0.5 involute | Desk-clock size | ~44 mm case, module 0.08-0.2, watch (cycloidal) profiles |
| 12 g of solid brass display parts | ~100x too heavy | Hollow Ti or cast-silver shells (40-90 mg each), skeletonised Ti disc, Al minute ring: ~1-2 g total |
| High-carbon steel base plate | Magnetic and corrodes next to the escapement | Brass (plated) or Ti / 316L |
| Cost: €22 / plate @ 1000 pcs, €30/h machine | Unrealistic for 10-100 pcs | Re-cost per process in `suppliers/` |
| Every part machined in-house | Tolerances and cost | Buy movement, jewels, springs, screws, crystals; outsource micro parts; make only the signature parts |

## Open questions

- Hour-sphere numerals: engraved, enamel-filled, or lume? (Latvian engraving partner)
- Rocket minute hand: cast silver vs. printed Ti; balance it on the ring to avoid positional error
- Prior-art search for "rotating/flipping hour satellites" (Urwerk satellite cubes, Barrelhand Geneva hour) before any public posting. See `DECISIONS.md` D-004 (IP).
