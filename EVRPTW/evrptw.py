import gurobipy as gp
import common as com
import numpy as np

def solver(depot: list, recharge_stations: list, clients: list, vehicle: list, instance: str, threads: int, time_limit: int, plot: bool) -> tuple[int, float, float, int, float, float]:
    """
    Solves an Electric Vehicle Routing Problem with Time Windows (EVRPTW) instance using a mixed-integer linear programming (MILP) model.

    This function constructs and optimizes an EVRPTW model that minimizes the total travel distance while respecting constraints such as battery capacity, load capacity, and time windows.
    The function takes into account the depot, clients, and recharge stations, using vehicle-specific parameters to find the optimal route.

    Args:
        depot (list): Attributes of the depot, including coordinates, time windows, and service time.
        recharge_stations (list): Attributes of recharge stations, including coordinates and time windows.
        clients (list): Attributes of the clients, such as coordinates, demand, time windows, and service time.
        vehicle (list): List of vehicle attributes:
            - Q (float): Battery capacity.
            - C (float): Load capacity.
            - h (float): Battery consumption rate.
            - g (float): Recharge rate at stations.
            - v (float): Average travel speed.
        instance (str): Identifier for the instance, used in plot title and saved file name.
        threads (int): Number of threads for the optimization solver.
        time_limit (int): Time limit in seconds for the optimization solver.
        plot (bool): If True, plots the solution path using `plot_result`.

    Returns:
        tuple: A tuple containing:
            - vehicles_used (int): Number of vehicles required.
            - m.ObjVal (float): Objective value, representing minimized total travel distance.
            - total_route_time (float): Total travel time across the solution path.
            - m.Status (int): Solver status (e.g., optimal, infeasible).
            - m.Runtime (float): Solver runtime in seconds.
            - m.MIPgap (float): Final MIP gap achieved by the solver, if applicable.
    """
    # x_c coordenada x
    # y_c coordenada y
    # q demanda
    # e início da janela de tempo
    # l fim da janela de tempo
    # s tempo de serviço
    x_c, y_c, q, e, l, s = [], [], [], [], [], []

    # Q capacidade da bateria do veículo
    # C capacidade de carga do veículo 
    # r taxa de consumo de bateria
    # g taxa de recarga 
    # v velocidade média
    Q, C, h, g, v = vehicle
    v = 52 #(média das velocidades máximas permitidas em vias urbanas (br))

    com.append_data(depot, x_c, y_c, q, e, l, s)
    com.append_data(recharge_stations, x_c, y_c, q, e, l, s, repeat=2)
    com.append_data(clients, x_c, y_c, q, e, l, s)
    com.append_data(depot, x_c, y_c, q, e, l, s)

    num_depots = len(depot)
    num_recharge_stations = len(recharge_stations)*2
    num_clients = len(clients)

    depot_0 = [0]
    depot_np1 = [num_recharge_stations+num_clients+1]
    F = [i for i in range(1, num_recharge_stations+1)]
    V = [i for i in range(num_recharge_stations+1, num_recharge_stations+num_clients+1)]
    F_0 = depot_0 + F
    V_0 = depot_0 + V
    V_line = F + V
    V_line_0 = depot_0 + V_line
    V_line_np1 = V_line + depot_np1
    V_line_0_np1 = depot_0 + F + V + depot_np1

    A = [(i, j) for i in V_line_0_np1 for j in V_line_0_np1 if i != j]
    d = {(i, j): np.hypot(x_c[i]-x_c[j], y_c[i]-y_c[j]) for i, j in A}
    t = {(i, j): (np.hypot(x_c[i]-x_c[j], y_c[i]-y_c[j]))/v for i, j in A}

    m = gp.Model()
    print(f'Running: {instance}')
    # variáveis de decisão
    tau = m.addVars(V_line_0_np1, vtype=gp.GRB.CONTINUOUS)
    u = m.addVars(V_line_0_np1, vtype=gp.GRB.CONTINUOUS)
    b = m.addVars(V_line_0_np1, vtype=gp.GRB.CONTINUOUS)
    x = m.addVars(A, vtype=gp.GRB.BINARY)

    # função objetivo
    distance =  gp.quicksum(d[i, j] * x[i, j] for i in V_line_0 for j in V_line_np1 if i != j)
    m.setObjective(
        distance,
        sense=gp.GRB.MINIMIZE)

    # restrições
    # c1 (restrição 2 no artigo)
    m.addConstrs( 
        gp.quicksum(x[i, j] for j in V_line_np1 if i!=j) == 1 for i in V)

    # c2 (restrição 3 no artigo)
    m.addConstrs(
        gp.quicksum(x[i, j] for j in V_line_np1 if i!=j) <= 1 for i in F)

    # c3 (restrição 4 no artigo)
    m.addConstrs(
        gp.quicksum(x[j, i] for i in V_line_np1 if i!=j) - gp.quicksum(x[i, j] for i in V_line_0 if i!=j) == 0 for j in V_line)

    # c4 (restrição 5 no artigo)
    m.addConstrs(
        (tau[i] + (t[i, j]+s[i])*x[i, j] - l[0]*(1 - x[i, j])) <= tau[j] for i in V_0 for j in V_line_np1 if i!=j)

    # c5 (restrição 6 no artigo)
    m.addConstrs(
        (tau[i] + t[i, j]*x[i, j] + g*(Q - b[i]) - (l[0] + g*Q)*(1 - x[i, j])) <= tau[j] for i in F for j in V_line_np1 if i!=j)

    # c6 (restrição 7 no artigo)
    m.addConstrs(tau[j] <= l[j] for j in V_line_0_np1)
    m.addConstrs(e[j] <= tau[j]  for j in V_line_0_np1)

    # c7 (restrição 8 no artigo)
    m.addConstrs(u[j] >= 0 for j in V_line_np1)
    m.addConstrs(u[j] <= u[i] - q[i]*x[i, j] + C*(1 - x[i, j]) for i in V_line_0 for j in V_line_np1 if i !=j)

    # c8 (restrição 9 no artigo)
    m.addConstr(u[0] >= 0)
    m.addConstr(u[0] <= C)

    # c9 (restrição 10 no artigo)
    m.addConstrs(b[j] >= 0 for j in V_line_np1)
    m.addConstrs(b[j] <= b[i] - (h*d[i, j])*x[i,j] + Q*(1-x[i, j]) for j in V_line_np1 for i in V if i!=j)

    # c10 (restrição 11 no artigo)
    m.addConstrs(b[j] >= 0 for j in V_line_np1)
    m.addConstrs(b[j] <= Q - (h* d[i, j])*x[i, j] for j in V_line_np1 for i in F_0 if i!=j)

    m.setParam(gp.GRB.Param.OutputFlag, 0)
    m.Params.Threads = threads
    m.setParam(gp.GRB.Param.TimeLimit, time_limit)
    m.optimize()

    if plot:
        if m.SolCount > 0:
            active_arcs = [a for a in A if x[a].X > 0.99]
            com.plot_result(x_c, y_c, active_arcs, instance, num_recharge_stations)
        else: 
            print('Don\'t find a solution!')
    
    if m.SolCount > 0:
        vehicles_used = sum(x[depot_0[0], j].X > 0.99 for j in V_line_np1)
        total_route_time = sum(t[i, j] * x[i, j].X for i, j in A if x[i, j].X > 0.99)
        recharges = []
        for j in F:
            for i in V_line_0:
                if i != j:
                    if x[i, j].X > 0.99:
                        recharge_amount = max(0, b[j].X - (b[i].X - h * d[i, j]))
                        recharges.append(recharge_amount)
                        break
        qtd_recharge = sum(recharges)

    else:
        vehicles_used = 0 
        total_route_time = 0
    
    return vehicles_used, m.ObjVal, total_route_time, qtd_recharge, m.Status, m.Runtime, m.MIPgap