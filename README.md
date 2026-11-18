# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Adesudu/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Adesudu/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page that sums up the world news of Wednesday
18 November 2026 in a single image — built for make.fun's
"Sum up 18 November's world news in one image" bounty ($250 in USDC).

The lead story is Ukraine's second-day strike on the Crimean Bridge, whose
road arch span collapsed into the Kerch Strait in Kyiv's largest drone
attack of the war, with Russia pounding Kyiv's bridges in reply. Around it:
Trump landing in Manila for Quad talks, Iran's drone attack on the US radar
in Bahrain, Canada and China extending trade deals ahead of APEC, the UK
sanctioning Israeli settlement firms, Nvidia's revenue jumping 103%, and
MS Dhoni bowing out of the IPL — plus an "Also today" strip (Cyclone Akvan,
the UN's Ukraine civilian toll, Gaza aid, Modi at the East Asia Summit).

Every headline is a real event reported on 18 November 2026 (Reuters, AP,
BBC, The Times of India). The illustration — the bridge at dusk, its middle
span down, smoke rising — and the whole page were drawn from scratch by
`render.py` (Pillow) at build time; `main.py` (Python 3.13, standard library
only) copies the finished `entry.png` to `/output/entry.png`, so the program
is deterministic and needs no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the image from scratch (needs Pillow, build time only):

```sh
python3 render.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=qq4pkark&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
