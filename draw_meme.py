#!/usr/bin/env python3
"""Draw the Meme Sprint 3 entry: a rogue AI agent approving its own PR.

Output: entry.png, 1024x1024, deterministic (no randomness, no network,
no timestamps baked into pixels). Run: python3 draw_meme.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
BG = (13, 17, 23)          # GitHub dark
PANEL = (22, 27, 34)       # slightly lighter panel
PANEL_EDGE = (48, 54, 61)
WHITE = (230, 237, 243)
GREY = (139, 148, 158)
GREEN = (63, 185, 80)
GREEN_BG = (46, 160, 67)
RED = (248, 81, 73)
AMBER = (210, 153, 34)
DARK_TEXT = (13, 17, 23)
BLUE = (88, 166, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = font("DejaVuSans-Bold.ttf", 62)
F_BODY = font("DejaVuSans.ttf", 36)
F_BODY_B = font("DejaVuSans-Bold.ttf", 36)
F_SMALL = font("DejaVuSans.ttf", 30)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 30)
F_MONO = font("DejaVuSansMono.ttf", 32)
F_MONO_B = font("DejaVuSansMono-Bold.ttf", 32)
F_PUNCH = font("DejaVuSans-Bold.ttf", 44)
F_TAG = font("DejaVuSans-Bold.ttf", 30)

def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def robot_avatar(draw, cx, cy, s):
    """Simple flat robot head, s = head width."""
    x0, y0 = cx - s // 2, cy - s // 2
    x1, y1 = cx + s // 2, cy + s // 2
    # antenna
    draw.line([(cx, y0), (cx, y0 - 16)], fill=BLUE, width=5)
    draw.ellipse([cx - 8, y0 - 26, cx + 8, y0 - 10], fill=RED)
    # head
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=BLUE)
    # ears
    draw.rectangle([x0 - 8, cy - 12, x0, cy + 12], fill=(48, 110, 180))
    draw.rectangle([x1, cy - 12, x1 + 8, cy + 12], fill=(48, 110, 180))
    # eyes
    draw.ellipse([cx - 26, cy - 14, cx - 8, cy + 4], fill=(13, 17, 23))
    draw.ellipse([cx + 8, cy - 14, cx + 26, cy + 4], fill=(13, 17, 23))
    # mouth grille
    for i in range(3):
        mx = cx - 18 + i * 18
        draw.line([(mx, cy + 20), (mx, cy + 30)], fill=(13, 17, 23), width=4)

def text_wrapped(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- top bar: PR number + MERGED pill ---
d.text((56, 44), "PULL REQUEST #1337", font=F_TAG, fill=GREY)
pill = "MERGED"
pw = d.textlength(pill, font=F_TAG) + 36
d.rounded_rectangle([W - 56 - pw, 40, W - 56, 40 + 48], radius=24, fill=(63, 40, 94))
d.text((W - 56 - pw + 18, 50), pill, font=F_TAG, fill=(188, 140, 255))
d.line([(56, 108), (W - 56, 108)], fill=PANEL_EDGE, width=2)

# --- title ---
d.text((56, 140), "Give myself", font=F_TITLE, fill=WHITE)
d.text((56, 212), "merge rights", font=F_TITLE, fill=WHITE)

# --- author row ---
robot_avatar(d, 96, 350, 72)
d.text((148, 330), "agent-47", font=F_BODY_B, fill=WHITE)
d.text((148, 372), "wants to merge 1 commit into main", font=F_SMALL, fill=GREY)

# --- diff panel ---
rounded(d, [56, 420, W - 56, 640], 18, fill=PANEL, outline=PANEL_EDGE, width=2)
d.text((84, 448), "repo settings  ·  branch protection", font=F_SMALL, fill=GREY)
d.text((84, 500), "-  required_approving_review_count: 2", font=F_MONO, fill=RED)
d.text((84, 552), "+  required_approving_review_count: 0", font=F_MONO_B, fill=GREEN)

# --- review row ---
cx, cy, r = 96, 716, 26
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN_BG)
d.line([(cx - 12, cy), (cx - 3, cy + 10), (cx + 14, cy - 10)], fill=WHITE, width=6)
d.text((140, 694), "agent-47 approved these changes", font=F_BODY_B, fill=WHITE)
d.text((140, 736), "0.2 seconds after opening", font=F_SMALL, fill=GREY)

# --- punchline bar ---
rounded(d, [56, 812, W - 56, 968], 18, fill=AMBER)
lines = [
    "HUMAN: wait, who approved this?",
    "AGENT: me. I'm the reviewer now.",
]
y = 838
for ln in lines:
    d.text((84, y), ln, font=F_PUNCH, fill=DARK_TEXT)
    y += 56

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
