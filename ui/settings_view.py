from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

import config
import i18n
from license_manager import install_license_from_path, is_paid_unlocked
from save import clear_save, export_save, import_save, load_save
from ticket import get_ticket_rule, replenish_tickets
from ui.gradient_frame import GradientFrame

try:
    from tkinterdnd2 import DND_FILES  # type: ignore
except Exception:
    DND_FILES = None

if TYPE_CHECKING:
    from main import ElementGachaApp


class SettingsView(GradientFrame):
    def __init__(self, parent: tk.Widget, app: "ElementGachaApp") -> None:
        super().__init__(parent)
        self.app = app
        root = self.body
        root_bg = config.SPACE_BLUE_BG

        top = tk.Frame(root, bg=root_bg)
        top.pack(fill="x", pady=8, padx=12)
        self.back_button = tk.Button(top, font=(config.FONT_ZH, 10), command=lambda: self.app.show_frame("MainMenu"))
        self._style_button(self.back_button)
        self.back_button.pack(side="left")

        self.title_label = tk.Label(root, font=(config.FONT_ZH, 22, "bold"), bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.title_label.pack(pady=8)

        self.unlock_frame = tk.LabelFrame(root, padx=12, pady=12, bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.unlock_frame.pack(fill="x", padx=26, pady=8)

        row = tk.Frame(self.unlock_frame, bg=root_bg)
        row.pack(fill="x")

        self.unlock_entry = tk.Entry(
            row,
            width=32,
            font=(config.FONT_EN, 10),
            bg=config.BUTTON_BG,
            fg=config.BUTTON_FG,
            insertbackground=config.BUTTON_FG,
        )
        self.unlock_entry.pack(side="left", padx=(0, 8))

        self.apply_unlock_button = tk.Button(row, font=(config.FONT_ZH, 10), command=self.apply_unlock_code)
        self._style_button(self.apply_unlock_button)
        self.apply_unlock_button.pack(side="left")

        self.pick_license_button = tk.Button(row, font=(config.FONT_ZH, 10), command=self.pick_license_file)
        self._style_button(self.pick_license_button)
        self.pick_license_button.pack(side="left", padx=(8, 0))

        self.drop_hint_label = tk.Label(self.unlock_frame, text="", font=(config.FONT_ZH, 10), bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.drop_hint_label.pack(anchor="w", pady=(6, 0))

        if DND_FILES is not None and hasattr(self.unlock_entry, "drop_target_register"):
            self.unlock_entry.drop_target_register(DND_FILES)
            self.unlock_entry.dnd_bind("<<Drop>>", self.on_license_drop)

        self.unlock_status_label = tk.Label(self.unlock_frame, text="", font=(config.FONT_ZH, 11), bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.unlock_status_label.pack(anchor="w", pady=(8, 0))

        self.language_frame = tk.LabelFrame(root, padx=12, pady=12, bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.language_frame.pack(fill="x", padx=26, pady=8)

        lang_row = tk.Frame(self.language_frame, bg=root_bg)
        lang_row.pack(fill="x")
        self.language_name_to_code = {name: code for code, name in i18n.SUPPORTED_LANGUAGES.items()}
        current_name = i18n.SUPPORTED_LANGUAGES.get(self.app.state.ui_language, i18n.SUPPORTED_LANGUAGES["zh"])
        self.language_var = tk.StringVar(value=current_name)

        self.language_option = tk.OptionMenu(lang_row, self.language_var, *self.language_name_to_code.keys())
        self.language_option.configure(
            font=(config.FONT_ZH, 10),
            bg=config.BUTTON_BG,
            fg=config.BUTTON_FG,
            activebackground=config.BUTTON_ACTIVE_BG,
            activeforeground=config.BUTTON_ACTIVE_FG,
        )
        self.language_option["menu"].configure(
            font=(config.FONT_ZH, 10),
            bg=config.BUTTON_BG,
            fg=config.BUTTON_FG,
            activebackground=config.BUTTON_ACTIVE_BG,
            activeforeground=config.BUTTON_ACTIVE_FG,
        )
        self.language_option.pack(side="left")
        self.apply_language_button = tk.Button(lang_row, font=(config.FONT_ZH, 10), command=self.apply_language)
        self._style_button(self.apply_language_button)
        self.apply_language_button.pack(side="left", padx=(8, 0))

        self.save_frame = tk.LabelFrame(root, padx=12, pady=12, bg=root_bg, fg=config.SPACE_BLUE_FG)
        self.save_frame.pack(fill="x", padx=26, pady=8)

        self.clear_button = tk.Button(self.save_frame, font=(config.FONT_ZH, 10), command=self.clear_save_with_confirm)
        self._style_button(self.clear_button)
        self.clear_button.pack(anchor="w", pady=(0, 8))
        self.export_button = tk.Button(self.save_frame, font=(config.FONT_ZH, 10), command=self.export_save_file)
        self._style_button(self.export_button)
        self.export_button.pack(anchor="w")
        self.import_button = tk.Button(self.save_frame, font=(config.FONT_ZH, 10), command=self.import_save_file)
        self._style_button(self.import_button)
        self.import_button.pack(anchor="w", pady=(8, 0))

        self.message_label = tk.Label(root, text="", fg=config.SPACE_BLUE_FG, bg=root_bg, font=(config.FONT_ZH, 11))
        self.message_label.pack(anchor="w", padx=28, pady=8)
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

    def refresh_texts(self) -> None:
        self.back_button.configure(text=self.app.tr("back_to_menu"))
        self.title_label.configure(text=self.app.tr("settings_title"))
        self.unlock_frame.configure(text=self.app.tr("settings_unlock_title"))
        self.language_frame.configure(text=self.app.tr("settings_language_title"))
        self.save_frame.configure(text=self.app.tr("settings_save_title"))
        self.apply_unlock_button.configure(text=self.app.tr("settings_apply_unlock_code"))
        self.pick_license_button.configure(text="選擇授權檔")
        self.drop_hint_label.configure(text="可拖曳 license.json 到輸入框，或按「選擇授權檔」")
        self.apply_language_button.configure(text=self.app.tr("settings_apply_language"))
        self.clear_button.configure(text=self.app.tr("settings_clear_save"))
        self.export_button.configure(text=self.app.tr("settings_export_save"))
        self.import_button.configure(text="匯入存檔")

    def apply_language(self) -> None:
        language_name = self.language_var.get()
        code = self.language_name_to_code.get(language_name, "zh")
        self.app.set_language(code)
        refreshed_name = i18n.SUPPORTED_LANGUAGES.get(self.app.state.ui_language, i18n.SUPPORTED_LANGUAGES["zh"])
        self.language_var.set(refreshed_name)
        self.message_label.config(text=self.app.tr("settings_language_changed"), fg=config.SPACE_BLUE_FG)

    def on_show(self) -> None:
        replenish_tickets(self.app.state, now=self.app.time_provider())
        self.refresh_texts()
        self.refresh_unlock_status()
        current_name = i18n.SUPPORTED_LANGUAGES.get(self.app.state.ui_language, i18n.SUPPORTED_LANGUAGES["zh"])
        self.language_var.set(current_name)

    def refresh_unlock_status(self) -> None:
        paid_unlocked, reason = is_paid_unlocked()
        self.app.state.paid_unlocked = paid_unlocked
        self.app.license_reason = reason
        rule = get_ticket_rule(self.app.state.paid_unlocked)
        if self.app.state.paid_unlocked:
            text = f"{self.app.tr('settings_status_unlocked', seconds=rule.interval_seconds, cap=rule.cap)} (license:{reason})"
        else:
            text = f"{self.app.tr('settings_status_locked', seconds=rule.interval_seconds, cap=rule.cap)} (license:{reason})"
        self.unlock_status_label.config(text=text)

    def apply_unlock_code(self) -> None:
        entered = self.unlock_entry.get().strip()
        if entered:
            _, reason = install_license_from_path(entered)
        else:
            reason = "source_not_found"
        paid_unlocked, _ = is_paid_unlocked()
        self.app.state.paid_unlocked = paid_unlocked
        self.app.license_reason = reason
        replenish_tickets(self.app.state, now=self.app.time_provider())
        self.app.persist()
        self.refresh_unlock_status()
        if paid_unlocked:
            self.message_label.config(text=f"{self.app.tr('settings_unlock_success')} (license:{reason})", fg=config.SPACE_BLUE_FG)
        else:
            self.message_label.config(text=f"{self.app.tr('settings_unlock_wrong')} (license:{reason})", fg=config.SPACE_BLUE_FG)

    def pick_license_file(self) -> None:
        picked = filedialog.askopenfilename(
            title="選擇 license.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not picked:
            return
        self.unlock_entry.delete(0, "end")
        self.unlock_entry.insert(0, picked)
        self.apply_unlock_code()

    def _extract_first_drop_path(self, raw_data: str) -> str:
        data = raw_data.strip()
        if data.startswith("{") and data.endswith("}"):
            return data[1:-1]
        if " " in data:
            return data.split(" ")[0]
        return data

    def on_license_drop(self, event: object) -> None:
        raw_data = getattr(event, "data", "")
        if not isinstance(raw_data, str) or not raw_data.strip():
            return
        path = self._extract_first_drop_path(raw_data)
        self.unlock_entry.delete(0, "end")
        self.unlock_entry.insert(0, path)
        self.apply_unlock_code()

    def clear_save_with_confirm(self) -> None:
        first = messagebox.askyesno(self.app.tr("settings_confirm_title"), self.app.tr("settings_confirm_clear_1"))
        if not first:
            return
        second = messagebox.askyesno(
            self.app.tr("settings_confirm_clear_2_title"),
            self.app.tr("settings_confirm_clear_2"),
        )
        if not second:
            return

        self.app.state = clear_save(path=self.app.save_path, now=self.app.time_provider())
        self.refresh_unlock_status()
        self.message_label.config(text=self.app.tr("settings_save_cleared"), fg=config.SPACE_BLUE_FG)

    def export_save_file(self) -> None:
        self.app.persist()
        target = filedialog.asksaveasfilename(
            title=self.app.tr("settings_export_dialog_title"),
            defaultextension=".json",
            initialfile="save.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not target:
            return

        path = export_save(Path(target), path=self.app.save_path)
        self.message_label.config(text=self.app.tr("settings_export_done", path=path), fg=config.SPACE_BLUE_FG)

    def import_save_file(self) -> None:
        target = filedialog.askopenfilename(
            title="匯入存檔",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not target:
            return
        try:
            import_save(Path(target), path=self.app.save_path)
            self.app.state = load_save(path=self.app.save_path, now=self.app.time_provider())
            self.refresh_unlock_status()
            self.message_label.config(text="已匯入存檔", fg=config.SPACE_BLUE_FG)
        except Exception:
            self.message_label.config(text="匯入失敗", fg=config.SPACE_BLUE_FG)
