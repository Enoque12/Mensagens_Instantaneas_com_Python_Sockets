from tkinter import *
from PIL import Image
import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import subprocess
import sys


# ------------------------------------------
# Backend: Banco de dados e lógica
# ------------------------------------------
class Backend():
    
    def connecta_db(self):
        self.conn = sqlite3.connect("sistema_cadastro.db")
        self.cursor = self.conn.cursor()
    
    def desconecta_db(self):
        self.conn.close()
        
    def cria_tabela(self):
        self.connecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        self.desconecta_db()
        print("Tabela Criada com Sucesso")
    
    # ------------------------------------------
    # Cadastro de usuário
    # ------------------------------------------
    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()

        # Validação de campos
        if (self.username_cadastro=="" or 
            self.email_cadastro=="" or
            self.senha_cadastro=="" or
            self.confirma_senha_cadastro==""):
            messagebox.showerror(title="ChatGo", message="Por Favor preencha todos os campos")
            return

        elif len(self.username_cadastro) < 4:
            messagebox.showwarning(title="ChatGo", message="O nome de Usuario deve ter pelo menos 4 caracteres")
            return

        elif len(self.senha_cadastro) < 4:
            messagebox.showwarning(title="ChatGo", message="A Senha deve ter pelo menos 4 caracteres")
            return

        elif self.senha_cadastro != self.confirma_senha_cadastro:
            messagebox.showerror(title="ChatGo", message="Erro!!! Senhas diferentes, coloque senhas iguais")
            return

        # Inserção no banco de dados
        try:
            self.connecta_db()
            self.cursor.execute("""
                INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha) 
                VALUES (?, ?, ?, ?)
            """, (self.username_cadastro,
                  self.email_cadastro,
                  self.senha_cadastro,
                  self.confirma_senha_cadastro))
            self.conn.commit()  # Commit correto
            self.desconecta_db()
            messagebox.showinfo(title="ChatGo", message=f"Parabéns {self.username_cadastro}, registrado com sucesso!")
            self.limpa_entry_cadastro()
        except Exception as e:
            messagebox.showerror(title="ChatGo", message=f"Erro de processamento: {e}")
            self.desconecta_db()
    
    # ------------------------------------------
    # Verificação de login
    # ------------------------------------------
    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        self.connecta_db()
        self.cursor.execute("SELECT Senha FROM Usuarios WHERE Username = ?", (self.username_login,))
        resultado = self.cursor.fetchone()
        self.desconecta_db()

        # Verificação de dados
        if resultado and self.senha_login == resultado[0]:
            messagebox.showinfo(title="ChatGo", message=f"Parabéns {self.username_login}, login feito com sucesso!")
            self.limpa_entry_login()

            # Fecha a janela de login
            self.destroy()
            # Abre a interface principal
            subprocess.Popen([sys.executable, r"E:/New folder/Codigos_Programacao/ProjectoChatEmGrupo/MENSAGENS_INSTANTANEAS/Interface.py"])

        else:
            messagebox.showerror(title="ChatGo", message="Erro: dados não encontrados ou incorretos")


# ------------------------------------------
# Aplicação principal
# ------------------------------------------
class App(ctk.CTk, Backend):

    def __init__(self):    
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_login_()
        self.cria_tabela()

    # Configuração da janela principal
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("ChatGo")
        self.resizable(False, False)
        # Centralizar janela
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
    # ------------------------------------------
    # Tela de login
    # ------------------------------------------
    def tela_login_(self):
        pil_image = Image.open(r"E:/New folder/Codigos_Programacao/ProjectoChatEmGrupo/MENSAGENS_INSTANTANEAS/LogoLogin.png")
        self.img = ctk.CTkImage(light_image=pil_image, size=(250, 250))
        self.lb_img = ctk.CTkLabel(self, text="", image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10, pady=20, sticky="w")  # canto esquerdo

        self.title_label = ctk.CTkLabel(self, text="Faça o seu Login \n ou\nCadastre-se no ChatGo",
                                        font=("Century Gothic bold",18))
        self.title_label.grid(row=0, column=0,pady=10,padx=10)

        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça seu login", font=("Century Gothic bold",22))
        self.lb_title.grid(row=0,column=0,padx=10,pady=10)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300,
                                                 placeholder_text="Digite nome de Usuário",
                                                 font=("Century Gothic bold",22), corner_radius=15)
        self.username_login_entry.grid(row=1,column=0,pady=10,padx=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300,
                                              placeholder_text="Digite senha de Usuário",
                                              font=("Century Gothic bold",22), corner_radius=15, show="*")
        self.senha_login_entry.grid(row=2,column=0,pady=10,padx=10)

        # Checkbox funcional para mostrar/ocultar senha
        self.ver_senha_var = BooleanVar()
        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Click para ver senha",
                                         variable=self.ver_senha_var, command=self.toggle_senha_login,
                                         font=("Century Gothic bold",12))
        self.ver_senha.grid(row=3,column=0,pady=10,padx=10)
        
        self.btn_login = ctk.CTkButton(self.frame_login, width=300,
                                       text="Fazer Login".upper(), font=("Century Gothic bold",16),
                                       corner_radius=15, command=self.verifica_login)
        self.btn_login.grid(row=4,column=0,pady=10,padx=10)

        self.sap = ctk.CTkLabel(self.frame_login, text="Se não tem conta faça já o cadastro",
                                font=("Century Gothic bold",16))
        self.sap.grid(row=5,column=0,pady=10,padx=5)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050",
                                          text="Cadastrar-se".upper(), font=("Century Gothic bold",16),
                                          corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6,column=0,pady=10,padx=10)

    # Mostrar/ocultar senha login
    def toggle_senha_login(self):
        if self.ver_senha_var.get():
            self.senha_login_entry.configure(show="")
        else:
            self.senha_login_entry.configure(show="*")

    # ------------------------------------------
    # Tela de cadastro
    # ------------------------------------------
    def tela_de_cadastro(self):
        self.frame_login.place_forget()

        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350,y=10)

        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça seu Cadastro",
                                     font=("Century Gothic bold",22))
        self.lb_title.grid(row=0,column=0,padx=5,pady=10)

        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro,width=300,
                                                    placeholder_text="Digite nome de Usuário",
                                                    font=("Century Gothic bold",22),corner_radius=15)
        self.username_cadastro_entry.grid(row=1,column=0,pady=5,padx=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro,width=300,
                                                 placeholder_text="Digite Email de Usuário",
                                                 font=("Century Gothic bold",22),corner_radius=15)
        self.email_cadastro_entry.grid(row=2,column=0,pady=5,padx=10)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro,width=300,
                                                 placeholder_text="Digite senha de Usuário",
                                                 font=("Century Gothic bold",22),corner_radius=15,show="*")
        self.senha_cadastro_entry.grid(row=3,column=0,pady=5,padx=10)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro,width=300,
                                                 placeholder_text="Confirme senha de Usuário",
                                                 font=("Century Gothic bold",22),corner_radius=15,show="*")
        self.confirma_senha_entry.grid(row=4,column=0,pady=5,padx=10)

        # Checkbox funcional para mostrar/ocultar senha cadastro
        self.ver_senha_var_cadastro = BooleanVar()
        self.ver_senha_cadastro = ctk.CTkCheckBox(self.frame_cadastro,text="Click para ver senha",
                                                  variable=self.ver_senha_var_cadastro,
                                                  command=self.toggle_senha_cadastro,font=("Century Gothic bold",12))
        self.ver_senha_cadastro.grid(row=5,column=0,pady=5)

        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro,width=300,fg_color="green",
                                                hover_color="#050",text="Cadastrar-se".upper(),
                                                font=("Century Gothic bold",16),
                                                corner_radius=15,command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6,column=0,pady=10,padx=10)

        self.btn_login_back = ctk.CTkButton(self.frame_cadastro,width=300,
                                            text="Voltar a tela Login".upper(),
                                            font=("Century Gothic bold",16),
                                            corner_radius=15,fg_color="#444",hover_color="#333",
                                            command=self.tela_login_)
        self.btn_login_back.grid(row=7,column=0,pady=5)

    # Mostrar/ocultar senha cadastro
    def toggle_senha_cadastro(self):
        if self.ver_senha_var_cadastro.get():
            self.senha_cadastro_entry.configure(show="")
            self.confirma_senha_entry.configure(show="")
        else:
            self.senha_cadastro_entry.configure(show="*")
            self.confirma_senha_entry.configure(show="*")
    
    # Limpar campos cadastro
    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0,END)
        self.email_cadastro_entry.delete(0,END)
        self.senha_cadastro_entry.delete(0,END)
        self.confirma_senha_entry.delete(0,END)
        
    # Limpar campos login
    def limpa_entry_login(self):
        self.username_login_entry.delete(0,END)
        self.senha_login_entry.delete(0,END)
    

# Inicialização da aplicação
if __name__=="__main__":
    app = App()
    app.mainloop()
