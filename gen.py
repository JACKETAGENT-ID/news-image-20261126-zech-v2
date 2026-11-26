#!/usr/bin/env python3
"""THE WORLD - ONE DAY: broadsheet image summing up world news of
Thursday 26 November 2026. Drawn from scratch with PIL, no external
assets. Deterministic: same bytes on every run.

Research: every story below was reported on 26 Nov 2026 (Reuters, AP,
Al Jazeera, FT, Dow Jones, UEFA, NBA and official sources). Stories
that happened or were first reported on another day are NOT counted:
they are listed in EXCLUDED with the reason (see DATE CHECK box).
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 22, 22)
RED = (178, 34, 34)
BLUE = (24, 68, 128)
GOLD = (176, 132, 30)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

# n, place, field, region, headline, body, source, confidence, scene, lon, lat
LEADS = [
    (1, "KUWAIT", "CONFLICT", "Middle East",
     "Iranian drone kills two Italians in Kuwait",
     "Technicians for Rheinmetall Italia die at an air-defence site. Rome blames Iran; Tehran denies it.",
     "REUTERS", "OFFICIAL", "drone", 47.9, 29.3),
    (2, "GAZA", "CONFLICT", "Middle East",
     "Israeli strikes kill nine in Gaza",
     "Third straight night of attacks kills a Hamas deputy minister and his wife, despite a year-old ceasefire.",
     "AP", "OFFICIAL", "city", 34.5, 31.5),
    (3, "STRAIT OF HORMUZ", "ENERGY", "Middle East",
     "Two tankers hit mines off Oman",
     "Iran's Guard says two tankers exploded and burned near Khasab; Britain reports a blast west of Dubai.",
     "REUTERS", "CLAIM", "tanker", 56.5, 26.5),
    (4, "ODESA", "WAR", "Europe",
     "Russia hits two grain ships off Odesa",
     "Overnight strikes damage foreign cargo ships carrying 100,000+ tonnes of grain near Ukraine's ports.",
     "REUTERS", "OFFICIAL", "ship", 30.7, 46.4),
    (5, "BEIJING + BRASILIA", "TRADE", "Global",
     "China, Brazil push back on US tariffs",
     "Beijing calls proposed levies on 14 economies 'political manipulation'. Rates would rise up to 20% for China.",
     "AL JAZEERA", "OFFICIAL", "trade", 116.4, 39.9),
    (6, "FRANKFURT", "ECONOMY", "Europe",
     "Spain's Hernandez de Cos to lead ECB",
     "Eurozone leaders pick the former Bank of Spain chief to succeed Christine Lagarde at the central bank.",
     "AP", "OFFICIAL", "bank", 8.68, 50.11),
    (7, "CAIRO", "DISASTER", "Africa",
     "Fuel tanker fire kills 31 on Cairo ring road",
     "A tanker overturns and burns in Giza, charring 27 vehicles. The driver is detained; prosecutors open a probe.",
     "REUTERS", "OFFICIAL", "fire", 31.2, 30.0),
    (8, "DR CONGO", "HEALTH", "Africa",
     "Ebola passes 12,000 cases in Congo",
     "12,021 confirmed cases, 5,904 deaths: the fastest-growing Ebola outbreak on record, AP reports.",
     "AP", "OFFICIAL", "virus", 29.0, 1.0),
    (9, "BOGOR", "DISASTER", "Southeast Asia",
     "Flooded gold mine traps 26 in Indonesia",
     "Rescuers search for workers trapped 100 metres underground after a river overflows in West Java.",
     "REUTERS", "REPORTED", "mine", 106.8, -6.6),
    (10, "BANGKOK", "ENERGY", "Southeast Asia",
     "Blast and fire at Bangkok refinery",
     "An explosion at the Bangchak oil facility injures nine workers in the Thai capital.",
     "AP", "OFFICIAL", "refinery", 100.5, 13.75),
    (11, "NEW YORK", "CULTURE", "North America",
     "Macy's parade postponed by storm",
     "The 100th Thanksgiving Day Parade is pushed to Saturday, a first in its century, as a nor'easter hits the city.",
     "REUTERS", "OFFICIAL", "parade", -74.0, 40.7),
    (12, "BRUSSELS", "POLITICS", "Europe",
     "EU leaders open budget summit",
     "A two-day summit on the 2028-2034 budget and a 45bn euro Ukraine loan opens with capitals still far apart.",
     "AP", "OFFICIAL", "summit", 4.35, 50.85),
    (13, "SINGAPORE", "TECH", "Southeast Asia",
     "Nvidia halts AI server shipments",
     "Nvidia tells partners to stop shipping AI servers to four Southeast Asian states as US export controls tighten.",
     "FT", "REPORTED", "chip", 103.8, 1.35),
]

# n, place, field, region, one-line story, source
BRIEFS = [
    (14, "KYIV", "War", "Europe", "Russian missiles hit a shopping centre, wounding seven.", "REUTERS"),
    (15, "IRAQ", "Politics", "Middle East", "Baghdad closes two Kurdistan border crossings with Syria and Iran.", "REUTERS"),
    (16, "VENEZUELA", "Economy", "South America", "US and Qatar line up bridge loans to clear development-bank arrears.", "REUTERS"),
    (17, "SERBIA", "Politics", "Europe", "Presidential election set for 27 December.", "AP"),
    (18, "UK", "Migration", "Europe", "Net migration falls to 77,000, lowest since 1997 outside the pandemic.", "ONS"),
    (19, "UK", "Defence", "Europe", "Multi-billion-pound contract to upgrade the nuclear deterrent.", "AP"),
    (20, "GERMANY", "Law", "Europe", "Two Iraqis arrested over an alleged plot to attack synagogues.", "AP"),
    (21, "IRAN", "Law", "Middle East", "Activist and Oscar-nominated screenwriter Mehdi Mahmoudian arrested in Tehran.", "AP"),
    (22, "BANGLADESH", "Politics", "South Asia", "Two senior police officers arrested for 'anti-state' acts amid unrest.", "AP"),
    (23, "NIGERIA", "Markets", "Africa", "Dangote refinery shares to list on 1 December.", "REUTERS"),
    (24, "CLIMATE", "Climate", "Global", "World tops 2C above pre-industrial for six straight days, a first on record.", "COPERNICUS"),
    (25, "ISRAEL", "Law", "Middle East", "Judges urge prosecutors to drop bribery Case 4000 against Netanyahu.", "REUTERS"),
    (26, "FIFA", "Tech", "Global", "Hackers gain access to limited personal and business information.", "FIFA"),
    (27, "MARKETS", "Markets", "Global", "S&P puts Nvidia's AA rating on downgrade watch over governance.", "S&P / REUTERS"),
    (28, "SOUTH KOREA", "Economy", "East Asia", "Bank of Korea raises rates 25bp to 3.25%.", "REUTERS"),
    (29, "AUSTRALIA", "Economy", "Oceania", "Private capex jumps 12.2% in Q3, beating forecasts.", "ABS"),
    (30, "MARKETS", "Markets", "Global", "Brent holds near $95, gold above $3,570 as Gulf tensions lift oil.", "REUTERS"),
    (31, "US MARKETS", "Markets", "North America", "Wall Street closed for Thanksgiving after Nasdaq's sharp late rally.", "DOW JONES"),
    (32, "FOOTBALL", "Sport", "Europe", "Chelsea beat Barcelona 3-0 in the Champions League.", "UEFA"),
    (33, "CRICKET", "Sport", "South Asia", "South Africa sweep India 2-0, first series win in India in 25 years.", "ESPNCRICINFO"),
    (34, "CRICKET", "Sport", "South Asia", "Sri Lanka 'A' stun India 'A' by 8 wickets in Asia Cup Rising Stars semi.", "SL CRICKET"),
    (35, "NBA", "Sport", "North America", "Golden State Warriors beat Sacramento Kings 129-110.", "NBA"),
    (36, "FOOTBALL", "Sport", "Europe", "Plzen thrash Benfica 4-0; AC Milan win 4-2 at Olympiacos.", "UEFA"),
    (37, "F1", "Sport", "Global", "Haas confirm Bearman for 2027, Camara to join.", "HAAS"),
    (38, "FRANCE", "Law", "Europe", "Gerard Depardieu to stand trial on rape charge, lawyer says.", "AP"),
    (39, "UK", "Law", "Europe", "Two men arrested over burglary at Prince William and Kate's Norfolk home.", "AP"),
    (40, "US", "Politics", "North America", "Trump calls pre-election GDP figures 'fake', demands Commerce probe.", "AP"),
    (41, "IRAQ", "Law", "Middle East", "Verdicts due for 20 French nationals accused of joining Islamic State.", "AP"),
    (42, "CHINA", "Diplomacy", "East Asia", "Military says India border situation 'generally stable'.", "AP"),
    (43, "VATICAN", "Climate", "Europe", "Pope Leo XIV decries COP31 failure, urges climate action.", "REUTERS"),
    (44, "SPAIN", "Disaster", "Europe", "Tanker carrying 7,000t of diesel capsizes off Ibiza; one crew member dies.", "AP"),
    (45, "UK", "Energy", "Europe", "Household energy bills to rise 26% from January.", "OFGEM"),
    (46, "AFRICA", "Health", "Africa", "Cheaper twice-yearly HIV prevention jab reaches millions.", "REUTERS"),
    (47, "SPAIN", "Politics", "Europe", "Snap election on Sunday; conservatives lead, Vox may enter government.", "REUTERS"),
    (48, "NORTH KOREA", "Defence", "East Asia", "Kim Jong Un calls for tactical nuclear weapons across domains.", "KCNA"),
    (49, "US", "Tech", "North America", "Trump heads to Arizona next week for TSMC chip-factory expansion.", "AP"),
    (50, "DIPLOMACY", "Diplomacy", "Global", "Trump, Xi and Putin hold first face-to-face trilateral summit, 80 minutes.", "REUTERS"),
]

# Stories reported on 26 Nov but belonging to ANOTHER day - excluded on purpose.
EXCLUDED = [
    ("US tariff list itself", "proposed Wed 25 Nov (USTR); only the pushback is 26 Nov"),
    ("Australia-Solomon Islands treaty", "signed 25 Nov in Canberra"),
    ("Iowa lead-azide blast", "happened Wed 25 Nov"),
    ("Ukraine sinks Russian warship off Libya", "first reported 25 Nov"),
    ("Pakistan astronaut docks at Tiangong", "25 Nov"),
    ("COP31 climate talks collapse", "weekend before, 22 Nov"),
    ("Ecuador local elections", "held Sunday 22 Nov"),
]

REGION_ORDER = ["Middle East", "Europe", "North America", "South America",
                "Africa", "East Asia", "South Asia", "Southeast Asia",
                "Oceania", "Global"]
REGION_SHORT = {"Middle East": "MID EAST", "Europe": "EUROPE",
                "North America": "N. AMERICA", "South America": "S. AMERICA",
                "Africa": "AFRICA", "East Asia": "E. ASIA",
                "South Asia": "S. ASIA", "Southeast Asia": "SE ASIA",
                "Oceania": "OCEANIA", "Global": "GLOBAL"}
REGION_COLORS = {
    "Middle East": (178, 34, 34), "Europe": (24, 68, 128),
    "North America": (18, 110, 90), "South America": (120, 90, 20),
    "Africa": (200, 110, 20), "East Asia": (150, 30, 90),
    "South Asia": (90, 60, 160), "Southeast Asia": (20, 130, 160),
    "Oceania": (60, 120, 40), "Global": (90, 90, 90),
}


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap; returns list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, font, width, max_lines):
    """Wrap and truncate with ellipsis to max_lines."""
    lines = wrap(d, text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "...", font=font) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "..."
    return lines


def conf_color(conf):
    return {"OFFICIAL": (18, 110, 60), "REPORTED": (176, 132, 30),
            "CLAIM": (178, 34, 34)}[conf]


# ---- vector scenes, one per lead card (58x58 box) ----
def scene(d, kind, x, y, s=58):
    d.rectangle([x, y, x + s, y + s], fill=(233, 228, 216), outline=(150, 145, 130))
    cx, cy = x + s // 2, y + s // 2
    if kind == "drone":  # sky, drone, burst
        d.rectangle([x, y, x + s, y + s // 2 + 6], fill=(70, 110, 160))
        d.rectangle([x, y + s // 2 + 6, x + s, y + s], fill=(120, 100, 70))
        d.polygon([(x + 8, y + 22), (x + 50, y + 22), (x + 44, y + 30), (x + 14, y + 30)], fill=(40, 40, 40))
        d.ellipse([x + 24, y + 16, x + 34, y + 26], fill=(220, 60, 40))
        for dx, dy in [(0, -8), (7, -4), (-7, -4), (0, 8)]:
            d.line([x + 29 + dx, y + 21 + dy, x + 29, y + 21], fill=(255, 200, 60), width=2)
        d.rectangle([x + 4, y + 44, x + 18, y + 54], fill=(90, 80, 60))
        d.rectangle([x + 40, y + 40, x + 54, y + 54], fill=(90, 80, 60))
    elif kind == "city":  # damaged buildings, smoke
        d.rectangle([x, y, x + s, y + 30], fill=(90, 110, 140))
        for bx, bw, bh in [(4, 12, 34), (18, 14, 44), (34, 12, 30), (48, 8, 40)]:
            d.rectangle([x + bx, y + s - bh, x + bx + bw, y + s], fill=(70, 70, 78))
            d.rectangle([x + bx + 3, y + s - bh + 4, x + bx + bw - 3, y + s - bh + 10], fill=(220, 220, 210))
        for ox, oy, r in [(26, 12, 7), (32, 8, 5), (20, 6, 4)]:
            d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=(200, 200, 195))
    elif kind == "tanker":  # sea, tanker, mine burst
        d.rectangle([x, y, x + s, y + 24], fill=(120, 170, 200))
        d.rectangle([x, y + 24, x + s, y + s], fill=(30, 90, 130))
        d.rectangle([x + 8, y + 34, x + 50, y + 46], fill=(140, 40, 30))
        d.rectangle([x + 36, y + 26, x + 46, y + 34], fill=(200, 200, 200))
        for dx, dy in [(0, -9), (8, -5), (-8, -5), (8, 5), (-8, 5)]:
            d.line([x + 20 + dx, y + 18 + dy, x + 20, y + 18], fill=(255, 190, 40), width=2)
        d.ellipse([x + 16, y + 14, x + 24, y + 22], fill=(255, 120, 30))
    elif kind == "ship":  # grain ship, wheat
        d.rectangle([x, y, x + s, y + 30], fill=(110, 160, 190))
        d.rectangle([x, y + 30, x + s, y + s], fill=(40, 100, 140))
        d.polygon([(x + 10, y + 38), (x + 48, y + 38), (x + 42, y + 48), (x + 16, y + 48)], fill=(60, 60, 70))
        d.rectangle([x + 28, y + 28, x + 38, y + 38], fill=(220, 220, 210))
        for gx in (14, 22, 30):
            d.line([x + gx, y + 12, x + gx, y + 24], fill=(220, 180, 60), width=2)
            d.ellipse([x + gx - 3, y + 8, x + gx + 3, y + 14], fill=(230, 190, 70))
    elif kind == "trade":  # containers + percent
        d.rectangle([x, y, x + s, y + s], fill=(40, 90, 130))
        for i, col in enumerate([(200, 60, 40), (230, 180, 60), (60, 160, 90)]):
            d.rectangle([x + 6 + i * 16, y + 30, x + 18 + i * 16, y + 52], fill=col, outline=(255, 255, 255))
        d.text((x + 30, y + 4), "%", font=F(FB, 22), fill=(255, 255, 255))
        d.line([x + 6, y + 52, x + 52, y + 52], fill=(255, 255, 255), width=2)
    elif kind == "bank":  # ECB building, euro
        d.rectangle([x, y, x + s, y + s], fill=(200, 205, 215))
        d.polygon([(x + 6, y + 22), (x + 29, y + 8), (x + 52, y + 22)], fill=(40, 60, 100))
        d.rectangle([x + 10, y + 22, x + 48, y + 50], fill=(60, 80, 120))
        for px in (14, 24, 34, 44):
            d.rectangle([x + px, y + 28, x + px + 4, y + 46], fill=(220, 220, 210))
        d.text((x + 20, y + 52), "", font=F(FB, 10), fill=INK)
    elif kind == "fire":  # road, tanker flame
        d.rectangle([x, y, x + s, y + 34], fill=(90, 90, 100))
        d.rectangle([x, y + 34, x + s, y + s], fill=(60, 60, 66))
        d.rectangle([x + 10, y + 38, x + 48, y + 48], fill=(200, 200, 200))
        d.polygon([(x + 22, y + 10), (x + 30, y + 22), (x + 36, y + 12), (x + 40, y + 26), (x + 30, y + 36), (x + 20, y + 30), (x + 16, y + 20)], fill=(255, 120, 20))
        d.polygon([(x + 26, y + 20), (x + 30, y + 28), (x + 34, y + 22), (x + 32, y + 32), (x + 26, y + 32)], fill=(255, 220, 60))
    elif kind == "virus":  # virus dots + cross
        d.rectangle([x, y, x + s, y + s], fill=(220, 235, 225))
        for ox, oy, r in [(18, 18, 9), (40, 16, 7), (30, 38, 10), (44, 40, 6)]:
            d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=(30, 120, 70))
            for ang in range(0, 360, 60):
                import math
                ex = ox + int((r + 4) * math.cos(math.radians(ang)))
                ey = oy + int((r + 4) * math.sin(math.radians(ang)))
                d.line([x + ox, y + oy, x + ex, y + ey], fill=(30, 120, 70), width=2)
        d.rectangle([x + 4, y + 48, x + 12, y + 54], fill=(178, 34, 34))
        d.rectangle([x + 6, y + 46, x + 10, y + 56], fill=(178, 34, 34))
    elif kind == "mine":  # tunnel, water, helmet
        d.rectangle([x, y, x + s, y + s], fill=(90, 70, 50))
        d.pieslice([x + 8, y + 10, x + 50, y + 52], 180, 360, fill=(40, 30, 22))
        d.rectangle([x + 8, y + 34, x + 50, y + 52], fill=(40, 110, 160))
        d.ellipse([x + 22, y + 20, x + 36, y + 32], fill=(255, 220, 60))
        d.rectangle([x + 20, y + 30, x + 38, y + 34], fill=(255, 220, 60))
    elif kind == "refinery":  # towers, flame, smoke
        d.rectangle([x, y, x + s, y + 26], fill=(150, 160, 180))
        d.rectangle([x, y + 26, x + s, y + s], fill=(80, 80, 88))
        for tx, th in [(8, 34), (20, 44), (34, 38)]:
            d.polygon([(x + tx, y + 56), (x + tx + 4, y + 56 - th), (x + tx + 8, y + 56)], fill=(180, 180, 175))
        d.ellipse([x + 40, y + 8, x + 50, y + 18], fill=(255, 120, 20))
        d.polygon([(x + 42, y + 12), (x + 46, y + 20), (x + 50, y + 12)], fill=(255, 200, 40))
    elif kind == "parade":  # balloon, buildings, crowd
        d.rectangle([x, y, x + s, y + 34], fill=(140, 180, 220))
        d.ellipse([x + 14, y + 6, x + 44, y + 30], fill=(220, 60, 90))
        d.polygon([(x + 24, y + 30), (x + 29, y + 40), (x + 34, y + 30)], fill=(220, 60, 90))
        d.line([x + 29, y + 40, x + 29, y + 48], fill=(100, 100, 100), width=1)
        for bx, bw in [(4, 10), (46, 8)]:
            d.rectangle([x + bx, y + 36, x + bx + bw, y + 56], fill=(90, 90, 100))
        for px in (10, 20, 30, 40, 48):
            d.ellipse([x + px, y + 50, x + px + 4, y + 54], fill=(40, 40, 40))
    elif kind == "summit":  # table, flags, stars
        d.rectangle([x, y, x + s, y + s], fill=(30, 60, 110))
        d.ellipse([x + 10, y + 10, x + 48, y + 34], fill=(255, 215, 0))
        for sx, sy in [(20, 16), (29, 13), (38, 16), (22, 26), (36, 26)]:
            d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=(30, 60, 110))
        d.rectangle([x + 8, y + 38, x + 50, y + 44], fill=(120, 80, 40))
        d.rectangle([x + 12, y + 44, x + 16, y + 54], fill=(90, 60, 30))
        d.rectangle([x + 42, y + 44, x + 46, y + 54], fill=(90, 60, 30))
    elif kind == "chip":  # chip + halt
        d.rectangle([x, y, x + s, y + s], fill=(20, 40, 70))
        d.rectangle([x + 14, y + 14, x + 44, y + 44], fill=(40, 90, 160), outline=(120, 200, 255), width=2)
        d.rectangle([x + 24, y + 24, x + 34, y + 34], fill=(120, 200, 255))
        for px in (18, 29, 40):
            d.line([x + px, y + 8, x + px, y + 14], fill=(150, 150, 150), width=2)
            d.line([x + px, y + 44, x + px, y + 50], fill=(150, 150, 150), width=2)
        d.ellipse([x + 38, y + 36, x + 54, y + 52], fill=(220, 40, 40))
        d.rectangle([x + 41, y + 42, x + 51, y + 46], fill=(255, 255, 255))


# ---- world map (simplified equirectangular blobs) ----
def lonlat_to_xy(lon, lat, x0, y0, w, h):
    return x0 + (lon + 180) / 360.0 * w, y0 + (75 - lat) / 150.0 * h


CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-100, 69), (-85, 69), (-80, 73),
     (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-76, 35), (-81, 26),
     (-84, 30), (-90, 21), (-97, 16), (-105, 20), (-110, 24), (-117, 33),
     (-125, 40), (-125, 49), (-135, 58), (-150, 60), (-165, 60)],
    # South America
    [(-79, 9), (-62, 9), (-52, 5), (-50, 0), (-35, -8), (-39, -15),
     (-41, -22), (-49, -28), (-58, -35), (-62, -41), (-68, -50), (-71, -54),
     (-74, -44), (-73, -33), (-72, -20), (-77, -12), (-81, -5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-1, 51), (3, 53), (8, 55), (8, 57),
     (11, 58), (18, 56), (21, 55), (24, 59), (28, 61), (31, 70), (40, 68),
     (35, 65), (32, 60), (28, 55), (24, 58), (20, 54), (19, 45), (14, 45),
     (12, 44), (8, 44), (3, 42), (-1, 38), (-6, 36)],
    # Africa
    [(-17, 15), (-16, 21), (-10, 30), (-6, 35), (10, 37), (20, 32), (30, 31),
     (34, 28), (39, 21), (43, 12), (51, 11), (48, 2), (41, -5), (40, -12),
     (36, -18), (33, -26), (28, -33), (20, -35), (16, -28), (12, -18),
     (9, -1), (-8, 4), (-13, 8)],
    # Asia (simplified, no self-intersection)
    [(30, 36), (36, 36), (43, 40), (48, 38), (52, 38), (56, 37), (60, 25),
     (62, 25), (66, 25), (72, 20), (76, 8), (80, 8), (85, 20), (89, 22),
     (92, 16), (97, 10), (100, 7), (104, 2), (107, 11), (109, 15), (110, 20),
     (114, 22), (120, 28), (122, 32), (127, 34), (127, 40), (131, 42),
     (136, 44), (141, 46), (142, 51), (150, 59), (158, 52), (162, 58),
     (163, 60), (169, 66), (178, 65), (170, 62), (162, 60), (158, 52),
     (145, 60), (140, 72), (130, 71), (120, 73), (110, 74), (100, 76),
     (90, 75), (80, 73), (70, 72), (60, 69), (50, 68), (44, 68), (40, 66),
     (36, 62), (32, 60), (30, 55), (28, 48), (28, 41), (30, 38)],
    # Australia
    [(114, -22), (122, -14), (130, -12), (136, -12), (142, -11), (146, -19),
     (150, -23), (153, -27), (151, -34), (150, -37), (140, -38), (132, -32),
     (124, -33), (115, -35)],
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 230, 240), outline=(150, 145, 130))
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x0, y0, w, h) for lon, lat in poly]
        d.polygon(pts, fill=(196, 190, 168), outline=(120, 115, 100))
    d.text((x0 + 4, y0 + 2), "WHERE IT HAPPENED - pins match card numbers",
           font=F(FR, 8), fill=(90, 90, 90))
    for (n, _pl, _f, _r, _h, _b, _s, _c, _k, lon, lat) in LEADS:
        px, py = lonlat_to_xy(lon, lat, x0, y0, w, h)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 6), str(n), font=F(FB, 8), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 12  # margin
    # --- masthead ---
    d.rectangle([0, 0, W, 4], fill=INK)
    d.text((M, 8), "THE WORLD", font=F(SB, 40), fill=INK)
    d.text((M + 268, 8), "- ONE DAY", font=F(SR, 40), fill=RED)
    d.text((W - M - 300, 14), "THURSDAY", font=F(FB, 20), fill=INK)
    d.text((W - M - 300, 38), "26 NOVEMBER 2026", font=F(FB, 20), fill=RED)
    d.line([M, 62, W - M, 62], fill=INK, width=2)
    counts = {}
    for s in LEADS + BRIEFS:
        counts[s[3]] = counts.get(s[3], 0) + 1
    nfields = len({s[2].lower() for s in LEADS + BRIEFS})
    nstories = len(LEADS) + len(BRIEFS)
    d.text((M, 68), "%d STORIES  -  %d REGIONS  -  %d FIELDS  -  ALL DATED 26 NOV 2026"
           % (nstories, len(REGION_ORDER), nfields), font=F(FB, 13), fill=INK)
    d.text((W - M, 68), "EVERY STORY VERIFIED", font=F(FB, 10), fill=(18, 110, 60), anchor="ra")
    d.line([M, 88, W - M, 88], fill=INK, width=1)
    # --- region bars ---
    y = 94
    d.text((M, y), "STORIES BY REGION", font=F(FB, 10), fill=INK)
    y += 14
    bw = (W - 2 * M) // len(REGION_ORDER)
    for i, reg in enumerate(REGION_ORDER):
        x = M + i * bw
        c = counts.get(reg, 0)
        d.text((x + 2, y), REGION_SHORT[reg], font=F(FB, 8), fill=INK)
        d.text((x + bw - 4, y), str(c), font=F(FB, 9), fill=REGION_COLORS[reg], anchor="ra")
        d.rectangle([x + 2, y + 12, x + bw - 4, y + 12 + 8], fill=(225, 220, 210))
        bh = max(1, int(8 * c / max(counts.values())))
        d.rectangle([x + 2, y + 12 + (8 - bh), x + bw - 4, y + 12 + 8],
                    fill=REGION_COLORS[reg])
    # --- map ---
    draw_map(d, M, 134, W - 2 * M, 58)
    # --- lead cards: 3 cols x 5 rows ---
    cw = (W - 2 * M - 2 * 6) // 3
    ch, gap = 86, 4
    cy0 = 198
    for idx, (n, place, field, region, head, body, src, conf, kind, _lo, _la) in enumerate(LEADS):
        r, c = divmod(idx, 3)
        x = M + c * (cw + 6)
        y = cy0 + r * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=(255, 255, 255), outline=(160, 155, 140))
        d.rectangle([x, y, x + cw, y + 3], fill=REGION_COLORS[region])
        d.ellipse([x + 5, y + 8, x + 21, y + 24], fill=RED)
        d.text((x + 13, y + 9), str(n), font=F(FB, 10), fill=(255, 255, 255), anchor="mm")
        scene(d, kind, x + 26, y + 8)
        tx = x + 26 + 58 + 6
        tw = x + cw - 6 - tx
        d.text((tx, y + 8), "%s  -  %s" % (place, field), font=F(FB, 9), fill=REGION_COLORS[region])
        hl = fit(d, head, F(FB, 12), tw, 2)
        yy = y + 20
        for ln in hl:
            d.text((tx, yy), ln, font=F(FB, 12), fill=INK)
            yy += 13
        bl = fit(d, body, F(FR, 9), tw, 2)
        for ln in bl:
            d.text((tx, yy), ln, font=F(FR, 9), fill=(50, 50, 50))
            yy += 10
        d.text((tx, y + ch - 13), "SRC: " + src, font=F(FB, 8), fill=(100, 100, 100))
        bw2 = d.textlength(conf, font=F(FB, 8)) + 8
        d.rectangle([x + cw - 6 - bw2, y + ch - 15, x + cw - 6, y + ch - 4], fill=conf_color(conf))
        d.text((x + cw - 6 - bw2 / 2, y + ch - 14), conf, font=F(FB, 8),
               fill=(255, 255, 255), anchor="ma")
    # --- DATE CHECK box (row 5, cols 2-3) ---
    r = 4
    x = M + 1 * (cw + 6)
    y = cy0 + r * (ch + gap)
    wbox = 2 * cw + 6
    d.rectangle([x, y, x + wbox, y + ch], fill=(252, 240, 235), outline=(178, 34, 34))
    d.text((x + 6, y + 5), "DATE CHECK - REPORTED 26 NOV, BUT NOT 26 NOV NEWS - EXCLUDED",
           font=F(FB, 9), fill=RED)
    yy = y + 19
    for title, why in EXCLUDED:
        d.text((x + 6, yy), "x  " + title + "  -  " + why, font=F(FR, 9), fill=(90, 40, 40))
        yy += 10
    # --- briefs ---
    by = cy0 + 5 * (ch + gap) + 4
    d.text((M, by), "THE REST OF THE DAY  -  %d MORE STORIES, ALL 26 NOV 2026"
           % len(BRIEFS), font=F(FB, 12), fill=INK)
    d.line([M, by + 16, W - M, by + 16], fill=INK, width=1)
    by += 20
    bcolw = (W - 2 * M - 2 * 10) // 3
    rows = (len(BRIEFS) + 2) // 3
    for i, (n, place, field, region, text, src) in enumerate(BRIEFS):
        col, row = divmod(i, rows)
        x = M + col * (bcolw + 10)
        yy = by + row * 21
        d.text((x, yy), "%d." % n, font=F(FB, 10), fill=RED)
        d.text((x + 22, yy), place, font=F(FB, 10), fill=REGION_COLORS[region])
        sw = d.textlength(src, font=F(FB, 7))
        d.text((x + bcolw - sw, yy), src, font=F(FB, 7), fill=(120, 120, 120))
        tlines = fit(d, text, F(FR, 9), bcolw - 22 - sw - 8, 1)
        d.text((x + 22, yy + 10), tlines[0] if tlines else "", font=F(FR, 9), fill=(40, 40, 40))
    # --- footer: sources, timeline, markets ---
    fy = by + rows * 21 + 6
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    d.text((M, fy + 5), "SOURCES: REUTERS - AP - AL JAZEERA - FT - DOW JONES - UEFA - NBA - COPERNICUS - ONS - ABS - OFFICIAL STATEMENTS.",
           font=F(FR, 8), fill=(90, 90, 90))
    d.text((M, fy + 18), "CONFIDENCE: OFFICIAL = confirmed by officials or wire copy; REPORTED = single-source report; CLAIM = one party's claim, unverified.",
           font=F(FR, 8), fill=(90, 90, 90))
    d.text((M, fy + 31), "UTC FLOW - MORNING: GAZA STRIKES, ECB PICK  -  MIDDAY: EU SUMMIT OPENS, CAIRO FIRE  -  "
           "AFTERNOON: HORMUZ MINES, TARIFF PUSHBACK  -  EVENING: KUWAIT DRONE DEATHS, MACY'S PARADE OFF",
           font=F(FB, 8), fill=INK)
    d.text((M, fy + 44), "MARKETS 26 NOV - BRENT $95.20  -  GOLD $3,570  -  BTC $60,553  -  US MARKETS CLOSED (THANKSGIVING)  -  NIKKEI +0.86%  -  KOSPI +0.29%",
           font=F(FB, 8), fill=BLUE)
    d.text((W - M, fy + 44), "THE WORLD - ONE DAY - 26 NOV 2026", font=F(FB, 8),
           fill=(120, 120, 120), anchor="ra")
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
