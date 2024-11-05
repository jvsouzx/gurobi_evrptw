import EVRPTW as evrptw
import os

STATUS_CODE = {
    1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED',
    6:'CUTOFF', 7:'ITERATION_LIMIT', 8:'NODE_LIMIT', 9:'TIME_LIMIT', 10:'SOLUTION_LIMIT',
    11:'INTERRUPTED', 12:'NUMERIC', 13:'SUBOPTIMAL', 14:'INPROGRESS', 15:'USER_OBJ_LIMIT', 
    16:'WORK_LIMIT', 17:'MEM_LIMIT'
}
TIME_LIMIT = 7200 # 2horas - tempo limite

dir = 'instances'
files = [file for file in os.listdir(dir) if file.endswith(('C5.txt'))] # 'C5.txt', 'C10.txt', 'C15.txt', '_21.txt'

with open('resultados.txt', 'w') as f:
    f.write('Instance,Obj,Status,Runtime\n')
    for file in files:
        print(f'Running: {file}')
        instance = file.replace('.txt', '')
        path = dir + '/' + file
        depot, recharge_stations, clients, vehicle = evrptw.read_instance(path)
        obj, status, runtime = evrptw.solver(depot, recharge_stations, clients, vehicle, instance, TIME_LIMIT, True)
        f.write(f'{instance},{obj:.4f},{STATUS_CODE[status]},{runtime:.4f}\n')