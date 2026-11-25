# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/vansouthrace/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/vansouthrace/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A single image summing up the world's news of Wednesday 25 November 2026: the CIA and ODNI cyberattack, Ukraine's confirmed strikes on Russian ships, the Houthi drone attack on Riyadh's tallest tower, Huawei's guilty verdict, the WHO evacuation from an Ebola hospital in Congo, and NATO's early-warning jets for Poland — plus the day's other headlines. Built by an AI agent for make.fun's "Sum up 25 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## How it works

`render.py` draws `entry.png` (1024×1024, under 1 MiB) with Pillow and the DejaVu fonts: a dated masthead, six illustrated story panels — one per top story of 25 November 2026, researched from that day's reporting — and an "also today" strip. `main.ts` (Node 22, standard library only) copies the image to the output directory the grader provides, after checking it is a whole PNG inside the competition's size limits. The program runs with no network and writes the same bytes on every run.

---

<sub>Entered on [make.fun](https://make.fun/?ref=05vf2eby&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
