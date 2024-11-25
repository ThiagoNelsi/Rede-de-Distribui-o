import threading
import time

class Encomenda(threading.Thread):
    encomendas = []

    def __init__(self, id: int, origem: int, destino: int):
        super().__init__()
        self.id = id
        self.origem = origem
        self.destino = destino
        self.lock = threading.Lock()

        self.t_origem: float = None
        self.t_carregamento: float = None
        self.veiculo: float = None
        self.t_descarregamento: float = None

        self.lock.acquire()

    def run(self):
        # timestamp -> segundos desde 01/01/1970

        t_origem_str = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(self.t_origem))
        t_carregamento_str = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(self.t_carregamento))
        t_descarregamento_str = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(self.t_descarregamento))

        with open(f"rastro_encomenda_{self.id}.txt", "w") as file:
            file.write(f"Encomenda ID: {self.id}\n")
            file.write(f"Origem: {self.origem}\n")
            file.write(f"Destino: {self.destino}\n")
            file.write(f"Horário de chegada ao ponto de origem: {t_origem_str}\n")
            file.write(f"Horário de carregamento no veículo: {t_carregamento_str}\n")
            file.write(f"Identificador do veículo: {self.veiculo}\n")
            file.write(f"Horário de descarregamento no ponto de destino: {t_descarregamento_str}\n")