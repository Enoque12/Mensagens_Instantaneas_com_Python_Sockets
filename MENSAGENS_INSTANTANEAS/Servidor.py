"""
import socket

HOST = '127.0.0.1'   # localhost
PORT = 5000          # porta qualquer acima de 1024

# cria o socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Servidor iniciado em {HOST}:{PORT}, aguardando conexão...")

conn, addr = server_socket.accept()
print(f"Conectado por {addr}")

while True:
    # recebe mensagem do cliente
    data = conn.recv(1024).decode()
    if not data or data.lower() == "sair":
        print("Cliente desconectou.")
        break
    print("Cliente:", data)

    # envia resposta
    resposta = input("Servidor > ")
    conn.sendall(resposta.encode())
    if resposta.lower() == "sair":
        break

conn.close()
server_socket.close()
"""
"""
import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

# função para atender cada cliente
def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] Cliente {addr} conectado.")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data or data.lower() == "sair":
                print(f"[DESCONECTADO] Cliente {addr}")
                break
            print(f"Cliente {addr}: {data}")

            resposta = input("Servidor > ")
            conn.sendall(resposta.encode())
            if resposta.lower() == "sair":
                break
        except:
            print(f"[ERRO] Conexão perdida com {addr}")
            break
    conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor rodando em {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ATIVOS] Clientes conectados: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
"""

import socket
import threading

HOST = '192.168.104.7'
PORT = 12345

clientes = []

def handle_client(conn, nome):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            mensagem = f"{data.decode()}"
            print(mensagem)

            # envia a mensagem para o outro cliente
            for cliente in clientes:
                if cliente != conn:
                    cliente.sendall(mensagem.encode())
        except:
            break

    print(f"{nome} desconectou.")
    clientes.remove(conn)
    conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)  # limite: 2 clientes
    print("Servidor de chat aguardando 2 clientes...")

    nomes = ["Cliente A", "Cliente B"]

    while len(clientes) < 2:
        conn, addr = server_socket.accept()
        clientes.append(conn)
        nome = nomes[len(clientes) - 1]
        print(f"{nome} conectado de {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, nome))
        thread.start()

if __name__ == "__main__":
    start_server()
