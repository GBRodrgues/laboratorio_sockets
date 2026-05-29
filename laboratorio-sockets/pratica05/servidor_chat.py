import socket
import threading

HOST = "0.0.0.0"
PORTA = 5004

clientes = {}
lock = threading.Lock()


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
        entrada = f"[SERVIDOR] {nome} entrou no chat.\n"
        print(entrada.strip())

        #Mensagem de boas vindas com instrucoes de uso
        boas_vindas="""
        Bem-vindo ao chat!
        Digite /LISTAR para ver os usuários.
        Digite /SAIR para sair.
        Digite /MSG [usuario]:[mensagem] para enviar uma mensagem privada.
        Digite uma mensagem normal para enviar uma mensagem para todos os usuários.
        """       
        conexao.sendall(boas_vindas.encode("utf-8"))

        enviar_para_todos(entrada, remetente=conexao)
        while True:
            dados = conexao.recv(1024)
            if not dados:
                break
            texto = dados.decode("utf-8").strip()
            if texto.upper() == "/SAIR":
                break

            #listando usuários
            if texto.upper() == "/LISTAR":
                with lock:
                    lista = "Usuários online:\n"
                    for n in clientes.values():
                        lista += f"- {n}\n"
                    conexao.sendall(lista.encode("utf-8"))
                continue
            
            #mensagem privada
            if texto.startswith("/MSG"):
                texto = texto[4:].strip()
                if ":" in texto:
                    destinatario, mensagem = texto.split(":", 1)
                    with lock:
                        for sock, n in clientes.items():
                            if n == destinatario:
                                sock.sendall(f"[{nome} -> privado] {mensagem}\n".encode("utf-8"))
                continue


            #registro das conversas em um arquivo
            with open("conversas.txt", "a") as arquivo:
                arquivo.write(f"[{nome}] {texto}\n")
            
            mensagem = f"[{nome}] {texto}\n"
            print(mensagem.strip())
            enviar_para_todos(mensagem, remetente=conexao)

    finally:
        with lock:
            if conexao in clientes:
                del clientes[conexao]
        conexao.close()
        saida = f"[SERVIDOR] {nome} saiu do chat.\n"
        print(saida.strip())
        enviar_para_todos(saida)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(10)
    print(f"Servidor de chat em {HOST}:{PORTA}")
    while True:
        conexao, endereco = servidor.accept()
        print(conexao)
        threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()