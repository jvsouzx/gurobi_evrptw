import EVRPTW as evrptw
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

STATUS_CODE = {
    1: 'LOADED', 2: 'OPTIMAL', 3: 'INFEASIBLE', 4: 'INF_OR_UNBD', 5: 'UNBOUNDED',
    6: 'CUTOFF', 7: 'ITERATION_LIMIT', 8: 'NODE_LIMIT', 9: 'TIME_LIMIT', 10: 'SOLUTION_LIMIT',
    11: 'INTERRUPTED', 12: 'NUMERIC', 13: 'SUBOPTIMAL', 14: 'INPROGRESS', 15: 'USER_OBJ_LIMIT', 
    16: 'WORK_LIMIT', 17: 'MEM_LIMIT'
}

def parse_args():
    parser = argparse.ArgumentParser(description="Solver for EVRPTW instances.")
    parser.add_argument('-l', type=int, default=500, help="Time limit for solving each instance.")
    parser.add_argument('-t', type=int, default=1, help="Number of threads per instance.")
    parser.add_argument('-p', type=int, default=1, help="Number of parallel instances to solve.")
    parser.add_argument('-plot', action='store_true', help="Enable plotting of solutions.")
    parser.add_argument('--instances', choices=['small', 'large', 'all'], default='all', help="Choose instance set.")
    return parser.parse_args()

def get_instances(instance_set):
    dir_path = 'instances'
    small_instances = [file for file in os.listdir(dir_path) if file.endswith(('C5.txt', 'C10.txt', 'C15.txt'))]
    large_instances = [file for file in os.listdir(dir_path) if file.endswith('_21.txt')]
    all_instances = small_instances + large_instances
    return {
        'small': small_instances,
        'large': large_instances,
        'all': all_instances
    }.get(instance_set, all_instances)

def solve_instance(file, dir_path, threads, time_limit, plot):
    name = file.replace('.txt', '')
    path = os.path.join(dir_path, file)
    depot, recharge_stations, clients, vehicle = evrptw.read_instance(path)
    obj, status, runtime = evrptw.solver(depot, recharge_stations, clients, vehicle, name, threads, time_limit, plot)
    return f'{name},{obj:.4f},{STATUS_CODE[status]},{runtime:.4f}\n'

def main():
    args = parse_args()
    instances = get_instances(args.instances)
    dir_path = 'instances'
    
    print(f'Time Limit: {args.l}s\tThreads: {args.t}\tParallelism: {args.p}\tInstances: {args.instances}\tPlot: {args.plot}\n')

    with open('resultados.txt', 'w') as f, ThreadPoolExecutor(max_workers=min(args.p, len(instances))) as executor:
        f.write('instance,obj,status,runtime\n')
        futures = {executor.submit(solve_instance, instance, dir_path, args.t, args.l, args.plot): instance for instance in instances}
        
        for future in as_completed(futures):
            f.write(future.result())

if __name__ == '__main__':
    main()
