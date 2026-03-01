# main.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Цветовая схема (тёмная, современная)
BG_COLOR = "#1e1e2e"
FG_COLOR = "#cdd6f4"
ENTRY_BG = "#2e2e44"
BUTTON_BG = "#89b4fa"
BUTTON_FG = "#1e1e2e"
ACCENT = "#a6e3a1"      # зелёный для успешных сообщений
ERROR = "#f38ba8"

class ChatLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Чат — Подключение")
        self.geometry("480x620")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        tk.Label(self, text="Подключение к чат-комнате", font=("Segoe UI", 16, "bold"),
                 bg=BG_COLOR, fg=FG_COLOR).pack(pady=(20, 10))

        # Фрейм с полями (выровненные метки + поля)
        form_frame = tk.Frame(self, bg=BG_COLOR)
        form_frame.pack(padx=30, pady=10, fill="x")

        labels = ["Название сервера", "Название комнаты", "Ник", "Пароль"]
        self.entries = {}

        for label_text in labels:
            row = tk.Frame(form_frame, bg=BG_COLOR)
            row.pack(fill="x", pady=6)

            lbl = tk.Label(row, text=label_text, width=16, anchor="e",
                           bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 11))
            lbl.pack(side="left")

            entry = tk.Entry(row, bg=ENTRY_BG, fg=FG_COLOR, insertbackground="white",
                             font=("Segoe UI", 11), width=24)
            entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

            if label_text == "Пароль":
                entry.config(show="•")

            self.entries[label_text] = entry

        # Поле лога / статуса
        tk.Label(self, text="Статус / лог подключения:", font=("Segoe UI", 10),
                 bg=BG_COLOR, fg="#94a3b8").pack(anchor="w", padx=30, pady=(15, 5))

        self.log_area = scrolledtext.ScrolledText(self, height=10, width=50,
                                                  bg=ENTRY_BG, fg=FG_COLOR,
                                                  font=("Consolas", 10),
                                                  state="disabled", wrap="word")
        self.log_area.pack(padx=30, pady=(0, 15), fill="both", expand=False)

        # Кнопка с большой стрелкой
        connect_btn = tk.Button(self, text="ПОДКЛЮЧИТЬСЯ  →", command=self.try_connect,
                                font=("Segoe UI", 13, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                                activebackground=ACCENT, activeforeground=BUTTON_FG,
                                width=20, height=2, relief="flat", bd=0)
        connect_btn.pack(pady=20)

        # Подсказка снизу
        tk.Label(self, text="Поля «Название комнаты» и «Пароль» — опционально",
                 font=("Segoe UI", 9), bg=BG_COLOR, fg="#64748b").pack(pady=(0, 10))

    def log(self, message, tag="info"):
        self.log_area.config(state="normal")
        if tag == "success":
            color = ACCENT
        elif tag == "error":
            color = ERROR
        else:
            color = FG_COLOR
        self.log_area.insert("end", message + "\n", f"color_{tag}")
        self.log_area.tag_config(f"color_{tag}", foreground=color)
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def try_connect(self):
        server_name = self.entries["Название сервера"].get().strip()
        room_name   = self.entries["Название комнаты"].get().strip()
        nickname    = self.entries["Ник"].get().strip()
        password    = self.entries["Пароль"].get().strip()

        if not server_name:
            messagebox.showwarning("Ошибка", "Укажите название сервера или IP")
            return

        if not nickname:
            messagebox.showwarning("Ошибка", "Введите ник")
            return

        self.log(f"Попытка подключения к {server_name} ...", "info")

        # Здесь должна быть реальная логика подключения
        # Пока просто имитация для демонстрации интерфейса
        import time
        self.after(800, lambda: self.log("Соединение установлено", "success"))
        self.after(1400, lambda: self.log(f"Комната: {room_name or 'Общая'}", "success"))
        self.after(2000, lambda: self.log(f"Вход выполнен как {nickname}", "success"))
        self.after(2800, lambda: self.log("Добро пожаловать в чат!", "success"))

        # В реальном коде здесь:
        # 1. Подключение по socket
        # 2. Отправка ника / комнаты / пароля
        # 3. Если успешно → открыть окно чата
        # self.after(3500, lambda: self.open_chat_window(nickname, server_name))

    def on_close(self):
        if messagebox.askokcancel("Выход", "Закрыть программу?"):
            self.destroy()

if __name__ == "__main__":
    app = ChatLauncher()
    app.mainloop()
