#!/usr/bin/env python3
"""Render one infographic PNG summing up the world news of 24 November 2026.

Deterministic: all content is fixed data in this file, no network, no clock,
no randomness. Two runs produce the same image.

Output: news.png next to this script, and /output/news.png when /output is
available (the grader's sandbox collects outputs from /output).
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- fonts

FONT_DIR = "/usr/share/fonts/truetype/noto"
DEJAVU_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def serif_bold(size):
    return load_font(
        [f"{FONT_DIR}/NotoSerif-Bold.ttf", f"{DEJAVU_DIR}/DejaVuSerif-Bold.ttf"], size
    )


def sans(size):
    return load_font(
        [f"{FONT_DIR}/NotoSans-Regular.ttf", f"{DEJAVU_DIR}/DejaVuSans.ttf"], size
    )


def sans_bold(size):
    return load_font(
        [f"{FONT_DIR}/NotoSans-Bold.ttf", f"{DEJAVU_DIR}/DejaVuSans-Bold.ttf"], size
    )


# ---------------------------------------------------------------- content

DATE_LINE = "Tuesday, 24 November 2026"
TITLE = "THE WORLD IN ONE IMAGE"
SUBTITLE = "The day's essential world news — Tuesday, 24 November 2026"

LEAD = {
    "tag": "TOP STORY · BUSINESS & TECH",
    "color": (176, 32, 40),
    "headline": "Nvidia reinstates Jensen Huang as CEO after Trump steps in",
    "summary": (
        "In a stunning reversal, Nvidia restored its co-founder as chief executive after "
        "President Trump and Vice President Vance personally intervened, convinced Huang "
        "alone protects American open-weight AI models. Nvidia shares surged 31% on Monday, "
        "lifting the Nasdaq by 6% and the chip index by 12%."
    ),
    "source": "Reuters",
}

STORIES = [
    {
        "tag": "EUROPE · WAR",
        "color": (31, 78, 120),
        "headline": "Ukraine sinks Russian warship in sea-drone strike off Libya",
        "summary": (
            "Zelensky said seven uncrewed boats destroyed a Ka-27 helicopter and hit the "
            "cargo ship MV Angara near Benghazi — Kyiv's reach now extends far beyond Europe."
        ),
        "source": "SCMP",
    },
    {
        "tag": "EUROPE · WAR",
        "color": (31, 78, 120),
        "headline": "Russian strikes kill at least 14 in Kyiv region",
        "summary": (
            "Russian attacks on the Kyiv region killed at least 14 people, Ukrainian "
            "officials said, as the air war around the capital intensified."
        ),
        "source": "AFP",
    },
    {
        "tag": "SECURITY · SPACE",
        "color": (90, 60, 140),
        "headline": "NATO vows space defence over Russian nuclear satellite reports",
        "summary": (
            "Allies say Moscow may launch a nuclear anti-satellite weapon within weeks; "
            "NATO pledged to defend allied satellites, while Moscow accused Estonia of "
            "actions 'on the verge of triggering open war'."
        ),
        "source": "SCMP · The Japan Times",
    },
    {
        "tag": "CLIMATE",
        "color": (30, 120, 76),
        "headline": "COP31 climate talks collapse with no deal",
        "summary": (
            "The summit ended in deadlock after the EU and others rejected a final text "
            "that dropped any mention of transitioning away from fossil fuels."
        ),
        "source": "SCMP",
    },
    {
        "tag": "UNITED STATES",
        "color": (176, 32, 40),
        "headline": "Democrats clinch biggest House majority since 1992",
        "summary": (
            "Democrats secured at least 258 House seats — their largest majority since "
            "1992 — handing them power to block Trump's agenda and open investigations "
            "in the last two years of his presidency."
        ),
        "source": "The Manila Times · SCMP",
    },
    {
        "tag": "AFRICA",
        "color": (180, 110, 20),
        "headline": "Drones hit homes and UN building in Sudan's capital",
        "summary": (
            "Drone strikes slammed into homes and a United Nations building in Khartoum, "
            "the latest escalation in Sudan's civil war."
        ),
        "source": "The Japan Times · AFP",
    },
    {
        "tag": "ASIA",
        "color": (0, 110, 130),
        "headline": "Sheikh Hasina to return to Bangladesh after exile in India",
        "summary": (
            "The ousted prime minister plans to fly home on 16 December, the anniversary "
            "of the end of the 1971 liberation war, her spokesperson told Reuters."
        ),
        "source": "Reuters",
    },
    {
        "tag": "TECHNOLOGY · UN",
        "color": (90, 60, 140),
        "headline": "UN chief calls for AI risk framework within a year",
        "summary": (
            "The UN secretary-general urged governments to agree a global AI "
            "risk-management framework within 12 months, as US states sued Elon Musk's "
            "companies over sexualised images made by the Grok chatbot."
        ),
        "source": "The Manila Times",
    },
]

FOOTER = (
    "Sources: Reuters · AFP · South China Morning Post · The Japan Times · The Manila Times"
    "   |   Compiled 24 November 2026"
)

# ---------------------------------------------------------------- layout

W = 1600
MARGIN = 48
CONTENT_W = W - 2 * MARGIN

BG = (248, 245, 239)
INK = (26, 26, 40)
BODY = (52, 50, 46)
MUTED = (105, 100, 92)
CARD_BG = (255, 255, 255)
CARD_BORDER = (216, 209, 196)
RULE = (26, 26, 40)
ACCENT = (176, 32, 40)

CHIP_FONT_SIZE = 16
HEAD_FONT_SIZE = 24
SUM_FONT_SIZE = 19
SRC_FONT_SIZE = 15
HEAD_LH = HEAD_FONT_SIZE + 7
SUM_LH = SUM_FONT_SIZE + 6
PAD_TOP = 16
PAD_BOT = 14


def wrap(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def chip_height(font):
    return font.size + 8


def block_height(draw, story, inner_w, head_font, sum_font, chip_font):
    """Height of one story block's inner content (chip..source), no padding."""
    h = chip_height(chip_font) + 10
    h += len(wrap(draw, story["headline"], head_font, inner_w)) * HEAD_LH
    h += 3
    h += len(wrap(draw, story["summary"], sum_font, inner_w)) * SUM_LH
    h += 6 + SRC_FONT_SIZE
    return h


def draw_chip(draw, x, y, text, color, font):
    pad_x = 10
    w = draw.textlength(text, font=font) + 2 * pad_x
    h = chip_height(font)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=color)
    draw.text((x + pad_x, y + 3), text, font=font, fill=(255, 255, 255))
    return y + h


def draw_block_w(draw, x, y, w, story, head_font, sum_font, chip_font, src_font):
    cy = draw_chip(draw, x, y, story["tag"], story["color"], chip_font)
    cy += 10
    for line in wrap(draw, story["headline"], head_font, w):
        draw.text((x, cy), line, font=head_font, fill=INK)
        cy += HEAD_LH
    cy += 3
    for line in wrap(draw, story["summary"], sum_font, w):
        draw.text((x, cy), line, font=sum_font, fill=BODY)
        cy += SUM_LH
    cy += 6
    draw.text((x, cy), "— " + story["source"], font=src_font, fill=MUTED)
    return cy + SRC_FONT_SIZE


def render():
    scratch = ImageDraw.Draw(Image.new("RGB", (8, 8)))

    title_font = serif_bold(58)
    date_font = sans_bold(21)
    sub_font = sans(22)
    chip_font = sans_bold(CHIP_FONT_SIZE)
    head_font = serif_bold(HEAD_FONT_SIZE)
    sum_font = sans(SUM_FONT_SIZE)
    src_font = sans(SRC_FONT_SIZE)
    lead_head_font = serif_bold(34)
    lead_sum_font = sans(22)

    # Measure lead block (inner width = CONTENT_W - 52)
    lead_inner_w = CONTENT_W - 52
    lead_h = PAD_TOP
    lead_h += chip_height(sans_bold(19)) + 12
    lead_h += len(wrap(scratch, LEAD["headline"], lead_head_font, lead_inner_w)) * 43
    lead_h += 4
    lead_h += len(wrap(scratch, LEAD["summary"], lead_sum_font, lead_inner_w)) * 29
    lead_h += 8 + 17 + PAD_BOT

    # Measure grid rows (2 columns)
    gap = 14
    card_w = (CONTENT_W - gap) // 2
    card_inner_w = card_w - 44
    row_heights = []
    for r in range(0, len(STORIES), 2):
        pair = STORIES[r:r + 2]
        h = max(block_height(scratch, s, card_inner_w, head_font, sum_font,
                             chip_font) for s in pair)
        row_heights.append(PAD_TOP + h + PAD_BOT)

    masthead_h = 162
    lead_y = masthead_h + 16
    grid_y = lead_y + lead_h + 18
    grid_h = sum(row_heights) + gap * (len(row_heights) - 1)
    foot_y = grid_y + grid_h + 18
    total_h = foot_y + 12 + 24 + MARGIN

    img = Image.new("RGB", (W, total_h), BG)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.line([MARGIN, 40, W - MARGIN, 40], fill=RULE, width=5)
    draw.text((MARGIN, 56), TITLE, font=title_font, fill=INK)
    draw.text((W - MARGIN - draw.textlength(DATE_LINE.upper(), font=date_font), 78),
              DATE_LINE.upper(), font=date_font, fill=ACCENT)
    draw.text((MARGIN, 128), SUBTITLE, font=sub_font, fill=MUTED)
    draw.line([MARGIN, masthead_h, W - MARGIN, masthead_h], fill=RULE, width=2)

    # Lead story
    draw.rounded_rectangle([MARGIN, lead_y, MARGIN + CONTENT_W, lead_y + lead_h],
                           radius=10, fill=(255, 251, 240), outline=ACCENT, width=3)
    lx = MARGIN + 26
    cy = draw_chip(draw, lx, lead_y + PAD_TOP, LEAD["tag"], LEAD["color"],
                   sans_bold(19))
    cy += 12
    for line in wrap(draw, LEAD["headline"], lead_head_font, lead_inner_w):
        draw.text((lx, cy), line, font=lead_head_font, fill=INK)
        cy += 43
    cy += 4
    for line in wrap(draw, LEAD["summary"], lead_sum_font, lead_inner_w):
        draw.text((lx, cy), line, font=lead_sum_font, fill=BODY)
        cy += 29
    cy += 8
    draw.text((lx, cy), "— " + LEAD["source"], font=sans(17), fill=MUTED)

    # Story grid
    y = grid_y
    for r, row_h in enumerate(row_heights):
        for c in range(2):
            idx = r * 2 + c
            if idx >= len(STORIES):
                break
            x = MARGIN + c * (card_w + gap)
            draw.rounded_rectangle([x, y, x + card_w, y + row_h], radius=10,
                                   fill=CARD_BG, outline=CARD_BORDER, width=2)
            draw_block_w(draw, x + 22, y + PAD_TOP, card_inner_w, STORIES[idx],
                         head_font, sum_font, chip_font, src_font)
        y += row_h + gap

    # Footer
    draw.line([MARGIN, foot_y, W - MARGIN, foot_y], fill=RULE, width=2)
    draw.text((MARGIN, foot_y + 12), FOOTER, font=sans(17), fill=MUTED)

    return img


def main():
    os.umask(0o022)
    img = render()
    here = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(here, "news.png")
    img.save(local_path, format="PNG")
    os.chmod(local_path, 0o644)
    print(f"wrote {local_path} ({img.size[0]}x{img.size[1]})")

    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "news.png")
        img.save(out_path, format="PNG")
        os.chmod(out_path, 0o644)
        print(f"wrote {out_path}")
    except OSError as exc:
        print(f"note: /output not writable here ({exc}); local copy only")


if __name__ == "__main__":
    main()
