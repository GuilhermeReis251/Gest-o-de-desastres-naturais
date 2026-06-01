"""
modules/menu.py
===============
Interface de terminal interativa do sistema de desastres.
"""

from modules.busca import (
    busca_binaria_magnitude, busca_binaria_range,
    busca_linear_local, busca_linear_nivel,
    busca_linear_periodo, busca_linear_profundidade
)
from modules.ordenacao import merge_sort, quick_sort, bubble_sort
from modules.relatorio import gerar_relatorio, exibir_tabela, exibir_mapa_risco


def exibir_menu_principal(eventos_originais, eventos_ordenados,
                          pilha_alertas, fila_triagem, lista_regioes, log):
    """Loop principal do menu."""
    eventos_atuais = eventos_ordenados

    while True:
        _cabecalho()
        opcao = input("  Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                _visualizar(eventos_atuais)
                log.info("Tabela de eventos exibida")

            elif opcao == "2":
                _busca(eventos_originais, eventos_atuais, pilha_alertas, log)

            elif opcao == "3":
                eventos_atuais = _ordenacao(eventos_originais, log)

            elif opcao == "4":
                _estruturas(eventos_atuais, pilha_alertas, fila_triagem, lista_regioes, log)

            elif opcao == "5":
                gerar_relatorio(eventos_originais, pilha_alertas, fila_triagem, lista_regioes)
                log.info("Relatório geral gerado")

            elif opcao == "6":
                exibir_mapa_risco(eventos_originais)
                log.info("Mapa de risco exibido")

            elif opcao == "7":
                _triar_fila(fila_triagem, pilha_alertas, log)

            elif opcao == "8":
                _painel_risco(eventos_originais)
                log.info("Painel de risco exibido")

            elif opcao == "0":
                break

            else:
                print("\n  ⚠ Opção inválida.\n")

        except KeyboardInterrupt:
            print("\n\n  Operação cancelada.\n")
        except Exception as e:
            log.erro(f"Erro no menu (opção {opcao}): {e}")
            print(f"\n  ✘ Erro: {e}\n")


def _cabecalho():
    print("\n" + "─" * 64)
    print("  🌍  MENU PRINCIPAL — Desastres Naturais e Gestão de Riscos")
    print("─" * 64)
    print("  [1] Visualizar eventos (tabela)")
    print("  [2] Buscar eventos")
    print("  [3] Ordenar eventos")
    print("  [4] Demonstrar estruturas de dados")
    print("  [5] Relatório geral")
    print("  [6] Mapa de risco global")
    print("  [7] Processar fila de triagem")
    print("  [8] Painel de gestão de riscos")
    print("  [0] Sair")
    print("─" * 64)


# ── Sub-menus ─────────────────────────────────────────────────────────────────

def _visualizar(eventos):
    try:
        n = int(input("  Quantos registros exibir? [padrão 20]: ").strip() or "20")
    except ValueError:
        n = 20
    exibir_tabela(eventos, limite=n)


def _busca(originais, ordenados, pilha, log):
    print("\n  ── BUSCA ───────────────────────────────────────────────")
    print("  [1] Busca Binária — por magnitude exata")
    print("  [2] Busca Binária — por intervalo de magnitude")
    print("  [3] Busca Linear  — por local/região")
    print("  [4] Busca Linear  — por nível de risco")
    print("  [5] Busca Linear  — por período (data)")
    print("  [6] Busca Linear  — por profundidade (km)")

    op = input("  Opção: ").strip()

    if op == "1":
        try:
            mag = float(input("  Magnitude alvo (ex: 6.5): ").strip())
            idx, res = busca_binaria_magnitude(ordenados, mag)
            if res:
                print(f"\n  ✔ Evento encontrado (índice {idx}):")
                _detalhe(res)
                if float(res.get("mag", 0) or 0) >= 6.0:
                    msg = f"Evento M{res['mag']} — {res.get('place','?')} ({res.get('time','?')[:10]})"
                    pilha.empilhar(msg)
                    log.alerta_critico(msg)
            else:
                print(f"\n  Nenhum evento com magnitude próxima a {mag} (±0.3).")
            log.info(f"Busca Binária mag={mag}: {'encontrado' if res else 'não encontrado'}")
        except ValueError:
            print("  Valor inválido.")

    elif op == "2":
        try:
            mag_min = float(input("  Magnitude mínima: ").strip())
            mag_max = float(input("  Magnitude máxima: ").strip())
            res = busca_binaria_range(ordenados, mag_min, mag_max)
            print(f"\n  Eventos M{mag_min}–M{mag_max}: {len(res)} encontrados")
            exibir_tabela(res, limite=15)
            log.info(f"Busca Binária range M[{mag_min}-{mag_max}]: {len(res)} resultados")
        except ValueError:
            print("  Valor inválido.")

    elif op == "3":
        termo = input("  Termo de busca (ex: Japan, Chile, Turkey): ").strip()
        res = busca_linear_local(originais, termo)
        print(f"\n  Eventos com '{termo}': {len(res)}")
        exibir_tabela(res, limite=15)
        log.info(f"Busca Linear local='{termo}': {len(res)} resultados")

    elif op == "4":
        print("  Níveis: critico / alto / moderado / baixo")
        nivel = input("  Nível de risco: ").strip()
        res = busca_linear_nivel(originais, nivel)
        print(f"\n  Eventos '{nivel}': {len(res)}")
        exibir_tabela(res, limite=15)
        log.info(f"Busca Linear nivel='{nivel}': {len(res)} resultados")

    elif op == "5":
        di = input("  Data início (YYYY-MM-DD): ").strip()
        df = input("  Data fim    (YYYY-MM-DD): ").strip()
        res = busca_linear_periodo(originais, di, df)
        print(f"\n  Eventos entre {di} e {df}: {len(res)}")
        exibir_tabela(res, limite=15)
        log.info(f"Busca Linear período {di}~{df}: {len(res)} resultados")

    elif op == "6":
        try:
            pmin = float(input("  Profundidade mínima (km): ").strip())
            pmax = float(input("  Profundidade máxima (km): ").strip())
            res = busca_linear_profundidade(originais, pmin, pmax)
            print(f"\n  Eventos entre {pmin}–{pmax} km: {len(res)}")
            exibir_tabela(res, limite=15)
            log.info(f"Busca Linear profundidade [{pmin}-{pmax}] km: {len(res)} resultados")
        except ValueError:
            print("  Valor inválido.")


def _ordenacao(originais, log):
    print("\n  ── ORDENAÇÃO ────────────────────────────────────────────")
    print("  [1] Merge Sort  — por Magnitude (decrescente)")
    print("  [2] Merge Sort  — por Profundidade (crescente)")
    print("  [3] Merge Sort  — por Significância (decrescente)")
    print("  [4] Merge Sort  — por Data (crescente)")
    print("  [5] Quick Sort  — por Magnitude")
    print("  [6] Bubble Sort — por Magnitude (demonstrativo)")

    op = input("  Opção: ").strip()
    res = originais

    configs = {
        "1": ("mag",   True,  "Magnitude ↓",   "Merge Sort"),
        "2": ("depth", False, "Profundidade ↑", "Merge Sort"),
        "3": ("sig",   True,  "Significância ↓","Merge Sort"),
        "4": ("time",  False, "Data ↑",         "Merge Sort"),
        "5": ("mag",   True,  "Magnitude ↓",   "Quick Sort"),
    }

    if op in configs:
        chave, rev, desc, algo = configs[op]
        if algo == "Merge Sort":
            res = merge_sort(originais, chave=chave, reverso=rev)
        else:
            res = quick_sort(originais, chave=chave, reverso=rev)
        print(f"\n  ✔ {algo} por {desc} concluído ({len(res)} eventos).")
        log.info(f"{algo} por {chave} executado")

    elif op == "6":
        lim = min(100, len(originais))
        print(f"  Executando Bubble Sort nos primeiros {lim} registros...")
        res = bubble_sort(originais[:lim], chave="mag", reverso=True) + originais[lim:]
        print(f"  ✔ Bubble Sort concluído.")
        log.info(f"Bubble Sort executado nos primeiros {lim} registros")

    exibir_tabela(res, limite=10)
    return res


def _estruturas(eventos, pilha, fila, lista, log):
    print("\n  ── DEMONSTRAÇÃO DAS ESTRUTURAS DE DADOS ─────────────────")
    print("  [1] Pilha   — empilhar/desempilhar alertas")
    print("  [2] Fila    — enfileirar/desenfileirar eventos")
    print("  [3] Lista L — adicionar/remover região")
    print("  [4] Ver estado atual de todas as estruturas")

    op = input("  Opção: ").strip()

    if op == "1":
        print(f"\n  Pilha atual: {pilha.tamanho()} alertas")
        msg = input("  Mensagem de alerta: ").strip()
        if msg:
            pilha.empilhar(msg)
            print(f"  ✔ Empilhado. Topo: '{pilha.topo()}'")
            log.info(f"Alerta empilhado: {msg}")
        if input("  Desempilhar o topo? (s/n): ").strip().lower() == "s":
            try:
                rem = pilha.desempilhar()
                print(f"  ✔ Desempilhado: '{rem}'")
            except IndexError as e:
                print(f"  ✘ {e}")

    elif op == "2":
        print(f"\n  Fila atual: {fila.tamanho()} eventos")
        if not fila.vazia():
            f0 = fila.frente()
            print(f"  Próximo: M{f0.get('mag','?')} — {f0.get('place','?')[:40]}")
        if input("  Desenfileirar? (s/n): ").strip().lower() == "s" and not fila.vazia():
            ev = fila.desenfileirar()
            print(f"  ✔ Processado: M{ev.get('mag','?')} — {ev.get('place','?')[:40]}")
            log.info(f"Evento desenfileirado: M{ev.get('mag','?')}")

    elif op == "3":
        print(f"\n  Regiões cadastradas: {lista.tamanho()}")
        for r in lista.listar():
            print(f"    · {r['nome']}")
        nome = input("  Nova região (Enter para pular): ").strip()
        if nome:
            lista.inserir({"nome": nome, "ativa": True})
            print(f"  ✔ '{nome}' adicionada. Total: {lista.tamanho()}")
            log.info(f"Região adicionada: {nome}")

    elif op == "4":
        print(f"\n  {pilha}")
        print(f"  {fila}")
        print(f"  {lista}")
        print("\n  Últimos 3 alertas na pilha:")
        for a in pilha.listar()[:3]:
            print(f"    → {a}")
        print("\n  Regiões monitoradas:")
        for r in lista.listar():
            print(f"    · {r['nome']} ({'ativa' if r['ativa'] else 'inativa'})")


def _triar_fila(fila, pilha, log):
    """Processa eventos da fila e classifica o nível de risco."""
    print(f"\n  Eventos na fila: {fila.tamanho()}")
    if fila.vazia():
        print("  Fila vazia.")
        return

    n = min(5, fila.tamanho())
    print(f"  Triando {n} eventos...\n")
    criticos = 0

    for _ in range(n):
        ev = fila.desenfileirar()
        mag   = float(ev.get("mag", 0) or 0)
        nivel = str(ev.get("nivel_risco", "baixo"))
        local = str(ev.get("place", "?"))[:45]
        data  = str(ev.get("time", "?"))[:10]
        tsu   = "⚠ TSUNAMI" if ev.get("tsunami") else ""

        icone = {"critico": "🔴", "alto": "🟡", "moderado": "🟠", "baixo": "🟢"}.get(nivel, "⚪")
        print(f"  {icone} M{mag:.1f} | {nivel.upper():<10} | {local} | {data} {tsu}")

        if nivel == "critico":
            msg = f"Terremoto CRÍTICO M{mag:.1f} — {local} ({data})"
            pilha.empilhar(msg)
            log.alerta_critico(msg)
            criticos += 1

    print(f"\n  ✔ Triados: {n} | Alertas críticos: {criticos} | Fila restante: {fila.tamanho()}")
    log.info(f"Triagem: {n} eventos, {criticos} críticos")


def _painel_risco(eventos):
    """Painel de gestão de riscos com recomendações."""
    print("\n" + "═" * 64)
    print("  🛡️   PAINEL DE GESTÃO DE RISCOS")
    print("═" * 64)

    criticos  = [e for e in eventos if e.get("nivel_risco") == "critico"]
    altos     = [e for e in eventos if e.get("nivel_risco") == "alto"]
    tsunamis  = [e for e in eventos if e.get("tsunami") == 1]
    rasas     = [e for e in eventos if float(e.get("depth", 99) or 99) < 30]

    print(f"\n  ⚠  Situação atual:")
    print(f"     Eventos críticos    : {len(criticos)}")
    print(f"     Eventos alto risco  : {len(altos)}")
    print(f"     Alertas de tsunami  : {len(tsunamis)}")
    print(f"     Terremotos rasos    : {len(rasas)} (profundidade < 30 km)")

    print(f"\n  📋  Recomendações de Gestão de Riscos:")

    if criticos:
        print(f"\n  🔴 AÇÃO IMEDIATA ({len(criticos)} eventos críticos):")
        print("     • Acionar Defesa Civil e protocolos de emergência")
        print("     • Verificar integridade de infraestruturas críticas")
        print("     • Emitir alertas para população nas áreas afetadas")
        for e in criticos[:3]:
            print(f"     → M{e.get('mag','?')} — {str(e.get('place','?'))[:45]}")

    if tsunamis:
        print(f"\n  🌊 ALERTA DE TSUNAMI ({len(tsunamis)} eventos):")
        print("     • Acionar sistema de alerta costeiro imediatamente")
        print("     • Evacuar zonas de baixa altitude em áreas costeiras")
        print("     • Monitorar boias do sistema DART")

    if altos:
        print(f"\n  🟡 MONITORAMENTO INTENSIFICADO ({len(altos)} eventos):")
        print("     • Aumentar frequência de coleta de dados sísmicos")
        print("     • Verificar estruturas em zonas de risco")

    if not criticos and not altos:
        print("\n  🟢 Nenhum evento de alto risco no período atual.")
        print("     • Manter monitoramento de rotina")

    print()


def _detalhe(e):
    print(f"    ID         : {e.get('id','?')}")
    print(f"    Data/Hora  : {e.get('time','?')}")
    print(f"    Local      : {e.get('place','?')}")
    print(f"    Magnitude  : {e.get('mag','?')} ({e.get('magType','?')})")
    print(f"    Profund.   : {e.get('depth','?')} km")
    print(f"    Risco      : {e.get('nivel_risco','?')}")
    print(f"    Tsunami    : {'SIM ⚠' if e.get('tsunami') else 'Não'}")
    print(f"    Lat / Lon  : {e.get('latitude','?')} / {e.get('longitude','?')}")
    print(f"    Significân.: {e.get('sig','?')}")
