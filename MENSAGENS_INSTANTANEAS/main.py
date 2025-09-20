# main.py
import tkinter as tk
from LoginCadastro import LoginCadastro
from Interface import ChatApp
from Cliente import Cliente


def iniciar_chat(usuario):
    """Abre a interface do chat para o usuário autenticado"""
    root_chat = tk.Tk()
    cliente = Cliente(usuario)  # inicializa o cliente
    chat_app = ChatApp(root_chat, meu_nome=usuario)
    root_chat.protocol("WM_DELETE_WINDOW", chat_app.on_close)
    root_chat.mainloop()


if __name__ == "__main__":
    # Inicializa a tela de login/cadastro estilizada
    app = LoginCadastro(on_login=iniciar_chat)
    app.mainloop()
