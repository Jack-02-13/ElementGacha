from __future__ import annotations

import tkinter as tk

import config


class GradientFrame(tk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self._gradient_after_id: str | None = None
        self._last_size: tuple[int, int] = (0, 0)

        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.body: tk.Widget = self.bg_canvas

        self.bg_canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_canvas_configure(self, event: tk.Event[tk.Misc]) -> None:
        width, height = int(event.width), int(event.height)
        if width <= 1 or height <= 1:
            return
        if (width, height) == self._last_size:
            return
        self._last_size = (width, height)
        if self._gradient_after_id is not None:
            self.after_cancel(self._gradient_after_id)
        self._gradient_after_id = self.after(60, lambda w=width, h=height: self._draw_gradient(w, h))

    def _draw_gradient(self, width: int, height: int) -> None:
        self._gradient_after_id = None
        self.bg_canvas.delete("gradient")
        r1, g1, b1 = self.winfo_rgb(config.SPACE_BLUE_GRADIENT_TOP)
        r2, g2, b2 = self.winfo_rgb(config.SPACE_BLUE_GRADIENT_BOTTOM)

        steps = max(2, min(height, 180))
        for i in range(steps):
            ratio = i / (steps - 1)
            nr = int(r1 + (r2 - r1) * ratio)
            ng = int(g1 + (g2 - g1) * ratio)
            nb = int(b1 + (b2 - b1) * ratio)
            color = f"#{nr // 256:02x}{ng // 256:02x}{nb // 256:02x}"
            y1 = int(i * height / steps)
            y2 = int((i + 1) * height / steps)
            self.bg_canvas.create_rectangle(0, y1, width, y2, outline="", fill=color, tags="gradient")
        self.bg_canvas.tag_lower("gradient")
