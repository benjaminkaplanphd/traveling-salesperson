"""
Module for plotting the result of the algorithm
"""
import os
from typing import List

import matplotlib.pyplot as plt

from traveling_salesperson import City


def plot_path(filename: str, path: List[str], cities: List[City], total_distance: int) -> None:
    """Construct and save a plot of the path connecting all cities.

    Args:
        filename: The name to use when saving the file
        path: The list of city names in the order they should be visited
        cities: The list of all City tuples
        total_distance: The total distance of the path
    """
    fig, axis = plt.subplots(1, 1, figsize=(9, 6))
    city_dict = {city.name: (city.x, city.y) for city in cities}
    x_coords, y_coords = zip(*[city_dict[city_name] for city_name in path + [path[0]]])
    axis.plot(x_coords, y_coords, 'ro', ls='-')
    axis.set_title(f'{filename} solved distance = {total_distance}')
    axis.set_xlabel('x coordinate')
    axis.set_ylabel('y coordinate')
    fig.savefig(os.path.join('results', f'{filename}_path.png'))
    plt.close(fig)
