#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world news
of Wednesday 18 November 2026. Pure Pillow drawing (no external assets);
run once at build time:  python3 render.py  ->  entry.png (1024x1024).

Headlines are the real events reported on 18 November 2026 (Reuters, AP,
BBC, The Times of India): the Crimean Bridge strike, Trump in Manila,
Iran's drone attack in Bahrain, Canada-China trade, UK sanctions, Nvidia's
results, Dhoni's IPL retirement, Cyclone Akvan.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 236)
INK = (22, 21, 19)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
GOLD = (184, 138, 44)
TEAL = (18, 102, 94)
GREY = (90, 86, 80)
LIGHT = (233, 227, 214)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, width, leading=None):
    leading = leading or int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, yy), (x1, yy)], fill=c)


def draw_bridge_scene(draw, box):
    """Stylised dusk scene: the Kerch Strait bridge with its middle span down."""
    x0, y0, x1, y1 = box
    horizon = y0 + int((y1 - y0) * 0.62)
    vgrad(draw, (x0, y0, x1, horizon), (46, 74, 107), (232, 165, 107))
    # sun
    sx, sy, sr = x0 + 130, y0 + 52, 34
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(250, 214, 140))
    # sea
    draw.rectangle([x0, horizon, x1, y1], fill=(23, 58, 82))
    for i, yy in enumerate(range(horizon + 12, y1 - 8, 16)):
        draw.line([(x0 + 20 + (i % 3) * 90, yy), (x0 + 120 + (i % 3) * 90, yy)],
                  fill=(70, 120, 150), width=2)
    # distant shore
    draw.polygon([(x0, horizon), (x0 + 150, horizon - 26), (x0 + 300, horizon),
                  (x1 - 260, horizon), (x1 - 120, horizon - 20), (x1, horizon)],
                 fill=(52, 66, 74))
    # bridge deck: left span, gap, right span
    deck_y = horizon - 58
    draw.rectangle([x0, deck_y, x0 + 330, deck_y + 12], fill=(38, 38, 40))
    draw.rectangle([x0 + 620, deck_y, x1, deck_y + 12], fill=(38, 38, 40))
    # collapsed span: tilted deck sliding into the water
    draw.polygon([(x0 + 350, deck_y + 4), (x0 + 470, deck_y + 4),
                  (x0 + 500, horizon + 26), (x0 + 380, horizon + 26)],
                 fill=(60, 58, 55))
    # pylons + cables
    for px in (x0 + 120, x0 + 760):
        draw.rectangle([px - 7, deck_y - 92, px + 7, deck_y], fill=(38, 38, 40))
        draw.line([(px, deck_y - 92), (px - 130, deck_y)], fill=(200, 200, 195), width=2)
        draw.line([(px, deck_y - 92), (px + 130, deck_y)], fill=(200, 200, 195), width=2)
    # smoke over the gap
    for cx, cy, r, col in [(470, 92, 52, (74, 72, 70)), (524, 70, 42, (96, 94, 92)),
                           (424, 68, 34, (110, 108, 106)), (566, 96, 34, (84, 82, 80)),
                           (496, 52, 26, (128, 126, 124))]:
        draw.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy - r], fill=col)
    # explosion flash at the break
    ex, ey = x0 + 480, deck_y - 6
    draw.polygon([(ex, ey - 26), (ex + 8, ey - 8), (ex + 26, ey - 4), (ex + 9, ey + 6),
                  (ex + 14, ey + 24), (ex, ey + 10), (ex - 14, ey + 24), (ex - 9, ey + 6),
                  (ex - 26, ey - 4), (ex - 8, ey - 8)], fill=(245, 176, 65))
    draw.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 226, 130))


def card(draw, x, y, w, h, tag, color, headline, deck):
    draw.rectangle([x, y, x + w, y + h], outline=(200, 193, 176), width=1)
    # tag chip
    chip = font(SANS_B, 16)
    tw = draw.textlength(tag, font=chip)
    draw.rectangle([x + 12, y + 10, x + 12 + tw + 16, y + 32], fill=color)
    draw.text((x + 20, y + 13), tag, font=chip, fill=(255, 255, 255))
    # one-line headline, shrunk until it fits
    size = 23
    while size > 16:
        hf = font(SANS_B, size)
        if draw.textlength(headline, font=hf) <= w - 24:
            break
        size -= 1
    draw.text((x + 12, y + 40), headline, font=hf, fill=INK)
    draw_text_block(draw, x + 12, y + 40 + size + 12, deck, font(SANS, 16),
                    (58, 56, 52), w - 24, 20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # double outer border
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # ---- masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34), title, font=tf, fill=INK)
    d.line([(40, 116), (W - 40, 116)], fill=RED, width=4)
    dateline = "WEDNESDAY  •  18 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE PICTURE"
    df = font(SANS_B, 20)
    d.text(((W - d.textlength(dateline, font=df)) / 2, 128), dateline, font=df, fill=RED)

    # ---- lead illustration ----
    draw_bridge_scene(d, (40, 162, W - 40, 372))
    d.rectangle([40, 162, W - 40, 372], outline=INK, width=2)
    cap = "KERCH STRAIT — THE CRIMEAN BRIDGE, AFTER UKRAINE'S STRIKE"
    cf = font(SANS_B, 15)
    cw = d.textlength(cap, font=cf)
    d.rectangle([40, 372 - 30, 40 + cw + 20, 372], fill=(255, 255, 255))
    d.text((50, 372 - 26), cap, font=cf, fill=INK)

    # ---- lead headline + deck ----
    y = 386
    y = draw_text_block(d, 40, y, "UKRAINE HITS CRIMEAN BRIDGE FOR SECOND DAY",
                        font(SERIF, 38), INK, W - 80, 44)
    y = draw_text_block(d, 40, y + 4,
                        "The road arch span collapses into the strait in Kyiv's largest drone "
                        "attack of the war — as Russia pounds Kyiv's own bridges in reply.",
                        font(SANS, 20), (58, 56, 52), W - 80, 24)
    div_y = y + 12
    d.line([(40, div_y), (W - 40, div_y)], fill=INK, width=2)

    # ---- story grid: 2 x 3 ----
    stories = [
        ("MANILA", RED, "Trump lands for Quad talks",
         "The US president arrives in the Philippines ahead of a China visit and a trilateral summit with Xi."),
        ("GULF", TEAL, "Iran drones hit US radar",
         "Bahrain sounds the all-clear after the overnight attack; Kuwait reports drone interceptions."),
        ("TRADE", BLUE, "Canada, China extend trade deals",
         "Xi meets Carney ahead of the APEC summit as Ottawa and Beijing move to ease tensions."),
        ("LONDON", GOLD, "UK sanctions settlement firms",
         "Britain blacklists Israeli firms over West Bank settlements and a group blocking Gaza aid."),
        ("MARKETS", BLUE, "Nvidia sales jump 103%",
         "Quarterly revenue hits $115.8bn — but Jensen Huang will not return as chief executive."),
        ("SPORT", RED, "Dhoni bows out of the IPL",
         "The Chennai legend retires as a player and becomes Super Kings mentor."),
    ]
    cw_, ch_, gap = 464, 104, 12
    x0, y0 = 40, div_y + 14
    for i, (tag, color, head, deck) in enumerate(stories):
        x = x0 + (i % 2) * (cw_ + gap)
        y = y0 + (i // 2) * (ch_ + gap)
        card(d, x, y, cw_, ch_, tag, color, head, deck)

    # ---- also today ----
    ay = y0 + 3 * ch_ + 2 * gap + 14
    d.line([(40, ay), (W - 40, ay)], fill=INK, width=2)
    also = ("ALSO TODAY  —  Cyclone Akvan strengthens in the Bay of Bengal  •  "
            "UN: 372 civilians killed in Ukraine in October  •  Gaza: one hot meal "
            "every two days (WFP)  •  Modi at the East Asia Summit")
    draw_text_block(d, 40, ay + 10, also, font(SANS, 17), (58, 56, 52), W - 80, 22)

    # ---- footer ----
    fy = H - 56
    d.line([(40, fy), (W - 40, fy)], fill=INK, width=1)
    foot = "Sources: Reuters · AP · BBC · The Times of India — every event reported on 18 November 2026"
    d.text((40, fy + 10), foot, font=font(SANS, 15), fill=GREY)
    d.text((W - 40 - d.textlength("make.fun", font=font(SANS_B, 15)), fy + 10),
           "make.fun", font=font(SANS_B, 15), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
