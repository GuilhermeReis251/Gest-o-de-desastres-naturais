class NoPilha:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class Pilha:
    

    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def empilhar(self, dado):
        no = NoPilha(dado)
        no.proximo = self._topo
        self._topo = no
        self._tamanho += 1

    def desempilhar(self):
        if self.vazia():
            raise IndexError("Pilha vazia.")
        dado = self._topo.dado
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return dado

    def topo(self):
        return self._topo.dado if self._topo else None

    def vazia(self):
        return self._tamanho == 0

    def tamanho(self):
        return self._tamanho

    def listar(self):
        resultado, atual = [], self._topo
        while atual:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def __repr__(self):
        return f"Pilha(tamanho={self._tamanho}, topo={self.topo()})"
    
    
class NoFila:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class Fila:
  
    def __init__(self):
        self._cabeca = None
        self._cauda = None
        self._tamanho = 0

    def enfileirar(self, dado):
        no = NoFila(dado)
        if self._cauda:
            self._cauda.proximo = no
        self._cauda = no
        if self._cabeca is None:
            self._cabeca = no
        self._tamanho += 1

    def desenfileirar(self):
        if self.vazia():
            raise IndexError("Fila vazia.")
        dado = self._cabeca.dado
        self._cabeca = self._cabeca.proximo
        if self._cabeca is None:
            self._cauda = None
        self._tamanho -= 1
        return dado

    def frente(self):
        return self._cabeca.dado if self._cabeca else None

    def vazia(self):
        return self._tamanho == 0

    def tamanho(self):
        return self._tamanho

    def listar(self):
        resultado, atual = [], self._cabeca
        while atual:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def __repr__(self):
        return f"Fila(tamanho={self._tamanho}, frente={self.frente()})"


class NoLista:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaLigada:
 
    def __init__(self):
        self._cabeca = None
        self._tamanho = 0

    def inserir(self, dado):
        no = NoLista(dado)
        if self._cabeca is None:
            self._cabeca = no
        else:
            atual = self._cabeca
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = no
        self._tamanho += 1

    def inserir_inicio(self, dado):
        no = NoLista(dado)
        no.proximo = self._cabeca
        self._cabeca = no
        self._tamanho += 1

    def remover(self, campo, valor):
        anterior, atual = None, self._cabeca
        while atual:
            if isinstance(atual.dado, dict) and atual.dado.get(campo) == valor:
                if anterior:
                    anterior.proximo = atual.proximo
                else:
                    self._cabeca = atual.proximo
                self._tamanho -= 1
                return True
            anterior, atual = atual, atual.proximo
        return False

    def buscar(self, campo, valor):
        atual = self._cabeca
        while atual:
            if isinstance(atual.dado, dict) and atual.dado.get(campo) == valor:
                return atual.dado
            atual = atual.proximo
        return None

    def listar(self):
        resultado, atual = [], self._cabeca
        while atual:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def tamanho(self):
        return self._tamanho

    def vazia(self):
        return self._tamanho == 0

    def __repr__(self):
        return f"ListaLigada(tamanho={self._tamanho})"
