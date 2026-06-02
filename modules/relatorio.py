
from collections import Counter



def exibir_tabela(eventos, limite=20):
    """Exibe lista de eventos em tabela formatada."""
    cab = f"{'#':>4}  {'Data':>10}  {'Mag':>5}  {'Prof(km)':>8}  {'Risco':<10}  {'Tsunami':>7}  {'Local'}"
    print("\n  " + cab)
    print("  " + "─" * len(cab))

    for i, e in enumerate(eventos[:limite]):
        risco = str(e.get("nivel_risco", "?"))
        icone = {"critico": "🔴", "alto": "🟡", "moderado": "🟠", "baixo": "🟢"}.get(risco, "⚪")
        linha = (
            f"  {i+1:>4}  "
            f"{str(e.get('time','?'))[:10]:>10}  "
            f"{float(e.get('mag',0) or 0):>5.1f}  "
            f"{float(e.get('depth',0) or 0):>8.1f}  "
            f"{icone} {risco:<8}  "
            f"{'⚠' if e.get('tsunami') else ' ':>7}  "
            f"{str(e.get('place','?'))[:50]}"
        )
        print(linha)

    if len(eventos) > limite:
        print(f"\n  ... e mais {len(eventos) - limite} eventos (exibindo {limite} primeiros)")
    print()



def gerar_relatorio(eventos, pilha, fila, lista_regioes):
    print("\n" + "═" * 64)
    print("  📊  RELATÓRIO GERAL — DESASTRES NATURAIS")
    print("═" * 64)

    total = len(eventos)
    if total == 0:
        print("  Nenhum evento carregado.")
        return

    mags   = [float(e.get("mag", 0) or 0) for e in eventos]
    depths = [float(e.get("depth", 0) or 0) for e in eventos]
    tsunamis = sum(1 for e in eventos if e.get("tsunami"))

    print(f"\n  Total de eventos        : {total}")
    print(f"  Magnitude máxima        : {max(mags):.1f}")
    print(f"  Magnitude média         : {sum(mags)/total:.2f}")
    print(f"  Profundidade média      : {sum(depths)/total:.1f} km")
    print(f"  Eventos com risco tsunami: {tsunamis}")

    print("\n  ── Distribuição por Nível de Risco ─────────────────────")
    cont_risco = Counter(str(e.get("nivel_risco", "?")) for e in eventos)
    ordem = ["critico", "alto", "moderado", "baixo"]
    icones = {"critico": "🔴", "alto": "🟡", "moderado": "🟠", "baixo": "🟢"}
    for nivel in ordem:
        qtd = cont_risco.get(nivel, 0)
        pct = 100 * qtd / total
        barra = "█" * int(pct / 3)
        print(f"  {icones.get(nivel,'')} {nivel:<10} {barra:<25} {qtd:>4} ({pct:.1f}%)")

    print("\n  ── Top 8 Locais com Mais Eventos ────────────────────────")
    locais = []
    for e in eventos:
        lugar = str(e.get("place", ""))
        if " de " in lugar:
            lugar = lugar.split(" de ", 1)[-1]
        locais.append(lugar[:35])
    for local, qtd in Counter(locais).most_common(8):
        print(f"    {local:<35} {qtd:>3} eventos")

    print(f"\n  ── Pilha de Alertas ─────────────────────────────────────")
    print(f"  Alertas registrados: {pilha.tamanho()}")
    if not pilha.vazia():
        print(f"  Último alerta: {pilha.topo()}")

    print(f"\n  ── Fila de Triagem ──────────────────────────────────────")
    print(f"  Eventos aguardando triagem: {fila.tamanho()}")

    print(f"\n  ── Regiões Monitoradas (Lista Ligada) ───────────────────")
    for r in lista_regioes.listar():
        status = "✔ ATIVA" if r.get("ativa") else "✘ inativa"
        print(f"    · {r['nome']:<35} {status}")

    print("\n" + "═" * 64)



def exibir_mapa_risco(eventos):
    print("\n" + "═" * 64)
    print("  🗺️   MAPA DE RISCO SÍSMICO GLOBAL (esquemático)")
    print("═" * 64)

    regioes_risco = {
        "Japão/Pacífico NW":  {"lat": (30, 45),  "lon": (130, 150)},
        "Chile/América S.":   {"lat": (-55,-15),  "lon": (-80, -65)},
        "Indonésia":          {"lat": (-10,  5),  "lon": (95,  141)},
        "San Andreas/EUA":    {"lat": (32,  42),  "lon": (-125,-114)},
        "Turquia/Grécia":     {"lat": (35,  42),  "lon": (25,   45)},
        "Peru/Equador":       {"lat": (-18,   2), "lon": (-82,  -68)},
        "Nova Zelândia":      {"lat": (-47, -34), "lon": (166,  178)},
        "México":             {"lat": (14,  22),  "lon": (-105, -87)},
        "Brasil":             {"lat": (-15,  5),  "lon": (-55,  -35)},
    }

    contagens = {k: {"critico": 0, "alto": 0, "total": 0} for k in regioes_risco}

    for e in eventos:
        lat = float(e.get("latitude", 0) or 0)
        lon = float(e.get("longitude", 0) or 0)
        nivel = str(e.get("nivel_risco", ""))
        for nome, limites in regioes_risco.items():
            if (limites["lat"][0] <= lat <= limites["lat"][1] and
                    limites["lon"][0] <= lon <= limites["lon"][1]):
                contagens[nome]["total"] += 1
                if nivel == "critico":
                    contagens[nome]["critico"] += 1
                elif nivel == "alto":
                    contagens[nome]["alto"] += 1

    print(f"\n  {'Região':<28} {'Total':>6}  {'Críticos':>8}  {'Altos':>6}  Nível")
    print("  " + "─" * 60)
    for nome, c in sorted(contagens.items(), key=lambda x: -x[1]["total"]):
        if c["total"] == 0:
            continue
        if c["critico"] > 0:
            nivel_str = "🔴 CRÍTICO"
        elif c["alto"] > 2:
            nivel_str = "🟡 ALTO"
        elif c["total"] > 5:
            nivel_str = "🟠 MODERADO"
        else:
            nivel_str = "🟢 BAIXO"
        print(f"  {nome:<28} {c['total']:>6}  {c['critico']:>8}  {c['alto']:>6}  {nivel_str}")

    print(f"\n  Total de eventos mapeados: {len(eventos)}")
    print("  Fonte: USGS Earthquake Hazards Program\n")
