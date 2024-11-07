# EVRPTW Gurobi Solver

Este repositório contém um solver para o *Electric Vehicle Routing Problem with Time Windows* (EVRPTW), desenvolvido como parte do meu trabalho de conclusão de curso. O solver é baseado no modelo de Schneider, Stenger e Goeke (2014) e é implementado em Python, utilizando o Gurobi como otimizador.

## Referência do Modelo

> Michael Schneider, Andreas Stenger, Dominik Goeke (2014). *The Electric Vehicle-Routing Problem with Time Windows and Recharging Stations*. Transportation Science, 48(4), 500-520.  
> [Link para o artigo](https://doi.org/10.1287/trsc.2013.0490)

## Dependências

Para executar o solver, é necessário instalar as seguintes bibliotecas:

- [**NumPy**](https://numpy.org/) — Para operações matemáticas e manipulação de arrays.
- [**Matplotlib**](https://matplotlib.org/) — Para visualização de gráficos e dados de rotas.
- [**Gurobi**](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python) — Otimizador utilizado para resolver o problema de roteamento.

## Instruções de Execução

Execute o solver com o comando abaixo no terminal:

```shell
python run.py -t {numero_de_threads} -l {tempo_em_segundos} -p {numero_de_instancias} --instances {small | large | all} -plot
```

### Descrição das Flags

- **`-l {tempo_em_segundos}`**: Define o tempo limite para a execução do solver (padrão: 500 segundos).
- **`-t {numero_de_threads}`**: Define o número de threads utilizadas pelo Gurobi (padrão: 2).
- **`-p {numero_de_instancias}`**: Número de instâncias a serem resolvidas em paralelo (padrão: 1).
- **`--instances {small | large | all}`**: Define o conjunto de instâncias (padrão: all).
- **`-plot`**: Ativa a geração de gráficos das rotas solucionadas (padrão: false).

### Exemplo de Execução

No exemplo abaixo, o solver é executado com 2 threads, resolvendo 2 instâncias em paralelo, com tempo limite de 2 horas, utilizando o conjunto de instâncias pequenas e sem geração de gráficos:

```shell
python run.py -t 2 -p 2 -l 7200 --instances small
```

> **Nota**: Verifique se todas as dependências estão instaladas e configuradas corretamente antes de iniciar o solver. Para resolver instâncias grandes, é necessário possuir uma licença do Gurobi. Caso o conjunto de instâncias não seja especificado, o solver usará o conjunto completo (`all`) por padrão. Todos os valores de flags possuem um valor padrão caso não sejam definidos na linha de comando.
