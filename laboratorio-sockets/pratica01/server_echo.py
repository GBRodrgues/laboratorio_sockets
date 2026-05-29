import socket

HOST = "127.0.0.1"
PORTA = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(1)
    print(f"Servidor TCP aguardando conexão em {HOST}:{PORTA}...")
    conexao, endereco = servidor.accept()

    with conexao:
        print(f"Cliente conectado: {endereco}")
        dados = conexao.recv(1024)
        print(f"Recebido em bytes: {dados}")
        mensagem = dados.decode("utf-8")
        print(f"Recebido como texto: {mensagem}")
        conexao.sendall(dados)
        print("Mensagem devolvida ao cliente.")