import os
from datetime import datetime


class Logger:
    def __init__(self, caminho="logs/execucao.log"):
        self.caminho = caminho
        os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
        with open(self.caminho, "w", encoding="utf-8") as f:
            f.write(f"=== Log iniciado em {self._agora()} ===\n\n")

    def _agora(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _gravar(self, nivel, msg):
        with open(self.caminho, "a", encoding="utf-8") as f:
            f.write(f"[{self._agora()}] [{nivel:5s}] {msg}\n")

    def info(self, msg):
        self._gravar("INFO", msg)

    def aviso(self, msg):
        self._gravar("AVISO", msg)
        print(f"  ⚠  {msg}")

    def erro(self, msg):
        self._gravar("ERRO", msg)
        print(f"  ✘  ERRO: {msg}")

    def alerta_critico(self, msg):
        self._gravar("ALERT", msg)
        print(f"\n  🚨  ALERTA CRÍTICO: {msg}\n")
