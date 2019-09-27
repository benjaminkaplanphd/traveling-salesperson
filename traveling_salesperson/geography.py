"""
Module for deriving the relevant geography (distance matrix)
"""
from itertools import product
import math
from typing import List

import numpy as np

from traveling_salesperson import City


def distance_matrix(cities: List[City], distance_metric_key: str = 'euclidean'):
    """Compute the matrix of distances between all cities, using the named distance metric.

    Args:
        cities: A list of cities to be visited visit
        distance_metric_key: The name of the distance metric to use
    Returns:
        A symmetric matrix of distances between cities.  The i and j indexes correspond to the index
            in the original list of cities
    """
    distance_metric_dict = {
        'euclidean': _euclidean_distance,
        'manhattan': _manhattan_distance
    }
    distance_metric = distance_metric_dict[distance_metric_key]

    distances = np.zeros((len(cities), len(cities)))

    for (i, start), (j, end) in product(enumerate(cities), repeat=2):
        if j <= i:
            continue
        distances[i][j] = distances[j][i] = distance_metric(start, end)
    return distances


def _euclidean_distance(city_a: City, city_b: City) -> int:
    """Helper method to compute the euclidean distance between two cities, rounded to the nearest
    integer."""
    delta_x = city_a.x - city_b.x
    delta_y = city_a.y - city_b.y
    return round(math.sqrt(pow(delta_x, 2) + pow(delta_y, 2)))


def _manhattan_distance(city_a: City, city_b: City) -> int:
    """Helper method to compute the manhattan distance between two cities, rounded to the nearest
    integer."""
    delta_x = abs(city_a.x - city_b.x)
    delta_y = abs(city_a.y - city_b.y)
    return int(delta_x + delta_y)
