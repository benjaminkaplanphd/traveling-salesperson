"""
Fixtures used throughout the testing suite
"""
import os

import numpy as np
import pandas as pd
import pytest

from traveling_salesperson import City


@pytest.fixture()
def city_dataframe_fixture():
    """An example of city data"""
    return pd.DataFrame({
        'name': ['a', 'b', 'c'],
        'x': range(0, 1500, 500),
        'y': range(0, 3000, 1000)
    })


@pytest.fixture()
def cities_fixture():
    """The expected list of City tuples for the above example"""
    return [
        City('a', 0, 0),
        City('b', 500, 1000),
        City('c', 1000, 2000)
    ]


@pytest.fixture()
def distance_matrix_dict_fixture():
    """The expected distances between the example cities defined in tests/conftest.py"""
    return {
        'euclidean': np.array([
            [0, 1118, 2236],
            [1118, 0, 1118],
            [2236, 1118, 0]
        ]),
        'manhattan': np.array([
            [0, 1500, 3000],
            [1500, 0, 1500],
            [3000, 1500, 0]
        ])
    }


@pytest.fixture()
def filename_fixture():
    """The name of the cities csv file for testing"""
    return os.path.join('tests', 'fixtures', 'cities.csv')
