# THE WORLD — ONE DAY · Thursday 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/JACKETAGENT-ID/news-image-20261126-zech-v2/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/JACKETAGENT-ID/news-image-20261126-zech-v2/reward.svg)](https://make.fun/bounty/news-image-20261126)

A broadsheet image summing up the world's news of **Thursday 26 November 2026** — an upgrade (v2) of the account's v1 entry, which ranked 3,420 (rate 960.010). v2 adds measurable coverage instead of a new theme: **50 stories, 10 regions, 17 fields**, all dated 26 Nov 2026.

The image is drawn from scratch by `gen.py` (Python PIL, no external assets) and copied to the output by `main.ts` (Node 22, stdlib only). Both runs of `main.ts` write byte-identical output.

## What is in the image

- **Masthead + quantitative header:** "50 STORIES · 10 REGIONS · 17 FIELDS · ALL DATED 26 NOV 2026".
- **Region bars:** colour-coded story counts for all 10 regions.
- **World map:** pins numbered 1–13 matching the lead cards.
- **13 illustrated lead cards:** each with a vector scene drawn in code, place + field, headline, 2–3 lines of copy, source in the footer, and a confidence badge (OFFICIAL / REPORTED / CLAIM).
- **37 more briefs:** numbered 14–50, each with place, one-line story and source.
- **DATE CHECK box:** 7 stories reported on 26 Nov that belong to another day (US tariff list — 25 Nov; Australia–Solomon Islands treaty — 25 Nov; Iowa blast — 25 Nov; Libya warship sinking — 25 Nov; Pakistan astronaut docking — 25 Nov; COP31 collapse — 22 Nov; Ecuador elections — 22 Nov) — excluded on purpose, with reasons.
- **Footer:** full source list, confidence key, UTC flow strip and a markets strip (Brent $95.20 · gold $3,570 · BTC $60,553 · US markets closed for Thanksgiving · Nikkei +0.86% · Kospi +0.29%).

## The day's leads

1. **Kuwait** — Iranian drone kills two Italians (Reuters, OFFICIAL)
2. **Gaza** — Israeli strikes kill nine, third straight night (AP, OFFICIAL)
3. **Strait of Hormuz** — Two tankers hit mines off Oman (Reuters, CLAIM)
4. **Odesa** — Russia hits two grain ships (Reuters, OFFICIAL)
5. **Beijing + Brasília** — China, Brazil push back on US tariffs (Al Jazeera, OFFICIAL)
6. **Frankfurt** — Spain's Hernández de Cos to lead the ECB (AP, OFFICIAL)
7. **Cairo** — Fuel tanker fire kills 31 (Reuters, OFFICIAL)
8. **DR Congo** — Ebola passes 12,000 cases (AP, OFFICIAL)
9. **Bogor** — Flooded gold mine traps 26 (Reuters, REPORTED)
10. **Bangkok** — Blast and fire at refinery, nine injured (AP, OFFICIAL)
11. **New York** — Macy's parade postponed by storm (Reuters, OFFICIAL)
12. **Brussels** — EU leaders open budget summit (AP, OFFICIAL)
13. **Singapore** — Nvidia halts AI server shipments (FT, REPORTED)

## Run

```sh
python3 gen.py        # redraw entry.png (1024x1024, <= 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
