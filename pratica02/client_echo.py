import socket
HOST = "127.0.0.1"
PORTA = 5001
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORTA))
    print("Conectado ao servidor. Comandos: PING, HORA, MAIUSCULA texto, MINUSCULA texto, REVERSO texto, SOMA a b, TAMANHO texto, SAIR")
    
    while True:
        comando = input("> ")
        cliente.sendall(comando.encode("utf-8"))
        resposta = cliente.recv(1024).decode("utf-8").strip()
        print("Servidor:", resposta)
        if comando.strip() == "SAIR":
            break