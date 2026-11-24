# Suppliers

`suppliers.csv` is the database (open it in Google Sheets / Excel). One row per supplier, with a source URL and a `verified` date for every claim.

**status:** `partner` (working with) · `quoted` (have a quote) · `lead` (found, credible) · `unverified` (known name, not yet checked) · `rejected` (with reason in notes).

## Sourcing map: which process for which part

| Part | Prototype (1-5 pcs) | Small batch (50-300) |
|---|---|---|
| Base movement | Seagull ST3600 via eBay/parts houses (S006-S008) | Alibaba/Seagull direct (S009), Sellita via S001/S002 |
| Display gears, sectors, jumper, snail | Micro-SLA resin for fit/function (S016/S017) → LIGA or micro-EDM metal (S018) | LIGA (S018), Chinese micro-gear makers (TBD) |
| Planets, rocket, sculptural parts | Cast in-house (S022) or micro metal print (S019) | Cast in-house |
| Module plate, bridges | CNC 1-pc (S014/S015) or Latvia (S023) | Latvia / photo-etching (TBD) |
| Case | Cast (S022) + CNC finish (S023) / CNC 1-pc (S014) | Same, or OEM (S013) |
| Dial | Latvia engraving / in-house | Dial maker (TBD) |
| Crystal, crown, gaskets, caseback | Parts houses (S001-S005), AliExpress | OEM (S013) |
| Hands | Parts houses / hand-made | OEM / etching |

## Research log
- [`research-log.md`](research-log.md): what was searched, found, and still missing (updated by the monthly scan)
- [`inventory.md`](inventory.md): movements and parts we already own
