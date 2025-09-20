# Cliente.py
import socket
import threading
import json

class Cliente:
    def __init__(self, nome, host="localhost", port=5000):
        self.nome = nome
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.on_message = None  # callback para interface

        self.running = True
        self._recv_buffer = ""

        # Envia mensagem de conexão (JSON framed)
        self._send_json({"acao": "conectar", "usuario": self.nome})

        # Inicia thread para ouvir servidor
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # Solicita histórico do chat geral
        self.pedir_historico()

    def _send_json(self, obj):
        try:
            raw = json.dumps(obj) + "\n"
            self.sock.send(raw.encode())
        except Exception as e:
            print("❌ Erro ao enviar JSON:", e)

    # envia mensagem para o chat geral
    def enviar_mensagem(self, mensagem):
        data = {
            "acao": "enviar",
            "remetente": self.nome,
            "mensagem": mensagem
        }
        self._send_json(data)

    # solicita histórico de mensagens do chat geral
    def pedir_historico(self):
        data = {
            "acao": "historico",
            "remetente": self.nome
        }
        self._send_json(data)

    # recebe mensagens do servidor (mensagens novas ou histórico)
    def receive_messages(self):
        while self.running:
            try:
                chunk = self.sock.recv(4096).decode()
                if not chunk:
                    break
                self._recv_buffer += chunk
                while "\n" in self._recv_buffer:
                    line, self._recv_buffer = self._recv_buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
                        if self.on_message:
                            self.on_message(msg)
                    except json.JSONDecodeError:
                        print("⚠️ Mensagem recebida inválida:", line)
            except Exception as e:
                if self.running:
                    print("❌ Erro ao receber mensagem:", e)
                break

    # fechar conexão
    def close(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass


if __name__ == "__main__":
    nome = input("Digite seu nome: ")
    cliente = Cliente(nome)

    try:
        while True:
            msg = input("Digite mensagem (ou 'sair' para encerrar): ")
            if msg.lower() == "sair":
                cliente.close()
                break
            cliente.enviar_mensagem(msg)
    except KeyboardInterrupt:
        cliente.close()
