#!/usr/bin/env python3
"""news-image-20261124 renderer — written fresh in this session, 24 Nov 2026.

Renders a one-page broadsheet (1024x1024 PNG) summing up Tuesday 24 November
2026 world news in 50 stories. Pure Pillow + DejaVu/Noto fonts, no network,
no photographs: every rule, glyph and icon is drawn by this program.
Deterministic: identical input always yields a byte-identical PNG (fixed
fonts, fixed geometry, no timestamps baked in beyond the printed snapshot
line, which is a constant in this file).

Usage:  python3 render.py [output_path]   (default: entry.png next to this file)
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

SNAPSHOT = "00:25 UTC"  # research snapshot, Tuesday 24 November 2026

W, H = 1024, 1024
PAPER = (247, 242, 228)   # newsprint cream
INK = (22, 22, 22)
SOFT = (48, 46, 42)
MUTED = (96, 89, 74)
RED = (168, 30, 30)
RULE = (64, 58, 46)
HAIR = (228, 221, 202)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ITALIC = "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


# (section, headline, one-line summary, named source)
STORIES = [
    ("WAR", "Russian drone over Poland", "Drone briefly violates Polish airspace overnight.", "Reuters"),
    ("WAR", "Russian jet over S. Korea", "Seoul warns Ulleung island as Russian jet enters its airspace.", "Reuters"),
    ("WAR", "NATO sends AWACS to Poland", "AWACS jet to deploy after missiles landed in Poland.", "Reuters"),
    ("WAR", "Russia planning new strikes", "Zelenskiy: new strikes coming; allies must hurry defences.", "Reuters"),
    ("WAR", "Nuclear satellite ready", "NATO intel: Russia plans to launch nuclear-armed satellite.", "Reuters"),
    ("WAR", "Merz warns Russia", "Merz to Moscow: stop 'dangerous provocations' after Poland hit.", "Reuters"),
    ("WAR", "Moscow accuses Estonia", "Russia: Estonia's acts are 'on the verge of triggering open war'.", "Reuters"),
    ("WAR", "EU's 22nd sanctions pack", "Brussels targets Russian banks and crypto in a new package.", "Reuters"),
    ("WAR", "Russia's $576m ferries", "Two giant ferries to secure Kaliningrad supplies by 2030.", "Reuters"),
    ("WAR", "Ukraine shows Libya strikes", "Kyiv shares video of drone strikes on Russian ships off Libya.", "BBC News"),
    ("WAR", "US hits Iran shadow banks", "Washington sanctions dozens tied to Iran's shadow banking networks.", "Reuters"),
    ("WAR", "Iran vows to fight blockade", "Tehran: it will use all its tools against the US naval blockade.", "Reuters"),
    ("POLITICS", "Huang back at Nvidia", "Board brings Jensen Huang back as CEO, 11 days after he quit.", "Reuters"),
    ("POLITICS", "Trump: 'I made the deal'", "President says he 'convinced' Nvidia to bring Huang back.", "BBC News"),
    ("POLITICS", "US to blacklist Megaspeed", "US moves against AI firm Megaspeed after the Nvidia scandal.", "BBC News"),
    ("POLITICS", "Trump halts Iowa blast", "Army told to pause detonation of toxic lead azide stockpile.", "Reuters"),
    ("POLITICS", "California Democrat quits", "Congress member to quit after sexual misconduct evidence emerges.", "BBC News"),
    ("POLITICS", "India pledges $1.6bn to Nepal", "New Delhi pledges $1.6bn in a reset of ties with Kathmandu.", "BBC News"),
    ("POLITICS", "India-China border talks", "Commanders meet in Arunachal to ease border tensions.", "Times of India"),
    ("POLITICS", "Modi opens AI centre", "PM opens an AI centre at IIT Patna and a Rs 400 crore research park.", "Times of India"),
    ("POLITICS", "Kenya, DR Congo mend ties", "Nairobi and Kinshasa agree to restore ties after war tensions.", "BBC News"),
    ("POLITICS", "Colombia: 10 yrs of peace", "Colombia marks a decade since the FARC peace deal.", "New York Times"),
    ("POLITICS", "Lebanon wants Israel out", "Aoun demands Israeli withdrawal, decries Iran's meddling.", "Al Jazeera"),
    ("POLITICS", "Bessent on military base", "Treasury chief still on a US base after an Israel warning.", "Al Jazeera"),
    ("MONEY", "Wall Street roars back", "S&P 500 up 4.73%, Nasdaq 6.51% on Monday after Friday's fall.", "Yahoo Finance"),
    ("MONEY", "Nvidia leaps 33%", "Shares jump by a third as Huang's return reignites the AI trade.", "Reuters"),
    ("MONEY", "European chips surge", "Chip stocks rally across Europe after Huang's return.", "Wall Street Journal"),
    ("MONEY", "Tokyo reopens after rout", "Markets resume after the Nikkei's 5.06% plunge on Friday.", "Asia Daily"),
    ("MONEY", "Taiwan's Taiex rallies 2.2%", "Taipei gains 2.2% on Monday, bucking the region's AI sell-off.", "Asia Daily"),
    ("MONEY", "Hang Seng slips 0.1%", "Hong Kong edges down after sliding nearly 2% earlier.", "Asia Daily"),
    ("MONEY", "VIX tumbles 25.8%", "Fear gauge falls to 26.62 as calm returns to Wall Street.", "Yahoo Finance"),
    ("MONEY", "India's private sector gains", "Activity improves in November as manufacturing growth strengthens.", "Times of India"),
    ("MONEY", "Blockade hits Iran's oil", "US blockade squeezes Iran's oil exports as Tehran shows missiles.", "Al Jazeera"),
    ("SOCIETY", "Iran flogs singer, 74 lashes", "Parastoo Ahmadi, four colleagues flogged over a no-hijab concert.", "Reuters"),
    ("SOCIETY", "Gaza 'toxic wasteland'", "Oxfam: contamination across 99% of Gaza from Israel's attacks.", "BBC News"),
    ("SOCIETY", "Baby dies of cold in Gaza", "A baby dies of cold in a tent in Khan Younis.", "Al Jazeera"),
    ("SOCIETY", "25 seafarers killed at Hormuz", "UN counts 25 dead near the strait since February.", "United Nations"),
    ("SOCIETY", "Nigeria boat tragedy", "Rescuers race to find survivors after a boat capsizes in Nigeria.", "BBC News"),
    ("SOCIETY", "Fury reveals diagnosis", "Heavyweight Tyson Fury diagnosed with schizophrenia.", "BBC News"),
    ("SOCIETY", "Andrew got $977,000", "A court hears Andrew received $977,000 from a Turkish millionaire.", "BBC News"),
    ("SOCIETY", "Melania's Christmas tree", "First Lady welcomes the 18-foot White House tree from Wisconsin.", "BBC News"),
    ("SOCIETY", "Seattle slams ICE arrests", "Airport operator 'outraged' over ICE arrest of two passengers.", "BBC News"),
    ("SOCIETY", "Zimbabwe preacher held", "Prominent preacher arrested on sexual assault allegations.", "BBC News"),
    ("SCIENCE", "Brentford crush Everton 4-0", "Lewis-Potter scores twice as Brentford climb into the top six.", "BBC Sport"),
    ("SCIENCE", "India-NZ Test drawn", "First Test at Wellington ends in a draw after a strong fightback.", "Times of India"),
    ("SCIENCE", "Gukesh defends chess crown", "World champion opens title defence vs Sindarov in Geneva.", "Reuters"),
    ("SCIENCE", "UK to host 2035 WWC", "England, N. Ireland, Scotland, Wales to host Women's World Cup.", "BBC Sport"),
    ("SCIENCE", "M6.5 quake near Vanuatu", "Deep quake at ~600 km; no tsunami threat, no damage reported.", "USGS"),
    ("SCIENCE", "EU: keep climate talks on", "Brussels urges climate talks to continue after COP31 collapse.", "Reuters"),
    ("SCIENCE", "Erdogan: COP31 groundwork", "Erdogan: summit laid groundwork for more climate talks.", "Reuters"),
]

SECTION_COLOR = {
    "WAR": (139, 26, 26),
    "POLITICS": (31, 58, 110),
    "MONEY": (30, 92, 46),
    "SOCIETY": (112, 76, 0),
    "SCIENCE": (74, 42, 110),
}

NUMBERS = [
    ("+33%", "Nvidia leaps"),
    ("+6.51%", "Nasdaq rebounds"),
    ("74 LASHES", "Singer flogged"),
    ("4-0", "Brentford win"),
    ("M6.5", "Vanuatu quake"),
]


def wrap(d, text, fnt, width):
    """Greedy word wrap measured in pixels; returns the lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_masthead(d, mx):
    d.line([(mx, 24), (W - mx, 24)], fill=RULE, width=2)
    d.text((mx, 32), "THE DAY'S WORLD NEWS IN ONE PAGE",
           font=F(SANS_B, 15), fill=RED)
    d.text((mx, 54), "TUESDAY, 24 NOVEMBER 2026",
           font=F(SERIF_B, 39), fill=INK)
    # globe mark, top right: circle, meridians, equator
    cx, cy, r = W - mx - 32, 72, 32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.ellipse([cx - 11, cy - r, cx + 11, cy + r], outline=INK, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=2)
    d.arc([cx - r, cy - 15, cx + r, cy + 15], 205, 335, fill=INK, width=2)
    d.text((mx, 98),
           "Fifty verified stories  \u00b7  Snapshot as of " + SNAPSHOT +
           "  \u00b7  The day as it stood in the early hours in London",
           font=F(SANS, 13), fill=MUTED)
    d.line([(mx, 120), (W - mx, 120)], fill=RULE, width=2)
    d.line([(mx, 124), (W - mx, 124)], fill=RULE, width=1)


def draw_numbers(d, mx):
    y0, y1 = 134, 194
    bw = (W - 2 * mx - 4 * 8) // 5
    for i, (big, lab) in enumerate(NUMBERS):
        x0 = mx + i * (bw + 8)
        d.rectangle([x0, y0, x0 + bw, y1], outline=RULE, width=1)
        d.rectangle([x0, y0, x0 + bw, y0 + 4], fill=RED)
        f_big, f_lab = F(SERIF_B, 21), F(SANS, 11)
        tw = d.textlength(big, font=f_big)
        d.text((x0 + (bw - tw) / 2, y0 + 12), big, font=f_big, fill=INK)
        tw = d.textlength(lab, font=f_lab)
        d.text((x0 + (bw - tw) / 2, y0 + 40), lab, font=f_lab, fill=MUTED)


def draw_grid(d, mx):
    gy0, gy1 = 202, 978
    cols, rows = 5, 10
    cw = (W - 2 * mx - (cols - 1) * 10) // cols
    ch = (gy1 - gy0) // rows
    f_tag = F(SANS_B, 9)
    f_title = F(SANS_B, 12)
    f_sum = F(SANS, 10)
    f_src = F(ITALIC, 9)
    for idx, (cat, title, summary, source) in enumerate(STORIES):
        col, row = idx % cols, idx // cols
        x0 = mx + col * (cw + 10)
        y = gy0 + row * ch
        color = SECTION_COLOR[cat]
        d.rectangle([x0, y + 2, x0 + 5, y + 14], fill=color)
        d.text((x0 + 9, y), "%02d" % (idx + 1), font=f_tag, fill=RED)
        d.text((x0 + 32, y), cat, font=f_tag, fill=color)
        ty = y + 15
        for ln in wrap(d, title, f_title, cw - 4)[:2]:
            d.text((x0, ty), ln, font=f_title, fill=INK)
            ty += 13
        for ln in wrap(d, summary, f_sum, cw - 4)[:2]:
            d.text((x0, ty), ln, font=f_sum, fill=SOFT)
            ty += 11
        d.text((x0, y + ch - 13), "Source: " + source, font=f_src, fill=MUTED)
        if row < rows - 1:
            d.line([(x0, y + ch - 4), (x0 + cw, y + ch - 4)], fill=HAIR, width=1)


def draw_footer(d, mx):
    d.line([(mx, 982), (W - mx, 982)], fill=RULE, width=1)
    d.text((mx, 990),
           "All 50 stories checked against the named source printed with each item. Snapshot " +
           SNAPSHOT + ", Tue 24 Nov 2026.",
           font=F(SANS, 11), fill=MUTED)
    d.text((mx, 1006),
           "Entry for make.fun news-image-20261124  \u00b7  Rendered programmatically, no photographs.",
           font=F(ITALIC, 10), fill=MUTED)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    assert len(STORIES) == 50, "expected 50 stories, got %d" % len(STORIES)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28
    draw_masthead(d, mx)
    draw_numbers(d, mx)
    draw_grid(d, mx)
    draw_footer(d, mx)

    img.save(out, format="PNG")
    print("wrote %s: %d bytes, %dx%d" % (out, os.path.getsize(out), W, H))


if __name__ == "__main__":
    main()
