"""
modules/ordenacao.py
====================
Algoritmos de ordenação:
  - Merge Sort  — O(n log n), estável, principal
  - Quick Sort  — O(n log n) médio, alternativo
  - Bubble Sort — O(n²), demonstrativo
"""


def _val(item, chave):
    """Extrai valor numérico ou string para comparação."""
    try:
        v = item.get(chave, 0) or 0
        return float(v)
    except (ValueError, TypeError):
        return str(item.get(chave, ""))


# ── Merge Sort ────────────────────────────────────────────

def merge_sort(lista, chave="mag", reverso=True):
    """Merge Sort recursivo — O(n log n)."""
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esq = merge_sort(lista[:meio], chave, reverso)
    dir = merge_sort(lista[meio:], chave, reverso)
    return _merge(esq, dir, chave, reverso)


def _merge(esq, dir, chave, reverso):
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        ve, vd = _val(esq[i], chave), _val(dir[j], chave)
        if (ve >= vd) if reverso else (ve <= vd):
            resultado.append(esq[i]); i += 1
        else:
            resultado.append(dir[j]); j += 1
    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado


# ── Quick Sort ────────────────────────────────────────────

def quick_sort(lista, chave="mag", reverso=True):
    """Quick Sort recursivo — O(n log n) médio."""
    if len(lista) <= 1:
        return lista
    pivo = _val(lista[len(lista) // 2], chave)
    if reverso:
        menores = [x for x in lista if _val(x, chave) >  pivo]
        iguais  = [x for x in lista if _val(x, chave) == pivo]
        maiores = [x for x in lista if _val(x, chave) <  pivo]
    else:
        menores = [x for x in lista if _val(x, chave) <  pivo]
        iguais  = [x for x in lista if _val(x, chave) == pivo]
        maiores = [x for x in lista if _val(x, chave) >  pivo]
    return quick_sort(menores, chave, reverso) + iguais + quick_sort(maiores, chave, reverso)


# ── Bubble Sort ───────────────────────────────────────────

def bubble_sort(lista, chave="mag", reverso=True):
    """Bubble Sort — O(n²), incluído para fins demonstrativos."""
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        trocou = False
        for j in range(n - i - 1):
            ve, vd = _val(arr[j], chave), _val(arr[j + 1], chave)
            trocar = ve < vd if reverso else ve > vd
            if trocar:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                trocou = True
        if not trocou:
            break
    return arr
