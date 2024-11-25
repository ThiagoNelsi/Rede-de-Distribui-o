# Rede de Entregas

Este projeto simula o comportamento de uma rede de entregas, onde encomendas são transportadas por veículos de um ponto de redistribuição para outro. A sincronização é feita utilizando semáforos e variáveis de trava (locks).

## Estrutura do Projeto

O projeto é dividido em várias classes principais:

- `Encomenda`: Representa uma encomenda a ser entregue.
- `Veiculo`: Representa um veículo que transporta encomendas.
- `PontoDeRedistribuicao`: Representa um ponto de redistribuição onde as encomendas são carregadas e descarregadas.
- `Interface`: Interface para monitoramento em tempo real.
- `entradas.py`: Contém as entradas S, C, P e A que definem o número de pontos de redistribuição, veículos, encomendas e espaços de carga, respectivamente.

## Implementação

### Orientação a Objetos

A escolha por orientação a objetos facilita a modelagem dos componentes do sistema (encomendas, veículos e pontos de redistribuição) como entidades independentes com seus próprios estados e comportamentos. Cada classe encapsula seus dados e métodos, promovendo a reutilização e a manutenção do código.

### Threads

Cada encomenda, veículo e ponto de redistribuição é implementado como um thread. Isso permite que as operações de carregamento, descarregamento e transporte ocorram simultaneamente, simulando um ambiente real de rede de entregas.

### Semáforos e Locks

- **Semáforos**: Utilizados para controlar o acesso aos pontos de redistribuição, garantindo que apenas um veículo seja atendido por vez.
- **Locks**: Utilizados para sincronizar o acesso às listas compartilhadas (como a lista de encomendas de um veículo) e para controlar o fluxo de execução dos threads.

## Detalhes das Classes

### Classe `Encomenda`

A classe `Encomenda` representa uma encomenda a ser entregue. Cada encomenda é um thread que registra seu próprio rastro em um arquivo.

```python
class Encomenda(threading.Thread):
    # ...existing code...
    def run(self):
        self.lock.acquire()
        # ...existing code...
        with open(f"rastro_encomenda_{self.id}.txt", "w") as file:
            # ...existing code...
```

- **Método `run`**: Executa o thread da encomenda, registrando os horários de chegada, carregamento e descarregamento. O uso de `self.lock.acquire()` garante que o thread só finalize após a encomenda ser descarregada.

### Classe `Veiculo`

A classe `Veiculo` representa um veículo que transporta encomendas entre pontos de redistribuição. Cada veículo é um thread que gerencia sua própria carga e viagem.

```python
class Veiculo(threading.Thread):
    # ...existing code...
    def run(self):
        while True:
            self.pontos_de_redistribuicao[self.ponto_de_redistribuicao].estacionar(self)
            self.lock.acquire()
            # ...existing code...
            if len(self.carga) == 0:
                if len(PontoDeRedistribuicao.get_aguardando_transporte()) == 0:
                    break
            # ...existing code...
```

- **Método `run`**: Controla o ciclo de vida do veículo, incluindo estacionar, carregar e descarregar encomendas, e viajar entre pontos de redistribuição. O uso de `self.lock.acquire()` e `self.lock.release()` sincroniza o acesso ao veículo durante o carregamento e descarregamento.
- **Método `carregar_encomenda`**: Adiciona uma encomenda à carga do veículo.
- **Método `descarregar_encomendas`**: Remove encomendas da carga do veículo ao chegar no destino.

### Classe `PontoDeRedistribuicao`

A classe `PontoDeRedistribuicao` gerencia a fila de veículos e a lista de encomendas aguardando transporte. Cada ponto de redistribuição é um thread que controla o carregamento e descarregamento de encomendas.

```python
class PontoDeRedistribuicao(threading.Thread):
    # ...existing code...
    def run(self):
        while not self._stop_event.is_set():
            self.lock.acquire()
            # ...existing code...
            veiculo = self.fila_de_veiculos.pop(0)
            # ...existing code...
    def stop(self):
        self._stop_event.set()
        self.lock.release()
```

- **Método `run`**: Controla o ciclo de vida do ponto de redistribuição, incluindo o gerenciamento da fila de veículos e o carregamento e descarregamento de encomendas. O uso de `self.lock.acquire()` e `self.lock.release()` sincroniza o acesso ao ponto de redistribuição.
- **Método `carregar`**: Carrega encomendas no veículo.
- **Método `descarregar`**: Descarrega encomendas do veículo.
- **Método `estacionar`**: Adiciona um veículo à fila de veículos aguardando atendimento.

### Classe `Interface`

A classe `Interface` é responsável por monitorar e exibir o status em tempo real das encomendas, veículos e pontos de redistribuição.

```python
class Interface(threading.Thread):
    # ...existing code...
    def run(self):
        while True:
            # ...existing code...
            print(table)
            # ...existing code...
            time.sleep(1 / 30)
```

- **Método `run`**: Atualiza a interface de monitoramento em tempo real, exibindo o status das encomendas, veículos e pontos de redistribuição.

## Fluxo do Programa

Vamos ilustrar o fluxo do programa com um exemplo:

1. **Inicialização**:

   - O programa principal (`main.py`) inicializa os pontos de redistribuição, encomendas e veículos, e inicia os threads correspondentes.
   - Exemplo:

     ```python
     for i in range(S):
         PontoDeRedistribuicao.pontos_de_redistribuicao.append(PontoDeRedistribuicao(i))

     for i in range(P):
         origem = random.randint(0, S - 1)
         destino = random.randint(0, S - 1)
         enquanto origem == destino:
             destino = random.randint(0, S - 1)
         Encomenda.encomendas.append(Encomenda(i, origem, destino))
         PontoDeRedistribuicao.pontos_de_redistribuicao[origem].aguardando_transporte.append(Encomenda.encomendas[-1])
         Encomenda.encomendas[-1].t_origem = time.time()

     for i in range(C):
         veiculo = Veiculo(i, A, S, PontoDeRedistribuicao.pontos_de_redistribuicao)
         Veiculo.veiculos.append(veiculo)
         PontoDeRedistribuicao.pontos_de_redistribuicao[veiculo.ponto_de_redistribuicao].estacionar(veiculo)
     ```

2. **Execução dos Threads**:

   - Os threads dos pontos de redistribuição e veículos são iniciados.
   - Exemplo:

     ```python
     for i in PontoDeRedistribuicao.pontos_de_redistribuicao:
         i.start()

     for i in Veiculo.veiculos:
         i.start()

     for i in Veiculo.veiculos:
         i.join()

     for i in PontoDeRedistribuicao.pontos_de_redistribuicao:
         i.stop()
     ```

3. **Interação entre Classes**:

   - **Veículo Estaciona**: O veículo estaciona em um ponto de redistribuição.

     ```python
     self.pontos_de_redistribuicao[self.ponto_de_redistribuicao].estacionar(self)
     self.lock.acquire()
     ```

   - **Ponto de Redistribuição Carrega e Descarrega**: O ponto de redistribuição carrega e descarrega encomendas do veículo.

     ```python
     veiculo = self.fila_de_veiculos.pop(0)
     self.descarregar(veiculo)
     self.carregar(veiculo)
     ```

4. **Finalização**:
   - Os threads dos pontos de redistribuição são parados após a entrega de todas as encomendas.
   - Exemplo:
     ```python
     for i in PontoDeRedistribuicao.pontos_de_redistribuicao:
         i.stop()
     ```

### Arquivos de Rastro

Cada encomenda gera um arquivo de rastro contendo:

- ID da encomenda
- Ponto de origem e destino
- Horários de chegada ao ponto de origem, carregamento no veículo e descarregamento no ponto de destino
- Identificador do veículo que transportou a encomenda

## Como Executar

1. Certifique-se de que todas as dependências estão instaladas.
2. Execute o script `main.py` para iniciar a simulação.

```sh
python main.py
```

## Conclusão

Este projeto demonstra o uso de programação concorrente para simular uma rede de entregas, utilizando conceitos de orientação a objetos, threads, semáforos e locks para garantir a sincronização e o funcionamento correto do sistema.
