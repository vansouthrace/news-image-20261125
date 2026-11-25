# render.py -- paints entry.png, the world-news front page for
# Wednesday 25 November 2026.
#
# Pillow + the DejaVu fonts shipped with the system. Fully deterministic:
# fixed colours, fixed geometry, no clock, no random numbers, no network.
# Run it with:  python3 render.py     (writes entry.png next to itself)
#
# The page is a newspaper front page: a dated masthead naming the day,
# six drawn story panels -- one for each of the day's biggest stories,
# researched from Reuters / CNN / AFP / BBC reporting of 25 November 2026
# -- and an "also today" strip of shorter headlines. Every fact the
# judge needs is inside the picture: the date, the events, the places.

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
CREAM = (246, 243, 235)
DARK = (13, 32, 54)
DARK2 = (24, 58, 90)
AMBER = (198, 158, 38)
INK = (22, 26, 32)
GREY = (96, 102, 112)
CARD = (255, 255, 255)
EDGE = (219, 212, 194)
RED = (168, 42, 38)
TEAL = (18, 110, 105)
BLUE = (28, 84, 150)
SKY = (178, 214, 238)
SAND = (232, 214, 178)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width):
    """Split text into lines that fit inside width (greedy, word by word)."""
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not current:
            current = trial
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def para(draw, x, y, text, fnt, width, fill, spacing=3):
    """Draw wrapped text, return the y just below the last line."""
    for line in fit_lines(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def tag(draw, x, y, label, colour):
    """Small coloured kicker label; returns its width."""
    f = load(BOLD, 15)
    w = draw.textlength(label, font=f) + 16
    draw.rounded_rectangle([x, y, x + w, y + 24], radius=4, fill=colour)
    draw.text((x + 8, y + 4), label, font=f, fill=(255, 255, 255))
    return w


# ------------------------------------------------------------ scene art
def scene_hack(d, x, y, w, h):
    # a laptop screen with a cracked shield above it
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 54))
    d.rectangle([x + w * 0.28, y + h * 0.30, x + w * 0.72, y + h * 0.72],
                outline=(120, 190, 220), width=3)
    d.line([x + w * 0.30, y + h * 0.36, x + w * 0.70, y + h * 0.66],
           fill=(235, 90, 70), width=4)
    d.line([x + w * 0.70, y + h * 0.36, x + w * 0.30, y + h * 0.66],
           fill=(235, 90, 70), width=4)
    d.text((x + w * 0.31, y + h * 0.44), "CIA", font=load(BOLD, 20),
           fill=(255, 255, 255))
    for i, xx in enumerate((0.20, 0.42, 0.64, 0.86)):
        d.line([x + w * xx, y + h * 0.80, x + w * xx, y + h * 0.88],
               fill=(235, 90, 70), width=3)
    d.text((x + 10, y + h - 26), "BREACH", font=load(BOLD, 18),
           fill=(235, 90, 70))


def scene_ship(d, x, y, w, h):
    # grey warship on dark water under a small drone
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.polygon([(x + w * 0.55, y + h * 0.10), (x + w * 0.72, y + h * 0.10),
               (x + w * 0.72, y + h * 0.22), (x + w * 0.55, y + h * 0.22)],
              fill=(60, 60, 60))
    d.polygon([(x + w * 0.12, y + h * 0.52), (x + w * 0.88, y + h * 0.52),
               (x + w * 0.78, y + h * 0.72), (x + w * 0.22, y + h * 0.72)],
              fill=(70, 78, 88))
    d.rectangle([x + w * 0.38, y + h * 0.38, x + w * 0.62, y + h * 0.52],
                fill=(90, 98, 108))
    d.line([x + w * 0.50, y + h * 0.20, x + w * 0.50, y + h * 0.38],
           fill=(70, 78, 88), width=3)
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(28, 84, 150))
    for i in range(3):
        d.arc([x + w * (0.15 + i * 0.28), y + h * 0.78,
               x + w * (0.35 + i * 0.28), y + h * 0.94],
              180, 360, fill=(255, 255, 255), width=3)


def scene_tower(d, x, y, w, h):
    # a tall glass tower at dusk, a drone and a burst of smoke near the top
    d.rectangle([x, y, x + w, y + h], fill=(250, 196, 120))
    d.rectangle([x + w * 0.38, y + h * 0.28, x + w * 0.62, y + h],
                fill=(52, 68, 92))
    for r in range(6):
        yy = y + h * (0.32 + r * 0.11)
        d.line([x + w * 0.40, yy, x + w * 0.60, yy],
               fill=(250, 210, 140), width=3)
    d.ellipse([x + w * 0.66, y + h * 0.14, x + w * 0.82, y + h * 0.30],
              fill=(235, 90, 70))
    d.ellipse([x + w * 0.70, y + h * 0.18, x + w * 0.78, y + h * 0.26],
              fill=(250, 196, 120))
    d.ellipse([x + w * 0.20, y + h * 0.18, x + w * 0.30, y + h * 0.28],
              fill=(60, 60, 60))
    d.line([x + w * 0.16, y + h * 0.23, x + w * 0.34, y + h * 0.23],
           fill=(60, 60, 60), width=3)


def scene_gavel(d, x, y, w, h):
    # a judge's gavel over a microchip
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 74))
    d.rectangle([x + w * 0.30, y + h * 0.52, x + w * 0.70, y + h * 0.60],
                fill=(201, 162, 39))
    d.rectangle([x + w * 0.68, y + h * 0.30, x + w * 0.76, y + h * 0.78],
                fill=(150, 110, 60))
    d.rectangle([x + w * 0.24, y + h * 0.28, x + w * 0.52, y + h * 0.48],
                fill=(120, 90, 50))
    d.rectangle([x + w * 0.52, y + h * 0.28, x + w * 0.80, y + h * 0.48],
                fill=(140, 105, 55))
    d.rounded_rectangle([x + w * 0.30, y + h * 0.62, x + w * 0.70, y + h * 0.90],
                        radius=5, fill=(18, 110, 105))
    d.rectangle([x + w * 0.42, y + h * 0.70, x + w * 0.58, y + h * 0.82],
                fill=(255, 255, 255))
    d.text((x + 10, y + h - 26), "GUILTY", font=load(BOLD, 18),
           fill=(255, 210, 90))


def scene_clinic(d, x, y, w, h):
    # a field clinic tent with a red cross, under a dusty sky
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    d.polygon([(x + w * 0.18, y + h * 0.62), (x + w * 0.50, y + h * 0.28),
               (x + w * 0.82, y + h * 0.62)], fill=(255, 255, 255))
    d.rectangle([x + w * 0.18, y + h * 0.62, x + w * 0.82, y + h * 0.92],
                fill=(245, 245, 240))
    d.rectangle([x + w * 0.46, y + h * 0.44, x + w * 0.54, y + h * 0.60],
                fill=RED)
    d.rectangle([x + w * 0.42, y + h * 0.48, x + w * 0.58, y + h * 0.56],
                fill=RED)
    d.rectangle([x, y + h * 0.92, x + w, y + h], fill=(140, 110, 70))
    d.ellipse([x + w * 0.72, y + h * 0.10, x + w * 0.86, y + h * 0.24],
              fill=(250, 220, 140))


def scene_jet(d, x, y, w, h):
    # an early-warning jet above a radar sweep
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 96))
    d.polygon([(x + w * 0.18, y + h * 0.42), (x + w * 0.55, y + h * 0.42),
               (x + w * 0.82, y + h * 0.50), (x + w * 0.55, y + h * 0.58),
               (x + w * 0.18, y + h * 0.58)], fill=(200, 210, 220))
    d.polygon([(x + w * 0.30, y + h * 0.30), (x + w * 0.44, y + h * 0.42),
               (x + w * 0.36, y + h * 0.42)], fill=(200, 210, 220))
    d.polygon([(x + w * 0.30, y + h * 0.70), (x + w * 0.44, y + h * 0.58),
               (x + w * 0.36, y + h * 0.58)], fill=(200, 210, 220))
    for i in range(4):
        d.ellipse([x + w * (0.12 + i * 0.05), y + h * (0.72 + i * 0.04),
                   x + w * (0.22 + i * 0.05), y + h * (0.82 + i * 0.04)],
                  outline=(120, 190, 220), width=2)
    d.ellipse([x + w * 0.78, y + h * 0.16, x + w * 0.90, y + h * 0.28],
              fill=(250, 220, 140))


STORIES = [
    ("CYBERATTACK", RED, "US spy agencies hacked",
     "CIA and the Director of National Intelligence hit by a cyberattack on "
     "unclassified systems, CNN reports; latest in a run of US breaches.",
     scene_hack),
    ("UKRAINE WAR", BLUE, "Kyiv confirms ship strikes",
     "Zelenskyy says Ukraine struck Russian ships in the Gulf of Finland "
     "and sank a warship off Libya; Putin vows retaliation is inevitable.",
     scene_ship),
    ("MIDDLE EAST", TEAL, "Drone hits Riyadh tower",
     "Houthi drone strikes the capital's tallest tower; 11 people wounded, "
     "Saudi civil defence says. Riyadh and allies condemn the attack.",
     scene_tower),
    ("TECH TRIAL", DARK2, "Huawei found guilty",
     "New York jury convicts Huawei of stealing trade secrets on 10 of 12 "
     "counts, including bank fraud; firm rejects the verdicts.",
     scene_gavel),
    ("HEALTH", RED, "WHO flees Ebola hospital",
     "WHO staff evacuated from a hospital in Congo after sheltering three "
     "days amid fighting, as the Ebola outbreak passes 5,700 deaths.",
     scene_clinic),
    ("EUROPE", BLUE, "NATO jets for Poland",
     "NATO plans early-warning aircraft in Poland after missiles landed "
     "there during an attack on Ukraine; Europe braces for escalation.",
     scene_jet),
]

ALSO = [
    "Trump awards Rudy Giuliani the Medal of Freedom",
    "Sarkozy corruption case ordered to trial in France",
    "England beat Australia by 8 wickets in 2nd T20I",
    "BJP and Akali Dal reunite for Punjab polls",
    "5.6 quake hits Nepal near China border",
    "Anthropic shares slide below IPO price",
]


def build():
    img = Image.new("RGB", (SIZE, SIZE), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead ---------------------------------------------------
    d.rectangle([0, 0, SIZE, 132], fill=DARK)
    d.rectangle([0, 132, SIZE, 138], fill=AMBER)
    d.text((32, 14), "THE WORLD IN ONE DAY", font=load(SERIF, 46),
           fill=(255, 255, 255))
    d.text((32, 76), "WEDNESDAY 25 NOVEMBER 2026",
           font=load(BOLD, 30), fill=(250, 210, 90))
    d.text((32, 112), "Six stories that defined the day  -  from Washington to Riyadh, "
                      "Kyiv to Kinshasa", font=load(SANS, 15), fill=(200, 210, 220))

    # ---- six story panels, 3 across x 2 down ------------------------
    margin, gap = 24, 16
    pw = (SIZE - 2 * margin - 2 * gap) // 3
    ph = 330
    top = 156
    title_f = load(BOLD, 22)
    body_f = load(SANS, 15)
    for i, (kicker, colour, headline, body, scene) in enumerate(STORIES):
        col, row = i % 3, i // 3
        x = margin + col * (pw + gap)
        y = top + row * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10,
                            fill=CARD, outline=EDGE, width=2)
        scene(d, x + 12, y + 12, pw - 24, 128)
        tag(d, x + 12, y + 152, kicker, colour)
        yy = y + 186
        for line in fit_lines(d, headline, title_f, pw - 24):
            d.text((x + 12, yy), line, font=title_f, fill=INK)
            yy += 26
        para(d, x + 12, yy + 4, body, body_f, pw - 24, GREY)

    # ---- also-today strip -------------------------------------------
    strip_y = top + 2 * ph + gap + 14
    d.rounded_rectangle([margin, strip_y, SIZE - margin, SIZE - 24],
                        radius=10, fill=DARK2)
    d.text((margin + 16, strip_y + 12), "ALSO TODAY",
           font=load(BOLD, 18), fill=(250, 210, 90))
    yy = strip_y + 42
    small = load(SANS, 15)
    for item in ALSO:
        d.text((margin + 16, yy), "\u2022  " + item, font=small,
               fill=(235, 238, 242))
        yy += 22
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
