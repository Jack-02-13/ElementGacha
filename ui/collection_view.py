from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

import config
from data.elements import ELEMENTS, Element
from gacha import collected_count
from ui.element_detail import ElementDetailPanel
from ui.gradient_frame import GradientFrame

if TYPE_CHECKING:
    from main import ElementGachaApp


ALKALI_METALS = {3, 11, 19, 37, 55, 87}
ALKALINE_EARTH = {4, 12, 20, 38, 56, 88}
METALLOIDS = {5, 14, 32, 33, 51, 52}
NONMETALS = {1, 6, 7, 8, 15, 16, 34}
HALOGENS = {9, 17, 35, 53, 85, 117}
NOBLE_GASES = {2, 10, 18, 36, 54, 86, 118}
POST_TRANSITION = {13, 31, 49, 50, 81, 82, 83, 84, 113, 114, 115, 116}
LANTHANIDES = set(range(57, 72))
ACTINIDES = set(range(89, 104))
TRANSITION = set(range(21, 31)) | set(range(39, 49)) | set(range(72, 81)) | set(range(104, 113))

CATEGORY_ORDER = (
    "alkali_metal",
    "alkaline_earth",
    "transition_metal",
    "post_transition_metal",
    "metalloid",
    "nonmetal",
    "halogen",
    "noble_gas",
    "lanthanide",
    "actinide",
    "unknown",
)


def _build_periodic_positions() -> dict[int, tuple[int, int]]:
    positions: dict[int, tuple[int, int]] = {}

    positions[1] = (1, 1)
    positions[2] = (1, 18)

    for atomic, group in zip((3, 4, 5, 6, 7, 8, 9, 10), (1, 2, 13, 14, 15, 16, 17, 18)):
        positions[atomic] = (2, group)
    for atomic, group in zip((11, 12, 13, 14, 15, 16, 17, 18), (1, 2, 13, 14, 15, 16, 17, 18)):
        positions[atomic] = (3, group)

    for group, atomic in enumerate(range(19, 37), start=1):
        positions[atomic] = (4, group)
    for group, atomic in enumerate(range(37, 55), start=1):
        positions[atomic] = (5, group)

    row6 = [55, 56, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86]
    for group, atomic in zip((1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18), row6):
        positions[atomic] = (6, group)

    row7 = [87, 88, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118]
    for group, atomic in zip((1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18), row7):
        positions[atomic] = (7, group)

    for group, atomic in enumerate(range(57, 72), start=3):
        positions[atomic] = (8, group)
    for group, atomic in enumerate(range(89, 104), start=3):
        positions[atomic] = (9, group)

    return positions


PERIODIC_POSITIONS = _build_periodic_positions()


class CollectionView(GradientFrame):
    def __init__(self, parent: tk.Widget, app: "ElementGachaApp") -> None:
        super().__init__(parent)
        self.app = app
        root = self.body
        root_bg = config.SPACE_BLUE_BG
        self.configure(bg=root_bg)
        if isinstance(root, tk.Canvas):
            root.configure(bg=root_bg)
        self.mode_var = tk.StringVar(value="rarity")
        self.rarity_section_labels: dict[int, tk.Label] = {}
        self.rarity_card_widgets: dict[int, tuple[tk.Frame, tk.Label, tk.Label, tk.Label]] = {}
        self.periodic_card_widgets: dict[int, tuple[tk.Frame, tk.Label, tk.Label, tk.Label]] = {}
        self.periodic_legend_title_label: tk.Label | None = None
        self.periodic_legend_labels: dict[str, tk.Label] = {}

        top = tk.Frame(root, bg=root_bg)
        top.pack(fill="x", pady=8, padx=12)
        self.back_button = tk.Button(top, font=(config.FONT_ZH, 10), command=lambda: self.app.show_frame("MainMenu"))
        self._style_button(self.back_button)
        self.back_button.pack(side="left")

        switch_frame = tk.Frame(top, bg=root_bg)
        switch_frame.pack(side="left", padx=10)
        self.mode_rarity_button = tk.Button(switch_frame, font=(config.FONT_ZH, 10), command=lambda: self._set_mode("rarity"))
        self._style_button(self.mode_rarity_button)
        self.mode_rarity_button.pack(side="left", padx=(0, 6))
        self.mode_periodic_button = tk.Button(switch_frame, font=(config.FONT_ZH, 10), command=lambda: self._set_mode("periodic"))
        self._style_button(self.mode_periodic_button)
        self.mode_periodic_button.pack(side="left")

        self.progress_label = tk.Label(top, text="", font=(config.FONT_ZH, 12, "bold"), bg=root_bg, fg="#111111")
        self.progress_label.pack(side="right")

        main_area = tk.Frame(root, bg=root_bg)
        main_area.pack(fill="both", expand=True, padx=12, pady=4)
        main_area.grid_columnconfigure(0, weight=1)
        main_area.grid_columnconfigure(1, weight=0)
        main_area.grid_rowconfigure(0, weight=1)

        canvas_wrap = tk.Frame(main_area, bg=root_bg)
        canvas_wrap.grid(row=0, column=0, sticky="nsew")

        self.canvas = tk.Canvas(canvas_wrap, highlightthickness=0, bg=root_bg)
        self.v_scrollbar = tk.Scrollbar(canvas_wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        canvas_wrap.grid_rowconfigure(0, weight=1)
        canvas_wrap.grid_columnconfigure(0, weight=1)

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        self.content_frame = tk.Frame(self.canvas, bg=root_bg)
        self.window_id = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.content_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.rarity_container = tk.Frame(self.content_frame, bg=root_bg)
        self.periodic_container = tk.Frame(self.content_frame, bg=root_bg)

        self.detail_panel = ElementDetailPanel(main_area, self.app, panel_width=240)
        self.detail_panel.grid(row=0, column=1, sticky="ns", padx=(10, 0))

        self._build_rarity_view(self.rarity_container)
        self._build_periodic_view(self.periodic_container)

        self._show_mode(self.mode_var.get())

    def _style_button(self, button: tk.Button) -> None:
        button.configure(
            bg="SystemButtonFace",
            fg="SystemButtonText",
            activebackground="SystemButtonFace",
            activeforeground="SystemButtonText",
            relief="raised",
            bd=1,
            cursor="hand2",
        )

    def _on_frame_configure(self, _: tk.Event[tk.Misc]) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event[tk.Misc]) -> None:
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def _bind_mousewheel(self, _: tk.Event[tk.Misc]) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, _: tk.Event[tk.Misc]) -> None:
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event: tk.Event[tk.Misc]) -> None:
        if hasattr(event, "delta") and event.delta:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
            return
        if getattr(event, "num", None) == 4:
            self.canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5:
            self.canvas.yview_scroll(1, "units")

    def _set_mode(self, mode: str) -> None:
        if mode not in {"rarity", "periodic"}:
            return
        if self.mode_var.get() == mode:
            return
        self.mode_var.set(mode)
        self._show_mode(mode)

    def _show_mode(self, mode: str) -> None:
        self.detail_panel.grid_remove()
        self.rarity_container.pack_forget()
        self.periodic_container.pack_forget()
        if mode == "periodic":
            self.periodic_container.pack(anchor="nw")
        else:
            self.rarity_container.pack(fill="x", anchor="nw")
        self.canvas.yview_moveto(0.0)
        self.refresh_texts()
        self.content_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.detail_panel.grid(row=0, column=1, sticky="ns", padx=(10, 0))

    def _periodic_category(self, atomic_number: int) -> str:
        if atomic_number in ALKALI_METALS:
            return "alkali_metal"
        if atomic_number in ALKALINE_EARTH:
            return "alkaline_earth"
        if atomic_number in LANTHANIDES:
            return "lanthanide"
        if atomic_number in ACTINIDES:
            return "actinide"
        if atomic_number in TRANSITION:
            return "transition_metal"
        if atomic_number in POST_TRANSITION:
            return "post_transition_metal"
        if atomic_number in METALLOIDS:
            return "metalloid"
        if atomic_number in NONMETALS:
            return "nonmetal"
        if atomic_number in HALOGENS:
            return "halogen"
        if atomic_number in NOBLE_GASES:
            return "noble_gas"
        return "unknown"

    def _create_card(
        self,
        parent: tk.Widget,
        element: Element,
        width: int,
        height: int,
        mode: str,
        category_color: str | None = None,
    ) -> tuple[tk.Frame, tk.Label, tk.Label, tk.Label]:
        bg = category_color if (mode == "periodic" and category_color) else config.RARITY_COLORS[element.rarity_level]
        card = tk.Frame(parent, width=width, height=height, bd=1, relief="solid", bg=bg)
        card.grid_propagate(False)

        if mode == "periodic":
            header_font = (config.FONT_EN, 7, "bold")
            symbol_font = (config.FONT_EN, 12, "bold")
            footer_font = (config.FONT_ZH, 7)
        else:
            header_font = (config.FONT_ZH, 7, "bold")
            symbol_font = (config.FONT_EN, 14, "bold")
            footer_font = (config.FONT_ZH, 8)

        header = tk.Label(card, bg=bg, fg="#111111", font=header_font)
        header.place(relx=0.5, rely=0.15, anchor="center")

        symbol = tk.Label(card, bg=bg, fg="#111111", font=symbol_font)
        symbol.place(relx=0.5, rely=0.5, anchor="center")

        footer = tk.Label(card, bg=bg, fg="#111111", font=footer_font)
        footer.place(relx=0.5, rely=0.86, anchor="center")

        def on_click(_: tk.Event[tk.Misc]) -> None:
            owned_count = self.app.state.owned.get(element.atomic_number, 0)
            self.detail_panel.show_element(element, owned_count, reveal=owned_count > 0)

        for widget in (card, header, symbol, footer):
            widget.configure(cursor="hand2")
            widget.bind("<Button-1>", on_click)
        return card, header, symbol, footer

    def _build_rarity_view(self, parent: tk.Widget) -> None:
        self.rarity_section_labels.clear()
        self.rarity_card_widgets.clear()
        columns = 10
        elements_by_rarity: dict[int, list[Element]] = {rarity: [] for rarity in config.RARITY_ORDER_DESC}
        for element in ELEMENTS:
            elements_by_rarity[element.rarity_level].append(element)
        for rarity in config.RARITY_ORDER_DESC:
            elements_by_rarity[rarity].sort(key=lambda element: element.atomic_number)

        for rarity in config.RARITY_ORDER_DESC:
            section = tk.Frame(parent, bg=config.SPACE_BLUE_BG)
            section.pack(fill="x", pady=(0, 10))

            section_label = tk.Label(section, font=(config.FONT_ZH, 12, "bold"), bg=config.SPACE_BLUE_BG, fg="#111111")
            section_label.pack(anchor="w", pady=(0, 4))
            self.rarity_section_labels[rarity] = section_label

            grid = tk.Frame(section, bg=config.SPACE_BLUE_BG)
            grid.pack(fill="x")
            for index, element in enumerate(elements_by_rarity[rarity]):
                row = index // columns
                col = index % columns
                card_widgets = self._create_card(grid, element, width=80, height=80, mode="rarity")
                card_widgets[0].grid(row=row, column=col, padx=4, pady=4)
                self.rarity_card_widgets[element.atomic_number] = card_widgets

    def _build_periodic_view(self, parent: tk.Widget) -> None:
        self.periodic_card_widgets.clear()
        self.periodic_legend_title_label = None
        self.periodic_legend_labels.clear()

        table_shell = tk.Frame(parent, bg=config.SPACE_BLUE_BG)
        table_shell.pack(anchor="nw")

        legend_block = tk.LabelFrame(table_shell, padx=8, pady=6, bg=config.SPACE_BLUE_BG, fg="#111111")
        legend_block.pack(fill="x", pady=(0, 8))
        self.periodic_legend_title_label = tk.Label(
            legend_block, font=(config.FONT_ZH, 10, "bold"), bg=config.SPACE_BLUE_BG, fg="#111111"
        )
        self.periodic_legend_title_label.pack(anchor="w", pady=(0, 4))

        legend_grid = tk.Frame(legend_block, bg=config.SPACE_BLUE_BG)
        legend_grid.pack(fill="x")
        legend_columns = 4
        for column in range(legend_columns):
            legend_grid.grid_columnconfigure(column, weight=1)

        for index, category in enumerate(CATEGORY_ORDER):
            item = tk.Frame(legend_grid, bg=config.SPACE_BLUE_BG)
            item.grid(
                row=index // legend_columns,
                column=index % legend_columns,
                sticky="w",
                padx=4,
                pady=1,
            )
            tk.Label(item, text="  ", bg=config.PERIODIC_CATEGORY_COLORS[category], bd=1, relief="solid").pack(side="left")
            text_label = tk.Label(item, font=(config.FONT_ZH, 9), bg=config.SPACE_BLUE_BG, fg="#111111")
            text_label.pack(side="left", padx=(4, 0))
            self.periodic_legend_labels[category] = text_label

        table = tk.Frame(table_shell, bg=config.SPACE_BLUE_BG)
        table.pack(anchor="nw")

        for group in range(1, 19):
            tk.Label(table, text=str(group), font=(config.FONT_EN, 7, "bold"), width=3, bg=config.SPACE_BLUE_BG, fg="#111111").grid(row=0, column=group, pady=(0, 2))
        for row in range(1, 8):
            tk.Label(table, text=f"P{row}", font=(config.FONT_EN, 7, "bold"), width=3, bg=config.SPACE_BLUE_BG, fg="#111111").grid(row=row, column=0, sticky="e")
        tk.Label(table, text="La-Lu", font=(config.FONT_EN, 7, "bold"), width=3, bg=config.SPACE_BLUE_BG, fg="#111111").grid(row=8, column=0, sticky="e")
        tk.Label(table, text="Ac-Lr", font=(config.FONT_EN, 7, "bold"), width=3, bg=config.SPACE_BLUE_BG, fg="#111111").grid(row=9, column=0, sticky="e")

        tk.Label(table, text="57-71", font=(config.FONT_EN, 7), width=4, fg="#9ab7e3", bg=config.SPACE_BLUE_BG).grid(row=6, column=3)
        tk.Label(table, text="89-103", font=(config.FONT_EN, 7), width=4, fg="#9ab7e3", bg=config.SPACE_BLUE_BG).grid(row=7, column=3)

        for element in ELEMENTS:
            position = PERIODIC_POSITIONS.get(element.atomic_number)
            if position is None:
                continue
            row, col = position
            category = self._periodic_category(element.atomic_number)
            card_widgets = self._create_card(
                table,
                element,
                width=46,
                height=46,
                mode="periodic",
                category_color=config.PERIODIC_CATEGORY_COLORS[category],
            )
            card_widgets[0].grid(row=row, column=col, padx=1, pady=1)
            self.periodic_card_widgets[element.atomic_number] = card_widgets

    def _update_cards(
        self,
        card_widgets: dict[int, tuple[tk.Frame, tk.Label, tk.Label, tk.Label]],
        periodic_mode: bool,
    ) -> None:
        for element in ELEMENTS:
            widgets = card_widgets.get(element.atomic_number)
            if widgets is None:
                continue
            card, header, symbol, footer = widgets
            owned_count = self.app.state.owned.get(element.atomic_number, 0)
            owned = owned_count > 0

            if periodic_mode:
                category = self._periodic_category(element.atomic_number)
                base_bg = config.PERIODIC_CATEGORY_COLORS[category] if owned else config.UNKNOWN_CARD_COLOR
                header_text = f"#{element.atomic_number}"
                symbol_text = element.symbol if owned else config.UNKNOWN_CELL_TEXT
                footer_text = self.app.element_name(element)[:4] if owned else config.UNKNOWN_CELL_TEXT
            else:
                base_bg = config.RARITY_COLORS[element.rarity_level] if owned else config.UNKNOWN_CARD_COLOR
                header_text = (
                    f"{self.app.element_name(element)} #{element.atomic_number}"
                    if owned
                    else f"{config.UNKNOWN_CELL_TEXT} #{element.atomic_number}"
                )
                symbol_text = element.symbol if owned else config.UNKNOWN_CELL_TEXT
                footer_text = f"×{owned_count}" if owned else "×0"

            card.configure(bg=base_bg)
            header.configure(text=header_text, bg=base_bg)
            symbol.configure(text=symbol_text, bg=base_bg)
            footer.configure(text=footer_text, bg=base_bg)

    def on_show(self) -> None:
        current = collected_count(self.app.state, ELEMENTS)
        self.progress_label.config(text=self.app.tr("collection_progress", collected=current))
        # Keep both modes up to date, so switching modes doesn't trigger reflow/flicker.
        self._update_cards(self.rarity_card_widgets, periodic_mode=False)
        self._update_cards(self.periodic_card_widgets, periodic_mode=True)

    def refresh_texts(self) -> None:
        self.back_button.configure(text=self.app.tr("back_to_menu"))
        self.mode_rarity_button.configure(text=self.app.tr("collection_mode_rarity"))
        self.mode_periodic_button.configure(text=self.app.tr("collection_mode_periodic"))

        for rarity, label in self.rarity_section_labels.items():
            label.configure(text=self.app.collection_section_title(rarity))

        if self.periodic_legend_title_label is not None and self.periodic_legend_title_label.winfo_exists():
            self.periodic_legend_title_label.configure(text=self.app.tr("periodic_legend_title"))
        for category, label in self.periodic_legend_labels.items():
            if label.winfo_exists():
                label.configure(text=self.app.periodic_category_label(category))

        self.detail_panel.refresh_texts()
        self.on_show()
