def read_instance(file: str) -> tuple[list[list], list[list], list[list], list]:
    """
    Reads an instance file and parses information about nodes and vehicles.

    This function reads a file containing data for a Electric Vehicle Routing 
    Problem with Time Windows (EVRPTW) instance. 
    The file is divided into two blocks: the first block provides information 
    about the nodes (depot, recharge stations, and clients), and the second 
    block provides information about the vehicles. 

    Args:
        file (str): The path to the instance file to be read.

    Returns:
        tuple: A tuple containing four lists:
            - depot (list of list): A list of coordinates for the depot node.
            - recharge_stations (list of list): A list of coordinates for each recharge station.
            - clients (list of list): A list of coordinates for each client node.
            - vehicle (list): A list of attributes for each vehicle, extracted from the second block.
    """
    # Divide o arquivo de instância em dois blocos, 
    # o primeiro contém informações sobre os nós do grafo e o segundo informações sobre os veículos
    with open(file, 'r') as f:
        blocks = [block.splitlines() for block in f.read().strip().split('\n\n')]
    
    depot = []
    recharge_stations = []
    clients = []
    
    # para cada linha do primeiro bloco, excluindo a primeira (cabeçalho), lê os valores e atribui às respectivas listas
    for row in blocks[0][1:]:
        values = row.strip().split()
        if values[1] == 'd':
            depot.append([float(i) for i in values[2:]])
        elif values[1] == 'f':
            recharge_stations.append([float(i) for i in values[2:]])
        elif values[1] == 'c':
            clients.append([float(i) for i in values[2:]])
            
    # para cada linha do segundo bloco, lê os atributos dos veículos        
    vehicle = [float(row.split()[-1].replace('/', '')) for row in blocks[1]]
    
    return depot, recharge_stations, clients, vehicle

def append_data(source: list, x_c: list, y_c: list, q: list, e: list, l: list, s: list, repeat: int=1):
    """
    Appends data from a source list to specified lists.

    This function takes a source list of rows, where each row contains information 
    about a location or node. Each element in a row represents specific data that 
    will be appended to its respective list: `x_c` for x-coordinates, `y_c` for y-coordinates, 
    `q` for demand, `e` for start of time window, `l` for end of time window, and `s` 
    for service time. The appending operation can be repeated multiple times.

    Args:
        source (list of list): A list of rows, where each row is a list containing 
            six elements in the following order: x-coordinate, y-coordinate, demand, 
            start of time window, end of time window, and service time.
        x_c (list): List to append x-coordinates from each row.
        y_c (list): List to append y-coordinates from each row.
        q (list): List to append demands from each row.
        e (list): List to append start of time windows from each row.
        l (list): List to append end of time windows from each row.
        s (list): List to append service times from each row.
        repeat (int, optional): Number of times to repeat the appending operation 
            for each row in `source`. Defaults to 1.

    Returns:
        None
    """
    for _ in range(repeat):
        for row in source:
            x_c.append(row[0])
            y_c.append(row[1])
            q.append(row[2])
            e.append(row[3])
            l.append(row[4])
            s.append(row[5])