from __future__ import annotations

import argparse
import random
import time
import tkinter as tk
from pathlib import Path
from typing import Callable

import config
import i18n
from data.elements import ELEMENTS
from gacha import GachaEngine, collected_count
from license_manager import is_paid_unlocked
from save import SaveData, get_save_path, load_save, write_save
from ticket import replenish_tickets
from ui import CollectionView, CongratsView, GachaView, MainMenu, SettingsView

try:
    from tkinterdnd2 import TkinterDnD  # type: ignore

    TkBase = TkinterDnD.Tk
except Exception:
    TkBase = tk.Tk


class ElementGachaApp(TkBase):
    def __init__(self, seed: int | None = None, time_provider: Callable[[], float] | None = None) -> None:
        super().__init__()
        self.geometry(config.WINDOW_SIZE)
        self.minsize(920, 640)
        self.state("zoomed")
        self.configure(bg=config.SPACE_BLUE_BG)

        self.time_provider: Callable[[], float] = time_provider or time.time
        self.save_path: Path = get_save_path()
        self.state: SaveData = load_save(self.save_path, now=self.time_provider())
        paid_unlocked, self.license_reason = is_paid_unlocked()
        self.state.paid_unlocked = paid_unlocked
        self.state.ui_language = i18n.normalize_language(self.state.ui_language)
        replenish_tickets(self.state, now=self.time_provider())
        self.title(self.tr("app_title"))

        self.rng = random.Random(seed)
        self.gacha_engine = GachaEngine(ELEMENTS, rng=self.rng)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, tk.Frame] = {}
        self.current_frame: tk.Frame | None = None

        for frame_cls in (MainMenu, GachaView, CollectionView, SettingsView, CongratsView):
            frame = frame_cls(container, self)
            self.frames[frame_cls.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_frame("MainMenu")

    def persist(self) -> None:
        write_save(self.state, self.save_path)

    def on_close(self) -> None:
        replenish_tickets(self.state, now=self.time_provider())
        self.persist()
        self.destroy()

    def tr(self, key: str, **kwargs: object) -> str:
        return i18n.t(self.state.ui_language, key, **kwargs)

    def rarity_label(self, rarity: int) -> str:
        return i18n.rarity_label(self.state.ui_language, rarity)

    def collection_section_title(self, rarity: int) -> str:
        return i18n.collection_section_title(self.state.ui_language, rarity)

    def periodic_category_label(self, category: str) -> str:
        return i18n.periodic_category_label(self.state.ui_language, category)

    def element_name(self, element: "Element") -> str:
        return i18n.element_name(
            self.state.ui_language,
            element.atomic_number,
            element.name_zh,
            element.name_en,
        )

    def set_language(self, language: str) -> None:
        normalized = i18n.normalize_language(language)
        if normalized == self.state.ui_language:
            return
        self.state.ui_language = normalized
        self.title(self.tr("app_title"))
        self.refresh_all_texts()
        self.persist()

    def refresh_all_texts(self) -> None:
        for frame in self.frames.values():
            if hasattr(frame, "refresh_texts"):
                getattr(frame, "refresh_texts")()
        if self.current_frame is not None and hasattr(self.current_frame, "on_show"):
            getattr(self.current_frame, "on_show")()

    def show_frame(self, frame_name: str) -> None:
        if self.current_frame is not None and hasattr(self.current_frame, "on_hide"):
            getattr(self.current_frame, "on_hide")()

        frame = self.frames[frame_name]
        frame.tkraise()
        self.current_frame = frame

        if hasattr(frame, "on_show"):
            getattr(frame, "on_show")()

    def check_completion_and_show(self, previous_collected: int) -> None:
        current_collected = collected_count(self.state, ELEMENTS)
        if previous_collected < 118 and current_collected >= 118:
            self.show_frame("CongratsView")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="元素抽卡收集（tkinter 單機版）")
    parser.add_argument("--seed", type=int, default=None, help="指定隨機種子（測試用途）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ElementGachaApp(seed=args.seed)
    app.mainloop()


if __name__ == "__main__":
    main()
