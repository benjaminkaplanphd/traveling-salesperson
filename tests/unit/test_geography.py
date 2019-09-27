"""
Unit tests for the geography.py module
"""
# pragma pylint: disable=redefined-outer-name
import numpy as np
import pytest

from traveling_salesperson import geography


@pytest.mark.parametrize('metric', ['euclidean', 'manhattan'])
def test_distance_matrix_returns_expected_matrix(cities_fixture,
                                                 distance_matrix_dict_fixture,
                                                 metric):
    """Ensures that the distance_matrix() method returns the expected distances"""
    expected_matrix = distance_matrix_dict_fixture[metric]
    observed_matrix = geography.distance_matrix(cities_fixture, metric)
    np.testing.assert_array_equal(observed_matrix, expected_matrix)
