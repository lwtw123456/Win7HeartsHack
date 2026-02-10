import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ControlWindowUi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Win7版64位《红心大战》六项修改器")
        self.geometry("720x595")
        self.configure(bg="#f5f7fa")
        self._center_window(720, 595)
        self._build_ui()

    def _center_window(self, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def log(self, msg):
        now = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{now}] {msg}\n")
        self.log_text.see(tk.END)

    def _build_ui(self):
        top_frame = ttk.LabelFrame(self, text="功能区")
        top_frame.pack(fill="x", padx=15, pady=10)

        switch_defs = [
            ("自由模式", "free_play"),
            ("透视模式", "see_all"),
            ("明牌模式", "exposed_hand"),
            ("无敌模式", "god_mode"),
            ("全二模式", "all_two"),
        ]

        self.switch_vars = {}

        for i, (text, key) in enumerate(switch_defs):
            var = tk.BooleanVar(value=False)
            self.switch_vars[key] = var

            cb = ttk.Checkbutton(
                top_frame,
                text=text,
                variable=var,
                command=lambda k=key: self.on_switch_change(k)
            )
            cb.grid(row=0, column=i, padx=15, pady=10, sticky="w")

        self.win_btn = ttk.Button(
            top_frame,
            text="直接取胜",
            command=self.on_win
        )
        self.win_btn.grid(row=0, column=5, padx=15, pady=10)

        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.listboxes = {}

        log_frame = ttk.LabelFrame(self, text="运行日志")
        log_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.log_text = tk.Text(log_frame, height=6, font=("Consolas", 10))
        self.log_text.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        titles = ["上家", "对家", "下家"]

        for col, title in enumerate(titles):
            lf = ttk.LabelFrame(list_frame, text=title)
            lf.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
            list_frame.columnconfigure(col, weight=1)

            lb = tk.Listbox(
                lf,
                height=14,
                font=("微软雅黑", 11),
                activestyle="dotbox"
            )
            lb.pack(fill="both", expand=True, padx=8, pady=8)

            self.listboxes[title] = lb

    def on_switch_change(self, key):
        pass

    def on_win(self):
        pass
