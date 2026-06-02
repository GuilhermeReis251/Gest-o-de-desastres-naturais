
import os
import sys

from modules.logger import Logger
from modules.data_loader import carregar_dados_csv, baixar_dados_usgs, gerar_dataset_exemplo
from modules.estruturas import Pilha, Fila, ListaLigada
from modules.ordenacao import merge_sort
from modules.menu import exibir_menu_principal

log = Logger("logs/execucao.log")


def main():
    log.info("=== Sistema de Monitoramento de Desastres Naturais iniciado ===")

    print("\n" + "═" * 64)
    print("  🌍  MONITORAMENTO DE DESASTRES NATURAIS E GESTÃO DE RISCOS")
    print("       Dados: USGS Earthquake Hazards Program")
    print("       Estruturas de Dados — Global Solution 2025")
    print("═" * 64)

    print("\n[1/4] Carregando base de dados de terremotos (USGS)...")
    caminho_csv = "data/terremotos.csv"

    if not os.path.exists(caminho_csv):
        print("     Arquivo local não encontrado. Tentando API da USGS...")
        try:
            baixar_dados_usgs(caminho_csv)
        except Exception as e:
            log.erro(f"Falha ao baixar dados USGS: {e}")
            print("     ⚠ Sem conexão. Usando dataset de exemplo.")
            gerar_dataset_exemplo(caminho_csv)

    try:
        eventos = carregar_dados_csv(caminho_csv)
        log.info(f"Base carregada: {len(eventos)} eventos")
        print(f"     ✔ {len(eventos)} eventos carregados com sucesso.")
    except Exception as e:
        log.erro(f"Erro ao carregar CSV: {e}")
        print(f"     ✘ Erro: {e}")
        sys.exit(1)

    print("\n[2/4] Inicializando estruturas de dados...")

    pilha_alertas     = Pilha()
    fila_triagem      = Fila()
    lista_regioes     = ListaLigada()

    for evento in eventos[:50]:
        fila_triagem.enfileirar(evento)

    for regiao in [
        {"nome": "Anel de Fogo — Pacífico", "ativa": True},
        {"nome": "Falha de San Andreas",     "ativa": True},
        {"nome": "Placa Euroasiática",        "ativa": True},
        {"nome": "Zona Sísmica Brasil",       "ativa": True},
        {"nome": "Mar Mediterrâneo",          "ativa": True},
    ]:
        lista_regioes.inserir(regiao)

    log.info("Estruturas inicializadas: Pilha, Fila, Lista Ligada")
    print("     ✔ Pilha de alertas criada.")
    print("     ✔ Fila de triagem criada.")
    print("     ✔ Lista ligada de regiões criada.")

    print("\n[3/4] Ordenando eventos por magnitude (Merge Sort)...")
    try:
        eventos_ordenados = merge_sort(eventos, chave="mag", reverso=True)
        log.info(f"Merge Sort concluído: {len(eventos_ordenados)} eventos")
        print(f"     ✔ {len(eventos_ordenados)} eventos ordenados por magnitude.")
    except Exception as e:
        log.erro(f"Erro na ordenação: {e}")
        eventos_ordenados = eventos

    print("\n[4/4] Sistema pronto!\n")
    log.info("Entrando no menu principal")

    exibir_menu_principal(
        eventos_originais=eventos,
        eventos_ordenados=eventos_ordenados,
        pilha_alertas=pilha_alertas,
        fila_triagem=fila_triagem,
        lista_regioes=lista_regioes,
        log=log,
    )

    log.info("=== Sistema encerrado normalmente ===")
    print("\n🌍 Sistema encerrado. Log salvo em logs/execucao.log\n")


if __name__ == "__main__":
    main()
