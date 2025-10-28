import threading
import time
import random

# --- Constantes ---
N_FILOSOFOS = 5
# Tempo máximo (em segundos) que um filósofo passará pensando ou comendo
TEMPO_MAX_ACAO = 5 

# --- Recursos Compartilhados ---

# Cada garfo é um "Lock" (mutex). 
# Um filósofo deve "adquirir" o lock para pegar o garfo.
garfos = [threading.Lock() for _ in range(N_FILOSOFOS)]

# O "Garçom" (Waiter) é a nossa solução para o deadlock.
# É um semáforo que permite que no máximo N-1 filósofos 
# tentem pegar os garfos ao mesmo tempo.
# Isso garante que sempre haverá pelo menos um garfo livre
# para que um filósofo possa completar seu par.
garcon = threading.Semaphore(N_FILOSOFOS - 1)

class Filosofo(threading.Thread):
    """
    Representa um filósofo como uma thread independente.
    Cada filósofo alterna entre pensar, pegar garfos, comer e devolver garfos.
    """
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.nome = f"Filósofo {self.id}"
        # Define os índices dos garfos à esquerda e à direita
        self.garfo_esq = self.id
        self.garfo_dir = (self.id + 1) % N_FILOSOFOS
        self.rodadas_comendo = 0

    def run(self):
        """ O ciclo de vida do filósofo """
        try:
            while True:
                self.pensar()
                self.pegar_garfos()
                self.comer()
                self.devolver_garfos()
        except KeyboardInterrupt:
            print(f"{self.nome} foi interrompido.")

    def pensar(self):
        """ Simula o filósofo pensando por um tempo aleatório """
        print(f"[{self.nome}] está PENSANDO.")
        time.sleep(random.uniform(1, TEMPO_MAX_ACAO))

    def pegar_garfos(self):
        """
        Tenta pegar os garfos usando a solução do "Garçom" para evitar deadlock.
        """
        print(f"[{self.nome}] está com FOME e tenta sentar-se à mesa.")
        
        # 1. Pede permissão ao "Garçom" para sentar (acquire no semáforo)
        #    Isso bloqueia se já houver N-1 filósofos na mesa.
        garcon.acquire()
        print(f"[{self.nome}] SENTOU-SE à mesa.")

        # 2. Uma vez sentado, tenta pegar o garfo da esquerda
        garfos[self.garfo_esq].acquire()
        print(f"[{self.nome}] pegou o garfo da ESQUERDA ({self.garfo_esq}).")
        
        # Adicionamos um pequeno atraso para tornar a condição de 
        # corrida (e o potencial deadlock, se não fosse o garçom) mais provável.
        time.sleep(0.5) 

        # 3. Tenta pegar o garfo da direita
        garfos[self.garfo_dir].acquire()
        print(f"[{self.nome}] pegou o garfo da DIREITA ({self.garfo_dir}).")

    def comer(self):
        """ Simula o filósofo comendo por um tempo aleatório """
        self.rodadas_comendo += 1
        print(f"[{self.nome}] está COMENDO (pela {self.rodadas_comendo}ª vez).")
        time.sleep(random.uniform(1, TEMPO_MAX_ACAO))

    def devolver_garfos(self):
        """
        Devolve os garfos (libera os locks) e avisa o "Garçom" que 
        um lugar na mesa está livre (release no semáforo).
        """
        # A ordem de devolução não importa
        garfos[self.garfo_esq].release()
        garfos[self.garfo_dir].release()
        print(f"[{self.nome}] DEVOLVEU os garfos ({self.garfo_esq}, {self.garfo_dir}).")
        
        # Libera seu lugar na mesa para outro filósofo
        garcon.release()
        print(f"[{self.nome}] LEVANTOU-SE da mesa.")


# --- Função Principal ---
def main():
    print("--- Início do Jantar dos Filósofos ---")
    print(f"{N_FILOSOFOS} filósofos, {N_FILOSOFOS} garfos, {N_FILOSOFOS - 1} lugares na mesa.")
    print("Pressione CTRL+C para encerrar a simulação.")
    print("-" * 40)

    # Cria e inicia as threads dos filósofos
    filosofos = [Filosofo(id=i) for i in range(N_FILOSOFOS)]
    
    for filosofo in filosofos:
        filosofo.start()

    # Espera que todas as threads terminem (neste caso, nunca, até o CTRL+C)
    try:
        for filosofo in filosofos:
            filosofo.join()
    except KeyboardInterrupt:
        print("\n--- Jantar encerrado pelo usuário ---")


if __name__ == "__main__":
    main()
