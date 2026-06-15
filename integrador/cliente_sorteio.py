import socket
import threading
import sys
import argparse

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
    parser = argparse.ArgumentParser(description="Cliente para o Jogo de Sorteio")
    parser.add_argument("--host", default="127.0.0.1", help="Endereço IP do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=5004, help="Porta do servidor (padrão: 5004)")
    args = parser.parse_args()

    host = args.host
    porta = args.porta

    print(f"Conectando ao servidor em {host}:{porta}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((host, porta))
        except ConnectionRefusedError:
            print(f"Não foi possível conectar ao servidor em {host}:{porta}.")
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
