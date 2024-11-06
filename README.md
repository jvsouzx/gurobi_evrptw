# EVRPTW Gurobi Solver

Este repositório contém um solver para o *Electric Vehicle Routing Problem with Time Windows* (EVRPTW), desenvolvido como parte do meu trabalho de conclusão de curso. O solver, baseado no modelo proposto por Schneider, Stenger e Goeke (2014), é implementado em Python utilizando o Gurobi como otimizador.

## Referência do Modelo

> Michael Schneider, Andreas Stenger, Dominik Goeke (2014). *The Electric Vehicle-Routing Problem with Time Windows and Recharging Stations*. Transportation Science, 48(4), 500-520.  
> [https://doi.org/10.1287/trsc.2013.0490](https://doi.org/10.1287/trsc.2013.0490)

## Bibliotecas Necessárias

Para executar o solver, é necessário ter as seguintes bibliotecas instaladas:

- [**NumPy**](https://numpy.org/) — Manipulação de arrays e operações matemáticas.
- [**Matplotlib**](https://matplotlib.org/) — Visualização de gráficos e dados.
- [**Gurobi**](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python) — Solução de problemas de otimização no EVRPTW.

## Instruções de Execução

Para compilar e executar o solver, utilize o seguinte comando no terminal:

```shell
python run.py -t {tempo_em_segundos} -p
```

- **`-t {tempo_em_segundos}`**: Define o tempo limite para a execução do solver (padrão: 500 segundos).
- **`-p`**: Define se os gráficos das rotas serão gerados (padrão: `false`).

Exemplo:

```shell
python run.py -t 7200 # Define o tempo limite de 2 horas para a execução do solver e não gera os gráficos das rotas.
```

> **Nota**: Certifique-se de que todas as bibliotecas necessárias estão instaladas e configuradas antes de iniciar o solver. Para solucionar as instâncias maiores é necessária uma licensa do GUROBI.

## O Problema de Roteamento de Veículos Elétricos com Janelas de Tempo e Estações de Recarga (EVRPTW)

O EVRPTW pode ser formalmente definido da seguinte maneira:

Seja $V$ um conjunto de vértices, com $V' = V \cup F'$, onde $V = \{1,..., N\}$ denota o conjunto de clientes e $F'$ um conjunto de vértices fictícios gerados para permitir várias visitas a cada vértice no conjunto $F$ de estações de recarga.

Os vértices $0$ e $N+1$ denotam o mesmo depósito e cada rota começa em $0$ e termina em $N+1$. Para indicar que um conjunto contém a respectiva instância do depósito, o conjunto é subscrito com  $0$ e ou $N+1$, ou seja $F'_0 = F' \cup \{0\}$, $V'_0 = V' \cup \{0\}$, $V'_{N+1} = V' \cup \{N+1\}$ e $V'_{0,N+1} = V' \cup \{0\} \cup \{N+1\}$.

Assim o EVRPTW pode ser definido como um grafo direcionado completo $G = (V'_{0, N+1}, A)$, com o conjunto de arcos $A = \{(i,j)|i,j \in V'_{0, N+1}, i \neq j\}$.

A cada arco uma distância $d_{ij}$ e um tempo de viagem $t_{ij}$ são associados. Cada arco percorrido consome a quantidade $h \cdot d_{ij}$ do restante da bateria do veículo que percorre o arco, onde $h$ indica a taxa de consumo de carga constante.

Um conjunto de veículos homogêneos com capacidade máxima $C$ é posicionado no depósito. Para cada vértice $i\in V'_{0, N+1}$ é atribuída uma demanda positiva $q_i$, sendo essa demanda $0$ se $i \notin V$. Além disso, uma janela de tempo $[e_i, l_i]$ na qual o serviço deve começar está associada a cada vértice $i \in V'_{0, N+1}$ e todos os vértices $i \in V_{0, N+1}$ têm um tempo de serviço $s_i (s_0, s_{N+1} = 0)$. O serviço não pode começar antes de $e_i$, o que pode causar um tempo de espera, e não tem permissão para iniciar depois de $l_i$, mas pode terminar mais tarde do que o tempo declarado em $l_i$.

Em uma estação de carregamento, a diferença entre o nível de carga atual e a capacidade da bateria Q é recarregada com uma taxa de carregamento $g$, ou seja, o tempo de carregamento incorrido depende do nível de energia do veículo quando chega no respectivo posto de recarga.

São utilizadas variáveis de decisão associadas aos vértices para acompanhar os estados dos veículos mantendo assimm o número de variáveis necessárias baixo. A variável $\tau_i$ especifica a hora de chegada, $u_i$ a carga restante e $y_i$ o nível de carga restante na chegada ao vértice $i \in V'_{0, N+1}$. As variáveis de decisão $x_ij, i \in V'_0, j \in V'_{N+1}, i \neq j$ são binárias e iguais a 1 se o arco é percorrido e 0 caso contrário.

A função objetivo busca minimizar a distância total percorrida.

O modelo matemático do EVRPTW é formulado como um problema de programação linear inteira mista (MILP) do seguinte modo:

$\begin{equation}
\min \sum_{i \in V'_0, j \in V'_{N+1}, i \neq j} d_{ij}x_{ij}
\end{equation}$

$\begin{equation}
\sum_{j \in V'_{N+1}, i \neq j} x_{ij} = 1 \ \ \forall i \in V
\end{equation}$

$\begin{equation}
\sum_{j \in V'_{N+1}, i \neq j} x_{ij} \leq 1 \ \ \forall i \in F'
\end{equation}$

$\begin{equation}
\sum_{i \in V'_{N+1}, i \neq j} x_{ji} - \sum_{i \in V'_0, i\neq j} x_{ij} = 0 \ \ \forall j \in V'
\end{equation}$

$\begin{equation}
\tau_i + (t_{ij} + s_i)x_{ij} - l_0(1-x_{ij}) \leq \tau_j \ \ \forall i \in V_0, \forall j \in V'_{N+1}, i\neq j
\end{equation}$

$\begin{equation}
\tau_i + t_{ij}x_{ij}+ g(Q-y_i)-(l_0 +gQ)(1-x_{ij}) \leq \tau_j \ \ \forall i \in F', \forall j \in V'_{N+1}, i\neq j
\end{equation}$

$\begin{equation}
e_j \leq \tau_j \leq l_j \ \ \forall j \in V'_{0, N+1}
\end{equation}$

$\begin{equation}
0 \leq u_j \leq u_i - q_{ij}x_{ij} + C(1 - x_{ij}) \ \ \forall i \in V'_0, \forall j \in V'_{N+1}, i \neq j
\end{equation}$

$\begin{equation}
0 \leq u_0 \leq C
\end{equation}$

$\begin{equation}
0 \leq y_j \leq y_i - (h \cdot d_{ij})x_{ij} + Q(1 - x_{ij}) \ \ \forall j \in V'_{N+1}, \forall i \in V, i \neq j
\end{equation}$

$\begin{equation}
0 \leq y_j \leq Q - (h \cdot d_{ij})x_{ij} \ \ \forall j \in V'_{N+1}, \forall i \in F'_0, i \neq j
\end{equation}$

$\begin{equation}
x_{ij} \in \{0, 1\} \forall i \in V'_0, j \in V'_{N+1}, i\neq j
\end{equation}$
