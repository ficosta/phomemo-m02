"""
Script de Impressão Interativa em Sequência com PAUSA para Corte
Imprime tiras pedagógicas de verbos na Phomemo M02 com avanço e pausa entre cada uma.
"""

import sys
import time
import argparse
from pathlib import Path
from phomemo import PhomemoM02
from generate_verb_strip import VERBS_DATA, generate_verb_strip

DEFAULT_ORDER = [
    "ser", "estar", "haber", "tener", "hacer",
    "poder", "decir", "ir", "ver", "dar",
    "saber", "querer", "llegar", "pasar", "poner",
    "hablar", "comer", "vivir"
]

def main():
    parser = argparse.ArgumentParser(description="Imprime tiras de verbos em sequência com pausa para corte")
    parser.add_argument("verbs", nargs="*", default=[], help="Lista de verbos específicos (ex: ser estar tener). Deixe vazio para escolher.")
    parser.add_argument("--all", action="store_true", help="Imprimir todos os 18 verbos disponíveis")
    parser.add_argument("--top5", action="store_true", help="Imprimir os 5 primeiros mais comuns (ser, estar, haber, tener, hacer)")
    parser.add_argument("--port", default=None, help="Porta COM da impressora (padrão: auto-detectada)")
    parser.add_argument("--auto-delay", type=int, default=None, help="Segundos de pausa automática em vez de esperar Enter")
    
    args = parser.parse_args()

    # Seleciona os verbos
    if args.verbs:
        selected_verbs = [v.lower() for v in args.verbs if v.lower() in VERBS_DATA]
    elif args.top5:
        selected_verbs = ["ser", "estar", "haber", "tener", "hacer"]
    elif args.all:
        selected_verbs = DEFAULT_ORDER
    else:
        # Default de teste amigável: os 3 regulares ou os 5 primeiros
        selected_verbs = ["hablar", "comer", "vivir"]

    if not selected_verbs:
        print("Nenhum verbo válido selecionado.")
        print("Disponíveis:", ", ".join(VERBS_DATA.keys()))
        return

    print("=" * 60)
    print(" 🇪🇸 IMPRESSÃO DE TIRAS DE VERBOS - PHOMEMO M02")
    print("=" * 60)
    print(f"Total de tiras para imprimir: {len(selected_verbs)}")
    print(f"Sequência: {', '.join([v.upper() for v in selected_verbs])}\n")

    tiras_dir = Path("tiras")
    tiras_dir.mkdir(exist_ok=True)

    print("Conectando à impressora...")
    with PhomemoM02(port=args.port) as printer:
        print(f"Conectado com sucesso na {printer.port}!\n")

        for idx, verb_key in enumerate(selected_verbs, 1):
            verb_info = VERBS_DATA[verb_key]
            print(f"[{idx}/{len(selected_verbs)}] Preparando tira: {verb_info['verb']} ({verb_info['pt']})...")
            
            # Gera imagem (ou carrega se já existir)
            img_path = tiras_dir / f"tira_{verb_key}.png"
            if not img_path.exists():
                img = generate_verb_strip(verb_key)
                img.save(img_path)
            else:
                img = Image.open(img_path)

            print(f" -> Enviando impressão...")
            printer.print_image(img)
            print(f" -> [OK] Tira '{verb_info['verb']}' impressa!")

            # Se for a última tira, não precisa pausar
            if idx == len(selected_verbs):
                print("\n🎉 Todas as tiras selecionadas foram impressas!")
                break

            # Pausa para o corte manual
            print("-" * 50)
            print(f"✂ CORTE A TIRA '{verb_info['verb']}' na linha pontilhada.")
            
            if args.auto_delay:
                print(f"Aguardando {args.auto_delay} segundos para o próximo verbo...")
                time.sleep(args.auto_delay)
            else:
                try:
                    resp = input(f"Pressione [ENTER] para imprimir o próximo ({selected_verbs[idx].upper()}) ou digite 'q' para pausar: ")
                    if resp.strip().lower() == 'q':
                        print("\nImpressão pausada pelo usuário. Até a próxima!")
                        break
                except KeyboardInterrupt:
                    print("\nImpressão interrompida.")
                    break
            print("-" * 50 + "\n")

if __name__ == "__main__":
    main()
