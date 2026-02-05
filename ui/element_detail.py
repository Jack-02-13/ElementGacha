from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

import config
from data.elements import Element

if TYPE_CHECKING:
    from main import ElementGachaApp


class ElementDetailPanel(tk.LabelFrame):
    def __init__(self, parent: tk.Widget, app: "ElementGachaApp", panel_width: int = 320) -> None:
        super().__init__(parent, padx=10, pady=10)
        self.app = app
        base_bg = config.SPACE_BLUE_BG
        self.configure(bg=base_bg, fg=config.SPACE_BLUE_FG)
        self.configure(width=panel_width)
        self.grid_propagate(False)
        self._current_element: Element | None = None
        self._current_owned_count = 0
        self._current_reveal = True
        self._current_card_color: str | None = None

        self._placeholder = tk.Label(self, font=(config.FONT_ZH, 11), bg=base_bg, fg=config.SPACE_BLUE_FG)
        self._placeholder.pack(fill="x", pady=(18, 12))

        self.top_card = tk.Frame(self, bd=1, relief="solid", width=280, height=110)
        self.top_card.pack(fill="x", pady=(0, 10))
        self.top_card.pack_propagate(False)

        self.symbol_label = tk.Label(self.top_card, text="-", fg=config.ELEMENT_CARD_FG, font=(config.FONT_EN, 28, "bold"))
        self.symbol_label.pack(side="left", padx=12)
        self.name_label = tk.Label(self.top_card, text="-", fg=config.ELEMENT_CARD_FG, font=(config.FONT_ZH, 13, "bold"))
        self.name_label.pack(side="left")

        self.value_vars: dict[str, tk.StringVar] = {
            "atomic_number": tk.StringVar(value="-"),
            "symbol": tk.StringVar(value="-"),
            "name_local": tk.StringVar(value="-"),
            "name_en": tk.StringVar(value="-"),
            "rarity": tk.StringVar(value="-"),
            "earth_abundance": tk.StringVar(value="-"),
            "owned_count": tk.StringVar(value="-"),
        }

        rows = [
            ("detail_atomic_number", "atomic_number"),
            ("detail_symbol", "symbol"),
            ("detail_local_name", "name_local"),
            ("detail_name_en", "name_en"),
            ("detail_rarity", "rarity"),
            ("detail_earth_abundance", "earth_abundance"),
            ("detail_owned_count", "owned_count"),
        ]
        self.row_label_widgets: dict[str, tk.Label] = {}

        for label_key, key in rows:
            row = tk.Frame(self, bg=base_bg)
            row.pack(fill="x", pady=1)
            row_label = tk.Label(row, width=10, anchor="w", font=(config.FONT_ZH, 10, "bold"), bg=base_bg, fg=config.SPACE_BLUE_FG)
            row_label.pack(side="left")
            self.row_label_widgets[label_key] = row_label
            tk.Label(row, textvariable=self.value_vars[key], anchor="w", font=(config.FONT_ZH, 10), bg=base_bg, fg=config.SPACE_BLUE_FG).pack(
                side="left"
            )
        self.refresh_texts()

    def show_element(
        self,
        element: Element,
        owned_count: int,
        reveal: bool = True,
        card_color: str | None = None,
    ) -> None:
        self._current_element = element
        self._current_owned_count = owned_count
        self._current_reveal = reveal
        self._current_card_color = card_color

        color = (
            (card_color if card_color is not None else config.RARITY_COLORS[element.rarity_level])
            if reveal
            else config.UNKNOWN_CARD_COLOR
        )
        self._placeholder.pack_forget()

        self.top_card.configure(bg=color)
        if not reveal:
            self.symbol_label.configure(text=config.UNKNOWN_CELL_TEXT, bg=color)
            self.name_label.configure(text=config.UNKNOWN_CELL_TEXT, bg=color)
            self.value_vars["atomic_number"].set(config.UNKNOWN_CELL_TEXT)
            self.value_vars["symbol"].set(config.UNKNOWN_CELL_TEXT)
            self.value_vars["name_local"].set(config.UNKNOWN_CELL_TEXT)
            self.value_vars["name_en"].set(config.UNKNOWN_CELL_TEXT)
            self.value_vars["rarity"].set(config.UNKNOWN_CELL_TEXT)
            self.value_vars["earth_abundance"].set(config.UNKNOWN_CELL_TEXT)
            self.value_vars["owned_count"].set(config.UNKNOWN_CELL_TEXT)
            return

        local_name = self.app.element_name(element)
        self.symbol_label.configure(text=element.symbol, bg=color)
        header_name = f"{local_name} / {element.name_en}" if local_name != element.name_en else element.name_en
        self.name_label.configure(text=header_name, bg=color)
        self.value_vars["atomic_number"].set(str(element.atomic_number))
        self.value_vars["symbol"].set(element.symbol)
        self.value_vars["name_local"].set(local_name)
        self.value_vars["name_en"].set(element.name_en)
        self.value_vars["rarity"].set(f"R{element.rarity_level} {self.app.rarity_label(element.rarity_level)}")
        abundance = config.EARTH_ABUNDANCE_PPM.get(
            element.atomic_number,
            self.app.tr("detail_abundance_na"),
        )
        self.value_vars["earth_abundance"].set(abundance)
        self.value_vars["owned_count"].set(str(owned_count))

    def refresh_current_data(self) -> None:
        if self._current_element is None:
            return
        owned_count = self.app.state.owned.get(self._current_element.atomic_number, 0)
        self.show_element(
            self._current_element,
            owned_count,
            reveal=owned_count > 0,
            card_color=self._current_card_color,
        )

    def refresh_texts(self) -> None:
        self.configure(text=self.app.tr("detail_panel_title"))
        self._placeholder.configure(text=self.app.tr("detail_placeholder"))
        for key, label in self.row_label_widgets.items():
            label.configure(text=f"{self.app.tr(key)}:")

        self.refresh_current_data()


class ElementDetailBanner(tk.LabelFrame):
    def __init__(self, parent: tk.Widget, app: "ElementGachaApp") -> None:
        super().__init__(parent, padx=8, pady=8)
        self.app = app
        base_bg = config.SPACE_BLUE_BG
        self.configure(bg=base_bg, fg=config.SPACE_BLUE_FG)
        self._current_element: Element | None = None
        self._current_owned_count = 0
        self._current_reveal = True
        self._current_card_color: str | None = None

        self._placeholder = tk.Label(self, font=(config.FONT_ZH, 11), bg=base_bg, fg=config.SPACE_BLUE_FG)
        self._placeholder.pack(fill="x")

        self.banner = tk.Frame(self, bd=1, relief="solid", padx=8, pady=6)
        self.banner.pack(fill="x", pady=(6, 0))

        self.symbol_label = tk.Label(self.banner, text="-", width=4, fg=config.ELEMENT_CARD_FG, font=(config.FONT_EN, 18, "bold"))
        self.symbol_label.pack(side="left")
        self.name_label = tk.Label(self.banner, text="-", width=20, anchor="w", fg=config.ELEMENT_CARD_FG, font=(config.FONT_ZH, 12, "bold"))
        self.name_label.pack(side="left", padx=(8, 12))

        self.info_vars: dict[str, tk.StringVar] = {
            "atomic_number": tk.StringVar(value="-"),
            "symbol": tk.StringVar(value="-"),
            "name_local": tk.StringVar(value="-"),
            "name_en": tk.StringVar(value="-"),
            "rarity": tk.StringVar(value="-"),
            "earth_abundance": tk.StringVar(value="-"),
            "owned_count": tk.StringVar(value="-"),
        }
        self.info_labels: dict[str, tk.Label] = {}
        self.value_labels: dict[str, tk.Label] = {}
        self.info_boxes: list[tk.Frame] = []

        fields = [
            ("detail_atomic_number", "atomic_number"),
            ("detail_symbol", "symbol"),
            ("detail_local_name", "name_local"),
            ("detail_name_en", "name_en"),
            ("detail_rarity", "rarity"),
            ("detail_earth_abundance", "earth_abundance"),
            ("detail_owned_count", "owned_count"),
        ]
        for label_key, value_key in fields:
            box = tk.Frame(self.banner, padx=4, bg=base_bg)
            box.pack(side="left", fill="y")
            label = tk.Label(box, font=(config.FONT_ZH, 9, "bold"), fg=config.ELEMENT_CARD_FG)
            label.pack(anchor="w")
            value = tk.Label(box, textvariable=self.info_vars[value_key], font=(config.FONT_ZH, 9), fg=config.ELEMENT_CARD_FG)
            value.pack(anchor="w")
            self.info_labels[label_key] = label
            self.value_labels[value_key] = value
            self.info_boxes.append(box)

        self.refresh_texts()

    def show_element(
        self,
        element: Element,
        owned_count: int,
        reveal: bool = True,
        card_color: str | None = None,
    ) -> None:
        self._current_element = element
        self._current_owned_count = owned_count
        self._current_reveal = reveal
        self._current_card_color = card_color

        color = (
            (card_color if card_color is not None else config.RARITY_COLORS[element.rarity_level])
            if reveal
            else config.UNKNOWN_CARD_COLOR
        )
        self._placeholder.pack_forget()
        self.banner.configure(bg=color)

        widgets = [self.symbol_label, self.name_label, *self.info_boxes, *self.info_labels.values(), *self.value_labels.values()]
        for widget in widgets:
            widget.configure(bg=color)

        if not reveal:
            self.symbol_label.configure(text=config.UNKNOWN_CELL_TEXT)
            self.name_label.configure(text=config.UNKNOWN_CELL_TEXT)
            for key in self.info_vars:
                self.info_vars[key].set(config.UNKNOWN_CELL_TEXT)
            return

        local_name = self.app.element_name(element)
        self.symbol_label.configure(text=element.symbol)
        self.name_label.configure(text=local_name)
        self.info_vars["atomic_number"].set(str(element.atomic_number))
        self.info_vars["symbol"].set(element.symbol)
        self.info_vars["name_local"].set(local_name)
        self.info_vars["name_en"].set(element.name_en)
        self.info_vars["rarity"].set(f"R{element.rarity_level} {self.app.rarity_label(element.rarity_level)}")
        self.info_vars["earth_abundance"].set(
            config.EARTH_ABUNDANCE_PPM.get(element.atomic_number, self.app.tr("detail_abundance_na"))
        )
        self.info_vars["owned_count"].set(str(owned_count))

    def refresh_current_data(self) -> None:
        if self._current_element is None:
            return
        owned_count = self.app.state.owned.get(self._current_element.atomic_number, 0)
        self.show_element(
            self._current_element,
            owned_count,
            reveal=owned_count > 0,
            card_color=self._current_card_color,
        )

    def refresh_texts(self) -> None:
        self.configure(text=self.app.tr("detail_panel_title"))
        self._placeholder.configure(text=self.app.tr("detail_placeholder"))
        for key, label in self.info_labels.items():
            label.configure(text=self.app.tr(key))

        self.refresh_current_data()
