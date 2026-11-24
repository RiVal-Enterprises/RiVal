# Decision log

Newest first. Format: ID · date · decision · why · revisit when.

### D-006 · 2026-11-24 · Instagram posting runs fully autonomously, 3x/week, via the official API
- **Why:** Owner's choice; capacity is limited. Using the official Instagram Graph API (through Zapier, or later a direct Meta app) is the sanctioned route. Shadowban risk comes from unofficial tools, password sharing, and bulk like/follow/comment bots, none of which we use.
- **Guardrails:** every post must be *transformed* (our analysis, our carousel layouts, commentary, comparisons), not a plain repost, because of Instagram's April 2026 aggregator policy. Always credit and tag. Honour any takedown request at once. No automated likes/follows/comments/DMs.
- **Revisit:** monthly learning-loop review, or immediately if reach drops > 50 % week-over-week.

### D-005 · 2026-11-24 · Brand name "RiVal" pending trademark clearance
- **Why:** "Rival" is a common word; check EUIPO/TMview class 14 (watches, jewellery) before investing in logo/packaging.

### D-004 · 2026-11-24 · IP triage before publishing any design
- **Why:** In Europe, publishing an invention before filing destroys patentability (no grace period). Registered EU designs have a 12-month grace period.
- **Rule:** each design in `designs/` gets an `ip:` field: `open` (share freely, e.g. aesthetics) · `design-reg` (register within 12 months of first post) · `secret` (novel mechanism, do not show until decided).

### D-003 · 2026-11-24 · Celestial v2 uses a snail-cam jump hour, not a 1x/h Geneva
- **Why:** Geneva gives a ~25 min hour change; energy model shows thesis-weight parts exceed the torque budget ~5x. See `engineering/celestial_v2/report.md`.

### D-002 · 2026-11-24 · Prototype base movement: Seagull ST3600 (6497 clone)
- **Why:** large, robust, about €30-50, torque headroom, easy to modify. Shrink to SW200/Miyota class after the concept is proven.

### D-001 · 2026-11-24 · Operating model: design & engineer in-house, outsource parts, hand-finish, crowdfund
- **Why:** owners work full-time / run the jewellery business; Tallinn-Kuressaare distance. Bootstrap; Kickstarter before investors.
