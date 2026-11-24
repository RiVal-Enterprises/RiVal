# Content pipeline (@rival_watches)

| File | Purpose |
|---|---|
| [`strategy.md`](strategy.md) | Rules, pillars, cadence, learning loop (**read first**) |
| [`style-guide.md`](style-guide.md) | Voice, caption template, carousel layout |
| [`setup-instagram.md`](setup-instagram.md) | How to connect the account (owner to-do) |
| `queue.csv` | Planned posts (written by the weekly research job, consumed by the posting job) |
| `posted.csv` | Every published post + performance metrics |
| `brands.csv` | Every brand/campaign we've researched (also feeds `insights/`) |
| `do-not-feature.csv` | Brands that asked not to be featured |
| `slides/` | Rendered carousel images (PNG 1080×1350) per post |
| `learning/` | Monthly learning-loop reviews |
| `templates/` | Permission/outreach message templates |

## Flow

```
Sun weekly research job ─► brands.csv + insights/ + queue.csv (+ slides/)
Mon/Wed/Fri posting job ─► takes next "ready" row in queue.csv ─► publish via official API ─► posted.csv
1st of month            ─► learning/YYYY-MM.md, update strategy mix
```
