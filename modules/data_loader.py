"""
modules/data_loader.py
======================
Carregamento de dados de terremotos.

Fontes:
  1. USGS Earthquake Hazards Program — API pública (JSON → CSV)
  2. Dataset sintético realista (fallback offline)
"""

import csv
import json
import random
import os
from datetime import datetime, timedelta

try:
    import urllib.request as req
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

# ── USGS API ──────────────────────────────────────────────────────────────────
# Últimos 30 dias, magnitude ≥ 2.5, mundo todo
USGS_URL = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query"
    "?format=geojson&starttime={inicio}&endtime={fim}"
    "&minmagnitude=2.5&orderby=magnitude&limit=500"
)

COLUNAS = [
    "id", "time", "latitude", "longitude", "depth",
    "mag", "magType", "place", "status", "tsunami",
    "sig", "net", "nivel_risco"
]

# ── Classificação de risco ────────────────────────────────────────────────────

def _nivel_risco(mag, depth, tsunami):
    """Classifica nível de risco com base em magnitude, profundidade e tsunami."""
    mag = float(mag or 0)
    depth = float(depth or 0)
    tsunami = int(tsunami or 0)

    if mag >= 7.0 or (mag >= 6.0 and tsunami == 1):
        return "critico"
    elif mag >= 5.5 or (mag >= 5.0 and depth < 70):
        return "alto"
    elif mag >= 4.0:
        return "moderado"
    else:
        return "baixo"


# ── Download USGS ─────────────────────────────────────────────────────────────

def baixar_dados_usgs(caminho_destino):
    """Baixa dados da API USGS e salva como CSV."""
    if not HAS_URLLIB:
        raise RuntimeError("urllib não disponível.")

    fim = datetime.utcnow()
    inicio = fim - timedelta(days=30)
    url = USGS_URL.format(
        inicio=inicio.strftime("%Y-%m-%d"),
        fim=fim.strftime("%Y-%m-%d")
    )

    print(f"     Conectando à USGS API...")
    with req.urlopen(url, timeout=15) as resp:
        dados = json.loads(resp.read().decode("utf-8"))

    features = dados.get("features", [])
    print(f"     {len(features)} eventos recebidos da USGS.")

    os.makedirs(os.path.dirname(caminho_destino) or ".", exist_ok=True)

    with open(caminho_destino, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUNAS)
        writer.writeheader()
        for feat in features:
            p = feat.get("properties", {})
            geo = feat.get("geometry", {}).get("coordinates", [0, 0, 0])
            mag = p.get("mag", 0)
            depth = geo[2] if len(geo) > 2 else 0
            tsunami = p.get("tsunami", 0)
            ts = p.get("time", 0)
            try:
                data = datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%dT%H:%M:%S")
            except Exception:
                data = ""
            writer.writerow({
                "id":         feat.get("id", ""),
                "time":       data,
                "latitude":   round(geo[1], 4) if len(geo) > 1 else 0,
                "longitude":  round(geo[0], 4) if len(geo) > 0 else 0,
                "depth":      round(float(depth or 0), 1),
                "mag":        round(float(mag or 0), 1),
                "magType":    p.get("magType", ""),
                "place":      p.get("place", ""),
                "status":     p.get("status", ""),
                "tsunami":    tsunami,
                "sig":        p.get("sig", 0),
                "net":        p.get("net", ""),
                "nivel_risco": _nivel_risco(mag, depth, tsunami),
            })

    print(f"     ✔ CSV salvo: {caminho_destino}")


# ── Carregamento CSV ──────────────────────────────────────────────────────────

def carregar_dados_csv(caminho):
    """Lê CSV e retorna lista de dicionários normalizados."""
    eventos = []
    with open(caminho, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            evento = _normalizar(linha)
            eventos.append(evento)
    return eventos


def _normalizar(linha):
    e = {}
    for campo in ["latitude", "longitude", "depth", "mag", "sig"]:
        try:
            e[campo] = float(linha.get(campo, 0) or 0)
        except (ValueError, TypeError):
            e[campo] = 0.0
    for campo in ["id", "time", "magType", "place", "status", "net"]:
        e[campo] = str(linha.get(campo, "")).strip()
    try:
        e["tsunami"] = int(linha.get("tsunami", 0) or 0)
    except (ValueError, TypeError):
        e["tsunami"] = 0

    # Recalcula nível de risco se ausente
    nivel = str(linha.get("nivel_risco", "")).strip()
    e["nivel_risco"] = nivel if nivel else _nivel_risco(e["mag"], e["depth"], e["tsunami"])
    return e


# ── Dataset de exemplo ────────────────────────────────────────────────────────

REGIOES = [
    ("Anel de Fogo — Japão",      35.6, 139.6),
    ("Anel de Fogo — Chile",     -33.4, -70.6),
    ("Anel de Fogo — Indonésia",  -6.2, 106.8),
    ("Falha de San Andreas",      37.7, -122.4),
    ("Grécia — Mar Egeu",         37.9,  23.7),
    ("Turquia — Anatólia",        39.9,  32.8),
    ("Peru — Costa Pacífica",    -12.0, -77.0),
    ("Nova Zelândia",            -36.8, 174.7),
    ("México — Subducção",        19.4, -99.1),
    ("Zona Sísmica Brasil",       -3.7, -40.3),
]

MAG_TYPES = ["ml", "mb", "mw", "ms", "md"]
NETS = ["us", "ci", "nc", "uu", "ak", "pr"]


def gerar_dataset_exemplo(caminho, n=400):
    """Gera CSV sintético com dados realistas de terremotos."""
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    random.seed(2025)

    hoje = datetime.utcnow()
    registros = []

    for i in range(n):
        nome, lat_b, lon_b = random.choice(REGIOES)
        dias_atras = random.randint(0, 30)
        data = (hoje - timedelta(
            days=dias_atras,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )).strftime("%Y-%m-%dT%H:%M:%S")

        # Magnitudes com distribuição realista (mais eventos pequenos)
        mag = round(random.choices(
            [random.uniform(2.5, 3.9),
             random.uniform(4.0, 5.4),
             random.uniform(5.5, 6.9),
             random.uniform(7.0, 9.0)],
            weights=[60, 25, 12, 3]
        )[0], 1)

        depth = round(random.choices(
            [random.uniform(0, 70),
             random.uniform(70, 300),
             random.uniform(300, 700)],
            weights=[60, 30, 10]
        )[0], 1)

        tsunami = 1 if (mag >= 7.0 and depth < 100 and random.random() < 0.4) else 0
        sig = int(mag * 100 + random.randint(0, 200))

        registros.append({
            "id":         f"us{i:06d}",
            "time":       data,
            "latitude":   round(lat_b + random.uniform(-3, 3), 4),
            "longitude":  round(lon_b + random.uniform(-3, 3), 4),
            "depth":      depth,
            "mag":        mag,
            "magType":    random.choice(MAG_TYPES),
            "place":      f"{round(random.uniform(10,200))}km de {nome}",
            "status":     random.choice(["reviewed", "automatic"]),
            "tsunami":    tsunami,
            "sig":        sig,
            "net":        random.choice(NETS),
            "nivel_risco": _nivel_risco(mag, depth, tsunami),
        })

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUNAS)
        writer.writeheader()
        writer.writerows(registros)

    print(f"     Dataset de exemplo gerado: {n} eventos → {caminho}")
    return registros
