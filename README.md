🍽️ O Problema do Jantar dos Filósofos
Curso: Sistemas Operacionais (T303)

Professor: MSc. Felipe Jucá dos Santos
Alunos: Davi Monte Klein

🧠 Introdução

O Jantar dos Filósofos é um problema clássico da ciência da computação, proposto por Edsger Dijkstra, que ilustra os desafios da sincronização em sistemas concorrentes.

O cenário envolve cinco filósofos sentados ao redor de uma mesa circular, com cinco garfos, um entre cada par.
Cada filósofo alterna entre dois estados:

Pensar 🧩

Comer 🍝

Para comer, cada filósofo precisa dos dois garfos adjacentes — o da esquerda e o da direita.
O desafio é criar um algoritmo que permita que todos consigam comer sem que ocorra deadlock (interbloqueio) ou starvation (inanição).

Este projeto apresenta uma implementação prática em Python, utilizando a biblioteca threading.

⚙️ Estrutura da Implementação

A solução foi implementada em Python e usa threads e mecanismos de sincronização (Lock e Semaphore) da biblioteca threading.

🧩 Componentes Principais

Classe Filosofo (threading.Thread)

Representa cada filósofo como uma thread independente.

Cada filósofo tem um estado (pensando, com fome, comendo) e sabe quais garfos precisa (esquerda e direita).

Lista de Garfos (list[threading.Lock])

Cada garfo é um objeto Lock (mutex).

Antes de "pegar" o garfo, o filósofo executa garfo.acquire().

Ao liberar, chama garfo.release().

Semáforo garcon (threading.Semaphore)

O "garçom" controla o número de filósofos que podem tentar comer simultaneamente.

É inicializado com o valor N - 1 (no caso, 4 para 5 filósofos).

Garante que no máximo quatro filósofos tentem pegar garfos ao mesmo tempo, evitando o deadlock.

🔄 Ciclo de Vida de um Filósofo

Pensar (pensar())

Exibe o estado "PENSANDO" e pausa (time.sleep()) por um tempo aleatório.

Pegar Garfos (pegar_garfos())

O filósofo tenta adquirir o semáforo garcon.

Se permitido, tenta adquirir seus dois garfos (esquerda e direita).

Comer (comer())

Quando possui ambos os garfos, muda o estado para "COMENDO".

Dorme por um tempo aleatório simulando a refeição.

Devolver Garfos (devolver_garfos())

Libera os dois garfos e o semáforo (garcon.release()), permitindo que outro filósofo tente comer.

⚠️ Problemas de Sincronização
🔒 Deadlock (Interbloqueio)

Ocorre se todos os filósofos pegam primeiro o garfo à esquerda e depois tentam o da direita — nenhum consegue prosseguir, pois todos estão esperando uns pelos outros.

🍽️ Starvation (Inanição)

Mesmo sem deadlock, um filósofo pode ficar "faminto" se outros sempre conseguirem pegar os garfos antes dele.

🧩 Estratégia de Solução: O “Garçom”

A estratégia utilizada é a Bounded Concurrency (Concorrência Limitada), também chamada de solução do Garçom.

Como Funciona

O semáforo garcon é inicializado com N - 1.

Apenas 4 filósofos podem tentar pegar garfos simultaneamente.

Isso quebra a condição de espera circular, eliminando o deadlock.

Por Que Funciona

Se quatro filósofos estão sentados e seguram seus garfos esquerdos, o quinto ainda não pode se sentar (semáforo bloqueado).
Assim, pelo menos um garfo sempre estará livre, permitindo que um filósofo consiga comer e liberar recursos para os demais.

🧮 Conclusões sobre Sincronização

O Jantar dos Filósofos é uma metáfora poderosa para o gerenciamento de recursos em sistemas concorrentes.

Elemento	Representação no Mundo Real
Filósofos	Processos / Threads
Garfos	Recursos de uso exclusivo (I/O, memória, arquivos, etc.)

A solução mostra que apenas o uso de exclusão mútua não é suficiente.
É necessário controlar a concorrência global para garantir vivacidade (liveness) e segurança (safety) no sistema.

A estratégia do garçom (semáforo N−1) assegura que o sistema sempre progrida, evitando bloqueios e garantindo justiça entre os processos.

🧰 Tecnologias Utilizadas

Python 3.x

threading (Threads, Lock, Semaphore)

time e random (para simulação de tempo e comportamento assíncrono)

▶️ Como Executar
# Clone o repositório
git clone https://github.com/<seu-usuario>/<seu-repositorio>.git

# Entre na pasta do projeto
cd jantar-dos-filosofos

# Execute o programa
python jantar_dos_filosofos.py

📚 Referências

Dijkstra, E. W. Cooperating Sequential Processes (1965)

Tanenbaum, A. S. Modern Operating Systems

Stallings, W. Operating Systems: Internals and Design Principles
