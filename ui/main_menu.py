from __future__ import annotations

import tkinter as tk
from pathlib import Path
from typing import TYPE_CHECKING

import config
from ui.gradient_frame import GradientFrame

try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

if TYPE_CHECKING:
    from main import ElementGachaApp

HELP_DIALOG_TITLE: dict[str, str] = {
    "zh": "怎麼玩",
    "en": "How to Play",
    "ja": "遊び方",
    "ko": "게임 방법",
}

HELP_DIALOG_BODY: dict[str, str] = {
    "zh": "\n".join(
        [
            "1) 用抽卡券抽元素，目標收集 118 種。",
            "2) 免費：60 秒 +1 券，上限 600。",
            "3) 付費授權：1 秒 +1 券，上限 36000。",
            "4) 抽卡機率固定，不會因付費改變。",
            "5) 設定可匯入/匯出存檔，授權檔可拖曳解鎖。",
            "詳見 README_GAME.md、README_LICENSE.md",
        ]
    ),
    "en": "\n".join(
        [
            "1) Use tickets to draw elements and collect all 118.",
            "2) Free: +1 ticket every 60s, cap 600.",
            "3) Paid unlock: +1 ticket every 1s, cap 36000.",
            "4) Draw rates are fixed and do not change after unlock.",
            "5) Settings supports save import/export and drag-drop license unlock.",
            "See README_GAME.md and README_LICENSE.md",
        ]
    ),
    "ja": "\n".join(
        [
            "1) チケットで元素を引いて、118種類コンプを目指します。",
            "2) 無料：60秒ごとに+1、上限600。",
            "3) 有料解放：1秒ごとに+1、上限36000。",
            "4) 解放しても排出率は変わりません。",
            "5) 設定でセーブ入出力とライセンス解放ができます。",
            "詳細は README_GAME.md / README_LICENSE.md を参照してください。",
        ]
    ),
    "ko": "\n".join(
        [
            "1) 티켓으로 원소를 뽑아 118종 수집을 목표로 합니다.",
            "2) 무료: 60초마다 +1, 최대 600.",
            "3) 유료 해금: 1초마다 +1, 최대 36000.",
            "4) 해금해도 뽑기 확률은 변하지 않습니다.",
            "5) 설정에서 저장 불러오기/내보내기와 라이선스 해금이 가능합니다.",
            "자세한 내용은 README_GAME.md / README_LICENSE.md를 참고하세요.",
        ]
    ),
}


class MainMenu(GradientFrame):
    def __init__(self, parent: tk.Widget, app: "ElementGachaApp") -> None:
        super().__init__(parent)
        self.app = app
        self._earth_images: list[tk.PhotoImage] = []
        self._earth_labels: list[tk.Label] = []
        root = self.body
        panel_bg = config.SPACE_BLUE_BG
        text_fg = config.SPACE_BLUE_FG

        self.title_label = tk.Label(
            root,
            font=(config.FONT_ZH, 30, "bold"),
            bg=panel_bg,
            fg=text_fg,
        )
        self.title_label.pack(pady=28)

        self.help_button = tk.Button(
            root,
            text="?",
            width=3,
            font=(config.FONT_EN, 12, "bold"),
            cursor="hand2",
            command=self.show_how_to_play,
        )
        self._style_button(self.help_button)
        self.help_button.place(relx=0.98, y=14, anchor="ne")

        button_frame = tk.Frame(root, bg=panel_bg, padx=12, pady=12)
        button_frame.pack(pady=18)

        self.start_button = tk.Button(
            button_frame,
            width=18,
            height=2,
            font=(config.FONT_ZH, 12),
            cursor="hand2",
            command=lambda: self.app.show_frame("GachaView"),
        )
        self._style_button(self.start_button)
        self.start_button.pack(pady=8)

        self.collection_button = tk.Button(
            button_frame,
            width=18,
            height=2,
            font=(config.FONT_ZH, 12),
            cursor="hand2",
            command=lambda: self.app.show_frame("CollectionView"),
        )
        self._style_button(self.collection_button)
        self.collection_button.pack(pady=8)

        self.settings_button = tk.Button(
            button_frame,
            width=18,
            height=2,
            font=(config.FONT_ZH, 12),
            cursor="hand2",
            command=lambda: self.app.show_frame("SettingsView"),
        )
        self._style_button(self.settings_button)
        self.settings_button.pack(pady=8)

        self.exit_button = tk.Button(
            button_frame,
            width=18,
            height=2,
            font=(config.FONT_ZH, 12),
            cursor="hand2",
            command=self.app.on_close,
        )
        self._style_button(self.exit_button)
        self.exit_button.pack(pady=8)

        self._add_earth_decorations()
        self.refresh_texts()

    def _style_button(self, button: tk.Button) -> None:
        button.configure(
            bg=config.BUTTON_BG,
            fg=config.BUTTON_FG,
            activebackground=config.BUTTON_ACTIVE_BG,
            activeforeground=config.BUTTON_ACTIVE_FG,
            relief="raised",
            bd=1,
        )

    def _add_earth_decorations(self) -> None:
        if not PIL_AVAILABLE:
            return
        project_root = Path(__file__).resolve().parents[1]
        candidates = (
            "earth.png",
            "Earth.png",
            "earth.jpg",
            "earth.jpeg",
            "earth.gif",
            "earth.webp",
        )
        image_path = next((project_root / name for name in candidates if (project_root / name).exists()), None)
        if image_path is None:
            return

        try:
            source = Image.open(image_path).convert("RGBA")
        except OSError:
            return

        max_size = 120
        source.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(source)

        self._earth_images = [image] * 4
        positions = (
            {"relx": 0.0, "x": 18, "y": 18, "anchor": "nw"},
            {"relx": 1.0, "x": -18, "y": 18, "anchor": "ne"},
            {"relx": 0.0, "rely": 1.0, "x": 18, "y": -18, "anchor": "sw"},
            {"relx": 1.0, "rely": 1.0, "x": -18, "y": -18, "anchor": "se"},
        )

        self._earth_labels.clear()
        for pos in positions:
            label = tk.Label(self, image=image, bd=0, highlightthickness=0, bg=config.SPACE_BLUE_BG)
            label.place(**pos)
            label.lower()
            self._earth_labels.append(label)

    def refresh_texts(self) -> None:
        self.title_label.configure(text=self.app.tr("app_title"))
        self.start_button.configure(text=self.app.tr("main_start_gacha"))
        self.collection_button.configure(text=self.app.tr("main_collection"))
        self.settings_button.configure(text=self.app.tr("main_settings"))
        self.exit_button.configure(text=self.app.tr("main_exit"))

    def show_how_to_play(self) -> None:
        lang = getattr(self.app.state, "ui_language", "zh")
        title = HELP_DIALOG_TITLE.get(lang, HELP_DIALOG_TITLE["zh"])
        body = HELP_DIALOG_BODY.get(lang, HELP_DIALOG_BODY["zh"])

        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.transient(self.winfo_toplevel())
        dialog.resizable(False, False)
        dialog.configure(bg=config.SPACE_BLUE_BG)

        width, height = 700, 460
        parent = self.winfo_toplevel()
        parent.update_idletasks()
        x = parent.winfo_x() + max((parent.winfo_width() - width) // 2, 20)
        y = parent.winfo_y() + max((parent.winfo_height() - height) // 2, 20)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        panel = tk.Frame(dialog, bg=config.SPACE_BLUE_BG, padx=20, pady=16)
        panel.pack(fill="both", expand=True)

        tk.Label(
            panel,
            text=title,
            font=(config.FONT_ZH, 18, "bold"),
            bg=config.SPACE_BLUE_BG,
            fg=config.SPACE_BLUE_FG,
        ).pack(anchor="w", pady=(0, 12))

        tk.Label(
            panel,
            text=body,
            justify="left",
            anchor="nw",
            font=(config.FONT_ZH, 13),
            bg=config.SPACE_BLUE_BG,
            fg=config.SPACE_BLUE_FG,
            wraplength=650,
        ).pack(fill="both", expand=True)

        close_btn = tk.Button(
            panel,
            text="OK",
            width=10,
            font=(config.FONT_EN, 11, "bold"),
            cursor="hand2",
            command=dialog.destroy,
        )
        self._style_button(close_btn)
        close_btn.pack(anchor="e", pady=(10, 0))

        dialog.grab_set()
        dialog.focus_set()
