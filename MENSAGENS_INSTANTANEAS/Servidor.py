# Servidor.py
import socket
import threading
import mysql.connector
import json
from datetime import datetime

class Servidor:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.clientes = {}          # mapa usuario -> conn
        self.lock = threading.Lock()

        # Conexão com MySQL (ajusta credenciais)
        self.conn_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chat_app"
        )
        self.cursor = self.conn_db.cursor()
        self.criar_tabela()

        # Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"✅ Servidor rodando em {self.host}:{self.port} (chat geral)")

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensagens (
                id INT AUTO_INCREMENT PRIMARY KEY,
                remetente VARCHAR(255),
                mensagem TEXT,
                timetamps TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn_db.commit()

    def salvar_mensagem(self, remetente, mensagem):
        sql = "INSERT INTO mensagens (remetente, mensagem) VALUES (%s, %s)"
        self.cursor.execute(sql, (remetente, mensagem))
        self.conn_db.commit()

    def obter_historico(self):
        sql = "SELECT remetente, mensagem, timetamps FROM mensagens ORDER BY timetamps ASC"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        # retorna lista de dicts para facilitar consumo
        historico = [
            {"remetente": r[0], "mensagem": r[1], "timestamp": str(r[2])}
            for r in rows
        ]
        return historico

    def _send_json(self, conn, obj):
        try:
            raw = json.dumps(obj, default=str) + "\n"
            conn.send(raw.encode())
        except Exception:
            # remova cliente se não responder
            with self.lock:
                to_remove = None
                for user, c in list(self.clientes.items()):
                    if c is conn:
                        to_remove = user
                        break
                if to_remove:
                    del self.clientes[to_remove]
                    print(f"⚠️ Removido cliente {to_remove} por erro de envio")

    def broadcast(self, remetente, mensagem):
        data = {"acao": "mensagem", "remetente": remetente, "mensagem": mensagem, "timestamp": str(datetime.now())}
        with self.lock:
            for nome, conn in list(self.clientes.items()):
                if nome == remetente:
                    continue  # opcional: não reenvia ao dono
                self._send_json(conn, data)

    def handle_client(self, conn, addr):
        buffer = ""
        usuario = None
        try:
            while True:
                chunk = conn.recv(4096).decode()
                if not chunk:
                    break
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
                    except json.JSONDecodeError as e:
                        print("JSON Decode Error:", e, "line:", line)
                        continue

                    acao = msg.get("acao")
                    if acao == "conectar":
                        usuario = msg.get("usuario")
                        if not usuario:
                            continue
                        with self.lock:
                            self.clientes[usuario] = conn
                        print(f"🔗 {usuario} conectado.")
                    elif acao == "historico":
                        hist = self.obter_historico()
                        resp = {"acao": "historico", "data": hist}
                        self._send_json(conn, resp)
                    elif acao == "enviar":
                        remetente = msg.get("remetente")
                        texto = msg.get("mensagem")
                        if remetente and texto is not None:
                            self.salvar_mensagem(remetente, texto)
                            self.broadcast(remetente, texto)
                    else:
                        print("⚠️ Ação desconhecida recebida:", acao)
        except (ConnectionResetError, ConnectionAbortedError):
            print(f"🔌 {usuario if usuario else addr} se desconectou.")
        except Exception as e:
            print("❌ Erro no handle_client:", e)
        finally:
            conn.close()
            if usuario:
                with self.lock:
                    if usuario in self.clientes and self.clientes[usuario] is conn:
                        del self.clientes[usuario]
                print(f"🛑 Conexão com {usuario} encerrada.")

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            # não faz recv() aqui — a thread fará o handshake
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    servidor = Servidor()
    servidor.run()
