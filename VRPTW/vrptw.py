import gurobipy as gp
import common as com
import numpy as np

def solver(depot: list, clients: list, vehicle: list, instance: str, threads: int, time_limit: int, plot: bool) -> tuple[int, float, float, int, float]:
    x_c, y_c, q, e, l, s = [], [], [], [], [], []
    Q, C, h, g, v = vehicle
    # velocidade média (52.5 km/h)
    v = 52.5
    
    com.append_data(depot, x_c, y_c, q, e, l, s)
    com.append_data(clients, x_c, y_c, q, e, l, s)
    com.append_data(depot, x_c, y_c, q, e, l, s)

    num_depots = len(depot)
    num_clients = len(clients)

    depot_0 = [0]
    depot_np1 = [num_clients + 1]
    V = [i for i in range(1, num_clients + 1)]
    V_0 = depot_0 + V
    V_line_np1 = V + depot_np1
    V_line_0_np1 = depot_0 + V + depot_np1

    A = [(i, j) for i in V_line_0_np1 for j in V_line_0_np1 if i != j]
    d = {(i, j): np.hypot(x_c[i]-x_c[j], y_c[i] - y_c[j]) for i, j in A}
    t = {(i, j): d[i, j]/v for i, j in A}

    m = gp.Model()
    print(f'Running: {instance}')
    # variáveis de decisão
    tau = m.addVars(V_line_0_np1, vtype=gp.GRB.CONTINUOUS)
    u = m.addVars(V_line_0_np1, vtype=gp.GRB.CONTINUOUS)
    x = m.addVars(A, vtype=gp.GRB.BINARY)

    # função objetivo
    # eq 1
    m.setObjective(
        gp.quicksum(d[i, j] * x[i, j] for i in V_0 for j in V_line_np1 if i!=j),
        sense = gp.GRB.MINIMIZE)
    
    # restrições
    # eq 2
    m.addConstrs(
    gp.quicksum(x[i, j] for j in V_line_np1 if i!=j) == 1 for i in V)

    # eq 4
    m.addConstrs(
    gp.quicksum(x[j, i] for i in V_line_np1 if i!=j) - gp.quicksum(x[i, j] for i in V_0 if i!=j) == 0 for j in V)

    # eq 5
    m.addConstrs(
    (tau[i] + (t[i, j]+s[i])*x[i, j] - l[0]*(1 - x[i, j])) <= tau[j] for i in V_0 for j in V_line_np1 if i!=j)

    # eq 7
    m.addConstrs(tau[j] <= l[j] for j in V_line_0_np1)
    m.addConstrs(e[j] <= tau[j]  for j in V_line_0_np1)

    # eq 8
    m.addConstrs(u[j] >= 0 for j in V_line_np1)
    m.addConstrs(u[j] <= u[i] - q[i]*x[i, j] + C*(1 - x[i, j]) for i in V_0 for j in V_line_np1 if i !=j)

    # eq 9 
    m.addConstr(u[0] >= 0)
    m.addConstr(u[0] <= C)

    m.setParam(gp.GRB.Param.OutputFlag, 0)
    m.Params.Threads = threads
    m.setParam(gp.GRB.Param.TimeLimit, time_limit)
    m.optimize()

    if plot:
        if m.SolCount > 0:
            active_arcs = [a for a in A if x[a].X > 0.99]
            com.plot_result(x_c, y_c, active_arcs, instance)
        else: 
            print('Don\'t find a solution!')

    if m.SolCount > 0:
        vehicles_used = sum(x[depot_0[0], j].X > 0.99 for j in V_line_np1)
        total_route_time = sum(t[i, j] * x[i, j].X for i, j in A if x[i, j].X > 0.99)
    else:
        vehicles_used = 0
        total_route_time = 0
    
    return vehicles_used, m.ObjVal, total_route_time, m.Status, m.Runtime, m.MIPgap