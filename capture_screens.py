"""
Captura screenshots de cada tela do Hero of the Water v5.0
para uso como referência no protótipo Figma.
Salva cada tela como PNG em 960x640.
"""

import pygame
import sys
import random
import math
import os

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)

SCREEN_W, SCREEN_H = 960, 640
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Screenshot Capture - Hero of the Water v5.0")

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figma_screens")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# CORES (copiadas do jogo)
# ============================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
DARK_BLUE = (13, 27, 42)
WATER_BLUE = (64, 164, 223)
WATER_LIGHT = (100, 195, 240)
WATER_DARK = (40, 120, 180)
GRASS_GREEN = (76, 153, 0)
GRASS_DARK = (55, 115, 0)
GRASS_LIGHT = (100, 180, 30)
DIRT_BROWN = (139, 90, 43)
DIRT_DARK = (100, 65, 30)
DIRT_LIGHT = (170, 120, 60)
RED = (220, 50, 50)
HEART_RED = (230, 60, 70)
YELLOW = (255, 215, 0)
STAR_YELLOW = (255, 200, 50)
ORANGE = (230, 126, 34)
GREEN_OK = (80, 200, 80)
GREEN_BTN = (100, 180, 60)
GREEN_BTN_H = (120, 200, 80)
BROWN_BTN = (120, 80, 40)
BROWN_BTN_H = (150, 100, 55)
GRAY_BTN = (100, 100, 110)
GOLD = (255, 200, 50)
CLOUD_WHITE = (245, 250, 255)
CLOUD_SHADOW = (215, 225, 238)
POPUP_BG = (20, 40, 60)
CONCRETE_GRAY = (160, 155, 150)
PIPE_GRAY = (140, 140, 150)
PIPE_DARK = (100, 100, 110)
PIPE_LIGHT = (180, 180, 190)
TREE_GREEN = (50, 140, 50)
TREE_DARK = (35, 100, 35)
TREE_LIGHT = (70, 170, 70)
TREE_TRUNK = (120, 70, 30)
POLLUTION_GREEN = (80, 120, 40)
POLLUTION_DARK = (50, 80, 30)

SAMUEL_SKIN = (160, 100, 60)
SAMUEL_SKIN_LIGHT = (180, 120, 75)
SAMUEL_HAIR = (45, 25, 12)
CAPE_RED = (200, 40, 40)
CAPE_DARK = (160, 30, 30)
SHIRT_WHITE = (240, 240, 240)
VEST_ORANGE = (220, 140, 40)
VEST_DARK = (190, 115, 30)
PANTS_BROWN = (100, 70, 40)
PANTS_DARK = (80, 55, 30)
SHOE_RED = (200, 50, 50)
BELT_BROWN = (80, 50, 25)

PHASE_CARD_1 = (60, 140, 180)
PHASE_CARD_2 = (140, 100, 60)
PHASE_CARD_3 = (80, 160, 100)
PHASE_CARD_4 = (100, 80, 150)
PHASE_CARD_5 = (180, 80, 80)
PHASE_CARD_LOCKED = (60, 65, 75)

STATION_FILTER = (100, 160, 200)
STATION_TREAT = (180, 140, 60)
STATION_DISINF = (160, 60, 160)
STATION_RELEASE = (60, 180, 100)

MACHINE_BLUE = (60, 140, 160)
MACHINE_DARK = (40, 100, 120)
WINDOW_DARK = (30, 35, 45)
WINDOW_LIT = (255, 220, 100)
HOUSE_WALL = (200, 180, 160)
HOUSE_ROOF = (180, 80, 60)
HOUSE_DOOR = (120, 70, 40)
SAND_COLOR = (210, 190, 150)

# ============================================================
# FONTES
# ============================================================
font_tiny = pygame.font.SysFont('arial', 16)
font_small = pygame.font.SysFont('arial', 20)
font_med = pygame.font.SysFont('arial', 26)
font_big = pygame.font.SysFont('arial', 36)
font_title = pygame.font.SysFont('arial', 48)
font_huge = pygame.font.SysFont('arial', 60)

# ============================================================
# PIXEL ART TITLE FONT
# ============================================================
PIXEL_LETTERS = {
    'H': ["1..1","1..1","1111","1..1","1..1"],
    'E': ["1111","1...","111.","1...","1111"],
    'R': ["111.","1..1","111.","1.1.","1..1"],
    'O': [".11.","1..1","1..1","1..1",".11."],
    'F': ["1111","1...","111.","1...","1..."],
    'T': ["11111","..1..","..1..","..1..","..1.."],
    'W': ["1...1","1...1","1.1.1","11.11",".1.1."],
    'A': [".11.","1..1","1111","1..1","1..1"],
    'D': ["111.","1..1","1..1","1..1","111."],
    ' ': ["...","...","...","...","..."],
}

def draw_pixel_text(surface, text, x, y, scale, color, shadow_color=None):
    cursor_x = x
    for ch in text.upper():
        letter = PIXEL_LETTERS.get(ch)
        if letter is None:
            cursor_x += 3 * scale + scale
            continue
        if shadow_color:
            for row_i, row in enumerate(letter):
                for col_i, c in enumerate(row):
                    if c == '1':
                        px = cursor_x + col_i * scale + 2
                        py = y + row_i * scale + 2
                        pygame.draw.rect(surface, shadow_color, (px, py, scale, scale))
        for row_i, row in enumerate(letter):
            for col_i, c in enumerate(row):
                if c == '1':
                    px = cursor_x + col_i * scale
                    py = y + row_i * scale
                    pygame.draw.rect(surface, color, (px, py, scale, scale))
        letter_width = max(len(row) for row in letter)
        cursor_x += letter_width * scale + scale

def pixel_text_width(text, scale):
    total = 0
    for ch in text.upper():
        letter = PIXEL_LETTERS.get(ch)
        if letter is None:
            total += 3 * scale + scale
            continue
        letter_width = max(len(row) for row in letter)
        total += letter_width * scale + scale
    total -= scale
    return max(0, total)

# ============================================================
# FUNCOES DE DESENHO
# ============================================================

def draw_sky_gradient(surface, top_color, bottom_color, height=350):
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_W, y))

def draw_cloud(surface, x, y, size=1.0):
    s = int(10 * size)
    pygame.draw.ellipse(surface, CLOUD_SHADOW, (x + 2, y + 4, s * 5, int(s * 1.8)))
    pygame.draw.ellipse(surface, CLOUD_WHITE, (x, y, s * 5, int(s * 1.8)))
    pygame.draw.ellipse(surface, CLOUD_WHITE, (x + s, y - s, s * 3, int(s * 1.6)))
    pygame.draw.ellipse(surface, (250, 252, 255), (x + int(s * 1.5), y - int(s * 0.4), s * 2, int(s * 1.2)))

def draw_tree(surface, x, y, variant=0):
    trunk_h = 30 + variant * 5
    pygame.draw.rect(surface, TREE_TRUNK, (x + 14, y + 28, 12, trunk_h))
    if variant % 2 == 0:
        pygame.draw.ellipse(surface, TREE_DARK, (x - 4, y - 4, 48, 38))
        pygame.draw.ellipse(surface, TREE_GREEN, (x, y, 40, 32))
        pygame.draw.ellipse(surface, TREE_LIGHT, (x + 8, y + 3, 18, 14))
    else:
        pygame.draw.ellipse(surface, TREE_DARK, (x - 2, y - 8, 44, 42))
        pygame.draw.ellipse(surface, TREE_GREEN, (x + 2, y - 4, 36, 36))
        pygame.draw.ellipse(surface, TREE_LIGHT, (x + 10, y, 16, 16))

def draw_water_drop_title(surface, x, y, size=30, frame=0):
    bob = int(math.sin(frame * 0.06) * 4)
    dy = y + bob
    r = size // 2
    pygame.draw.polygon(surface, WATER_BLUE, [(x + r, dy), (x, dy + int(r * 1.4)), (x + size, dy + int(r * 1.4))])
    pygame.draw.circle(surface, WATER_BLUE, (x + r, dy + int(r * 1.4)), r)
    pygame.draw.circle(surface, WATER_LIGHT, (x + r - r // 3, dy + int(r * 1.0)), r // 3)
    pygame.draw.circle(surface, WHITE, (x + r - r // 3, dy + int(r * 0.8)), max(1, r // 5))

def draw_button(surface, x, y, w, h, text, color, font=None):
    if font is None:
        font = font_big
    rect = pygame.Rect(x, y, w, h)
    shadow = pygame.Rect(x + 3, y + 3, w, h)
    pygame.draw.rect(surface, (0, 0, 0, 80), shadow, border_radius=12)
    pygame.draw.rect(surface, color, rect, border_radius=12)
    highlight = pygame.Rect(x + 4, y + 4, w - 8, h // 3)
    h_color = tuple(min(255, c + 30) for c in color)
    pygame.draw.rect(surface, h_color, highlight, border_radius=8)
    border_color = tuple(max(0, c - 40) for c in color)
    pygame.draw.rect(surface, border_color, rect, 3, border_radius=12)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def draw_heart(surface, x, y, filled=True):
    color = HEART_RED if filled else (70, 70, 75)
    pygame.draw.circle(surface, color, (x + 6, y + 5), 6)
    pygame.draw.circle(surface, color, (x + 16, y + 5), 6)
    pygame.draw.polygon(surface, color, [(x, y + 7), (x + 11, y + 20), (x + 22, y + 7)])
    if filled:
        pygame.draw.circle(surface, (255, 120, 130), (x + 8, y + 3), 2)

def draw_star(surface, x, y, filled=True, size=1.0):
    color = STAR_YELLOW if filled else (70, 70, 75)
    s = size
    points = []
    for i in range(5):
        angle = math.radians(i * 72 - 90)
        points.append((x + 10 + math.cos(angle) * 10 * s, y + 10 + math.sin(angle) * 10 * s))
        angle2 = math.radians(i * 72 - 90 + 36)
        points.append((x + 10 + math.cos(angle2) * 4 * s, y + 10 + math.sin(angle2) * 4 * s))
    pygame.draw.polygon(surface, color, points)

def draw_star_big(surface, x, y, filled=True, size=30):
    color = STAR_YELLOW if filled else (70, 70, 75)
    points = []
    for i in range(5):
        angle = math.radians(i * 72 - 90)
        points.append((x + math.cos(angle) * size, y + math.sin(angle) * size))
        angle2 = math.radians(i * 72 - 90 + 36)
        points.append((x + math.cos(angle2) * size * 0.4, y + math.sin(angle2) * size * 0.4))
    pygame.draw.polygon(surface, color, points)
    if filled:
        inner = []
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            inner.append((x + math.cos(angle) * size * 0.6, y + math.sin(angle) * size * 0.6))
        pygame.draw.polygon(surface, (255, 235, 120), inner)

def draw_mute_button(surface, x=SCREEN_W - 40, y=10):
    pygame.draw.circle(surface, (30, 30, 40), (x + 12, y + 12), 14)
    pygame.draw.circle(surface, (60, 60, 70), (x + 12, y + 12), 14, 2)
    pygame.draw.rect(surface, WHITE, (x + 4, y + 8, 6, 8))
    pygame.draw.polygon(surface, WHITE, [(x + 10, y + 6), (x + 16, y + 2), (x + 16, y + 22), (x + 10, y + 18)])
    pygame.draw.arc(surface, WHITE, (x + 16, y + 5, 8, 14), -0.8, 0.8, 2)

def draw_samuel(surface, x, y, facing_right=True, frame=0, carrying=False, has_grabber=False):
    s = 2
    cx = int(x)
    cy = int(y)
    leg_offset = int(math.sin(frame * 0.15) * 4) if frame != 0 else 0
    # Capa
    if facing_right:
        cape_pts = [(cx + 8, cy + 22), (cx - 4, cy + 52), (cx + 14, cy + 48)]
    else:
        cape_pts = [(cx + 24, cy + 22), (cx + 36, cy + 52), (cx + 18, cy + 48)]
    pygame.draw.polygon(surface, CAPE_RED, cape_pts)
    pygame.draw.polygon(surface, CAPE_DARK, cape_pts, 2)
    # Cabelo
    hair_cx = cx + 16
    hair_cy = cy + 8
    pygame.draw.ellipse(surface, SAMUEL_HAIR, (hair_cx - 11, hair_cy - 12, 22, 18))
    # Cabeca
    pygame.draw.rect(surface, SAMUEL_SKIN, (cx + 8, cy + 10, 16, 16))
    pygame.draw.rect(surface, SAMUEL_SKIN_LIGHT, (cx + 10, cy + 12, 6, 4))
    # Olhos
    if facing_right:
        pygame.draw.rect(surface, BLACK, (cx + 18, cy + 16, 3, 4))
        pygame.draw.rect(surface, WHITE, (cx + 19, cy + 16, 1, 2))
    else:
        pygame.draw.rect(surface, BLACK, (cx + 11, cy + 16, 3, 4))
        pygame.draw.rect(surface, WHITE, (cx + 11, cy + 16, 1, 2))
    # Boca
    pygame.draw.rect(surface, (120, 60, 30), (cx + 13, cy + 22, 6, 2))
    # Corpo
    pygame.draw.rect(surface, SHIRT_WHITE, (cx + 7, cy + 26, 18, 16))
    # Colete
    pygame.draw.rect(surface, VEST_ORANGE, (cx + 5, cy + 26, 6, 16))
    pygame.draw.rect(surface, VEST_ORANGE, (cx + 21, cy + 26, 6, 16))
    # Cinto
    pygame.draw.rect(surface, BELT_BROWN, (cx + 6, cy + 40, 20, 3))
    pygame.draw.rect(surface, YELLOW, (cx + 14, cy + 40, 4, 3))
    # Calcas
    pygame.draw.rect(surface, PANTS_BROWN, (cx + 7, cy + 43, 8, 13 + leg_offset))
    pygame.draw.rect(surface, PANTS_BROWN, (cx + 17, cy + 43, 8, 13 - leg_offset))
    # Tenis
    shoe_y1 = cy + 56 + leg_offset
    shoe_y2 = cy + 56 - leg_offset
    pygame.draw.rect(surface, SHOE_RED, (cx + 4, shoe_y1, 12, 6))
    pygame.draw.rect(surface, SHOE_RED, (cx + 16, shoe_y2, 12, 6))
    pygame.draw.rect(surface, WHITE, (cx + 4, shoe_y1, 12, 2))
    pygame.draw.rect(surface, WHITE, (cx + 16, shoe_y2, 12, 2))
    # Grabber
    if has_grabber:
        gx = cx + 28 if facing_right else cx - 2
        gy = cy + 26
        pygame.draw.rect(surface, (120, 120, 130), (gx, gy, 3, 22))
        pygame.draw.rect(surface, (150, 150, 160), (gx - 2, gy + 20, 7, 4))
    # Galao
    if carrying:
        gx = cx + 28 if facing_right else cx - 10
        gy = cy + 32
        pygame.draw.rect(surface, WATER_BLUE, (gx, gy, 10, 14))
        pygame.draw.rect(surface, WATER_LIGHT, (gx, gy, 10, 4))

def draw_samuel_hero(surface, x, y, frame=0):
    cx = int(x)
    cy = int(y)
    # Capa grande
    cape_pts = [(cx + 12, cy + 42), (cx - 8, cy + 130), (cx + 10, cy + 120),
                (cx + 70, cy + 120), (cx + 88, cy + 130), (cx + 68, cy + 42)]
    pygame.draw.polygon(surface, CAPE_RED, cape_pts)
    pygame.draw.polygon(surface, CAPE_DARK, cape_pts, 2)
    # Cabelo
    pygame.draw.ellipse(surface, SAMUEL_HAIR, (cx + 12, cy - 12, 56, 48))
    # Cabeca
    pygame.draw.rect(surface, SAMUEL_SKIN, (cx + 20, cy + 18, 40, 36))
    pygame.draw.rect(surface, SAMUEL_SKIN_LIGHT, (cx + 24, cy + 22, 14, 10))
    # Olhos
    pygame.draw.ellipse(surface, WHITE, (cx + 24, cy + 30, 14, 12))
    pygame.draw.ellipse(surface, BLACK, (cx + 28, cy + 32, 8, 9))
    pygame.draw.ellipse(surface, WHITE, (cx + 30, cy + 32, 4, 4))
    pygame.draw.ellipse(surface, WHITE, (cx + 42, cy + 30, 14, 12))
    pygame.draw.ellipse(surface, BLACK, (cx + 44, cy + 32, 8, 9))
    pygame.draw.ellipse(surface, WHITE, (cx + 46, cy + 32, 4, 4))
    # Sorriso
    pygame.draw.ellipse(surface, (120, 60, 30), (cx + 30, cy + 44, 20, 10))
    pygame.draw.rect(surface, WHITE, (cx + 33, cy + 44, 14, 5))
    # Corpo
    pygame.draw.rect(surface, SHIRT_WHITE, (cx + 16, cy + 54, 48, 32))
    pygame.draw.rect(surface, VEST_ORANGE, (cx + 10, cy + 54, 14, 32))
    pygame.draw.rect(surface, VEST_ORANGE, (cx + 56, cy + 54, 14, 32))
    # Cinto
    pygame.draw.rect(surface, BELT_BROWN, (cx + 12, cy + 84, 56, 6))
    pygame.draw.rect(surface, YELLOW, (cx + 34, cy + 84, 12, 6))
    # Calcas
    pygame.draw.rect(surface, PANTS_BROWN, (cx + 16, cy + 90, 22, 28))
    pygame.draw.rect(surface, PANTS_BROWN, (cx + 42, cy + 90, 22, 28))
    # Tenis
    pygame.draw.rect(surface, SHOE_RED, (cx + 10, cy + 118, 26, 12))
    pygame.draw.rect(surface, SHOE_RED, (cx + 44, cy + 118, 26, 12))
    pygame.draw.rect(surface, WHITE, (cx + 10, cy + 118, 26, 4))
    pygame.draw.rect(surface, WHITE, (cx + 44, cy + 118, 26, 4))

def draw_ods6_symbol(surface, x, y, size=50):
    rect = pygame.Rect(x, y, size, size)
    ods_cyan = (38, 189, 226)
    pygame.draw.rect(surface, ods_cyan, rect, border_radius=max(2, size // 12))
    drop_cx = x + size // 2
    drop_top = y + int(size * 0.12)
    drop_mid = y + int(size * 0.38)
    drop_r = int(size * 0.16)
    pygame.draw.polygon(surface, WHITE, [
        (drop_cx, drop_top), (drop_cx - drop_r, drop_mid + drop_r // 2),
        (drop_cx + drop_r, drop_mid + drop_r // 2),
    ])
    pygame.draw.circle(surface, WHITE, (drop_cx, drop_mid + drop_r // 2), drop_r)
    num_font = pygame.font.SysFont('arial', max(10, int(size * 0.38)), bold=True)
    num_surf = num_font.render("6", True, WHITE)
    surface.blit(num_surf, (x + size // 2 - num_surf.get_width() // 2, y + int(size * 0.58)))

def draw_water_bar(surface, x, y, current, maximum):
    bar_w = 140
    bar_h = 16
    pygame.draw.polygon(surface, WATER_BLUE, [(x - 10, y + 12), (x - 5, y + 2), (x, y + 12)])
    pygame.draw.circle(surface, WATER_BLUE, (x - 5, y + 13), 5)
    pygame.draw.rect(surface, (30, 30, 35), (x + 4, y + 2, bar_w, bar_h), border_radius=4)
    fill_w = max(0, int((current / maximum) * (bar_w - 4)))
    if fill_w > 0:
        pygame.draw.rect(surface, WATER_BLUE, (x + 6, y + 4, fill_w, bar_h - 4), border_radius=3)
        pygame.draw.rect(surface, WATER_LIGHT, (x + 6, y + 4, fill_w, 5), border_radius=3)

def draw_npc(surface, x, y, thirsty=True, variant=0):
    skin_colors = [(140, 90, 50), (180, 130, 80), (120, 75, 40), (160, 110, 65)]
    shirt_colors = [(80, 130, 180), (180, 80, 80), (80, 160, 80), (180, 160, 60)]
    skin = skin_colors[variant % 4]
    shirt = shirt_colors[variant % 4]
    droop = 4 if thirsty else 0
    pygame.draw.rect(surface, shirt, (x + 4, y + 20 + droop, 16, 18))
    pygame.draw.circle(surface, skin, (x + 12, y + 12 + droop), 10)
    if thirsty:
        pygame.draw.line(surface, BLACK, (x + 8, y + 11 + droop), (x + 10, y + 13 + droop), 2)
        pygame.draw.line(surface, BLACK, (x + 14, y + 11 + droop), (x + 16, y + 13 + droop), 2)
        pygame.draw.arc(surface, BLACK, (x + 8, y + 18 + droop, 8, 6), 0, 3.14, 2)
        pygame.draw.circle(surface, WATER_BLUE, (x + 22, y + 8), 3)
    else:
        pygame.draw.circle(surface, BLACK, (x + 9, y + 12), 2)
        pygame.draw.circle(surface, BLACK, (x + 15, y + 12), 2)
        pygame.draw.arc(surface, BLACK, (x + 7, y + 14, 10, 8), 3.14, 6.28, 2)
    pygame.draw.rect(surface, PANTS_BROWN, (x + 5, y + 38 + droop, 5, 12))
    pygame.draw.rect(surface, PANTS_BROWN, (x + 14, y + 38 + droop, 5, 12))
    pygame.draw.rect(surface, (50, 50, 55), (x + 3, y + 50 + droop, 8, 4))
    pygame.draw.rect(surface, (50, 50, 55), (x + 13, y + 50 + droop, 8, 4))

def draw_house(surface, x, y, has_water=False, variant=0):
    colors = [(HOUSE_WALL, HOUSE_ROOF), ((180, 160, 140), (160, 100, 70)),
              ((190, 190, 170), (100, 130, 100)), ((210, 195, 175), (130, 90, 70))]
    wall_c, roof_c = colors[variant % len(colors)]
    pygame.draw.rect(surface, wall_c, (x, y, 64, 52))
    roof = [(x - 6, y + 2), (x + 32, y - 28), (x + 70, y + 2)]
    pygame.draw.polygon(surface, roof_c, roof)
    pygame.draw.polygon(surface, tuple(max(0, c - 30) for c in roof_c), roof, 2)
    pygame.draw.rect(surface, HOUSE_DOOR, (x + 24, y + 22, 16, 30))
    pygame.draw.circle(surface, YELLOW, (x + 36, y + 38), 2)
    win_color = WATER_LIGHT if has_water else WINDOW_DARK
    pygame.draw.rect(surface, win_color, (x + 6, y + 12, 14, 14))
    pygame.draw.rect(surface, wall_c, (x + 12, y + 12, 1, 14))
    pygame.draw.rect(surface, wall_c, (x + 6, y + 18, 14, 1))
    pygame.draw.rect(surface, win_color, (x + 46, y + 12, 14, 14))

def draw_lixo(surface, x, y, tipo):
    if tipo == 0:
        pygame.draw.rect(surface, (140, 200, 140), (x, y, 14, 22))
        pygame.draw.rect(surface, (120, 180, 120), (x + 4, y - 6, 6, 8))
    elif tipo == 1:
        pygame.draw.rect(surface, (170, 170, 180), (x, y, 16, 18))
        pygame.draw.rect(surface, (200, 50, 50), (x, y + 5, 16, 8))
    elif tipo == 2:
        pygame.draw.circle(surface, (40, 40, 45), (x + 12, y + 12), 14)
        pygame.draw.circle(surface, (55, 55, 60), (x + 12, y + 12), 10)
    elif tipo == 3:
        pygame.draw.ellipse(surface, (210, 210, 220), (x, y, 18, 22))
    elif tipo == 4:
        pygame.draw.rect(surface, (160, 130, 80), (x, y, 18, 14))
        pygame.draw.rect(surface, (140, 110, 65), (x, y, 18, 14), 2)

def draw_water_drop_collectible(surface, x, y):
    pygame.draw.polygon(surface, WATER_BLUE, [(x + 8, y), (x, y + 14), (x + 16, y + 14)])
    pygame.draw.circle(surface, WATER_BLUE, (x + 8, y + 15), 8)
    pygame.draw.circle(surface, WHITE, (x + 5, y + 11), 3)

def draw_pipe_segment(surface, x, y, broken=True):
    pygame.draw.rect(surface, PIPE_GRAY, (x, y, 80, 22))
    pygame.draw.rect(surface, PIPE_LIGHT, (x, y, 80, 6))
    pygame.draw.rect(surface, PIPE_DARK, (x, y + 16, 80, 6))
    pygame.draw.rect(surface, PIPE_DARK, (x, y - 2, 8, 26))
    pygame.draw.rect(surface, PIPE_DARK, (x + 72, y - 2, 8, 26))
    if broken:
        pygame.draw.rect(surface, (160, 100, 60), (x + 30, y + 2, 20, 18))
        points = [(x + 38, y - 2), (x + 42, y + 8), (x + 36, y + 16), (x + 40, y + 24)]
        pygame.draw.lines(surface, BLACK, False, points, 3)
        for i in range(4):
            jx = x + 38 + random.randint(-8, 12)
            jy = y + 22 + random.randint(0, 20)
            pygame.draw.circle(surface, WATER_BLUE, (jx, jy), random.randint(2, 5))

def draw_trash_bin(surface, x, y):
    pygame.draw.rect(surface, (80, 90, 80), (x, y + 8, 36, 44))
    pygame.draw.rect(surface, (60, 70, 60), (x, y + 8, 36, 44), 2)
    pygame.draw.rect(surface, (90, 100, 90), (x - 3, y, 42, 10), border_radius=3)
    pygame.draw.rect(surface, (100, 110, 100), (x + 14, y - 4, 8, 6))
    pygame.draw.circle(surface, GREEN_OK, (x + 18, y + 30), 8, 2)

def draw_treatment_station(surface, x, y, station_type, active=False, completed=False):
    colors = {"filtrar": STATION_FILTER, "tratar": STATION_TREAT,
              "desinfetar": STATION_DISINF, "liberar": STATION_RELEASE}
    labels = {"filtrar": "FILTRAR", "tratar": "TRATAR",
              "desinfetar": "DESINF.", "liberar": "LIBERAR"}
    base_color = colors.get(station_type, PIPE_GRAY)
    if active:
        base_color = tuple(min(255, c + 40) for c in base_color)
    pygame.draw.rect(surface, (60, 60, 65), (x, y + 50, 70, 20))
    pygame.draw.rect(surface, base_color, (x + 5, y, 60, 55), border_radius=6)
    pygame.draw.rect(surface, tuple(max(0, c - 30) for c in base_color), (x + 5, y, 60, 55), 3, border_radius=6)
    label = font_tiny.render(labels.get(station_type, ""), True, WHITE)
    surface.blit(label, (x + 35 - label.get_width() // 2, y + 36))
    if completed:
        pygame.draw.line(surface, GREEN_OK, (x + 22, y + 28), (x + 30, y + 36), 4)
        pygame.draw.line(surface, GREEN_OK, (x + 30, y + 36), (x + 48, y + 18), 4)

def draw_hud(surface, lives, max_lives, water, max_water, stars_count, phase_name, phase_num,
             objective, progress, total, timer_val=None, carrying_count=0, carry_max=0):
    hud = pygame.Surface((SCREEN_W, 65), pygame.SRCALPHA)
    hud.fill((0, 0, 0, 160))
    surface.blit(hud, (0, 0))
    for i in range(max_lives):
        draw_heart(surface, 12 + i * 26, 6, i < lives)
    draw_water_bar(surface, 160, 6, water, max_water)
    for i in range(3):
        draw_star(surface, 330 + i * 26, 4, i < stars_count)
    phase_text = font_small.render(f"FASE {phase_num}: {phase_name}", True, WHITE)
    surface.blit(phase_text, (12, 38))
    obj_text = font_small.render(objective, True, YELLOW)
    surface.blit(obj_text, (SCREEN_W - obj_text.get_width() - 12, 8))
    prog_text = font_med.render(f"{progress}/{total}", True, WHITE)
    surface.blit(prog_text, (SCREEN_W - prog_text.get_width() - 12, 32))
    if carry_max > 0:
        carry_txt = font_small.render(f"Carga: {carrying_count}/{carry_max}", True, WATER_BLUE)
        surface.blit(carry_txt, (430, 38))
    draw_mute_button(surface)


# ============================================================
# TELA 1: DIFICULDADE
# ============================================================
def render_difficulty_screen():
    surface = pygame.Surface((SCREEN_W, SCREEN_H))
    draw_sky_gradient(surface, (60, 130, 200), (120, 180, 210), 400)
    pygame.draw.rect(surface, DIRT_BROWN, (0, 470, SCREEN_W, 170))

    for i, (cx, cy, sz) in enumerate([(80, 30, 1.3), (350, 55, 0.9), (650, 20, 1.1)]):
        draw_cloud(surface, cx, cy, sz)

    title = font_title.render("DIFICULDADE", True, WHITE)
    title_shadow = font_title.render("DIFICULDADE", True, BLACK)
    surface.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 62))
    surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 60))

    sub = font_med.render("Escolha como quer jogar:", True, (200, 220, 255))
    surface.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 220))

    draw_button(surface, SCREEN_W // 2 - 160, 280, 320, 70, "FÁCIL", (60, 160, 60))
    desc = font_tiny.render("Todas as fases desbloqueadas desde o início", True, (180, 240, 180))
    surface.blit(desc, (SCREEN_W // 2 - desc.get_width() // 2, 358))

    draw_button(surface, SCREEN_W // 2 - 160, 370, 320, 70, "MÉDIA", (180, 140, 30))
    desc2 = font_tiny.render("Desbloqueia fases em sequência, progresso salvo", True, (240, 220, 150))
    surface.blit(desc2, (SCREEN_W // 2 - desc2.get_width() // 2, 448))

    draw_button(surface, SCREEN_W // 2 - 160, 460, 320, 70, "DIFÍCIL", (180, 50, 50))
    desc3 = font_tiny.render("Falhar qualquer missão reseta TODO o progresso!", True, (255, 160, 160))
    surface.blit(desc3, (SCREEN_W // 2 - desc3.get_width() // 2, 538))

    draw_mute_button(surface)
    draw_water_drop_title(surface, 40, 55, 22, 20)
    draw_water_drop_title(surface, SCREEN_W - 70, 55, 22, 50)
    return surface


# ============================================================
# TELA 2: MENU PRINCIPAL
# ============================================================
def render_title_screen():
    surface = pygame.Surface((SCREEN_W, SCREEN_H))
    frame = 30

    draw_sky_gradient(surface, (60, 130, 200), (120, 180, 210), 400)

    for i, (cx, cy, sz) in enumerate([(80, 30, 1.3), (350, 55, 0.9), (650, 20, 1.1), (850, 50, 0.7)]):
        draw_cloud(surface, cx, cy, sz)

    # Buildings
    random.seed(77)
    for i in range(8):
        bx = i * 130 + random.randint(-10, 10)
        bw = 60 + random.randint(0, 40)
        bh = 80 + random.randint(0, 80)
        by = 370 - bh
        pygame.draw.rect(surface, (140, 150, 165), (bx, by, bw, bh))
        for wy in range(by + 8, by + bh - 10, 18):
            for wx in range(bx + 6, bx + bw - 12, 16):
                pygame.draw.rect(surface, (180, 210, 230), (wx, wy, 8, 10))
    random.seed()

    # Water
    pygame.draw.rect(surface, WATER_DARK, (0, 370, SCREEN_W, 100))
    for wx in range(0, SCREEN_W, 22):
        wy = 370 + math.sin((wx + frame * 2) * 0.02) * 6
        pygame.draw.ellipse(surface, WATER_BLUE, (wx, int(wy), 30, 12))

    pygame.draw.rect(surface, DIRT_BROWN, (0, 470, SCREEN_W, 170))

    # Title
    title_y = 40
    small_scale = 4
    text1 = "HERO OF THE"
    tw1 = pixel_text_width(text1, small_scale)
    text1_x = SCREEN_W // 2 - tw1 // 2
    draw_pixel_text(surface, text1, text1_x, title_y, small_scale, (220, 235, 255), BLACK)
    draw_water_drop_title(surface, text1_x - 40, title_y - 2, 24, frame)

    big_scale = 10
    text2 = "WATER"
    tw2 = pixel_text_width(text2, big_scale)
    water_text_x = SCREEN_W // 2 - tw2 // 2
    water_text_y = title_y + small_scale * 5 + 12
    draw_pixel_text(surface, text2, water_text_x, water_text_y, big_scale, (80, 170, 220), BLACK)
    draw_water_drop_title(surface, water_text_x + tw2 + 10, water_text_y + 10, 28, frame)

    # Samuel hero
    draw_samuel_hero(surface, SCREEN_W // 2 - 40, 160, frame)

    # ODS 6
    draw_ods6_symbol(surface, 860, 540, 45)

    tag = font_small.render("ODS 6 — Água Potável e Saneamento para Todos", True, (200, 220, 240))
    surface.blit(tag, (SCREEN_W // 2 - tag.get_width() // 2, 560))

    draw_button(surface, SCREEN_W // 2 - 110, 420, 220, 60, "JOGAR", GREEN_BTN)
    draw_button(surface, SCREEN_W // 2 - 110, 495, 220, 50, "INSTRUÇÕES", BROWN_BTN, font_med)
    draw_mute_button(surface)
    return surface


# ============================================================
# TELA 3: INSTRUÇÕES
# ============================================================
def render_instructions_screen():
    surface = pygame.Surface((SCREEN_W, SCREEN_H))
    frame = 30

    for y in range(SCREEN_H):
        ratio = y / SCREEN_H
        r = max(0, min(255, int(15 + 20 * ratio)))
        g = int(25 + 35 * ratio)
        b = max(0, min(255, int(50 + 40 * ratio)))
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_W, y))

    # Ripples
    for ri in range(8):
        rx = int((ri * 140 + frame * 0.6) % (SCREEN_W + 100)) - 50
        ry = SCREEN_H - 20
        pygame.draw.ellipse(surface, (30, 80, 140), (rx, ry, 80, 10))

    title = font_title.render("INSTRUÇÕES", True, WATER_BLUE)
    title_shadow = font_title.render("INSTRUÇÕES", True, BLACK)
    surface.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 22))
    surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 20))

    draw_water_drop_title(surface, 60, 15, 16, frame)
    draw_water_drop_title(surface, SCREEN_W - 80, 15, 16, frame + 30)

    # Samuel
    draw_samuel(surface, 70, 75, True, frame)

    section_y = 90
    sections = [
        ("CONTROLES", YELLOW, [
            ("Setas / WASD", "Mover Samuel"),
            ("Espaço / W / Seta cima", "Pular"),
            ("E", "Interagir (coletar, consertar, entregar)"),
            ("Clique direito (Fase 1)", "Lançar rede para lixo distante"),
            ("M", "Mutar/desmutar som"),
            ("ESC", "Menu / Sair"),
        ]),
        ("OBJETIVO", GOLD, [
            ("", "Samuel precisa salvar a cidade da crise hídrica!"),
            ("", "Complete as 5 fases para restaurar a água limpa."),
        ]),
        ("SISTEMA DE ESTRELAS", STAR_YELLOW, [
            ("3 Estrelas", "Perdeu no máximo 1 coração"),
            ("2 Estrelas", "Perdeu no máximo 2 corações"),
            ("1 Estrela", "Completou a fase (3+ corações perdidos)"),
        ]),
        ("ATENÇÃO", RED, [
            ("", "Se perder todas as vidas: perde TODO o progresso!"),
        ]),
    ]

    y_pos = section_y
    for sec_title, sec_color, items in sections:
        header = font_med.render(sec_title, True, sec_color)
        surface.blit(header, (160, y_pos))
        pygame.draw.line(surface, sec_color, (160, y_pos + 28), (SCREEN_W - 60, y_pos + 28), 1)
        y_pos += 34
        for entry in items:
            key, desc = entry[0], entry[1]
            if key:
                key_surf = font_tiny.render(key, True, WHITE)
                kw = key_surf.get_width() + 12
                pygame.draw.rect(surface, (40, 50, 70), (170, y_pos, kw, 22), border_radius=4)
                pygame.draw.rect(surface, (80, 90, 110), (170, y_pos, kw, 22), 1, border_radius=4)
                surface.blit(key_surf, (176, y_pos + 3))
                desc_surf = font_tiny.render(desc, True, (100, 180, 255))
                surface.blit(desc_surf, (180 + kw + 8, y_pos + 3))
            else:
                desc_surf = font_small.render(desc, True, WHITE)
                surface.blit(desc_surf, (170, y_pos))
            y_pos += 24
        y_pos += 6

    draw_ods6_symbol(surface, SCREEN_W - 70, 90, 40)
    ods_txt = font_tiny.render("ODS 6: Água Limpa", True, WATER_BLUE)
    surface.blit(ods_txt, (SCREEN_W - 120, 135))

    draw_button(surface, SCREEN_W // 2 - 100, 565, 200, 45, "VOLTAR", BROWN_BTN, font_med)
    draw_mute_button(surface)
    return surface


# ============================================================
# TELA 4: SELEÇÃO DE FASES
# ============================================================
def render_phase_select_screen():
    surface = pygame.Surface((SCREEN_W, SCREEN_H))
    frame = 30

    # Background
    for y in range(SCREEN_H):
        ratio = y / SCREEN_H
        r = int(50 + 80 * ratio)
        g = int(120 + 80 * ratio)
        b = int(200 - 30 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_W, y))

    # Sun
    pygame.draw.circle(surface, (255, 240, 160), (780, 100), 50)
    pygame.draw.circle(surface, (255, 250, 200), (780, 100), 38)

    # Clouds
    for i, (cx, cy, sz) in enumerate([(60, 40, 1.4), (280, 60, 1.0), (520, 30, 1.2), (770, 55, 0.8)]):
        draw_cloud(surface, cx, cy, sz)

    # Hills
    pts_hill = [(0, 430)]
    for hx in range(0, SCREEN_W + 20, 20):
        hy = 400 + int(20 * math.sin(hx * 0.01 + 1)) + int(10 * math.sin(hx * 0.025 + 2))
        pts_hill.append((hx, hy))
    pts_hill.append((SCREEN_W, 430))
    pygame.draw.polygon(surface, (55, 130, 60), pts_hill)

    # Trees
    random.seed(555)
    for _ in range(8):
        tx = random.randint(0, SCREEN_W - 40)
        ty = 380
        draw_tree(surface, tx, ty, random.randint(0, 3))
    random.seed()

    # Water
    pygame.draw.rect(surface, WATER_DARK, (0, 430, SCREEN_W, 80))
    for wx in range(0, SCREEN_W, 25):
        wy = 430 + math.sin((wx + frame * 1.5) * 0.025) * 5
        pygame.draw.ellipse(surface, WATER_BLUE, (wx, int(wy), 35, 14))

    pygame.draw.rect(surface, GRASS_GREEN, (0, 510, SCREEN_W, 15))
    pygame.draw.rect(surface, DIRT_BROWN, (0, 525, SCREEN_W, SCREEN_H - 525))

    # Overlay
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 60))
    surface.blit(overlay, (0, 0))

    # Title
    title = font_title.render("ESCOLHA A FASE", True, WHITE)
    title_shadow = font_title.render("ESCOLHA A FASE", True, BLACK)
    surface.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 32))
    surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 30))

    # Stars and progress
    draw_star(surface, 240, 95, True)
    stars_txt = font_med.render("Estrelas: 7/15", True, GOLD)
    surface.blit(stars_txt, (268, 92))
    prog_txt = font_med.render("Progresso: 60%", True, WHITE)
    surface.blit(prog_txt, (520, 92))

    bar_x, bar_y, bar_w = 240, 130, 480
    pygame.draw.rect(surface, (40, 45, 55), (bar_x, bar_y, bar_w, 14), border_radius=7)
    pygame.draw.rect(surface, GREEN_OK, (bar_x, bar_y, int(bar_w * 0.6), 14), border_radius=7)

    # Phase cards
    phase_names = ["Canal do Recife", "Bairro Precário", "Água p/ Todos",
                   "Est. Tratamento", "Crise Final"]
    phase_colors = [PHASE_CARD_1, PHASE_CARD_2, PHASE_CARD_3, PHASE_CARD_4, PHASE_CARD_5]
    descs = ["Limpeza de rios", "Consertar canos", "Distribuir água",
             "Puzzles tratamento", "Crise final!"]
    unlocked = [True, True, True, False, False]
    stars_per = [3, 2, 2, 0, 0]

    card_w, card_h = 150, 180
    total_w = 5 * card_w + 4 * 20
    start_x = (SCREEN_W - total_w) // 2
    for i in range(5):
        bx = start_x + i * (card_w + 20)
        by = 220
        rect = pygame.Rect(bx, by, card_w, card_h)
        color = phase_colors[i] if unlocked[i] else PHASE_CARD_LOCKED

        pygame.draw.rect(surface, BLACK, (rect.x + 4, rect.y + 4, rect.w, rect.h), border_radius=10)
        pygame.draw.rect(surface, color, rect, border_radius=10)
        border_c = tuple(max(0, c - 30) for c in color)
        pygame.draw.rect(surface, border_c, rect, 3, border_radius=10)

        num = font_big.render(str(i + 1), True, WHITE if unlocked[i] else (80, 80, 85))
        surface.blit(num, (rect.centerx - num.get_width() // 2, rect.y + 15))

        if unlocked[i]:
            name = font_tiny.render(phase_names[i], True, WHITE)
            surface.blit(name, (rect.centerx - name.get_width() // 2, rect.y + 60))
            for s in range(3):
                sx = rect.centerx - 36 + s * 26
                draw_star(surface, sx, rect.y + 90, s < stars_per[i])
            desc = font_tiny.render(descs[i], True, (200, 210, 220))
            surface.blit(desc, (rect.centerx - desc.get_width() // 2, rect.y + 130))
        else:
            # Lock icon
            lx, ly = rect.centerx, rect.y + 90
            pygame.draw.rect(surface, (90, 90, 95), (lx - 15, ly, 30, 25), border_radius=4)
            pygame.draw.arc(surface, (90, 90, 95), (lx - 10, ly - 15, 20, 20), 0, 3.14, 3)
            locked_txt = font_tiny.render("BLOQUEADA", True, (100, 100, 105))
            surface.blit(locked_txt, (rect.centerx - locked_txt.get_width() // 2, rect.y + 130))

    warn = font_small.render("Modo Média: desbloqueia fases em sequência", True, (200, 180, 100))
    surface.blit(warn, (SCREEN_W // 2 - warn.get_width() // 2, 440))
    ods = font_small.render("ODS 6 - Água Limpa e Saneamento", True, WATER_BLUE)
    surface.blit(ods, (SCREEN_W // 2 - ods.get_width() // 2, 490))

    draw_button(surface, 30, 560, 140, 40, "VOLTAR", BROWN_BTN, font_med)
    draw_mute_button(surface)
    return surface


# ============================================================
# TELA 5: GAMEPLAY (Fase 1 como exemplo)
# ============================================================
def render_gameplay_screen():
    surface = pygame.Surface((SCREEN_W, SCREEN_H))

    # Background river scene
    draw_sky_gradient(surface, (90, 170, 220), (160, 210, 230))

    # Clouds
    for cx, cy, sz in [(100, 30, 1.2), (350, 60, 0.9), (650, 25, 1.1), (850, 55, 0.7)]:
        draw_cloud(surface, cx, cy, sz)

    # Buildings with variety
    random.seed(42)
    building_colors = [(150,160,170), (140,130,120), (160,150,140), (130,140,155), (170,165,155)]
    for bx in range(0, SCREEN_W, 120):
        bh = 80 + random.randint(0, 60)
        by = 280 - bh
        bw = 40 + random.randint(0, 40)
        bc = building_colors[random.randint(0, len(building_colors)-1)]
        pygame.draw.rect(surface, bc, (bx + 10, by, bw, bh))
        for wy in range(by + 8, by + bh - 10, 18):
            for wx in range(bx + 16, bx + 10 + bw - 6, 16):
                pygame.draw.rect(surface, (180, 210, 230), (wx, wy, 8, 10))
    random.seed()

    # Trees
    for tx in [50, 250, 500, 750]:
        draw_tree(surface, tx, 250, tx % 3)

    # Upper bank
    pygame.draw.rect(surface, GRASS_GREEN, (0, 300, SCREEN_W, 40))
    pygame.draw.rect(surface, GRASS_DARK, (0, 300, SCREEN_W, 6))

    # River
    pygame.draw.rect(surface, WATER_DARK, (0, 340, SCREEN_W, 120))
    for wx in range(0, SCREEN_W, 25):
        wy = 340 + math.sin(wx * 0.025) * 6
        pygame.draw.ellipse(surface, WATER_BLUE, (wx, int(wy), 35, 14))

    # Lower bank
    pygame.draw.rect(surface, GRASS_GREEN, (0, 460, SCREEN_W, 20))
    pygame.draw.rect(surface, DIRT_BROWN, (0, 480, SCREEN_W, 160))
    pygame.draw.rect(surface, DIRT_DARK, (0, 480, SCREEN_W, 6))

    # Obstacles
    for ox in [200, 400, 600, 800]:
        pygame.draw.ellipse(surface, POLLUTION_DARK, (ox, 510, 45, 18))
        pygame.draw.ellipse(surface, POLLUTION_GREEN, (ox + 2, 512, 41, 14))

    # Trash bin
    draw_trash_bin(surface, 80, 475)

    # Ground lixos
    for i, lx in enumerate([250, 350, 500, 650, 850]):
        draw_lixo(surface, lx, 488, i % 5)

    # River lixos
    for i, lx in enumerate([150, 400, 700]):
        draw_lixo(surface, lx, 360 + i * 20, i % 3)

    # Water drops
    for dx in [180, 430, 720]:
        draw_water_drop_collectible(surface, dx, 435)

    # Samuel with grabber
    draw_samuel(surface, 300, 458, True, 15, False, True)

    # Net reticle in river
    pygame.draw.circle(surface, (255, 255, 100), (400, 380), 12, 2)
    pygame.draw.line(surface, (255, 255, 100), (388, 380), (412, 380), 1)
    pygame.draw.line(surface, (255, 255, 100), (400, 368), (400, 392), 1)

    # HUD
    draw_hud(surface, 4, 5, 72, 100, 0, "CANAL DO RECIFE", 1,
             "Deposite lixo na lixeira", 8, 35, None, 3, 7)

    return surface


# ============================================================
# TELA 6: VITÓRIA
# ============================================================
def render_victory_screen():
    surface = pygame.Surface((SCREEN_W, SCREEN_H))
    frame = 30

    draw_sky_gradient(surface, (80, 160, 200), (150, 200, 160), SCREEN_H)
    draw_cloud(surface, 100, 30, 1.2)
    draw_cloud(surface, 500, 60, 0.9)
    draw_cloud(surface, 750, 20, 1.0)

    # Confetti
    random.seed(42)
    for _ in range(20):
        cx = random.randint(0, SCREEN_W)
        cy = random.randint(0, SCREEN_H)
        cc = random.choice([GOLD, RED, GREEN_OK, WATER_BLUE, WHITE])
        pygame.draw.rect(surface, cc, (cx, cy, 6, 6))
    random.seed()

    title = font_title.render("MISSÃO CONCLUÍDA!", True, GOLD)
    surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 40))
    parabens = font_big.render("PARABÉNS!", True, WHITE)
    surface.blit(parabens, (SCREEN_W // 2 - parabens.get_width() // 2, 110))
    msg = font_med.render("Você limpou o Canal do Recife!", True, WHITE)
    surface.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, 165))

    # Stars
    for i in range(3):
        sx = SCREEN_W // 2 - 100 + i * 100
        sy = 230
        draw_star_big(surface, sx, sy, i < 2, 30)

    stats_y = 340
    score_txt = font_med.render("Pontuação: 420", True, WHITE)
    surface.blit(score_txt, (SCREEN_W // 2 - score_txt.get_width() // 2, stats_y))
    time_txt = font_med.render("Tempo: 85s", True, WHITE)
    surface.blit(time_txt, (SCREEN_W // 2 - time_txt.get_width() // 2, stats_y + 40))
    stars_txt = font_med.render("Estrelas: 2/3", True, GOLD)
    surface.blit(stars_txt, (SCREEN_W // 2 - stars_txt.get_width() // 2, stats_y + 80))

    draw_button(surface, SCREEN_W // 2 - 120, 500, 240, 55, "PRÓXIMA FASE", GREEN_BTN, font_med)
    draw_mute_button(surface)
    return surface


# ============================================================
# TELA 7: DERROTA
# ============================================================
def render_gameover_screen():
    surface = pygame.Surface((SCREEN_W, SCREEN_H))
    surface.fill((15, 10, 20))

    title = font_huge.render("MISSÃO FALHA", True, RED)
    surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 100))

    msg1 = font_big.render("A cidade ainda precisa de você!", True, WATER_BLUE)
    surface.blit(msg1, (SCREEN_W // 2 - msg1.get_width() // 2, 220))

    msg2 = font_med.render("Todo o progresso foi perdido.", True, (200, 100, 100))
    surface.blit(msg2, (SCREEN_W // 2 - msg2.get_width() // 2, 290))

    msg3 = font_med.render("Você precisa recomeçar da Fase 1.", True, WHITE)
    surface.blit(msg3, (SCREEN_W // 2 - msg3.get_width() // 2, 330))

    draw_button(surface, SCREEN_W // 2 - 120, 420, 240, 55, "RECOMEÇAR", RED, font_med)

    hint = font_small.render("Dica: colete gotas de água e evite obstáculos!", True, YELLOW)
    surface.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 520))

    draw_mute_button(surface)
    return surface


# ============================================================
# CAPTURAR TODAS AS TELAS
# ============================================================
def main():
    screens = [
        ("01_Dificuldade", render_difficulty_screen),
        ("02_Menu_Principal", render_title_screen),
        ("03_Instrucoes", render_instructions_screen),
        ("04_Selecao_Fases", render_phase_select_screen),
        ("05_Gameplay_Fase1", render_gameplay_screen),
        ("06_Vitoria", render_victory_screen),
        ("07_Derrota", render_gameover_screen),
    ]

    print("=" * 50)
    print("HERO OF THE WATER v5.0 — Captura de Telas")
    print("=" * 50)

    for name, render_func in screens:
        surface = render_func()
        filepath = os.path.join(OUTPUT_DIR, f"{name}.png")
        pygame.image.save(surface, filepath)
        print(f"  Salvo: {filepath}")

    print()
    print(f"Todas as {len(screens)} telas salvas em: {OUTPUT_DIR}")
    print("Importe os PNGs no Figma como frames de referência.")
    pygame.quit()


if __name__ == "__main__":
    main()
