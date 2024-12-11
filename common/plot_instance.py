import matplotlib.pyplot as plt
import os

def plot_result(x_c: list, y_c: list, active_arcs: list, instance: str, num_recharge_stations: int = 0):
    """    
    Plots and saves a visual representation of a routing solution.

    This function generates a scatter plot that shows the positions of a depot, 
    recharge stations, and customers. It also plots active arcs (routes) between 
    points as specified. The plot is saved as a PNG file in the 'images' folder, 
    with the file name based on the instance name.

    Args:
        x_c (list of float): x-coordinates of points (depot, recharge stations, and customers).
        y_c (list of float): y-coordinates of points (depot, recharge stations, and customers).
        active_arcs (list of tuple of int): Pairs of indices representing active arcs (connections) between points.
        instance (str): The name of the instance, used as the title of the plot and file name.
        num_recharge_stations (int): The number of recharge stations (default to 0).
    """
    if not os.path.exists('images'):
      os.makedirs('images')
    
    plt.figure()
    plt.scatter(x_c[0], y_c[0], c='red', marker='s', label='Deposit') 
    plt.scatter(x_c[1:num_recharge_stations], y_c[1:num_recharge_stations], c='green', marker='^', label='Recharge Stations')
    plt.scatter(x_c[num_recharge_stations+1:-1], y_c[num_recharge_stations+1:-1], c='black', label='Customers')
    for i, j in active_arcs:
        plt.plot([x_c[i], x_c[j]], [y_c[i], y_c[j]], ':',c='g')

    plt.legend()
    plt.title(f'{instance}')
    plt.savefig(r'images\{}.png'.format(instance), dpi = 200)
    plt.close()

