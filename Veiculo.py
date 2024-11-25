import threading
import random
import time
from Encomenda import Encomenda
from PontoDeRedistribuicao import PontoDeRedistribuicao
from constants import P, S, A

class Veiculo(threading.Thread):
    veiculos = []

    def __init__(
            self,
            id:int
        ):
        super().__init__()
        self.id = id
        self.capacidade_total = A
        self.pontos_de_redistribuicao = PontoDeRedistribuicao.pontos_de_redistribuicao
        self.carga: list[Encomenda] = []
        self.lock = threading.Lock()
        self.ponto_de_redistribuicao = random.randint(0, S - 1)

        self.carregando = False
        self.descarregando = False

        self.em_viagem = False
        self.viagem = [None, None]

        self.lock.acquire()

    def get_capacidade_atual(self):
        return self.capacidade_total - len(self.carga)

    def carregar_encomenda(self, encomenda: Encomenda) -> None:
        if self.get_capacidade_atual() > 0:
            self.carga.append(encomenda)

    def descarregar_encomendas(self, destino: int) -> list[Encomenda]:
        encomendas = []
        for encomenda in self.carga[:]:
            if encomenda.destino == destino:
                encomendas.append(encomenda)
                self.carga.remove(encomenda)
        return encomendas

    def run(self):
        while True:
            self.pontos_de_redistribuicao[self.ponto_de_redistribuicao].estacionar(self)
            self.lock.acquire()

            if len(self.carga) == 0 and len(PontoDeRedistribuicao.get_aguardando_transporte()) == 0:
                break

            self.em_viagem = True
            self.viagem = [self.ponto_de_redistribuicao, (self.ponto_de_redistribuicao + 1) % S]
            time.sleep(random.randint(3, 5))
            self.ponto_de_redistribuicao = (self.ponto_de_redistribuicao + 1) % S
            self.em_viagem = False
            self.viagem = [None, None]