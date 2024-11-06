import EVRPTW as evrptw
import os
import sys

STATUS_CODE = {
    1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED',
    6:'CUTOFF', 7:'ITERATION_LIMIT', 8:'NODE_LIMIT', 9:'TIME_LIMIT', 10:'SOLUTION_LIMIT',
    11:'INTERRUPTED', 12:'NUMERIC', 13:'SUBOPTIMAL', 14:'INPROGRESS', 15:'USER_OBJ_LIMIT', 
    16:'WORK_LIMIT', 17:'MEM_LIMIT'
}

PLOT = '-p' in sys.argv

if '-t' in sys.argv:
    try:
        TIME_LIMIT = sys.argv[sys.argv.index('-t') + 1]
    except IndexError:
        print('Um valor deve ser fornecido após "-t"')
        sys.exit(1)
else:
    TIME_LIMIT = 500

dir = 'instances'
files = [file for file in os.listdir(dir) if file.endswith(('C5.txt', 'C10.txt', 'C15.txt', '_21.txt'))]
print(f'Time Limit: {TIME_LIMIT}s\tPlot: {PLOT}\n')

with open('resultados.txt', 'w') as f:
    f.write('Instance,Obj,Status,Runtime\n')
    for file in files:
        instance = file.replace('.txt', '')
        path = dir + '/' + file
        depot, recharge_stations, clients, vehicle = evrptw.read_instance(path)
        obj, status, runtime = evrptw.solver(depot, recharge_stations, clients, vehicle, instance, TIME_LIMIT, PLOT)
        f.write(f'{instance},{obj:.4f},{STATUS_CODE[status]},{runtime:.4f}\n')