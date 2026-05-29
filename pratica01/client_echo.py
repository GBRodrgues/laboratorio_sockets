import socket


HOST = ""
PORTA = 5000

mensagem = input("Digite uma mensagem para enviar ao servidor: ")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORTA))
    cliente.sendall(mensagem.encode("utf-8"))
    resposta = cliente.recv(1024)
    print("Resposta do servidor:", resposta.decode("utf-8"))