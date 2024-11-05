import gurobipy as gp
import EVRPTW as evrptw
import numpy as np

def solver(depot: list, recharge_stations: list, clients: list, vehicle: list, instance: str, time_limit: int = 500, plot: bool = False) -> tuple[float, int, float]:
    """
    Solves an Electric Vehicle Routing Problem with Time Windows (EVRPTW) instance using a mixed-integer linear programming (MILP) model.

    This function constructs and solves an optimization model for an EVRPTW problem,
    considering factors such as battery capacity, demand, recharge stations, and time windows.
    It minimizes the total travel distance while meeting time windows and other constraints
    on battery consumption and load capacity.

    Args:
        depot (list): List of depot attributes, including coordinates, time windows, and service time.
        recharge_stations (list): List of recharge station attributes, with coordinates and time windows.
        clients (list): List of client attributes, including coordinates, demand, time windows, and service time.
        vehicle (list): List containing the vehicle attributes:
            - Q (float): Battery capacity of the vehicle.
            - C (float): Load capacity of the vehicle.
            - h (float): Battery consumption rate.
            - g (float): Recharge rate at recharge stations.
            - v (float): Average travel speed.
        instance (str): Name or identifier of the instance, used in plot title and saved file name.
        time_limit (int, optional): Time limit for the optimization solver in seconds. Defaults to 500.
        plot (bool, optional): If True, plots the solution path using `plot_result` function. Defaults to False.

    Returns:
        tuple: A tuple containing the following elements:
            - m.ObjVal (float): Objective value of the solved model, representing the minimized total travel distance.
            - m.Status (int): Status of the optimization model (e.g., optimal, infeasible).
            - m.Runtime (float): Time taken by the solver to find the solution.
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

    evrptw.append_data(depot, x_c, y_c, q, e, l, s)
    evrptw.append_data(recharge_stations, x_c, y_c, q, e, l, s, repeat=2)
    evrptw.append_data(clients, x_c, y_c, q, e, l, s)
    evrptw.append_data(depot, x_c, y_c, q, e, l, s)

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

    # c6 (restrição no artigo 7)
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
    m.setParam(gp.GRB.Param.TimeLimit, time_limit)
    m.optimize()

    if plot:
        active_arcs = [a for a in A if x[a].X > 0.99]
        evrptw.plot_result(x_c, y_c, active_arcs, num_recharge_stations, instance)
    
    return m.ObjVal, m.Status, m.Runtime