import socket
import threading
import random

HOST = "0.0.0.0"
PORTA = 5004

clientes = {}
lock = threading.Lock()

QUANTIDADE_NUMEROS = 5
numeros_sorteados = random.sample(range(1, 101), QUANTIDADE_NUMEROS)


def enviar_para_todos(mensagem, remetente=None):
    with lock:
        for cliente in clientes:
            if cliente != remetente:
                try:
                    cliente.sendall(mensagem.encode("utf-8"))
                except OSError:
                    pass


def atender_cliente(conexao, endereco):
    nome = "Desconhecido"
    try:

        conexao.sendall("Digite seu nome: ".encode("utf-8"))
        
        nome = conexao.recv(1024).decode("utf-8").strip()
        
        #verificação de nomes repetidos
        while True:
            with lock:
                em_uso = nome in clientes.values()
            if not em_uso:
                break
            conexao.sendall("Nome já em uso. Digite outro nome: ".encode("utf-8"))
            nome = conexao.recv(1024).decode("utf-8").strip()
        
        if not nome:
            nome = f"cliente-{endereco[1]}"
            
        with lock:
            clientes[conexao] = nome
        entrada = f"[SERVIDOR] {nome} entrou no jogo de sorteio.\n"
        print(entrada.strip())
        
        conexao.sendall(f"Tente adivinhar um dos {QUANTIDADE_NUMEROS} números sorteados entre 1 e 100! (ou /SAIR para sair)\n".encode("utf-8"))

        while True:
            dados = conexao.recv(1024)
            if not dados:
                break
            texto = dados.decode("utf-8").strip()
            if texto.upper() == "/SAIR":
                break

            if texto.startswith("/"):
                conexao.sendall(f"Comando desconhecido: {texto}. Comando válido: /SAIR\n".encode("utf-8"))
                print(f"[{nome}] tentou usar comando desconhecido: {texto}")
                continue

            try:
                chute = int(texto)
                if chute in numeros_sorteados:
                    conexao.sendall(f"Parabéns! Você acertou, {chute} é um dos números sorteados!\n".encode("utf-8"))
                else:
                    conexao.sendall(f"Você errou! {chute} não foi sorteado. Tente novamente.\n".encode("utf-8"))
                
                print(f"[{nome}] chutou o número {chute}")
            except ValueError:
                conexao.sendall("Entrada inválida. Por favor, envie um número inteiro válido ou o comando /SAIR.\n".encode("utf-8"))
                print(f"[{nome}] enviou entrada inválida: {texto}")

    finally:
        with lock:
            if conexao in clientes:
                del clientes[conexao]
        conexao.close()
        saida = f"[SERVIDOR] {nome} saiu do jogo.\n"
        print(saida.strip())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(10)
    print(f"Servidor de sorteio em {HOST}:{PORTA}")
    while True:
        conexao, endereco = servidor.accept()
        print(conexao)
        threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()