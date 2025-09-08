"""
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext, ttk
from Cliente import Cliente

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Clone")
        self.master.geometry("400x600")
        self.master.resizable(False, False)

        # Ícone da janela
        try:
            self.master.iconbitmap(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_icon2.png")
        except:
            print("Ícone não carregado.")

        # Wallpaper
        try:
            self.bg_image = tk.PhotoImage(file=r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_wallpaper.jpg")
            self.bg_label = tk.Label(self.master, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        except:
            print("Wallpaper não carregado.")

        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, font=("Segoe UI", 11), bg="white", fg="black")
        self.chat_area.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.75)
        self.chat_area.config(state=tk.DISABLED)

        # Entrada de texto
        self.entry = ttk.Entry(self.master, font=("Segoe UI", 11))
        self.entry.place(relx=0.05, rely=0.85, relwidth=0.7, relheight=0.07)
        self.entry.insert(0, "Type a message...")
        self.placeholder_active = True

        self.entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.entry.bind("<FocusOut>", lambda e: self.add_placeholder())

        # Botão de enviar
        self.send_button = ttk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.place(relx=0.77, rely=0.85, relwidth=0.18, relheight=0.07)

        # Cliente socket
        self.cliente = Cliente()
        self.cliente.on_message = self.receive_message

    def clear_placeholder(self):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.placeholder_active = False

    def add_placeholder(self):
        if not self.entry.get():
            self.entry.insert(0, "Type a message...")
            self.placeholder_active = True

    def send_message(self):
        msg = self.entry.get().strip()
        if msg and not self.placeholder_active:
            self.cliente.send_message(msg)
            self.update_chat(f"You: {msg}")
            self.entry.delete(0, tk.END)

    def receive_message(self, msg):
        self.update_chat(f"Friend: {msg}")

    def update_chat(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def on_close(self):
        self.cliente.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
"""

"""
import tkinter as tk
from PIL import Image, ImageTk   # precisa instalar: pip install pillow

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Clone")

        # Ícone (precisa ser .ico)
        try:
            self.master.iconbitmap(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_icon2.png")
        except Exception as e:
            print("Erro ao carregar ícone:", e)

        # Wallpaper (.jpg -> carrega com Pillow)
        try:
            image = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_wallpaper.jpg")
            self.bg_image = ImageTk.PhotoImage(image)
            
            self.bg_label = tk.Label(self.master, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print("Erro ao carregar wallpaper:", e)

        # Área de chat
        self.text_area = tk.Text(self.master, bg="white", fg="black", wrap="word")
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Campo de mensagem
        self.entry = tk.Entry(self.master, font=("Arial", 12))
        self.entry.insert(0, "Type a message...")
        self.entry.pack(padx=10, pady=5, fill=tk.X)

        # Botão enviar
        self.send_btn = tk.Button(self.master, text="Enviar", command=self.send_message)
        self.send_btn.pack(pady=5)

    def send_message(self):
        msg = self.entry.get()
        if msg.strip() != "":
            self.text_area.insert(tk.END, "Você: " + msg + "\n")
            self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x600")
    app = ChatApp(root)
    root.mainloop()
"""
""""
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext, ttk
from Cliente import Cliente

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Clone")
        self.master.geometry("600x600")
        self.master.resizable(False, False)

        # Ícone da janela (.ico obrigatório)
        try:
            self.master.iconbitmap(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_icon2.png")
        except:
            print("Ícone não carregado.")

        # Wallpaper (.jpg precisa do Pillow)
        try:
            image = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_wallpaper.jpg")
            self.bg_image = ImageTk.PhotoImage(image)

            self.bg_label = tk.Label(self.master, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print("Wallpaper não carregado:", e)

        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(
            self.master, wrap=tk.WORD, font=("Segoe UI", 11),
            bg="white", fg="black"
        )
        self.chat_area.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.75)
        self.chat_area.config(state=tk.DISABLED)

        # Entrada de texto
        self.entry = ttk.Entry(self.master, font=("Segoe UI", 11))
        self.entry.place(relx=0.05, rely=0.85, relwidth=0.7, relheight=0.07)
        self.entry.insert(0, "Type a message...")
        self.placeholder_active = True

        self.entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.entry.bind("<FocusOut>", lambda e: self.add_placeholder())

        # Botão de enviar
        self.send_button = ttk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.place(relx=0.77, rely=0.85, relwidth=0.18, relheight=0.07)

        # Cliente socket
        self.cliente = Cliente()
        self.cliente.on_message = self.receive_message

    def clear_placeholder(self):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.placeholder_active = False

    def add_placeholder(self):
        if not self.entry.get():
            self.entry.insert(0, "Type a message...")
            self.placeholder_active = True

    def send_message(self):
        msg = self.entry.get().strip()
        if msg and not self.placeholder_active:
            self.cliente.send_message(msg)
            self.update_chat(f"You: {msg}")
            self.entry.delete(0, tk.END)

    def receive_message(self, msg):
        self.update_chat(f"Friend: {msg}")

    def update_chat(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def on_close(self):
        self.cliente.close()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

"""
"""
# Interface.py
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from Cliente import Cliente   # seu módulo de rede separado

CANVAS_W = 500
CANVAS_H = 450
MAX_BUBBLE_WIDTH = 240
BUBBLE_PAD = 8
BUBBLE_SPACING = 10
FONT = ("WʜᴀᴛꜱAᴘᴘ", 12)

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Clone")
        self.master.geometry(f"{CANVAS_W}x600")
        self.master.resizable(True, False)

        # Ícone (.ico)
        try:
            self.master.iconbitmap(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_icon2.png")
        except Exception as e:
            print("Ícone não carregado:", e)

        # ==== Wallpaper no fundo da janela ====
        try:
            img = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_wallpaper.jpg")
            img = img.resize((CANVAS_W, 600), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)

            self.bg_label = tk.Label(self.master, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # cobre toda janela
        except Exception as e:
            print("Wallpaper não carregado:", e)
            self.master.configure(bg="#f0f0f0")

        # ==== Canvas por cima do wallpaper ====
        self.canvas = tk.Canvas(self.master, width=CANVAS_W, height=CANVAS_H,
                        highlightthickness=0, bd=0 )
        self.canvas.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.75)

        # Scrollbar ligada ao canvas
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(relx=0.95, rely=0.05, relheight=0.75)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # estado para empilhar mensagens
        self.next_y = 10

        # Bindings para scroll do mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)   # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)       # Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

        # Campo de entrada e botão (também por cima do wallpaper)
        self.entry = ttk.Entry(self.master, font=FONT)
        self.entry.place(relx=0.05, rely=0.85, relwidth=0.7, relheight=0.07)
        self.entry.insert(0, "Type a message...")
        self.placeholder_active = True
        self.entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.entry.bind("<FocusOut>", lambda e: self.add_placeholder())

        self.send_button = ttk.Button(self.master, text="Send", command=self.on_send)
        self.send_button.place(relx=0.77, rely=0.85, relwidth=0.18, relheight=0.07)

        # Cliente de rede
        self.cliente = None
        try:
            self.cliente = Cliente()
            self.cliente.on_message = self.receive_message
        except Exception as e:
            print("Não foi possível conectar ao servidor:", e)

        # garante que o canvas tem scrollregion inicial
        self.canvas.configure(scrollregion=(0,0,CANVAS_W, CANVAS_H))

    # placeholder helpers
    def clear_placeholder(self):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.placeholder_active = False

    def add_placeholder(self):
        if not self.entry.get():
            self.entry.insert(0, "Type a message...")
            self.placeholder_active = True

    def on_send(self):
        msg = self.entry.get().strip()
        if msg and not self.placeholder_active:
            if self.cliente:
                self.cliente.send_message(msg)
            self.add_message(msg, sent=True)
            self.entry.delete(0, tk.END)

    def receive_message(self, msg):
        self.add_message(msg, sent=False)

    def add_message(self, message, sent=True):
        bubble_color = "#DCF8C6" if sent else "#FFFFFF"
        text_color = "#000000"
        anchor = "ne" if sent else "nw"

        if sent:
            text_x = CANVAS_W - 70
        else:
            text_x = 30

        text_id = self.canvas.create_text(text_x, self.next_y, text=message, font=FONT,
                                          fill=text_color, width=MAX_BUBBLE_WIDTH, anchor=anchor)

        bbox = self.canvas.bbox(text_id)
        if not bbox:
            return
        x1, y1, x2, y2 = bbox

        rx1 = x1 - BUBBLE_PAD
        ry1 = y1 - BUBBLE_PAD
        rx2 = x2 + BUBBLE_PAD
        ry2 = y2 + BUBBLE_PAD

        rect_id = self.canvas.create_rectangle(rx1, ry1, rx2, ry2, fill=bubble_color, outline=bubble_color, width=1)
        self.canvas.tag_lower(rect_id, text_id)

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
            except:
                pass
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
"""

"""
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from Cliente import Cliente   # seu módulo de rede separado
import pygame  # para tocar o som de envio

CANVAS_W = 500
CANVAS_H = 450
MAX_BUBBLE_WIDTH = 240
BUBBLE_PAD = 8
BUBBLE_SPACING = 10
FONT = ("WʜᴀᴛꜱAᴘᴘ", 12)

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Clone")
        self.master.geometry(f"{CANVAS_W}x600")
        self.master.resizable(True, False)

        # Inicializa pygame mixer para som
        pygame.mixer.init()
        
                # ==== Logo no canto superior esquerdo ====
        try:
            logo_img = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_icon2.png")
            logo_img = logo_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)

            self.logo_label = tk.Label(self.master, image=self.logo_photo, bg="#1e1e1e")
            self.logo_label.place(x=10, y=10)

            # garante que o logo fique sempre por cima
            self.logo_label.lift()
        except Exception as e:
            print("Logo não carregado:", e)


        
        # Ícone (.ico)
        try:
            self.master.iconbitmap(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_icon2.png")
        except Exception as e:
            print("Ícone não carregado:", e)

        # ==== Wallpaper no fundo da janela ====
        try:
            img = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_wallpaper.jpg")
            img = img.resize((CANVAS_W, 600), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)

            self.bg_label = tk.Label(self.master, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Wallpaper não carregado:", e)
            self.master.configure(bg="#f0f0f0")

        # ==== Canvas por cima do wallpaper ====
        self.canvas = tk.Canvas(self.master, width=CANVAS_W, height=CANVAS_H,
                        highlightthickness=0, bd=0 )
        self.canvas.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.75)

        # Scrollbar ligada ao canvas
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(relx=0.95, rely=0.05, relheight=0.75)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # estado para empilhar mensagens
        self.next_y = 10

        # Bindings para scroll do mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)   # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)       # Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

        # Campo de entrada
        self.entry = ttk.Entry(self.master, font=FONT)
        self.entry.place(relx=0.05, rely=0.85, relwidth=0.7, relheight=0.07)
        self.entry.insert(0, "  Type a message...")
        self.placeholder_active = True
        self.entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.entry.bind("<FocusOut>", lambda e: self.add_placeholder())

        # ==== Botão de envio com ícone ====
        try:
            send_img = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/sendIcon.jpeg")
            send_img = send_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.send_photo = ImageTk.PhotoImage(send_img)
        except Exception as e:
            print("Ícone de envio não carregado:", e)
            self.send_photo = None

        self.send_button = tk.Button(self.master, image=self.send_photo, command=self.on_send, bd=0)
        self.send_button.place(relx=0.77, rely=0.85, relwidth=0.18, relheight=0.07)

        # Cliente de rede
        self.cliente = None
        try:
            self.cliente = Cliente()
            self.cliente.on_message = self.receive_message
        except Exception as e:
            print("Não foi possível conectar ao servidor:", e)

        # garante que o canvas tem scrollregion inicial
        self.canvas.configure(scrollregion=(0,0,CANVAS_W, CANVAS_H))

    # placeholder helpers
    def clear_placeholder(self):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.placeholder_active = False

    def add_placeholder(self):
        if not self.entry.get():
            self.entry.insert(0, "  Type a message...")
            self.placeholder_active = True

    def on_send(self):
        msg = self.entry.get().strip()
        if msg and not self.placeholder_active:
            if self.cliente:
                self.cliente.send_message(msg)
            self.add_message(msg, sent=True)
            self.entry.delete(0, tk.END)
            # Toca o som de envio
            try:
                pygame.mixer.music.load(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/send_sound.mp3")
                pygame.mixer.music.play()
            except Exception as e:
                print("Erro ao tocar som:", e)

    def receive_message(self, msg):
        self.add_message(msg, sent=False)

    def add_message(self, message, sent=True):
        bubble_color = "#DCF8C6" if sent else "#FFFFFF"
        text_color = "#000000"
        anchor = "ne" if sent else "nw"

        if sent:
            text_x = CANVAS_W - 70
        else:
            text_x = 30

        text_id = self.canvas.create_text(text_x, self.next_y, text=message, font=FONT,
                                          fill=text_color, width=MAX_BUBBLE_WIDTH, anchor=anchor)

        bbox = self.canvas.bbox(text_id)
        if not bbox:
            return
        x1, y1, x2, y2 = bbox

        rx1 = x1 - BUBBLE_PAD
        ry1 = y1 - BUBBLE_PAD
        rx2 = x2 + BUBBLE_PAD
        ry2 = y2 + BUBBLE_PAD

        rect_id = self.canvas.create_rectangle(rx1, ry1, rx2, ry2, fill=bubble_color, outline=bubble_color, width=1)
        self.canvas.tag_lower(rect_id, text_id)

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
            except:
                pass
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

"""

# 1- Colocar o icone acima na interface;
# 2-

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from Cliente import Cliente   # seu módulo de rede separado
import pygame  # para tocar o som de envio

CANVAS_W = 500
CANVAS_H = 450
MAX_BUBBLE_WIDTH = 240
BUBBLE_PAD = 8
BUBBLE_SPACING = 10
FONT = ("Segoe UI", 11)

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Clone")
        self.master.geometry(f"{CANVAS_W}x600")
        self.master.resizable(True, False)

        # Inicializa pygame mixer para som
        pygame.mixer.init()

        # Ícone da janela
        try:
            self.master.iconbitmap(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_icon2.png")
        except Exception as e:
            print("Ícone da janela não carregado:", e)

        # ==== Wallpaper no fundo da janela ====
        try:
            img = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_wallpaper.jpg")
            img = img.resize((CANVAS_W, 600), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)

            self.bg_label = tk.Label(self.master, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Wallpaper não carregado:", e)
            self.master.configure(bg="#f0f0f0")

        # ==== Canvas por cima do wallpaper ====
        self.canvas = tk.Canvas(
            self.master, width=CANVAS_W, height=CANVAS_H,
            highlightthickness=0, bd=0
        )
        self.canvas.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.75)

        # Adiciona logotipo no canto superior esquerdo dentro do canvas
        try:
            logo_img = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/messenger_icon2.png")
            logo_img = logo_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            self.canvas.create_image(10, 10, image=self.logo_photo, anchor="nw")
        except Exception as e:
            print("Erro ao carregar logotipo no canvas:", e)

        # Scrollbar ligada ao canvas
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(relx=0.95, rely=0.05, relheight=0.75)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # estado para empilhar mensagens
        self.next_y = 60  # começa abaixo do logo

        # Bindings para scroll do mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)   # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)       # Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

        # Campo de entrada
        self.entry = ttk.Entry(self.master, font=FONT)
        self.entry.place(relx=0.05, rely=0.85, relwidth=0.7, relheight=0.07)
        self.entry.insert(0, "  Type a message...")
        self.placeholder_active = True
        self.entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.entry.bind("<FocusOut>", lambda e: self.add_placeholder())

        # ==== Botão de envio com ícone ====
        try:
            send_img = Image.open(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/sendIcon.jpeg")
            send_img = send_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.send_photo = ImageTk.PhotoImage(send_img)
        except Exception as e:
            print("Ícone de envio não carregado:", e)
            self.send_photo = None

        self.send_button = tk.Button(self.master, image=self.send_photo, command=self.on_send, bd=0)
        self.send_button.place(relx=0.77, rely=0.85, relwidth=0.18, relheight=0.07)

        # Cliente de rede
        self.cliente = None
        try:
            self.cliente = Cliente()
            self.cliente.on_message = self.receive_message
        except Exception as e:
            print("Não foi possível conectar ao servidor:", e)

        # garante que o canvas tem scrollregion inicial
        self.canvas.configure(scrollregion=(0,0,CANVAS_W, CANVAS_H))

    # placeholder helpers
    def clear_placeholder(self):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.placeholder_active = False

    def add_placeholder(self):
        if not self.entry.get():
            self.entry.insert(0, "  Type a message...")
            self.placeholder_active = True

    def on_send(self):
        msg = self.entry.get().strip()
        if msg and not self.placeholder_active:
            if self.cliente:
                self.cliente.send_message(msg)
            self.add_message(msg, sent=True)
            self.entry.delete(0, tk.END)
            # Toca o som de envio
            try:
                pygame.mixer.music.load(r"C:/Users/Kayron/Documents/MENSAGENS_INSTANTANEAS/send_sound.mp3")
                pygame.mixer.music.play()
            except Exception as e:
                print("Erro ao tocar som:", e)

    def receive_message(self, msg):
        self.add_message(msg, sent=False)

    def add_message(self, message, sent=True):
        bubble_color = "#DCF8C6" if sent else "#FFFFFF"
        text_color = "#000000"
        anchor = "ne" if sent else "nw"

        if sent:
            text_x = CANVAS_W - 70
        else:
            text_x = 30

        text_id = self.canvas.create_text(text_x, self.next_y, text=message, font=FONT,
                                          fill=text_color, width=MAX_BUBBLE_WIDTH, anchor=anchor)

        bbox = self.canvas.bbox(text_id)
        if not bbox:
            return
        x1, y1, x2, y2 = bbox

        rx1 = x1 - BUBBLE_PAD
        ry1 = y1 - BUBBLE_PAD
        rx2 = x2 + BUBBLE_PAD
        ry2 = y2 + BUBBLE_PAD

        rect_id = self.canvas.create_rectangle(rx1, ry1, rx2, ry2, fill=bubble_color, outline=bubble_color, width=1)
        self.canvas.tag_lower(rect_id, text_id)

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
            except:
                pass
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
 