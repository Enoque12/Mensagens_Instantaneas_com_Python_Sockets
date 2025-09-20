import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import os
from PIL import Image

DB_FILE = "cadastro.db"

class LoginCadastro(ctk.CTk):
    def __init__(self, on_login=None):
        super().__init__()
        self.title("ChatGo - Login")
        self.geometry("700x400")
        self.resizable(False, False)
        self.on_login = on_login

        self.create_db()
        self.tela_login()

    def create_db(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                senha TEXT
            )
        """)
        conn.commit()
        conn.close()

    def hash_password(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    # ------------------- Tela Login -------------------
    def tela_login(self):
        # Caminho relativo da imagem
        BASE_DIR = os.path.dirname(__file__)
        image_path = os.path.join(BASE_DIR, "LogoLogin.png")

        try:
            pil_image = Image.open(image_path)
            self.img = ctk.CTkImage(light_image=pil_image, size=(250, 250))
        except FileNotFoundError:
            self.img = None

        if self.img:
            self.lb_img = ctk.CTkLabel(self, text="", image=self.img)
            self.lb_img.grid(row=1, column=0, padx=10, pady=20, sticky="w")

        self.title_label = ctk.CTkLabel(self, text="Faça o seu Login \n ou\nCadastre-se no ChatGo",
                                        font=("Century Gothic bold",18))
        self.title_label.grid(row=0, column=0,pady=10,padx=10)

        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça seu login", font=("Century Gothic bold",22))
        self.lb_title.grid(row=0,column=0,padx=10,pady=10)

        self.entry_user = ctk.CTkEntry(self.frame_login, width=300,
                                       placeholder_text="Digite nome de Usuário",
                                       font=("Century Gothic bold",22), corner_radius=15)
        self.entry_user.grid(row=1,column=0,pady=10,padx=10)

        self.entry_pass = ctk.CTkEntry(self.frame_login, width=300,
                                       placeholder_text="Digite senha de Usuário",
                                       font=("Century Gothic bold",22), corner_radius=15, show="*")
        self.entry_pass.grid(row=2,column=0,pady=10,padx=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=300,
                                       text="Fazer Login".upper(), font=("Century Gothic bold",16),
                                       corner_radius=15, command=self.login)
        self.btn_login.grid(row=3,column=0,pady=10,padx=10)

        self.sap = ctk.CTkLabel(self.frame_login, text="Se não tem conta faça já o cadastro",
                                font=("Century Gothic bold",16))
        self.sap.grid(row=4,column=0,pady=10,padx=5)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050",
                                          text="Cadastrar-se".upper(), font=("Century Gothic bold",16),
                                          corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=5,column=0,pady=10,padx=10)

    def login(self):
        user = self.entry_user.get().strip()
        senha = self.entry_pass.get().strip()
        if not user or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT senha FROM usuarios WHERE username = ?", (user,))
        row = cursor.fetchone()
        conn.close()

        if row and self.hash_password(senha) == row[0]:
            messagebox.showinfo("Login", f"Bem-vindo, {user}!")
            if self.on_login:
                self.destroy()
                self.on_login(user)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    # ------------------- Tela Cadastro -------------------
    def tela_de_cadastro(self):
        self.frame_login.place_forget()

        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350,y=10)

        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça seu Cadastro",
                                     font=("Century Gothic bold",22))
        self.lb_title.grid(row=0,column=0,padx=5,pady=10)

        self.entry_user_cad = ctk.CTkEntry(self.frame_cadastro,width=300,
                                           placeholder_text="Digite nome de Usuário",
                                           font=("Century Gothic bold",22),corner_radius=15)
        self.entry_user_cad.grid(row=1,column=0,pady=5,padx=10)

        self.entry_pass_cad = ctk.CTkEntry(self.frame_cadastro,width=300,
                                           placeholder_text="Digite senha de Usuário",
                                           font=("Century Gothic bold",22),corner_radius=15,show="*")
        self.entry_pass_cad.grid(row=2,column=0,pady=5,padx=10)

        self.entry_conf_cad = ctk.CTkEntry(self.frame_cadastro,width=300,
                                           placeholder_text="Confirme senha de Usuário",
                                           font=("Century Gothic bold",22),corner_radius=15,show="*")
        self.entry_conf_cad.grid(row=3,column=0,pady=5,padx=10)

        self.btn_cadastrar = ctk.CTkButton(self.frame_cadastro,width=300,fg_color="green",
                                           hover_color="#050",text="Cadastrar-se".upper(),
                                           font=("Century Gothic bold",16),
                                           corner_radius=15,command=self.cadastrar_usuario)
        self.btn_cadastrar.grid(row=4,column=0,pady=10,padx=10)

        self.btn_login_back = ctk.CTkButton(self.frame_cadastro,width=300,
                                            text="Voltar a tela Login".upper(),
                                            font=("Century Gothic bold",16),
                                            corner_radius=15,fg_color="#444",hover_color="#333",
                                            command=self.voltar_login)
        self.btn_login_back.grid(row=5,column=0,pady=5)

    def voltar_login(self):
        self.frame_cadastro.place_forget()
        self.tela_login()

    def cadastrar_usuario(self):
        user = self.entry_user_cad.get().strip()
        senha = self.entry_pass_cad.get().strip()
        conf = self.entry_conf_cad.get().strip()

        if not user or not senha or not conf:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

        if senha != conf:
            messagebox.showerror("Erro", "Senhas não conferem!")
            return

        if len(user) < 3 or len(senha) < 4:
            messagebox.showwarning("Aviso", "Usuário ou senha muito curto")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)",
                           (user, self.hash_password(senha)))
            conn.commit()
            messagebox.showinfo("Cadastro", f"Usuário {user} cadastrado com sucesso!")
            self.voltar_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe!")
        finally:
            conn.close()
