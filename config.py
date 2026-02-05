from __future__ import annotations

import sys
from pathlib import Path

APP_TITLE = "元素抽卡收集"
WINDOW_SIZE = "1100x760"

if sys.platform == "darwin":
    FONT_ZH = "PingFang TC"
    FONT_EN = "Helvetica Neue"
else:
    FONT_ZH = "Microsoft JhengHei"
    FONT_EN = "Segoe UI"

SPACE_BLUE_BG = "#000000"
SPACE_BLUE_FG = "#ffffff"
SPACE_BLUE_GRADIENT_TOP = "#000000"
SPACE_BLUE_GRADIENT_BOTTOM = "#000000"

BUTTON_BG = "#1f1f1f"
BUTTON_FG = "#ffffff"
BUTTON_ACTIVE_BG = "#2b2b2b"
BUTTON_ACTIVE_FG = "#ffffff"
ELEMENT_CARD_FG = "#111111"

UNLOCK_CODE = "ZIMEI-UNLOCK-2026"

SAVE_VERSION = "2.0"
SAVE_DIR = Path.home() / ".element_gacha"
SAVE_FILENAME = "save.json"

RARITY_WEIGHTS: dict[int, float] = {
    1: 0.50,
    2: 0.30,
    3: 0.145,
    4: 0.05,
    5: 0.005,
}

RARITY_LABELS: dict[int, str] = {
    1: "極常見",
    2: "常見",
    3: "不常見",
    4: "稀有",
    5: "極稀有",
}

RARITY_ABUNDANCE_LABELS: dict[int, str] = {
    1: "> 10,000 ppm",
    2: "1,000 - 10,000 ppm",
    3: "10 - 1,000 ppm",
    4: "0.1 - 10 ppm",
    5: "< 0.1 ppm 或自然界幾乎不存在",
}

# 近似地殼含量（ppm，質量比）。資料不足者以「trace / N/A」標示。
EARTH_ABUNDANCE_PPM: dict[int, str] = {
    1: "1,400 ppm",
    2: "0.008 ppm",
    3: "20 ppm",
    4: "2.8 ppm",
    5: "10 ppm",
    6: "200 ppm",
    7: "19 ppm",
    8: "461,000 ppm",
    9: "585 ppm",
    10: "0.005 ppm",
    11: "23,600 ppm",
    12: "23,300 ppm",
    13: "82,300 ppm",
    14: "282,000 ppm",
    15: "1,050 ppm",
    16: "350 ppm",
    17: "145 ppm",
    18: "3.5 ppm",
    19: "20,900 ppm",
    20: "41,500 ppm",
    21: "22 ppm",
    22: "5,650 ppm",
    23: "120 ppm",
    24: "102 ppm",
    25: "950 ppm",
    26: "56,300 ppm",
    27: "25 ppm",
    28: "84 ppm",
    29: "60 ppm",
    30: "70 ppm",
    31: "19 ppm",
    32: "1.5 ppm",
    33: "1.8 ppm",
    34: "0.05 ppm",
    35: "2.4 ppm",
    36: "0.0001 ppm",
    37: "90 ppm",
    38: "370 ppm",
    39: "33 ppm",
    40: "165 ppm",
    41: "20 ppm",
    42: "1.2 ppm",
    43: "trace",
    44: "0.001 ppm",
    45: "0.001 ppm",
    46: "0.015 ppm",
    47: "0.075 ppm",
    48: "0.15 ppm",
    49: "0.25 ppm",
    50: "2.3 ppm",
    51: "0.2 ppm",
    52: "0.001 ppm",
    53: "0.45 ppm",
    54: "0.00003 ppm",
    55: "3.0 ppm",
    56: "425 ppm",
    57: "39 ppm",
    58: "66.5 ppm",
    59: "9.2 ppm",
    60: "41.5 ppm",
    61: "trace",
    62: "7.05 ppm",
    63: "2.0 ppm",
    64: "6.2 ppm",
    65: "1.2 ppm",
    66: "5.2 ppm",
    67: "1.3 ppm",
    68: "3.5 ppm",
    69: "0.52 ppm",
    70: "3.2 ppm",
    71: "0.8 ppm",
    72: "3.0 ppm",
    73: "2.0 ppm",
    74: "1.25 ppm",
    75: "0.0007 ppm",
    76: "0.0015 ppm",
    77: "0.001 ppm",
    78: "0.005 ppm",
    79: "0.004 ppm",
    80: "0.085 ppm",
    81: "0.85 ppm",
    82: "14 ppm",
    83: "0.0085 ppm",
    84: "0.0000000002 ppm",
    85: "trace",
    86: "0.0000000000004 ppm",
    87: "trace",
    88: "0.0000009 ppm",
    89: "0.00000000055 ppm",
    90: "9.6 ppm",
    91: "0.0000014 ppm",
    92: "2.7 ppm",
    93: "trace",
    94: "trace",
}

RARITY_ORDER_DESC: tuple[int, ...] = (5, 4, 3, 2, 1)

COLLECTION_SECTION_TITLES: dict[int, str] = {
    5: "極稀有 0.5%",
    4: "稀有 5%",
    3: "不常見 14.5%",
    2: "常見 30%",
    1: "極常見 50%",
}

FREE_TICKET_INTERVAL_SECONDS = 60
PAID_TICKET_INTERVAL_SECONDS = 1

FREE_TICKET_CAP = 600
PAID_TICKET_CAP = 36_000

FREE_DRAW_OPTIONS: tuple[int, ...] = (1, 5, 10, 60)
PAID_DRAW_OPTIONS: tuple[int, ...] = (1, 10, 50, 100, 1000, 3600)

RARITY_COLORS: dict[int, str] = {
    1: "#8fd694",  # 綠
    2: "#90bfff",  # 藍
    3: "#b898ff",  # 紫
    4: "#ff9898",  # 紅
    5: "#f1d07a",  # 金
}

UNKNOWN_CARD_COLOR = "#d9d9d9"

UNKNOWN_CELL_TEXT = "???"

PERIODIC_CATEGORY_COLORS: dict[str, str] = {
    "alkali_metal": "#f7b267",
    "alkaline_earth": "#f9d29d",
    "transition_metal": "#ffd166",
    "post_transition_metal": "#a0d8ef",
    "metalloid": "#b8e986",
    "nonmetal": "#7dd3fc",
    "halogen": "#93c5fd",
    "noble_gas": "#c4b5fd",
    "lanthanide": "#fbcfe8",
    "actinide": "#fecdd3",
    "unknown": "#d1d5db",
}
