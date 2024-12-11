# EVRPTW/VRPTW Gurobi Solver

Este repositório contém um solver para o *Electric Vehicle Routing Problem with Time Windows* (EVRPTW) e um solver para o *Vehicle Routing Problem with Time Windows* (VRPTW), desenvolvido como parte do meu trabalho de conclusão de curso. Os solvers são baseados no modelo proposto por Schneider, Stenger e Goeke (2014) e foram implementado em Python, utilizando o Gurobi (gurobipy) como otimizador.

## Referência

> Michael Schneider, Andreas Stenger, Dominik Goeke (2014). *The Electric Vehicle-Routing Problem with Time Windows and Recharging Stations*. Transportation Science, 48(4), 500-520.  
> [Link para o artigo](https://doi.org/10.1287/trsc.2013.0490)

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
- **`-vprtw`**: Define o modelo a ser solucionado (padrão: evrptw)
- **`-plot`**: Ativa a geração de gráficos das rotas solucionadas (padrão: false).

### Exemplo de Execução

No exemplo abaixo, o solver é executado com 2 threads, resolvendo 2 instâncias do EVRPTW em paralelo, com tempo limite de 2 horas, utilizando o conjunto de instâncias pequenas e sem geração de gráficos:

```shell
python run.py -t 2 -p 2 -l 7200 --instances small
```

> **Nota**:Para resolver instâncias grandes, é necessário possuir uma licença do Gurobi. Caso o conjunto de instâncias não seja especificado, o solver usará o conjunto completo (`all`) por padrão. Todos os valores de flags possuem um valor padrão caso não sejam definidos na linha de comando.
