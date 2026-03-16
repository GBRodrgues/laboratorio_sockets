# Teste de Traceroute

Este material cria um teste simples de rota para a disciplina de redes no Linux.

## Arquivos

- `teste_traceroute.sh`: executa os testes e salva os resultados.
- `alvos.txt`: lista de destinos padrao.
- `resultados/`: pasta criada automaticamente para armazenar as saidas.

## Como usar

1. Dar permissao de execucao:

```bash
chmod +x teste_traceroute.sh
```

2. Executar com a lista padrao:

```bash
./teste_traceroute.sh
```

3. Executar com alvos especificos:

```bash
./teste_traceroute.sh 8.8.8.8 google.com 200.130.1.35
```

## Dependencias

O script usa `traceroute` quando disponivel. Se nao existir, usa `tracepath` automaticamente.

Cada alvo tem timeout padrao de 20 segundos para evitar que a coleta fique presa. Se quiser alterar:

```bash
PER_TARGET_TIMEOUT=10 ./teste_traceroute.sh
```

Para instalar `traceroute`:

```bash
sudo apt install traceroute
```

## Saida

Cada alvo gera um arquivo proprio em `resultados/`, e o script tambem cria um resumo com data e status de cada teste.