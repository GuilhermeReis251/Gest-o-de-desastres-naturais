# 🌍 Sistema de Monitoramento de Desastres Naturais e Gestão de Riscos

## 📋 Descrição do Projeto

Sistema em Python para coleta, organização, análise e monitoramento de eventos sísmicos ao redor do mundo. O sistema consome dados reais do **USGS Earthquake Hazards Program** (Serviço Geológico dos Estados Unidos) via API pública e demonstra a aplicação prática de estruturas de dados e algoritmos estudados na disciplina.

---

## 🎯 Objetivo da Solução

Auxiliar equipes de Defesa Civil e gestores de risco no:

- Monitoramento de terremotos em tempo real via satélites e sensores globais
- Classificação automática de eventos por nível de risco (crítico / alto / moderado / baixo)
- Geração de alertas para eventos com risco de tsunami
- Suporte à tomada de decisão com painel de gestão de riscos e recomendações

---

## 🛰️ Tema e Relação com Economia Espacial

**Desastres Naturais e Gestão de Riscos** — monitoramento sísmico depende diretamente de satélites e redes de sensores geodésicos espaciais (GPS/GNSS) para triangulação de epicentros, detecção de deformações na crosta terrestre e sistema de alerta de tsunamis via boias DART conectadas por satélite.

---

## 🗂️ Fonte dos Dados

| Fonte | URL |
|-------|-----|
| USGS Earthquake Hazards Program | https://earthquake.usgs.gov/fdsnws/event/1/ |
| USGS GeoJSON Feed | https://earthquake.usgs.gov/earthquakes/feed/ |

O sistema baixa automaticamente os eventos dos últimos 30 dias com magnitude ≥ 2.5. Em caso de falha de conexão, um dataset sintético realista com 400 registros é gerado automaticamente.

---

## 🏗️ Estruturas de Dados Implementadas

### 1. Pilha (Stack) — `modules/estruturas.py`
- **Implementação:** Lista encadeada com `NoPilha`
- **Uso:** Histórico de alertas críticos (LIFO) — último alerta sempre acessível no topo
- **Operações:** `empilhar()`, `desempilhar()`, `topo()` — O(1)

### 2. Fila (Queue) — `modules/estruturas.py`
- **Implementação:** Lista encadeada com referências à cabeça e cauda
- **Uso:** Fila de eventos aguardando triagem de risco (FIFO)
- **Operações:** `enfileirar()`, `desenfileirar()`, `frente()` — O(1)

### 3. Lista Ligada Simples — `modules/estruturas.py`
- **Implementação:** Encadeamento por ponteiros com `NoLista`
- **Uso:** Catálogo de regiões sísmicas monitoradas
- **Operações:** `inserir()`, `remover()`, `buscar()`, `listar()`

---

## ⚙️ Algoritmos Utilizados

### Ordenação

| Algoritmo | Arquivo | Complexidade | Uso |
|-----------|---------|--------------|-----|
| **Merge Sort** | `modules/ordenacao.py` | O(n log n) | Principal — ordena por magnitude, profundidade, data, significância |
| Quick Sort | `modules/ordenacao.py` | O(n log n) médio | Alternativo para magnitude |
| Bubble Sort | `modules/ordenacao.py` | O(n²) | Demonstrativo |

### Busca

| Algoritmo | Arquivo | Complexidade | Uso |
|-----------|---------|--------------|-----|
| **Busca Binária** | `modules/busca.py` | O(log n) | Busca por magnitude exata / intervalo de magnitude |
| Busca Linear | `modules/busca.py` | O(n) | Busca por local, nível de risco, profundidade, período |

---

## 🛠️ Tecnologias e Bibliotecas

- **Python 3.10+** — linguagem principal (sem dependências obrigatórias externas)
- **csv** (stdlib) — leitura e escrita de dados
- **json** (stdlib) — parsing da resposta da API USGS
- **urllib** (stdlib) — download dos dados via HTTP
- **collections.Counter** (stdlib) — estatísticas e contagens
- **datetime** (stdlib) — manipulação de datas

---

## 🔄 Funcionamento do Sistema

```
main.py
  │
  ├── data_loader.py  ── Baixa JSON da USGS API → converte para CSV
  │                      (ou gera dataset de exemplo offline)
  │
  ├── estruturas.py   ── Inicializa Pilha, Fila e Lista Ligada
  │
  ├── ordenacao.py    ── Merge Sort nos eventos por magnitude
  │
  └── menu.py         ── Loop interativo:
        ├── [1] Tabela de eventos
        ├── [2] Busca (binária/linear)
        ├── [3] Reordenar por critério
        ├── [4] Demonstração das estruturas
        ├── [5] Relatório geral + estatísticas
        ├── [6] Mapa de risco global (por região)
        ├── [7] Processar fila de triagem
        └── [8] Painel de gestão de riscos com recomendações
```

### Classificação automática de risco

| Critério | Nível |
|----------|-------|
| Mag ≥ 7.0 **ou** Mag ≥ 6.0 + tsunami | 🔴 Crítico |
| Mag ≥ 5.5 **ou** Mag ≥ 5.0 + prof < 70km | 🟡 Alto |
| Mag ≥ 4.0 | 🟠 Moderado |
| Mag < 4.0 | 🟢 Baixo |

---

## ▶️ Instruções de Execução

### Pré-requisitos

- Python 3.10 ou superior
- Conexão com a internet (opcional)

### Execução

```bash
python main.py
```

O sistema:
1. Tenta baixar dados reais da API USGS (últimos 30 dias, mag ≥ 2.5)
2. Se sem internet, gera dataset de 400 eventos de exemplo
3. Ordena eventos por magnitude via Merge Sort
4. Abre o menu interativo no terminal

---

## 📁 Estrutura do Projeto

```
disaster_monitor/
├── main.py                  # Ponto de entrada
├── README.md
├── data/
│   └── terremotos.csv       # Gerado automaticamente
├── logs/
│   └── execucao.log         # Log de execução com timestamps
└── modules/
    ├── __init__.py
    ├── estruturas.py        # Pilha, Fila, Lista Ligada
    ├── ordenacao.py         # Merge Sort, Quick Sort, Bubble Sort
    ├── busca.py             # Busca Binária e Linear
    ├── data_loader.py       # API USGS + gerador de exemplo
    ├── relatorio.py         # Tabelas, relatório e mapa ASCII
    ├── menu.py              # Interface de terminal
    └── logger.py            # Sistema de logs
```

---

## 👥 Integrantes do Grupo

| Nome Completo | RM |
|---------------|----|
| Guilherme Reis | RM564226 |
| Paulo Rodrigues | RM565898 |
| Victor Pereira | RM561548 |
| Vinicius Gama | RM561617 |



