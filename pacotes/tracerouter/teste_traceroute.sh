#!/usr/bin/env bash

set -u

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGETS_FILE="$ROOT_DIR/alvos.txt"
OUTPUT_DIR="$ROOT_DIR/resultados"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
SUMMARY_FILE="$OUTPUT_DIR/resumo_$TIMESTAMP.txt"
PER_TARGET_TIMEOUT="${PER_TARGET_TIMEOUT:-20}"

mkdir -p "$OUTPUT_DIR"

detect_command() {
    if command -v traceroute >/dev/null 2>&1; then
        echo "traceroute"
        return
    fi

    if command -v tracepath >/dev/null 2>&1; then
        echo "tracepath"
        return
    fi

    echo ""
}

run_with_timeout() {
    if command -v timeout >/dev/null 2>&1; then
        timeout "${PER_TARGET_TIMEOUT}s" "$@"
        return
    fi

    "$@"
}

load_targets() {
    if [ "$#" -gt 0 ]; then
        printf '%s\n' "$@"
        return
    fi

    if [ ! -f "$TARGETS_FILE" ]; then
        echo "Arquivo de alvos nao encontrado: $TARGETS_FILE" >&2
        exit 1
    fi

    grep -v '^[[:space:]]*#' "$TARGETS_FILE" | sed '/^[[:space:]]*$/d'
}

run_test() {
    local cmd="$1"
    local target="$2"
    local safe_target
    local output_file

    safe_target="$(printf '%s' "$target" | tr '/ :' '___')"
    output_file="$OUTPUT_DIR/${TIMESTAMP}_${safe_target}.txt"

    {
        echo "Teste de rota"
        echo "Data: $(date)"
        echo "Alvo: $target"
        echo "Comando: $cmd"
        echo
    } > "$output_file"

    if [ "$cmd" = "traceroute" ]; then
        run_with_timeout traceroute -n -w 2 -m 15 "$target" >> "$output_file" 2>&1
    else
        run_with_timeout tracepath -m 15 "$target" >> "$output_file" 2>&1
    fi

    local status=$?

    if [ "$status" -eq 0 ]; then
        echo "[OK] $target -> $output_file" | tee -a "$SUMMARY_FILE"
    elif [ "$status" -eq 124 ]; then
        echo "[TEMPO ESGOTADO] $target -> $output_file" | tee -a "$SUMMARY_FILE"
    else
        echo "[FALHA:$status] $target -> $output_file" | tee -a "$SUMMARY_FILE"
    fi
}

main() {
    local cmd
    cmd="$(detect_command)"

    if [ -z "$cmd" ]; then
        echo "Nem traceroute nem tracepath estao instalados." >&2
        echo "Ubuntu/Debian: sudo apt install traceroute" >&2
        echo "Fedora: sudo dnf install traceroute" >&2
        echo "Arch: sudo pacman -S traceroute" >&2
        exit 1
    fi

    {
        echo "Resumo dos testes"
        echo "Data: $(date)"
        echo "Ferramenta: $cmd"
        echo "Timeout por alvo: ${PER_TARGET_TIMEOUT}s"
        echo
    } > "$SUMMARY_FILE"

    while IFS= read -r target; do
        run_test "$cmd" "$target"
    done < <(load_targets "$@")

    echo
    echo "Resumo salvo em: $SUMMARY_FILE"
}

main "$@"