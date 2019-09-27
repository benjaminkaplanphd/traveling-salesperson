"""
Unit tests for the algorithm.py module
"""
# pragma pylint: disable=redefined-outer-name
import numpy as np
import pytest

from traveling_salesperson import algorithm


@pytest.fixture()
def pyramid_distance_matrix_fixture():
    r"""A distance matrix, corresponding to a lopsided pyramid,
    for testing the nearest neighbor algorithm

    a -- 10 --,b
     \`9   ,2 /
      \ `c   /
      11 | 10
       \ 5 /
        \|/
         d
    """
    return [
        [0, 10, 9, 11],
        [10, 0, 2, 10],
        [9, 2, 0, 5],
        [11, 10, 5, 0]
    ]


@pytest.fixture()
def sub_optimal_path_fixture():
    """A sub-optimal path, and associated distance, along the nodes of the pyramid"""
    return [0, 2, 1, 3], 9 + 2 + 10


@pytest.fixture()
def optimal_path_fixture():
    """An optimal path, and associated distance, along the nodes of the pyramid"""
    return [0, 1, 2, 3], 10 + 2 + 5


def test_nearest_neighbor_path_returns_expected_path(sub_optimal_path_fixture,
                                                     pyramid_distance_matrix_fixture):
    """Ensures that the nearest_neighbor_path returns the expected (and not necessarily optimal)
    path."""
    observed_path = algorithm.nearest_neighbor_path(4,
                                                    pyramid_distance_matrix_fixture)
    assert observed_path == sub_optimal_path_fixture


def test_nearest_neighbor_path_with_swapping_returns_expected_path(optimal_path_fixture,
                                                                   pyramid_distance_matrix_fixture):
    """Ensures that the nearest_neighbor_path_with_swapping() method finds a more optimal path
    than nearest neighbor alone, assume such  a path exists."""
    observed_path = algorithm.nearest_neighbor_path_with_swapping(4,
                                                                  pyramid_distance_matrix_fixture)
    assert observed_path == optimal_path_fixture


def test_two_node_swap_optimization_optimizes_path(sub_optimal_path_fixture,
                                                   optimal_path_fixture,
                                                   pyramid_distance_matrix_fixture):
    """Ensures that if a shorter path can be found through 2-opt swapping, the
    two_node_swap_optimization() method returns that path."""
    observed_path = algorithm.two_node_swap_optimization(sub_optimal_path_fixture[0],
                                                         pyramid_distance_matrix_fixture,
                                                         sub_optimal_path_fixture[1])
    assert np.array_equal(observed_path, optimal_path_fixture)


def test_two_node_swap_optimization_leaves_optimal_path_as_is(
        optimal_path_fixture,
        pyramid_distance_matrix_fixture):
    """Ensures that when no further optimization from swapping can be achieved, the
    two_node_swap_optimization() method leaves the path as is."""
    observed_path = algorithm.two_node_swap_optimization(optimal_path_fixture[0],
                                                         pyramid_distance_matrix_fixture,
                                                         optimal_path_fixture[1])
    assert np.array_equal(observed_path, optimal_path_fixture)


@pytest.fixture()
def expected_segments_fixture():
    """The segments along the pyramid to consider for swapping"""
    return [(0, 2), (0, 3), (1, 3)]


def test_path_segments_yields_expected_iterator(expected_segments_fixture):
    """Ensures that the path_segments() iterator yields the expected 2-tuples."""
    observed_iterator = algorithm.path_segments([], 0, 3, 2)
    for observed_segment, expected_segment in zip(observed_iterator,
                                                  expected_segments_fixture):
        assert observed_segment == expected_segment


@pytest.mark.parametrize('segment,expected_value',
                         [((0, 2), -4), ((0, 3), 0), ((1, 3), 0)])
def test_better_path_from_swap_returns_expected_bool(sub_optimal_path_fixture,
                                                     pyramid_distance_matrix_fixture,
                                                     segment, expected_value):
    """Ensures that the better_path_from_swap() method returns True, if and only if
    reversing the nodes between the two to "swap" would lead to a shorter path."""
    observed_value = algorithm.delta_if_better_path_from_swap(sub_optimal_path_fixture[0],
                                                              pyramid_distance_matrix_fixture,
                                                              *segment)
    assert observed_value == expected_value
