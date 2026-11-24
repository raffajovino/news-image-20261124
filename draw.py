#!/usr/bin/env python3
"""draw.py — THE WORLD IN ONE DAY, Tuesday 24 November 2026.

Generates entry.png (1024x1024, RGB) for the make.fun news-image-20261124
bounty: "Sum up 24 November's world news in one image".

Layout (newspaper front page, vintage paper feel):
  masthead -> stats strip -> 3 leads -> 12-story grid -> 18 briefs
  -> DATE CHECK box -> sources footer.
33 verified stories dated Tue 24 Nov 2026 (3 leads + 12 grid + 18 briefs).
DATE CHECK items are excluded from the main page and listed in the box.

Deterministic: fixed fonts, no randomness, no timestamps, no network.
Running this script twice produces a byte-identical entry.png.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
_outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
if not _outdir:
    _outdir = "/output" if os.path.isdir("/output") else os.path.dirname(os.path.abspath(__file__))
os.makedirs(_outdir, exist_ok=True)
OUT = os.path.join(_outdir, "entry.png")

# --- palette (vintage paper, 70s feel) ---
PAPER = (246, 241, 229)      # warm cream
INK = (28, 26, 23)           # near-black warm ink
INK_SOFT = (74, 68, 60)      # muted warm grey for fact lines
RED = (179, 53, 43)          # vintage red accent
TEAL = (31, 78, 95)          # deep teal accent
BAND = (34, 48, 60)          # dark slate for the stats strip
BAND_TEXT = (240, 234, 218)  # cream on the dark band
RULE = (28, 26, 23)
FAINT = (196, 188, 172)      # light rule / dotted map dots
BOX_BG = (238, 232, 214)     # DATE CHECK box background

FONT_DIR = "/usr/share/fonts/truetype"
SERIF = os.path.join(FONT_DIR, "dejavu", "DejaVuSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "dejavu", "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "dejavu", "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "dejavu", "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap. Returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    """Draw lines top-to-bottom; returns y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_one_line(draw, text, fnt, max_w):
    """Shrink font size until text fits max_w on one line. Returns (font, text)."""
    size = fnt.size
    while size > 9 and draw.textlength(text, font=fnt) > max_w:
        size -= 1
        fnt = font(fnt.path, size)
    return fnt, text


# ---------------------------------------------------------------- content
MASTHEAD = "THE WORLD IN ONE DAY"
DATE_LINE = "TUESDAY 24 NOVEMBER 2026"
SUBLINE = "ONE DAY  \u2022  THE WHOLE WORLD  \u2022  33 STORIES"

STATS_1 = "KOSPI +5.6% ~4,974  \u2022  NIKKEI +3.9% ~58,625  \u2022  TAIEX +2.2%  \u2022  HANG SENG +0.4%   \u2014  TUE 24 NOV MORNING"
STATS_2 = "S&P 500 +4.73% 7,237  \u2022  NASDAQ +6.51% 24,090  \u2022  DOW +3.01% 49,595  \u2022  NVIDIA +31%   \u2014  MON CLOSE  \u2022  GOLD ~$3,666  \u2022  BTC ~$63,400"

LEAD1_HEAD = "THREE TANKERS ABLAZE IN HORMUZ"
LEAD1_FACT = ("Iran says three oil tankers hit naval mines and caught fire in the Strait of "
              "Hormuz on Tuesday. Qatar's prime minister warns the region \u201ccannot withstand "
              "another escalation\u201d as 14+ tankers wait at Kharg Island.")

LEAD2_HEAD = "HUANG'S RETURN IGNITES ASIA RALLY"
LEAD2_FACT = ("KOSPI +5.6% to ~4,974 and Nikkei +3.9% to ~58,625 in Tuesday morning trade "
              "after Nvidia reinstated Jensen Huang as CEO on Monday; Nvidia jumped 31%.")

LEAD3_HEAD = "KOREA SCRAMBLES JETS IN AIRSPACE SCARE"
LEAD3_FACT = ("South Korea issued a 3-minute evacuation warning for Ulleung island and "
              "scrambled fighter jets after aircraft entered the ADIZ; their identity "
              "\u2014 Russian or North Korean \u2014 is unconfirmed.")

# (headline, fact) — 12 grid stories. Headlines kept to one line each;
# facts kept short enough to finish inside two lines.
GRID = [
    ("NATO SENDS AWACS TO POLAND",
     "NATO agreed Monday to send an AWACS to its eastern flank; Poland did not invoke Article 4."),
    ("DYMER TOLL RISES TO 11",
     "Toll in Dymer rose to 11, including a young girl; two missing, seven hurt."),
    ("HUANG BACK AT NVIDIA HQ",
     "Huang returned to Nvidia HQ to applause; Monday's +31% lifted its value to $3.94T."),
    ("IRAN HITS US BASES AGAIN",
     "Iran hit US bases and civilian sites in the Gulf \u201cafter a lull,\u201d Al Jazeera reports Tuesday."),
    ("EU PLANS SPORTS BAN",
     "The EU plans a sports ban in new Russia sanctions, targeting crypto financing and \u201cpropaganda.\u201d"),
    ("450 GERMAN SCHOOLS GET BOMB THREATS",
     "Some 450 German schools got bomb threats by email; police in Germany and Denmark investigate."),
    ("GRAMEEN BANK UNDER ATTACK",
     "Branches of the Nobel-winning bank are targeted amid violence by Hasina supporters."),
    ("GAZA'S CHILDREN HUNT FOR INSULIN",
     "Children in besieged Gaza struggle to find life-saving insulin and blood-glucose testing supplies."),
    ("24 DEAD AS NIGERIA BOAT CAPSIZES",
     "At least 24 people were killed after a boat carrying mourners to a funeral capsized in Nigeria."),
    ("FIRE GUTS SIX ZANZIBAR HOTELS",
     "A fire tore through six hotels and dozens of shops in Nungwi, a popular tourist hotspot in Zanzibar."),
    ("IRAN FLOGS SINGER, 74 LASHES",
     "Iran flogged singer Parastoo Ahmadi, 74 lashes, for performing without a headscarf."),
    ("TRUMP OFF TO MAR-A-LAGO",
     "Trump returns to Palm Beach for Thanksgiving; South Ocean Boulevard closes from 5 a.m. Tuesday."),
]

# 18 briefs, one line each: bold lead-in + short fact (kept short so no
# brief is truncated with an ellipsis).
BRIEFS = [
    ("LAHORE TOPS POLLUTION RANKING", "AQI crosses 500."),
    ("4.0 QUAKE HITS PAKISTAN", "near the Afghanistan border."),
    ("SCO: PAKISTAN TO INVITE INDIA", "for a culture ministers' meeting."),
    ("CHINESE OFFICIAL SENTENCED TO DEATH", "for leaking 100 reports."),
    ("KIM RECEIVES INDIA'S NEW ENVOY", "credentials in Pyongyang."),
    ("MISSISSIPPI EX-MAYOR JAILED 37 MONTHS", "bribery over a hotel plan."),
    ("TRUMP TARGETS NEWSOM IN DOJ SPEECH", "over 548 commutations."),
    ("PATEL'S $41M MINNESOTA FRAUD PROBE", "child centres raided."),
    ("KING CHARLES REACHES OUT TO MEGHAN", "after her father's arrest."),
    ("MOSSAD SAVED SWIFT'S VIENNA SHOWS", "from an ISIS-inspired plot."),
    ("DUTCH ACTIVIST DIES BY EUTHANASIA AT 28", "after years of illness."),
    ("KALININGRAD'S $576M LIFELINE", "Russia plans railway ferries."),
    ("SUPERCELL STORM HITS TUPANCIRETA", "devastates the Brazilian town."),
    ("LION ON THE LOOSE IN TURKIYE", "sparks fear among residents."),
    ("KOSPI SIDECAR TRIGGERED 9:06 A.M.", "five minutes of curbed trading."),
    ("HASINA PLANS TO RETURN", "despite a death sentence."),
    ("ANC'S LOWEST-EVER VOTE SHARE", "in South African local elections."),
    ("STORMS BATTER PALESTINIAN TERRITORY", "as Israel curbs aid."),
]

DATECHECK_TITLE = "DATE CHECK \u2014 NOT TODAY"
DATECHECK_BODY = (
    "Big stories from Fri/Mon, NOT Tue 24 Nov: Kerch Bridge strikes (16\u201319 Nov)  \u2022  "
    "ICJ Myanmar genocide ruling (19 Nov)  \u2022  Oxfam Gaza report (23 Nov)  \u2022  "
    "Anthropic Claude Ship launch (23 Nov)  \u2022  Trump Iowa lead-azide pause (23 Nov)  \u2022  "
    "O'Hare ground stop (23 Nov)  \u2022  Nvidia board vote (23 Nov)  \u2022  Kyiv toll 12 + boy rescued (23 Nov)  \u2022  "
    "Java factory fire, 24 killed (23 Nov)  \u2022  Belgium airports shut (23 Nov)  \u2022  "
    "FIFA: UK to host 2035 Women's World Cup (23 Nov)  \u2022  COP31 collapse (22 Nov)"
)

FOOTER = ("Sources: Al Jazeera  \u2022  Reuters  \u2022  Korea JoongAng Daily  \u2022  Times of India  \u2022  AP  \u2022  Fox49/CBS12  \u2014  "
          "Tue 24 Nov 2026. Market figures labelled with as-of; Asian figures are Tuesday-morning, US figures Monday closes.")


# ---------------------------------------------------------------- drawing
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 28                      # side margin
    CW = W - 2 * MX              # content width = 968
    y = 0

    # ---- masthead ----
    y = 16
    f_title = font(SERIF, 47)
    tw = d.textlength(MASTHEAD, font=f_title)
    d.text(((W - tw) / 2, y), MASTHEAD, font=f_title, fill=INK)
    y += 56
    d.line([(MX, y), (W - MX, y)], fill=RULE, width=2)
    y += 5
    d.line([(MX, y), (W - MX, y)], fill=RULE, width=1)
    y += 8
    f_date = font(SANS_B, 18)
    tw = d.textlength(DATE_LINE, font=f_date)
    d.text(((W - tw) / 2, y), DATE_LINE, font=f_date, fill=RED)
    y += 26
    f_sub = font(SANS, 11)
    tw = d.textlength(SUBLINE, font=f_sub)
    d.text(((W - tw) / 2, y), SUBLINE, font=f_sub, fill=INK_SOFT)
    y += 20

    # ---- stats strip (dark band, two lines) ----
    band_y0 = y
    band_h = 46
    d.rectangle([0, band_y0, W, band_y0 + band_h], fill=BAND)
    for i, line in enumerate([STATS_1, STATS_2]):
        # shrink until the line fits the band with a small side margin
        size = 12
        f_stat = font(SANS_B, size)
        while size > 9 and d.textlength(line, font=f_stat) > W - 16:
            size -= 1
            f_stat = font(SANS_B, size)
        tw = d.textlength(line, font=f_stat)
        d.text(((W - tw) / 2, band_y0 + 6 + i * 20), line, font=f_stat, fill=BAND_TEXT)
    y = band_y0 + band_h + 12

    # ---- LEAD 1 (full width, red left bar) ----
    d.rectangle([MX, y, MX + 6, y + 96], fill=RED)
    lx = MX + 18
    f_l1h = font(SERIF, 31)
    f_l1h, _ = fit_one_line(d, LEAD1_HEAD, f_l1h, CW - 18)
    d.text((lx, y), LEAD1_HEAD, font=f_l1h, fill=INK)
    y += 40
    f_l1f = font(SANS, 14)
    lines = wrap(d, LEAD1_FACT, f_l1f, CW - 18)
    y = draw_lines(d, lines, lx, y, f_l1f, INK_SOFT, 19)
    y += 8
    d.line([(MX, y), (W - MX, y)], fill=FAINT, width=1)
    y += 10

    # ---- LEAD 2 + LEAD 3 (two columns) ----
    col_w = (CW - 16) // 2
    col2_x = MX + col_w + 16
    d.line([(MX + col_w + 8, y), (MX + col_w + 8, y + 108)], fill=FAINT, width=1)
    for cx, head, fact in ((MX, LEAD2_HEAD, LEAD2_FACT), (col2_x, LEAD3_HEAD, LEAD3_FACT)):
        f_h = font(SERIF, 19)
        # headline may take two lines
        hlines = wrap(d, head, f_h, col_w)
        yy = y
        yy = draw_lines(d, hlines, cx, yy, f_h, INK, 23)
        yy += 3
        f_f = font(SANS, 12)
        flines = wrap(d, fact, f_f, col_w)
        draw_lines(d, flines, cx, yy, f_f, INK_SOFT, 16)
    y += 108
    y += 8
    d.line([(MX, y), (W - MX, y)], fill=RULE, width=2)
    y += 8

    # ---- GRID: 12 stories, 3 cols x 4 rows ----
    f_gsec = font(SANS_B, 12)
    d.text((MX, y), "AROUND THE WORLD", font=f_gsec, fill=TEAL)
    y += 20
    grid_top = y
    gutter = 14
    cell_w = (CW - 2 * gutter) // 3
    row_h = 66
    f_gh = font(SERIF, 15)
    f_gf = font(SANS, 11)
    for i, (head, fact) in enumerate(GRID):
        r, c = divmod(i, 3)
        cx = MX + c * (cell_w + gutter)
        cy = grid_top + r * row_h
        if c > 0:
            d.line([(cx - gutter // 2, cy + 2), (cx - gutter // 2, cy + row_h - 10)], fill=FAINT, width=1)
        fh, _ = fit_one_line(d, head, f_gh, cell_w)
        d.text((cx, cy), head, font=fh, fill=INK)
        flines = wrap(d, fact, f_gf, cell_w)[:2]
        draw_lines(d, flines, cx, cy + 20, f_gf, INK_SOFT, 14)
    y = grid_top + 4 * row_h
    y += 4
    d.line([(MX, y), (W - MX, y)], fill=RULE, width=2)
    y += 8

    # ---- BRIEFS: 18, two columns x 9 rows ----
    d.text((MX, y), "IN BRIEF", font=f_gsec, fill=TEAL)
    y += 20
    brief_top = y
    bcol_w = (CW - 16) // 2
    bcol2_x = MX + bcol_w + 16
    brow_h = 18
    f_bb = font(SANS_B, 11)
    f_br = font(SANS, 11)
    for i, (lead, rest) in enumerate(BRIEFS):
        c = 0 if i < 9 else 1
        r = i % 9
        bx = MX if c == 0 else bcol2_x
        by = brief_top + r * brow_h
        # red bullet
        d.ellipse([bx, by + 5, bx + 5, by + 10], fill=RED)
        tx = bx + 11
        lead_txt = lead + " \u2014 "
        lw = d.textlength(lead_txt, font=f_bb)
        avail = bcol_w - 11
        rest_txt = rest
        # truncate the rest (with an ellipsis) only if the full line overflows
        combined_w = lw + d.textlength(rest_txt, font=f_br)
        while combined_w > avail and len(rest_txt) > 10:
            rest_txt = rest_txt.rsplit(" ", 1)[0] + "\u2026"
            combined_w = lw + d.textlength(rest_txt, font=f_br)
        d.text((tx, by), lead_txt, font=f_bb, fill=INK)
        d.text((tx + lw, by), rest_txt, font=f_br, fill=INK_SOFT)
    y = brief_top + 9 * brow_h
    y += 6
    d.line([(MX, y), (W - MX, y)], fill=RULE, width=2)
    y += 8

    # ---- DATE CHECK box ----
    box_y0 = y
    box_h = 74
    d.rectangle([MX, box_y0, W - MX, box_y0 + box_h], fill=BOX_BG, outline=RULE, width=1)
    f_dt = font(SANS_B, 13)
    d.text((MX + 10, box_y0 + 6), DATECHECK_TITLE, font=f_dt, fill=RED)
    f_db = font(SANS, 11)
    blines = wrap(d, DATECHECK_BODY, f_db, CW - 20)[:3]
    draw_lines(d, blines, MX + 10, box_y0 + 26, f_db, INK_SOFT, 14)
    y = box_y0 + box_h + 6

    # ---- footer ----
    f_ft = font(SANS, 10)
    flines = wrap(d, FOOTER, f_ft, CW)[:2]
    for line in flines:
        tw = d.textlength(line, font=f_ft)
        d.text(((W - tw) / 2, y), line, font=f_ft, fill=INK_SOFT)
        y += 13

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes, final y={y}")


if __name__ == "__main__":
    main()
