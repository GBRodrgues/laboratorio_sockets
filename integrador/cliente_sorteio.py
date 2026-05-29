import socket
import threading
import sys

HOST = "127.0.0.1"
PORTA = 5004

def receber_mensagens(conexao):
    while True:
        try:
            mensagem = conexao.recv(1024).decode("utf-8")
            if not mensagem:
                print("\n[Conexão encerrada pelo servidor]")
                break
            # O servidor já envia com a quebra de linha (\n)
            print(mensagem, end="")
        except OSError:
            break

def principal():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORTA))
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor.")
            return

        thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
        thread_receber.daemon = True
        thread_receber.start()

        try:
            while True:
                mensagem = input()
                if not mensagem:
                    continue
                cliente.sendall(mensagem.encode("utf-8"))
                if mensagem.upper() == "/SAIR":
                    break
        except KeyboardInterrupt:
            print("\nSaindo...")
            cliente.sendall("/SAIR".encode("utf-8"))

if __name__ == "__main__":
    principal()
