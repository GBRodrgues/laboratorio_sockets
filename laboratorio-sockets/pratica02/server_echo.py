import socket
from datetime import datetime
HOST = "127.0.0.1"
PORTA = 5001
def processar_comando(linha: str) -> str:
    linha = linha.strip()
    
    if linha == "PING":
        return "PONG"
    if linha == "HORA":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if linha.startswith("MAIUSCULA "):
        texto = linha[len("MAIUSCULA "):]
        return texto.upper()
    if linha.startswith("TAMANHO "):
        texto = linha[len("TAMANHO "):]
        return str(len(texto))
    
    if linha.startswith("MINUSCULA "):
        texto = linha[len("MINUSCULA "):]
        return texto.lower()
    
    if linha.startswith("REVERSO "):
        texto = linha[len("REVERSO "):]
        return texto[::-1]
    
    if linha.startswith("SOMA "):
        try:
            numeros_str = linha[len("SOMA "):].split()
            numeros = [float(num) for num in numeros_str]
            return str(sum(numeros))
        except ValueError:
            return "ERRO: argumentos inválidos para SOMA"

    if linha == "SAIR":
        return "Encerrando conexão."
    
    return "ERRO: comando desconhecido"
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(1)
    print(f"Servidor de comandos em {HOST}:{PORTA}")
    
    conexao, endereco = servidor.accept()
    with conexao:
        
        print(f"Cliente conectado: {endereco}")
        while True:
            dados = conexao.recv(1024)
            if not dados:
                print("Cliente encerrou a conexão.")
                break
            
            comando = dados.decode("utf-8")
            print("Comando recebido:", comando.strip())
            
            resposta = processar_comando(comando)
            conexao.sendall((resposta + "\n").encode("utf-8"))
            
            if comando.strip() == "SAIR":
                break