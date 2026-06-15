# Documentação do Protocolo - Jogo de Sorteio

Este documento detalha o protocolo de aplicação para o jogo de sorteio cliente-servidor, implementado utilizando sockets raw (TCP/IP).

## 1. Visão Geral do Protocolo

- **Arquitetura**: Cliente-Servidor.
- **Camada de Transporte**: TCP (Transmission Control Protocol).
- **Codificação de Dados**: UTF-8. Todas as mensagens trafegadas são strings de texto codificadas em UTF-8.
- **Modelo de Comunicação**: O servidor suporta múltiplos clientes simultâneos em threads independentes. Os clientes comunicam-se enviando texto simples.

## 2. Fluxo de Comunicação e Mensagens

O protocolo funciona baseado no seguinte ciclo de vida:

### Fase 1: Conexão e Identificação
1. O cliente inicia uma conexão TCP com o servidor (IP fornecido ou `127.0.0.1`, porta padrão `5004`).
2. O servidor aceita a conexão e envia a mensagem: `"Digite seu nome: "`.
3. O cliente envia uma string em texto plano contendo seu nome.
4. O servidor verifica se o nome já está em uso:
   - Se estiver: O servidor envia `"Nome já em uso. Digite outro nome: "` e aguarda nova entrada.
   - Se não estiver (ou o cliente enviar vazio, assumindo um fallback): O servidor registra o cliente e transmite o nome para os logs.
5. O servidor envia as regras do jogo: `"Tente adivinhar um dos 5 números sorteados entre 1 e 100! (ou /SAIR para sair)\n"`.

### Fase 2: Jogo (Troca de Mensagens)
O servidor aguarda passivamente as tentativas dos clientes.
- **Cliente**: Envia um número inteiro em formato texto (ex: `"42"`).
- **Servidor**: 
  - Lê a entrada.
  - Verifica se a entrada é um comando especial (ex: `" /SAIR"`).
  - Tenta converter o dado para um inteiro.
  - Compara com os números sorteados em memória e retorna ao cliente:
    - Se acertou: `"Parabéns! Você acertou, X é um dos números sorteados!\n"`
    - Se errou: `"Você errou! X não foi sorteado. Tente novamente.\n"`

### Fase 3: Desconexão e Tratamento de Erros
- **Comandos Desconhecidos**: Se a entrada começar com `/` e não for `/SAIR`, o servidor avisa: `"Comando desconhecido: [comando]. Comando válido: /SAIR\n"`.
- **Entradas Inválidas (Não-numéricas)**: Se a conversão para inteiro falhar (ex: `"abc"`), o servidor retorna: `"Entrada inválida. Por favor, envie um número inteiro válido ou o comando /SAIR.\n"`.
- **Encerramento da Conexão**:
  - O cliente pode enviar o comando `/SAIR`.
  - O servidor então fecha o socket para aquele cliente e remove o registro, liberando o nome de usuário.
  - Uma desconexão abrupta do socket também é tratada (usando tratamento de exceções `OSError` e o retorno vazio do `.recv()`).

## 3. Limitações

1. **Protocolo Textual Simples**: Por usar texto simples (`UTF-8`) puro, não há distinção formal entre "metadados/cabeçalhos" e "payload" da aplicação. Isso dificulta extensões futuras (como envio de imagens ou estados mais complexos do jogo).
2. **Ausência de Criptografia**: As mensagens transitam em texto legível. Na rede local, qualquer sniffer (como o Wireshark) pode ler o tráfego e ver as tentativas dos jogadores.
3. **Bloqueios e Condições de Corrida**: O uso intenso de locks em estruturas mutáveis (como o dicionário de clientes) para gerenciar o estado compartilhado entre threads pode gerar gargalos se houver um número massivo de conexões concorrentes.
4. **Acoplamento Cliente-Servidor**: O cliente está muito atrelado às mensagens textuais formatadas pelo servidor. Não existe um código de erro/status definido; a interface (console) imprime exatamente o que o servidor enviar.

## 4. Possíveis Melhorias

1. **Estruturação de Dados com JSON**: Mudar a troca de dados de "texto puro" para um modelo estruturado como JSON (ex: `{"tipo": "chute", "valor": 42}`). Isso desacoplaria a lógica da exibição final e permitiria evoluções robustas no protocolo.
2. **Criptografia (TLS/SSL)**: Emvolver o socket em um contexto seguro usando a biblioteca `ssl` nativa do Python, para proteger a comunicação.
3. **IO Assíncrono (asyncio)**: Para suportar milhares de conexões, substituir o modelo Multi-Thread por Multiplexação/I/O não-bloqueante (utilizando `asyncio` nativo, sem frameworks externos).
4. **Autenticação Simples**: Exigir não apenas o nome, mas uma senha (ou um token) para evitar roubo de nomes em sessões persistentes.
