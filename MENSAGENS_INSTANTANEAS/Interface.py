from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from Cliente import Cliente
import pygame
import datetime

CANVAS_W = 500
CANVAS_H = 450
MAX_BUBBLE_WIDTH = 240
BUBBLE_PAD = 8
BUBBLE_SPACING = 10
FONT = ("Segoe UI", 11)

class ChatApp:
    def __init__(self, master, meu_nome):
        self.master = master
        self.master.title("Chat Geral")
        self.master.geometry(f"{CANVAS_W}x600")
        self.master.resizable(True, False)

        self.meu_nome = meu_nome

        # Inicializa pygame mixer
        pygame.mixer.init()

        # ==== Canvas de mensagens ====
        self.canvas = tk.Canvas(
            self.master, width=CANVAS_W, height=CANVAS_H,
            highlightthickness=0, bd=0, bg="white"
        )
        self.canvas.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.75)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(relx=0.95, rely=0.05, relheight=0.75)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # estado para empilhar mensagens
        self.next_y = 10

        # Bindings de scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

        # Campo de entrada
        self.entry = ttk.Entry(self.master, font=FONT)
        self.entry.place(relx=0.05, rely=0.85, relwidth=0.7, relheight=0.07)
        self.entry.insert(0, "  Type a message...")
        self.placeholder_active = True
        self.entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.entry.bind("<FocusOut>", lambda e: self.add_placeholder())

        # Botão de envio
        self.send_button = tk.Button(self.master, text="Enviar", command=self.on_send, bd=0, bg="#4CAF50", fg="white")
        self.send_button.place(relx=0.77, rely=0.85, relwidth=0.18, relheight=0.07)

        # Cliente de rede
        self.cliente = Cliente(nome=self.meu_nome)
        self.cliente.on_message = self.receive_message

        # Carregar histórico ao abrir
        self.cliente.pedir_historico()

        # garante que o canvas tem scrollregion inicial
        self.canvas.configure(scrollregion=(0, 0, CANVAS_W, CANVAS_H))

    # placeholder helpers
    def clear_placeholder(self):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.placeholder_active = False

    def add_placeholder(self):
        if not self.entry.get():
            self.entry.insert(0, "  Type a message...")
            self.placeholder_active = True

    # envio de mensagem
    def on_send(self):
        msg = self.entry.get().strip()
        if msg and not self.placeholder_active:
            if self.cliente:
                self.cliente.enviar_mensagem(msg)
            self.add_message(f"Eu: {msg}", sent=True)
            self.entry.delete(0, tk.END)
            # som opcional
            try:
                pygame.mixer.music.load("send_sound.mp3")
                pygame.mixer.music.play()
            except Exception:
                pass

    # recebimento de mensagens e histórico
    def receive_message(self, msg):
        # historico
        if isinstance(msg, dict) and msg.get("acao") == "historico":
            for item in msg.get("data", []):
                remetente = item["remetente"]
                texto = item["mensagem"]
                ts = item.get("timestamp")
                enviado = (remetente == self.meu_nome)
                display = f"[{ts}] {remetente}: {texto}"
                self.add_message(display, sent=enviado)
        # mensagem em tempo real
        elif isinstance(msg, dict) and msg.get("acao") == "mensagem":
            remetente = msg.get("remetente")
            texto = msg.get("mensagem")
            ts = msg.get("timestamp")
            enviado = (remetente == self.meu_nome)
            display = f"[{ts}] {remetente}: {texto}" if ts else f"{remetente}: {texto}"
            self.add_message(display, sent=enviado)
        else:
            # fallback: se for lista antiga ou outro formato
            try:
                # se for lista de tuples
                for item in msg:
                    # adapt as needed
                    pass
            except Exception:
                pass


    # adiciona bolha de mensagem
    def add_message(self, message, sent=True):
        # Cores
        bubble_color = "#DCF8C6" if sent else "#FFFFFF"
        text_color = "#000000"
        time_color = "#555555"

        # Posição e alinhamento
        anchor = "ne" if sent else "nw"
        text_x = CANVAS_W - 70 if sent else 30

        # Adiciona hora à mensagem
        hora = datetime.datetime.now().strftime("%H:%M")
        full_message = f"{message}\n\n{hora}"

        # Texto (mensagem + hora)
        text_id = self.canvas.create_text(
            text_x, self.next_y, text=full_message, font=FONT,
            fill=text_color, width=MAX_BUBBLE_WIDTH, anchor=anchor
        )

        # Bounding box para desenhar o balão
        bbox = self.canvas.bbox(text_id)
        if not bbox:
            return
        x1, y1, x2, y2 = bbox

        rx1 = x1 - BUBBLE_PAD
        ry1 = y1 - BUBBLE_PAD
        rx2 = x2 + BUBBLE_PAD
        ry2 = y2 + BUBBLE_PAD

        # Balão atrás do texto
        rect_id = self.canvas.create_rectangle(
            rx1, ry1, rx2, ry2,
            fill=bubble_color, outline=bubble_color, width=1
        )
        self.canvas.tag_lower(rect_id, text_id)

        # Atualiza posição para próxima mensagem
        self.next_y = ry2 + BUBBLE_SPACING
        self.canvas.configure(scrollregion=(0, 0, CANVAS_W, max(self.next_y, CANVAS_H)))
        self.canvas.yview_moveto(1.0)

    def _on_mousewheel_windows(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def on_close(self):
        if self.cliente:
            try:
                self.cliente.close()
                print(f"🛑 {self.meu_nome} se desconectou.")
            except:
                pass
        self.master.destroy()

if __name__ == "__main__":
    meu_nome = input("Digite seu nome: ")
    root = tk.Tk()
    app = ChatApp(root, meu_nome)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
