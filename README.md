# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/yangfa595/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/yangfa595/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A deterministic Python program that renders one infographic PNG summing up the world news of Tuesday, 24 November 2026: a newspaper-style front page with the day's top story (Nvidia reinstates Jensen Huang as CEO after Trump steps in) and eight more stories from Europe, the United States, Africa, Asia and the UN, each with a headline, a short summary and its source (Reuters, AFP, SCMP, The Japan Times, The Manila Times). Built with Pillow only — no network, no clock, no randomness — so every run produces the identical image.

![The world in one image — 24 November 2026](news.png)

## Run it

```sh
pip install Pillow
python3 main.py
```

This writes `news.png` next to `main.py` (and to `/output/news.png` when `/output` is available).

---
<sub>Entered on [make.fun](https://make.fun/?ref=75k23xv8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
