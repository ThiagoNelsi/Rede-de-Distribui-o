from Veiculo import Veiculo
from Encomenda import Encomenda
from PontoDeRedistribuicao import PontoDeRedistribuicao
from tabulate import tabulate
import time
import threading

class Interface(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        while True:
            #clear screen
            print("\033[H\033[J")

            # tabela de viagens
            headers = [f'Veiculo {i}' for i in range(len(Veiculo.veiculos))]
            data = [
                ["status"], # A -> B, carregando, descarregando, estacionado
                ["carga"],
                ["ponto de redistribuição"],
            ]

            for veiculo in Veiculo.veiculos:
                status = ''
                if veiculo.em_viagem:
                    status = f'Viagem de {veiculo.viagem[0]} -> {veiculo.viagem[1]}'
                elif veiculo.carregando:
                    status = 'Carregando'
                elif veiculo.descarregando:
                    status = 'Descarregando'
                else:
                    status = 'Estacionado'

                data[0].append(status)
                data[1].append([encomenda.id for encomenda in veiculo.carga])
                data[2].append(veiculo.ponto_de_redistribuicao)

            # Gerando a tabela
            table = tabulate(data, headers=headers, tablefmt="grid")
            print(table)

            print('\n\n')

            headers = [f'Ponto de redistribuição {i}' for i in range(len(PontoDeRedistribuicao.pontos_de_redistribuicao))]
            headers.insert(0, '')
            data = [
                ["estacionamento"],
                ["entregues"],
                ["aguardando transporte"],
            ]

            for ponto in PontoDeRedistribuicao.pontos_de_redistribuicao:
                data[0].append([veiculo.id for veiculo in ponto.fila_de_veiculos])
                data[1].append([encomenda.id for encomenda in ponto.entregues])
                data[2].append([encomenda.id for encomenda in ponto.aguardando_transporte])

            # Gerando a tabela
            table = tabulate(data, headers=headers, tablefmt="grid")
            print(table)

            print('\n\n')

            headers = ["Encomenda", "Origem", "Destino", "Status"]
            data = []

            for encomenda in Encomenda.encomendas:
                status = ''
                if encomenda.t_descarregamento is not None:
                    status = 'Entregue'
                elif encomenda.t_carregamento is not None:
                    status = 'Em transporte'
                else:
                    status = 'Aguardando transporte'

                data.append([encomenda.id, encomenda.origem, encomenda.destino, status])

            # Gerando a tabela
            table = tabulate(data, headers=headers, tablefmt="grid")
            print(table)

            # 30 FPS
            time.sleep(1 / 30)
