# @rival_watches: content strategy

**Goal:** build a community of watch enthusiasts who love independent and avant-garde horology, then turn them into the first RiVal backers.

**Phases:** (1) curator-analyst of new and crowdfunded watches → (2) mixing in "build in public" RiVal content → (3) RiVal-only. Move to the next phase when the engagement targets below are met.

## The rule that shapes everything: don't be an aggregator

Since **April 2026**, Instagram stops recommending accounts that mostly post content they didn't create or *meaningfully transform*, on all formats (photos, carousels, Reels). Existing followers still see the posts, but growth stops. ([PetaPixel](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/), [TechCrunch](https://techcrunch.com/2026/04/30/instagram-restricts-reach-of-content-aggregators-in-new-crackdown/))

So **every** RiVal post must add original value:

- our own **carousel layouts** (brand template, our typography), not the brand's photo dropped in unchanged
- **analysis**: what's mechanically new, the movement used, price vs. peers, why it works or fails
- **comparisons and data**: funding curves, price/spec tables, "3 watches that solve X differently"
- **engineering explainers**: how a jump hour, Geneva drive or wandering hour actually works (our own diagrams)
- later: our own photos and video from the workshop

## Content pillars & mix (phase 1)

| Pillar | Share | Format | Example |
|---|---|---|---|
| **Launch radar**: live/upcoming Kickstarter/Indiegogo watches + notable new microbrands | 40 % | Carousel (5-8 slides): hook → hero → what's new → specs/price → our verdict → credit | "This €600 watch has a planetary moon phase. Here's how it works" |
| **Autopsy**: why a campaign/brand succeeded or failed | 25 % | Carousel with numbers | "Raised €1.2M in 3 days: 5 things they did right" |
| **Mechanism explainer** | 20 % | Carousel / short Reel with diagrams | "Geneva drive vs. snail cam: why one jumps and one crawls" |
| **Throwback**: great past launches when < 3 new ones in a week | 15 % | Carousel | "2014: a student 3D-printed an Urwerk. What happened next" |

Phase 2 adds **build-in-public** (drawer designs with `ip: open`, casting, engraving, prototypes) and the **community vote** on which design RiVal builds.

## Cadence & timing

- **3 posts/week: Mon, Wed, Fri at 19:47 Tallinn** (= 12:47 New York / 09:47 California / 18:47 Berlin, which covers the EU evening and the US day).
- Carousels are the default (highest saves/shares for educational content); 1 Reel every 1-2 weeks once diagram animations are available.
- Reuse: each autopsy can later become a Reel and a Story.

## Captions & discovery

- First line = hook (≤ 125 chars, shown before "more").
- Body: 3-6 short lines of real substance; end with a question to invite comments ("Would you back this?").
- Credit line: `📷 & design: @brand. Campaign link in their bio / ours.` Always tag the brand on the image too.
- Hashtags: 3-5 specific ones (e.g. #microbrandwatch #independentwatchmaking #kickstarterwatch #watchmechanism). Instagram now treats hashtags as minor; keywords in the caption matter more for search.
- Alt text describing the watch (search + accessibility).

## Engagement targets (review monthly)

| Metric | Phase-1 target |
|---|---|
| Saves + shares per post | ≥ 3 % of reach |
| Non-follower reach share | ≥ 30 % (if near 0 → aggregator flag, fix transformation) |
| Follower growth | steady positive week-over-week |

## Learning loop (automated)

1. Every post is logged in `posted.csv` with pillar, format, hook type, topic, time.
2. Weekly job pulls insights (reach, saves, shares, comments, profile visits, follows) once the insights connection is live, and writes them into `posted.csv`.
3. Monthly, the job writes `learning/YYYY-MM.md`: top/bottom 3 posts, what they share, one change to test next month (A/B: hook style, slide count, pillar mix, time). Then update this file's mix table.
4. Guardrail: if non-follower reach collapses or a post gets removed, pause posting and flag it to the owner in a PR.

## What we never do

- Automated likes, follows, comments or DMs; buying followers; engagement pods
- Unofficial APIs, browser bots, sharing the account password with tools
- Posting RiVal designs whose `ip:` isn't `open`
- Plain reposts without transformation; posting without credit
