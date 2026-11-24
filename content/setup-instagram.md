# Connecting @rival_watches so Claude can post

There are two routes. **Start with A** (about 15 minutes, no developer work). Move to B when you want full analytics for the learning loop.

## Route A: Zapier (posting now, basic insights)

Your Zapier account is already connected to Claude. Steps (on your phone or computer):

1. **Make @rival_watches a professional account:** Instagram → Settings → *Account type and tools* → *Switch to professional account* → choose **Business** (or Creator) → category e.g. "Product/service".
2. **Create a Facebook Page** for RiVal (facebook.com/pages/create). A personal Facebook profile is needed to own it.
3. **Link the Page and Instagram:** Facebook Page → Settings → *Linked accounts* → Instagram → connect @rival_watches (or in Meta Business Suite → Settings → Instagram accounts). Make sure your Facebook user has **full control** of the Page.
4. **Connect Zapier:** open
   **https://mcp.zapier.com/api/v1/connect-auth/InstagramBusinessCLIAPI?accountId=27785418**
   → sign in with Facebook → select the RiVal Page and @rival_watches → **allow all requested permissions** (publish content, read insights).
5. Tell Claude "Instagram connected". Claude then sets it as the default connection, enables the *Publish Photo(s)* action, and does a test run.

> Two-factor authentication on Instagram and Facebook is strongly recommended. Claude never needs your password: the connection uses Meta's official login (OAuth) and can be revoked anytime in Facebook → Settings → *Business integrations*.

**Limits:** Meta allows up to 100 API posts per 24 h ([Meta docs](https://developers.facebook.com/docs/instagram-platform/content-publishing/)); we post 3 a week. Images must be at a public URL (Meta fetches them), so our rendered carousel slides are hosted in the repo/Drive with public links.

## Route B: direct Meta Graph API (full insights + Reels + carousels)

Needed for the learning loop's detailed metrics (reach, saves, shares, non-follower reach).

1. developers.facebook.com → *Create app* → type **Business** → add product **Instagram** (Instagram API with Facebook Login).
2. Permissions: `instagram_basic`, `instagram_content_publish`, `instagram_manage_insights`, `pages_show_list`, `pages_read_engagement`.
3. Generate a **long-lived Page access token** (Graph API Explorer → exchange for long-lived).
4. In a Claude session, say "add the Instagram API credential". Claude will open a secure form for host `graph.facebook.com`, and you paste the token **there, never in chat**. The token is stored on the cloud environment, not in this repo.
5. Optionally use an open-source Instagram MCP server (e.g. `adelaidasofia/instagram-mcp`, `luminarylane/instagram-mcp-server`). Review the code first; prefer ones restricted to Meta hosts.

## Why this won't get the account shadowbanned

- Official API publishing is how Meta Business Suite, Later, Buffer and Hootsuite post. Tests by schedulers found no reach penalty ([Hootsuite](https://blog.hootsuite.com/experiment-third-party-scheduling-instagram/), [Metricool](https://metricool.com/does-scheduling-social-media-posts-affect-reach/)); real penalties come from like/follow/comment bots and unofficial tools ([Storrito](https://storrito.com/resources/instagram-penalizes-aggressive-automation/)).
- The real risk today is the **aggregator policy**. See `strategy.md`; every post is transformed and credited.
- AI-written captions aren't penalised. Meta labels photorealistic AI-*generated images* ("AI info"), so we use real watch photos (credited) and our own diagrams, not fake AI watch renders.
- A dormant account restarting: post 3x/week steadily rather than bursting 20 posts on day one.
