"""
Integration tests for the algorithm.py module
"""
# pragma pylint: disable=redefined-outer-name
import pytest

from traveling_salesperson import algorithm


@pytest.fixture()
def expected_city_names_fixture():
    """A set of city names that must be in the path"""
    return {'b', 'a', 'c'}


@pytest.mark.parametrize('metric', ['euclidean', 'manhattan'])
def test_algorithm_returns_valid_pick_list(cities_fixture,
                                           distance_matrix_dict_fixture,
                                           expected_city_names_fixture,
                                           metric):
    """Ensure that the determine_path() method returns a valid list of cities, i.e. it contains
    every city once"""
    path, _ = algorithm.determine_path(cities_fixture,
                                       distance_matrix_dict_fixture[metric])
    assert set(path) == expected_city_names_fixture
