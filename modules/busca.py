"""
modules/busca.py
================
Algoritmos de busca:
  - Busca Binária  -> por magnitude (lista ordenada)
  - Busca Linear   -> por local, país, nível de risco, período
"""


# ── Busca Binária ─────────────────────────────────────────

def busca_binaria_magnitude(lista_ordenada, mag_alvo, tolerancia=0.3):
    """
    Busca Binária em lista ordenada por magnitude (decrescente).
    Retorna o evento com magnitude mais próxima ao alvo.
    """
    if not lista_ordenada:
        return None, None

    esq, dir = 0, len(lista_ordenada) - 1
    melhor_idx, melhor_diff = None, float("inf")

    while esq <= dir:
        meio = (esq + dir) // 2
        try:
            mag = float(lista_ordenada[meio].get("mag", 0) or 0)
        except (ValueError, TypeError):
            mag = 0.0

        diff = abs(mag - mag_alvo)
        if diff < melhor_diff:
            melhor_diff = diff
            melhor_idx = meio

        if mag == mag_alvo:
            return meio, lista_ordenada[meio]
        elif mag > mag_alvo:
            esq = meio + 1   # decrescente: maior está à esquerda
        else:
            dir = meio - 1

    if melhor_diff <= tolerancia:
        return melhor_idx, lista_ordenada[melhor_idx]
    return None, None


def busca_binaria_range(lista_ordenada, mag_min, mag_max):
    """
    Retorna todos os eventos com magnitude entre mag_min e mag_max.
    Lista deve estar ordenada por magnitude decrescente.
    """
    resultado = []
    n = len(lista_ordenada)
    inicio = _limite_superior(lista_ordenada, mag_max)
    if inicio is None:
        return resultado
    for i in range(inicio, n):
        try:
            mag = float(lista_ordenada[i].get("mag", 0) or 0)
        except (ValueError, TypeError):
            continue
        if mag < mag_min:
            break
        resultado.append(lista_ordenada[i])
    return resultado


def _limite_superior(lista, mag_max):
    esq, dir, res = 0, len(lista) - 1, None
    while esq <= dir:
        meio = (esq + dir) // 2
        try:
            mag = float(lista[meio].get("mag", 0) or 0)
        except (ValueError, TypeError):
            mag = 0.0
        if mag <= mag_max:
            res = meio; dir = meio - 1
        else:
            esq = meio + 1
    return res


# ── Busca Linear ──────────────────────────────────────────

def busca_linear_local(lista, termo):
    """Busca linear por texto no campo 'place' — O(n)."""
    alvo = termo.strip().lower()
    return [e for e in lista if alvo in str(e.get("place", "")).lower()]


def busca_linear_nivel(lista, nivel):
    """
    Busca linear por nível de risco — O(n).
    Níveis: critico, alto, moderado, baixo
    """
    alvo = nivel.strip().lower()
    return [e for e in lista if str(e.get("nivel_risco", "")).lower() == alvo]


def busca_linear_periodo(lista, data_inicio, data_fim):
    """Busca linear por intervalo de datas (YYYY-MM-DD) — O(n)."""
    resultado = []
    for e in lista:
        data = str(e.get("time", ""))[:10]
        if data_inicio <= data <= data_fim:
            resultado.append(e)
    return resultado


def busca_linear_profundidade(lista, prof_min, prof_max):
    """Busca linear por profundidade em km — O(n)."""
    resultado = []
    for e in lista:
        try:
            prof = float(e.get("depth", 0) or 0)
            if prof_min <= prof <= prof_max:
                resultado.append(e)
        except (ValueError, TypeError):
            continue
    return resultado
