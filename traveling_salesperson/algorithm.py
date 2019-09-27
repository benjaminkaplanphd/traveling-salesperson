"""
Module for the nearest-neighbor w/ 2-swapping algorithm
"""
from typing import Iterator, List, Tuple

import numpy as np

from traveling_salesperson import City


def determine_path(cities: List[City], distance_matrix: np.ndarray) -> Tuple[List[str], int]:
    """Determine the close-to-optimal path for the given list of Cities

    Args:
        cities: A list of cities to be visited visit
        distance_matrix: A symmetric matrix of distances between cities.  The i and j indexes
            correspond to the index in the original list of cities
    Returns:
        A tuple with
            (1) the list of city names, reordered to have a near-optimal (shortest) path
            (2) the total path length
    """
    path, total_distance = nearest_neighbor_path_with_swapping(len(cities), distance_matrix)
    total_distance += distance_matrix[path[-1]][path[0]]

    cities_to_visit = []
    for i in path:
        cities_to_visit.append(cities[i].name)

    return cities_to_visit, total_distance


def nearest_neighbor_path(nodes: int, distance_matrix: np.ndarray) -> Tuple[List[int], int]:
    """Determine the nearest neighbor path for a list of cities

    Args:
        nodes: The number of nodes (cities) that need to be visited
        distance_matrix: A symmetric matrix of distances between nodes.  The i and j indexes
            correspond to the index in the original list of cities
    Returns:
        A tuple with
            (1) the path according to the nearest neighbor algorithm
            (2) the total path length
    """

    def _nearest_index(_path: List[int], _distances: List[int]) -> int:
        """Helper method to determine the index of the next node to visit,
        that has not already been visited"""
        for _index in np.argsort(_distances):
            if _index not in _path:
                return _index
        raise IndexError

    path = [0]
    total_distance = 0
    while len(path) < nodes:
        current_index = path[-1]
        distances = distance_matrix[current_index]
        try:
            next_index = _nearest_index(path, distances)
            path.append(next_index)
            total_distance += distances[next_index]
        except IndexError:
            break
    return path, total_distance


def nearest_neighbor_path_with_swapping(nodes: int,
                                        distance_matrix: np.ndarray) -> Tuple[List[int], int]:
    """Determine the nearest neighbor path, after 2-opt swapping for a list of cities

    Args:
        nodes: The number of nodes (cities) that need to be visited
        distance_matrix: A symmetric matrix of distances between nodes.  The i and j indexes
            correspond to the index in the original list of cities
    Returns:
        A tuple with
            (1) the path according to the nearest neighbor algorithm, with swapping
            (2) the total path length
    """
    path, total_distance = nearest_neighbor_path(nodes, distance_matrix)
    path, total_distance = two_node_swap_optimization(path, distance_matrix, total_distance)
    return path, total_distance


def two_node_swap_optimization(path: List[int],
                               distance_matrix: np.ndarray,
                               total_distance: int) -> Tuple[List[int], int]:
    """Try swapping segments until no further improvement can be found

    Args:
        path: The starting path we want to optimize through swapping
        distance_matrix: A symmetric matrix of distances between nodes.  The i and j indexes
            correspond to the index in the original list of cities
        total_distance: the total length of the sarting path
    Returns:
        A tuple with
            (1) a path optimized with the 2-opt algorithm
            (2) the total path length
    """
    while True:
        best_swap = (0, None)
        for segment in path_segments(segment=[],
                                     start=0, end=len(path)-1,
                                     segment_length=2):
            delta = delta_if_better_path_from_swap(path, distance_matrix, *segment)
            if delta < best_swap[0]:
                best_swap = (delta, segment)
        if best_swap[0] < 0:
            i, j = best_swap[1]
            path[i + 1:j + 1] = reversed(path[i + 1:j + 1])
            total_distance += best_swap[0]
        else:
            break

    return path, total_distance


def path_segments(segment: List[int],
                  start: int,
                  end: int,
                  segment_length: int) -> Iterator[Tuple[int, ...]]:
    """Recursively build path segments (tuples of indexes)
        For example,
            path_segments([], 0, 3, 2)
            -> (0, 2), (0, 3), (1, 3)
            path_segments([], 0, 5, 3)
            -> (0, 2, 4), (0, 2, 5), (0, 3, 5), (1, 3, 5)
        Note: this is 400x times faster than using nested for loops or itertools.product

    Args:
        segment: The current segment being built
        start: The start of the index range to consider
        end: The end of the index range to consider
        segment_length: The length of the final segment (equal to the swap complexity)
    Yields:
        All possible segments of the desired length to consider for swapping
    """
    last = segment_length - 1 == 1
    for i in range(start, end):
        new_segment = segment + [i]

        if segment_length == 1:
            yield tuple(new_segment)
        else:
            yield from path_segments(new_segment, i + 2, end + last, segment_length - 1)


def delta_if_better_path_from_swap(path: List[int],
                                   distance_matrix: np.ndarray,
                                   i: int, j: int) -> int:
    """Determine if a shorter path can be achieved by swapping two nodes

    Args:
        path: The current best path
        distance_matrix: A symmetric matrix of distances between nodes.  The i and j indexes
            correspond to the index in the original list of cities
        i: the first node to swap
        j: the second node to swap
        Note that i < j
    Returns:
        A negative number indicating the reduction in path length, if a swapping i and j gives a
            shorter path, else 0
    """
    i_node = path[i]
    i_next_node = path[i+1]
    j_node = path[j]
    j_next_node = path[(j+1) % len(path)]
    current_distance = (distance_matrix[i_node][i_next_node]
                        + distance_matrix[j_node][j_next_node])
    swapped_distance = (distance_matrix[i_node][j_node]
                        + distance_matrix[i_next_node][j_next_node])
    return min(0, swapped_distance - current_distance)
