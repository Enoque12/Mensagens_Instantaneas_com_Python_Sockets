"""
import socket

HOST = '127.0.0.1'   # deve ser o mesmo do servidor
PORT = 5000

# cria socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Conectado ao servidor. Digite mensagens ou 'sair' para encerrar.")

while True:
    msg = input("Cliente > ")
    client_socket.sendall(msg.encode())
    if msg.lower() == "sair":
        break

    resposta = client_socket.recv(1024).decode()
    print("Servidor:", resposta)
    if resposta.lower() == "sair":
        break

client_socket.close()

"""
"""
import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

def receber(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print("\n" + msg)
        except:
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Conectado ao chat. Digite mensagens ou 'sair' para encerrar.")

    threading.Thread(target=receber, args=(client_socket,)).start()

    while True:
        msg = input()
        client_socket.sendall(msg.encode())
        if msg.lower() == "sair":
            client_socket.close()
            break

if __name__ == "__main__":
    main()
"""

import socket
import threading

class Cliente:
    def __init__(self, host="192.168.104.7", port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.running = True
        self.on_message = None  # callback para interface

        # inicia thread para ouvir mensagens
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, msg: str):
        try:
            self.socket.send(msg.encode("utf-8"))
        except Exception as e:
            print("Erro ao enviar:", e)

    def receive_messages(self):
        while self.running:
            try:
                msg = self.socket.recv(1024).decode("utf-8")
                if msg and self.on_message:
                    self.on_message(msg)  # envia msg para interface
            except:
                break

    def close(self):
        self.running = False
        try:
            self.socket.close()
        except:
            pass

"""
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

# CONFIGS DO SERVIDOR
HOST = "127.0.0.1"
PORT = 12345

class Cliente:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Clone")
        self.master.geometry("400x600")
        self.master.resizable(False, False)

        # Define o ícone
        try:
            self.master.iconbitmap(r"C:/Users/Kayron/Documents/MENSAGENS INSTANTANEAS/messenger_icon2.png")
        except Exception as e:
            print("Não foi possível carregar ícone:", e)
        
        # Cria frame com wallpaper
        self.bg_image = tk.PhotoImage(file=r"C:/Users/Kayron/Documents/MENSAGENS INSTANTANEAS/messenger_wallpaper.jpg")
        self.bg_label = tk.Label(self.master, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Área de mensagens (com scroll)
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, font=("Segoe UI", 11), bg="white", fg="black")
        self.chat_area.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.75)
        self.chat_area.config(state=tk.DISABLED)

        # Campo de entrada
        self.entry = ttk.Entry(self.master, font=("Segoe UI", 11))
        self.entry.place(relx=0.05, rely=0.85, relwidth=0.7, relheight=0.07)
        self.entry.insert(0, "Type a message...")

        # Remove placeholder quando focado
        self.entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.entry.bind("<FocusOut>", lambda e: self.add_placeholder())
        self.placeholder_active = True

        # Botão de enviar
        self.send_button = ttk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.place(relx=0.77, rely=0.85, relwidth=0.18, relheight=0.07)

        # Socket do cliente
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        # Thread para ouvir mensagens do servidor
        threading.Thread(target=self.receive_messages, daemon=True).start()

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
            try:
                self.client_socket.send(msg.encode("utf-8"))
                self.update_chat(f"You: {msg}")
                self.entry.delete(0, tk.END)
            except Exception as e:
                self.update_chat(f"[Erro ao enviar mensagem: {e}]")

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode("utf-8")
                if msg:
                    self.update_chat(f"Friend: {msg}")
            except:
                break

    def update_chat(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

# MAIN
if __name__ == "__main__":
    root = tk.Tk()
    client = Cliente(root)
    root.mainloop()

"""