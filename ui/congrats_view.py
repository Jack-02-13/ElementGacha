from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

import config
from data.elements import ELEMENTS

if TYPE_CHECKING:
    from main import ElementGachaApp

CONGRATS_TEXTS: dict[str, dict[str, str]] = {
    "zh": {
        "title": "?????",
        "subtitle": "?????? 118 ???",
        "stats_title": "????",
        "back": "?????",
        "line_collected": "?????{collected}/118",
        "line_total_draws": "??????{total_draws}",
        "line_total_cards": "??????{total_owned_cards}",
        "line_duplicates": "?????{duplicate_cards}",
        "line_top": "???????{top_symbol} {top_name} ?{top_count}",
        "line_top_none": "???????-",
    },
    "en": {
        "title": "Congratulations!",
        "subtitle": "You collected all 118 elements.",
        "stats_title": "Statistics",
        "back": "Back to Menu",
        "line_collected": "Collection: {collected}/118",
        "line_total_draws": "Total Draws: {total_draws}",
        "line_total_cards": "Total Owned Cards: {total_owned_cards}",
        "line_duplicates": "Duplicate Cards: {duplicate_cards}",
        "line_top": "Most Owned: {top_symbol} {top_name} ?{top_count}",
        "line_top_none": "Most Owned: -",
    },
    "ja": {
        "title": "????????",
        "subtitle": "118???????????????",
        "stats_title": "????",
        "back": "???????",
        "line_collected": "?????{collected}/118",
        "line_total_draws": "???????{total_draws}",
        "line_total_cards": "????????{total_owned_cards}",
        "line_duplicates": "???????{duplicate_cards}",
        "line_top": "???????{top_symbol} {top_name} ?{top_count}",
        "line_top_none": "???????-",
    },
    "ko": {
        "title": "?? ??!",
        "subtitle": "118? ??? ?? ??????",
        "stats_title": "??",
        "back": "?? ???",
        "line_collected": "?? ???: {collected}/118",
        "line_total_draws": "? ?? ??: {total_draws}",
        "line_total_cards": "? ?? ?? ?: {total_owned_cards}",
        "line_duplicates": "?? ?? ?: {duplicate_cards}",
        "line_top": "?? ?? ??: {top_symbol} {top_name} ?{top_count}",
        "line_top_none": "?? ?? ??: -",
    },
}


class CongratsView(tk.Frame):
    def __init__(self, parent: tk.Widget, app: "ElementGachaApp") -> None:
        super().__init__(parent, bg=config.SPACE_BLUE_BG)
        self.app = app

        self.title_label = tk.Label(self, font=(config.FONT_ZH, 30, "bold"), bg=config.SPACE_BLUE_BG, fg="#111111")
        self.title_label.pack(pady=(36, 8))

        self.subtitle_label = tk.Label(self, font=(config.FONT_ZH, 14), bg=config.SPACE_BLUE_BG, fg="#333333")
        self.subtitle_label.pack(pady=(0, 24))

        self.stats_box = tk.LabelFrame(self, padx=18, pady=14, bg=config.SPACE_BLUE_BG, fg="#111111")
        self.stats_box.pack(fill="x", padx=80)

        self.stats_labels: list[tk.Label] = []
        for _ in range(8):
            label = tk.Label(self.stats_box, anchor="w", font=(config.FONT_ZH, 12), bg=config.SPACE_BLUE_BG, fg="#111111")
            label.pack(fill="x", pady=2)
            self.stats_labels.append(label)

        self.back_button = tk.Button(
            self,
            font=(config.FONT_ZH, 12),
            width=16,
            command=lambda: self.app.show_frame("MainMenu"),
        )
        self.back_button.pack(pady=30)

        self.refresh_texts()

    def _texts(self) -> dict[str, str]:
        lang = getattr(self.app.state, "ui_language", "zh")
        return CONGRATS_TEXTS.get(lang, CONGRATS_TEXTS["zh"])

    def refresh_texts(self) -> None:
        texts = self._texts()
        self.title_label.configure(text=texts["title"])
        self.subtitle_label.configure(text=texts["subtitle"])
        self.stats_box.configure(text=texts["stats_title"])
        self.back_button.configure(text=texts["back"])

    def on_show(self) -> None:
        self.refresh_texts()
        texts = self._texts()

        collected = sum(1 for e in ELEMENTS if self.app.state.owned.get(e.atomic_number, 0) > 0)
        total_owned_cards = sum(self.app.state.owned.values())
        duplicate_cards = max(0, total_owned_cards - collected)
        total_draws = self.app.state.total_draws

        top_atomic = 0
        top_count = 0
        for atomic_number, count in self.app.state.owned.items():
            if count > top_count:
                top_atomic = atomic_number
                top_count = count
        top_element = next((e for e in ELEMENTS if e.atomic_number == top_atomic), None)
        top_name = self.app.element_name(top_element) if top_element is not None else "-"
        top_symbol = top_element.symbol if top_element is not None else "-"

        rarity_stats: list[str] = []
        for rarity in sorted(config.RARITY_WEIGHTS.keys(), reverse=True):
            total_in_rarity = sum(1 for e in ELEMENTS if e.rarity_level == rarity)
            owned_in_rarity = sum(
                1 for e in ELEMENTS if e.rarity_level == rarity and self.app.state.owned.get(e.atomic_number, 0) > 0
            )
            rarity_stats.append(f"R{rarity} {self.app.rarity_label(rarity)}: {owned_in_rarity}/{total_in_rarity}")

        lines = [
            texts["line_collected"].format(collected=collected),
            texts["line_total_draws"].format(total_draws=total_draws),
            texts["line_total_cards"].format(total_owned_cards=total_owned_cards),
            texts["line_duplicates"].format(duplicate_cards=duplicate_cards),
            (
                texts["line_top"].format(top_symbol=top_symbol, top_name=top_name, top_count=top_count)
                if top_count > 0
                else texts["line_top_none"]
            ),
            *rarity_stats,
        ]
        for idx, label in enumerate(self.stats_labels):
            label.configure(text=lines[idx] if idx < len(lines) else "")
