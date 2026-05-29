from datetime import datetime
import socket

HOST = "0.0.0.0"
PORTA = 5050


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)

    print(f"Acesse no navegador: http://127.0.0.1:{PORTA}")
    
    while True:
        conexao, endereco = servidor.accept()
        with conexao:
            requisicao = conexao.recv(2048).decode("utf-8", errors="replace") 
            linha_inicial = requisicao.splitlines()[0]
            partes = linha_inicial.split()
            metodo = partes[0]
            caminho = partes[1]
            if caminho == "/":
                corpo = """ <h1>Servidor HTTP mínimo com sockets</h1>
                            <h2>Disciplina de Redes de Computadores</h2>
                            <h3>Gabriel Cezar Rodrigues e Antônio Carlos</h3>
                            <p>Esta página foi enviada por um programa Python usando sockets TCP.</p>"""
            elif caminho == "/status":
                corpo = """<h1>Status: servidor ativo</h1>"""
            elif caminho == "/sobre":
                corpo = f"""
                <h1>Sobre o servidor</h1>
                <p>Este servidor foi criado usando sockets TCP.</p>
                <p>Feito por Gabriel Cezar Rodrigues e Antônio Carlos</p>
                <p>Hora local do servidor: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>"""
            else:
                corpo = """<h1>404 - Página não encontrada</h1>"""
            
            html = f"""<!DOCTYPE html>
            <html lang="pt-br">
            <head><meta charset="utf-8"><title>Servidor Python</title></head>
            <body>
            {corpo}
            </body>
            </html>
            """

            resposta = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html.encode('utf-8'))}\r\n"
                "Connection: close\r\n"
                "\r\n"
                + html
            )
            print("=" * 60)
            print(f"Requisição de {endereco}:")
            print(f"Método: {metodo}")
            print(f"Caminho: {caminho}")
            conexao.sendall(resposta.encode("utf-8"))