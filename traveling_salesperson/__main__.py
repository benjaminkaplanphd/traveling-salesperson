"""
Traveling Salesperson
"""
import os
from pathlib import Path
import time

import click
import numpy as np

from traveling_salesperson.algorithm import determine_path
from traveling_salesperson.etl import etl
from traveling_salesperson.geography import distance_matrix
from traveling_salesperson.plot import plot_path


@click.command()
@click.option('--metric', '-m', default='euclidean', show_default=True,
              type=click.Choice(['euclidean', 'manhattan']))
@click.option('--filename', '-f', default=os.path.join('data', 'djbouti38.csv'), show_default=True)
@click.option('--time_alg', '-t', default=True, show_default=True)
def main(metric: str = 'euclidean',
         filename: str = os.path.join('data', 'djbouti38.csv'),
         time_alg: bool = True) -> None:
    """Run the traveling-salesperson algorithm on the specified file and report the result

    Args:
        metric: the distance metric to use
        filename: the relative path to the csv file to use
        time_alg: whether or not to time the algorithm
    """

    # 1. Import the data from the named file
    cities, scale = etl(filename)

    # 2. Compute the distance between all cities
    distances = distance_matrix(cities, metric)

    # 3. Run the algorithm
    start_time = time.time() if time_alg else 0
    path, total_distance = determine_path(cities, distances)
    end_time = time.time() if time_alg else 0

    # 4. Report the results
    plot_path(Path(filename).stem, path, cities, total_distance)
    print('Total Path Length: ', total_distance / scale)
    print('Path: ', path)
    if time_alg:
        print('Time to Run: ', np.round(end_time - start_time, 3), 's')


if __name__ == '__main__':
    main()
