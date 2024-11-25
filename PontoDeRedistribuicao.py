import threading
import time
import random

from Encomenda import Encomenda

class PontoDeRedistribuicao(threading.Thread):
    pontos_de_redistribuicao = []

    def get_aguardando_transporte():
        return [encomenda for ponto in PontoDeRedistribuicao.pontos_de_redistribuicao for encomenda in ponto.aguardando_transporte]

    def __init__(self, id: int):
        super().__init__()
        self.id = id
        self.entregues: list[Encomenda] = []
        self.aguardando_transporte: list[Encomenda] = []
        self.fila_de_veiculos = []
        self.semaforo_veiculos = threading.Semaphore(1)
        self.lock = threading.Semaphore(0)
        self._stop_event = threading.Event()  # Add stop event

    def carregar(self, veiculo):
        hora_de_carregamento = time.time()
        veiculo.carregando = True
        time.sleep(random.randint(3, 4))
        while (len(self.aguardando_transporte) > 0) and (veiculo.get_capacidade_atual() > 0):
            encomenda = self.aguardando_transporte.pop(0)
            encomenda.t_carregamento = hora_de_carregamento
            encomenda.veiculo = veiculo.id
            veiculo.carga.append(encomenda)
        veiculo.carregando = False

    def descarregar(self, veiculo):
        veiculo.descarregando = True
        time.sleep(random.randint(3, 4))
        encomendas = veiculo.descarregar_encomendas(self.id)
        for encomenda in encomendas:
            encomenda.t_descarregamento = time.time()
            encomenda.start()
            self.entregues.append(encomenda)
        veiculo.descarregando = False

    def estacionar(self, veiculo):
        self.semaforo_veiculos.acquire()
        self.fila_de_veiculos.append(veiculo)
        self.semaforo_veiculos.release()
        self.lock.release()

    def run(self):
        while not self._stop_event.is_set():  # Check stop event
            self.lock.acquire()

            if not self.fila_de_veiculos:
                self.lock.release()
                continue

            veiculo = self.fila_de_veiculos.pop(0)

            time.sleep(.2)
            self.descarregar(veiculo)
            time.sleep(.2)
            self.carregar(veiculo)

            if veiculo.lock.locked():
                veiculo.lock.release()

    def stop(self):
        self._stop_event.set()
        self.lock.release()  # Ensure the thread can exit if waiting