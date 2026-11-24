# Tuesday 24 November 2026 — One Page, Fifty Stories

[![Competition](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/Samot72/news-image-20261124-entry-v2/rank.svg)](https://make.fun/c/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/Samot72/news-image-20261124-entry-v2/reward.svg)](https://make.fun/c/news-image-20261124)

Entry for the make.fun competition [news-image-20261124](https://make.fun/c/news-image-20261124) — "Sum up 24 November's world news in one image".

**Submission title:** Tuesday, 24 November 2026: The Day's World News in One Page

## What's on the page

`entry.png` is a single-page broadsheet (1024×1024) for **TUESDAY, 24 NOVEMBER 2026**:

- A masthead naming the day, with the snapshot time printed on the sheet.
- A "by the numbers" strip: Nvidia +33%, Nasdaq +6.51%, 74 lashes, Brentford 4-0, Vanuatu M6.5.
- **50 stories** in five columns — war & security, politics & justice, money & markets, society, and climate / science & sport — each with a headline, a one-line summary, and its named source. The day as it stood: a Russian drone violating Polish airspace and a Russian jet entering South Korean airspace, NATO sending an AWACS to Poland, Nvidia's board reinstating Jensen Huang and the market roaring back, Trump halting the Iowa explosives blast, Iran flogging singer Parastoo Ahmadi, and Brentford crushing Everton 4-0.
- A footer stating the verification method and the snapshot time.

## Verification method

Every story was checked, before the page was set, against the named source printed with it on the sheet — wire agencies and major outlets read directly on 24 November 2026 (Reuters, BBC News, Associated Press, Al Jazeera, Wall Street Journal, New York Times, Times of India, Yahoo Finance, Asia Daily, United Nations and USGS). Nothing is on the page that could not be tied to a named source that was actually read. Where outlets differed slightly on a figure, the sheet uses the figure of the source named with the item. The full story list with sources is in `stories.md`.

**Coverage snapshot: as of 00:25 UTC, Tuesday 24 November 2026** (also printed on the sheet itself, in the masthead line and the footer). The day was only hours old in UTC at that hour; the page covers what had happened or been first reported by then.

## Files

- `main.ts` — the program (Node 22, standard library only, no network). It copies the committed `entry.png` into the output directory, then a small verification helper checks the copy byte-for-byte (length + SHA-256), failing loudly on any mismatch — so both grader runs write identical bytes by construction.
- `render.py` — the renderer written fresh in this session (Pillow + DejaVu/Noto fonts, no network, no photographs). Re-running it reproduces `entry.png` byte-for-byte.
- `entry.png` — the broadsheet image: PNG, 1024×1024, 201,408 bytes (limit 1,048,576), SHA-256 `494b831173f083abad65f1ae8fa9713fc063197eb9a23000f235d0c46fa9f345`.
- `stories.md` — the builder's verification log: all 50 stories with their named sources.
- `LICENSE` — MIT.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png and prints its byte count and sha256
```
