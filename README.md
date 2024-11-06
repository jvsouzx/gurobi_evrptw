# EVRPTW Gurobi Solver

Este repositório contém um solver para o *Electric Vehicle Routing Problem with Time Windows* (EVRPTW), desenvolvido como parte do meu trabalho de conclusão de curso. O solver, baseado no modelo proposto por Schneider, Stenger e Goeke (2014), é implementado em Python utilizando o Gurobi como otimizador.

## Referência do Modelo

> Michael Schneider, Andreas Stenger, Dominik Goeke (2014). *The Electric Vehicle-Routing Problem with Time Windows and Recharging Stations*. Transportation Science, 48(4), 500-520.  
> [https://doi.org/10.1287/trsc.2013.0490](https://doi.org/10.1287/trsc.2013.0490)

## Bibliotecas Necessárias

Para executar o solver, é necessário ter as seguintes bibliotecas instaladas:

- [**NumPy**](https://numpy.org/)
- [**Matplotlib**](https://matplotlib.org/)
- [**Gurobi**](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python)

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
