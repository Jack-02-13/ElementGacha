from __future__ import annotations

import tkinter as tk
from collections import defaultdict
from typing import TYPE_CHECKING

import config
from data.elements import ELEMENTS
from gacha import DrawBatchResult, DrawEntry, collected_count, draw_batch
from ticket import get_ticket_rule, replenish_tickets
from ui.element_detail import ElementDetailPanel
from ui.gradient_frame import GradientFrame

if TYPE_CHECKING:
    from main import ElementGachaApp


class GachaView(GradientFrame):
    def __init__(self, parent: tk.Widget, app: "ElementGachaApp") -> None:
        super().__init__(parent)
        self.app = app
        root = self.body
        root_bg = config.SPACE_BLUE_BG
        self._active = False
        self._tick_id: str | None = None
        self._button_mode_paid: bool | None = None
        self._last_result: DrawBatchResult | None = None

        top = tk.Frame(root, bg=root_bg)
        top.pack(fill="x", padx=12, pady=8)
        self.back_button = tk.Button(top, font=(config.FONT_ZH, 10), command=lambda: self.app.show_frame("MainMenu"))
        self._style_button(self.back_button)
        self.back_button.pack(side="left")
        self.ticket_label = tk.Label(top, text="", font=(config.FONT_ZH, 12, "bold"), bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.ticket_label.pack(side="right")

        info = tk.Frame(root, bg=root_bg)
        info.pack(fill="x", padx=12, pady=2)
        self.speed_label = tk.Label(info, text="", font=(config.FONT_ZH, 11), bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.speed_label.pack(side="left")
        self.stats_label = tk.Label(info, text="", font=(config.FONT_ZH, 11), bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.stats_label.pack(side="right")

        self.draw_button_frame = tk.Frame(root, bg=root_bg)
        self.draw_button_frame.pack(fill="x", padx=12, pady=10)
        self.draw_count_title = tk.Label(self.draw_button_frame, font=(config.FONT_ZH, 11), bg=root_bg, fg=config.SPACE_BLUE_FG)

        self.notice_label = tk.Label(root, text="", fg=config.SPACE_BLUE_FG, bg=root_bg, font=(config.FONT_ZH, 11))
        self.notice_label.pack(anchor="w", padx=12)

        result_wrapper = tk.Frame(root, bg=root_bg)
        result_wrapper.pack(fill="both", expand=True, padx=12, pady=8)
        result_wrapper.grid_columnconfigure(0, weight=1)
        result_wrapper.grid_columnconfigure(1, weight=0)
        result_wrapper.grid_rowconfigure(0, weight=1)

        result_left = tk.Frame(result_wrapper, bg=root_bg)
        result_left.grid(row=0, column=0, sticky="nsew")

        self.result_canvas = tk.Canvas(result_left, highlightthickness=0, bg=root_bg)
        self.result_scrollbar = tk.Scrollbar(result_left, orient="vertical", command=self.result_canvas.yview)
        self.result_canvas.configure(yscrollcommand=self.result_scrollbar.set)
        self.result_canvas.pack(side="left", fill="both", expand=True)
        self.result_scrollbar.pack(side="right", fill="y")

        self.result_frame = tk.Frame(self.result_canvas, bg=root_bg)
        self.result_window_id = self.result_canvas.create_window((0, 0), window=self.result_frame, anchor="nw")
        self.result_frame.bind("<Configure>", self._on_result_frame_configure)
        self.result_canvas.bind("<Configure>", self._on_result_canvas_configure)
        self.result_canvas.bind("<Enter>", self._bind_mousewheel)
        self.result_canvas.bind("<Leave>", self._unbind_mousewheel)

        self.detail_panel = ElementDetailPanel(result_wrapper, self.app)
        self.detail_panel.grid(row=0, column=1, sticky="ns", padx=(10, 0))
        self.detail_panel.grid_remove()
        self.refresh_texts()

    def _style_button(self, button: tk.Button) -> None:
        button.configure(
            bg=config.BUTTON_BG,
            fg=config.BUTTON_FG,
            activebackground=config.BUTTON_ACTIVE_BG,
            activeforeground=config.BUTTON_ACTIVE_FG,
            relief="raised",
            bd=1,
            cursor="hand2",
        )

    def on_show(self) -> None:
        self._active = True
        self.detail_panel.grid_remove()
        self.refresh_status()
        self._tick()

    def on_hide(self) -> None:
        self._active = False
        if self._tick_id is not None:
            self.after_cancel(self._tick_id)
            self._tick_id = None

    def _tick(self) -> None:
        if not self._active:
            return
        self.refresh_status()
        self._tick_id = self.after(400, self._tick)

    def _on_result_frame_configure(self, _: tk.Event[tk.Misc]) -> None:
        self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))

    def _on_result_canvas_configure(self, event: tk.Event[tk.Misc]) -> None:
        self.result_canvas.itemconfigure(self.result_window_id, width=event.width)

    def _bind_mousewheel(self, _: tk.Event[tk.Misc]) -> None:
        self.result_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.result_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.result_canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, _: tk.Event[tk.Misc]) -> None:
        self.result_canvas.unbind_all("<MouseWheel>")
        self.result_canvas.unbind_all("<Button-4>")
        self.result_canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event: tk.Event[tk.Misc]) -> None:
        if hasattr(event, "delta") and event.delta:
            self.result_canvas.yview_scroll(int(-event.delta / 120), "units")
            return
        if getattr(event, "num", None) == 4:
            self.result_canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5:
            self.result_canvas.yview_scroll(1, "units")

    def _refresh_draw_buttons(self, force: bool = False) -> None:
        paid_mode = self.app.state.paid_unlocked
        if self._button_mode_paid == paid_mode and not force:
            return

        self._button_mode_paid = paid_mode
        for child in self.draw_button_frame.winfo_children():
            child.destroy()

        self.draw_count_title = tk.Label(
            self.draw_button_frame,
            text=self.app.tr("gacha_draw_count_label"),
            font=(config.FONT_ZH, 11),
            bg=config.SPACE_BLUE_BG,
            fg=config.SPACE_BLUE_FG,
        )
        self.draw_count_title.pack(side="left")
        options = config.PAID_DRAW_OPTIONS if paid_mode else config.FREE_DRAW_OPTIONS
        for option in options:
            draw_btn = tk.Button(
                self.draw_button_frame,
                text=str(option),
                width=7,
                font=(config.FONT_EN, 10),
                command=lambda draw_count=option: self.draw_many(draw_count),
            )
            self._style_button(draw_btn)
            draw_btn.pack(side="left", padx=4)

    def refresh_status(self) -> None:
        replenish_tickets(self.app.state, now=self.app.time_provider())
        self._refresh_draw_buttons()

        rule = get_ticket_rule(self.app.state.paid_unlocked)
        speed_text = self.app.tr("gacha_speed_paid") if self.app.state.paid_unlocked else self.app.tr("gacha_speed_free")
        collected = sum(1 for element in ELEMENTS if self.app.state.owned.get(element.atomic_number, 0) > 0)

        self.ticket_label.config(text=self.app.tr("gacha_ticket", current=self.app.state.ticket_count, cap=rule.cap))
        self.speed_label.config(text=speed_text)
        self.stats_label.config(text=self.app.tr("gacha_stats", total=self.app.state.total_draws, collected=collected))

    def _clear_results(self) -> None:
        for child in self.result_frame.winfo_children():
            child.destroy()

    def _create_card(self, parent: tk.Widget, entry: DrawEntry, is_new: bool) -> tk.Frame:
        rarity = entry.element.rarity_level
        bg_color = config.RARITY_COLORS[rarity]

        card = tk.Frame(parent, width=80, height=80, bg=bg_color, bd=1, relief="solid")
        card.grid_propagate(False)

        symbol = tk.Label(card, text=entry.element.symbol, bg=bg_color, fg=config.ELEMENT_CARD_FG, font=(config.FONT_EN, 16, "bold"))
        symbol.place(relx=0.5, rely=0.42, anchor="center")

        name = tk.Label(card, text=self.app.element_name(entry.element), bg=bg_color, fg=config.ELEMENT_CARD_FG, font=(config.FONT_ZH, 9))
        name.place(relx=0.5, rely=0.83, anchor="center")

        count = tk.Label(card, text=f"×{entry.count}", bg=bg_color, fg=config.ELEMENT_CARD_FG, font=(config.FONT_EN, 9, "bold"))
        count.place(relx=0.96, rely=0.97, anchor="se")

        clickable_widgets: list[tk.Widget] = [card, symbol, name, count]
        if is_new:
            tag = tk.Label(card, text="NEW", bg="#fff2a8", fg="#7a1f1f", font=(config.FONT_EN, 8, "bold"))
            tag.place(x=2, y=2, anchor="nw")
            clickable_widgets.append(tag)

        def on_click(_: tk.Event[tk.Misc]) -> None:
            owned_count = self.app.state.owned.get(entry.element.atomic_number, 0)
            self.detail_panel.grid(row=0, column=1, sticky="ns", padx=(10, 0))
            self.detail_panel.show_element(entry.element, owned_count)

        for widget in clickable_widgets:
            widget.configure(cursor="hand2")
            widget.bind("<Button-1>", on_click)

        return card

    def _render_grouped_results(self, result: DrawBatchResult) -> None:
        self._clear_results()
        is_new_map = {entry.element.atomic_number: True for entry in result.newly_obtained}

        grouped: dict[int, list[tuple[DrawEntry, bool]]] = defaultdict(list)
        all_entries = result.newly_obtained + result.already_owned
        for entry in all_entries:
            grouped[entry.element.rarity_level].append(
                (entry, is_new_map.get(entry.element.atomic_number, False))
            )

        columns = 10
        for rarity in config.RARITY_ORDER_DESC:
            items = grouped.get(rarity, [])
            if not items:
                continue

            items.sort(key=lambda pair: pair[0].element.atomic_number)
            section = tk.Frame(self.result_frame, bg=config.SPACE_BLUE_BG)
            section.pack(fill="x", pady=(0, 10))

            tk.Label(
                section,
                text=self.app.rarity_label(rarity),
                font=(config.FONT_ZH, 12, "bold"),
                bg=config.SPACE_BLUE_BG,
                fg=config.SPACE_BLUE_FG,
            ).pack(anchor="w", pady=(0, 4))

            grid = tk.Frame(section, bg=config.SPACE_BLUE_BG)
            grid.pack(fill="x")

            for index, (entry, is_new) in enumerate(items):
                row = index // columns
                column = index % columns
                card = self._create_card(grid, entry, is_new)
                card.grid(row=row, column=column, padx=4, pady=4)

    def draw_many(self, draw_count: int) -> None:
        replenish_tickets(self.app.state, now=self.app.time_provider())
        before_collected = collected_count(self.app.state, ELEMENTS)
        if self.app.state.ticket_count < draw_count:
            self.notice_label.config(
                text=self.app.tr(
                    "insufficient_tickets",
                    current=self.app.state.ticket_count,
                    need=draw_count,
                ),
                fg=config.SPACE_BLUE_FG,
            )
            self.refresh_status()
            return

        result = draw_batch(
            state=self.app.state,
            engine=self.app.gacha_engine,
            draw_count=draw_count,
            now=self.app.time_provider(),
        )
        if not result.success:
            self.notice_label.config(text=self.app.tr("insufficient_tickets", current=self.app.state.ticket_count, need=draw_count), fg=config.SPACE_BLUE_FG)
            return

        self._last_result = result
        self.app.persist()
        self.notice_label.config(text="", fg=config.SPACE_BLUE_FG)
        self.detail_panel.grid_remove()
        self._render_grouped_results(result)
        self.refresh_status()
        self.app.check_completion_and_show(before_collected)

    def refresh_texts(self) -> None:
        self.back_button.configure(text=self.app.tr("back_to_menu"))
        self._refresh_draw_buttons(force=True)
        self.detail_panel.refresh_texts()
        if self._last_result is not None:
            self._render_grouped_results(self._last_result)
        self.refresh_status()
