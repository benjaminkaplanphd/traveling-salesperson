"""
Unit tests for the etl.py module
"""
# pragma pylint: disable=redefined-outer-name
import numpy as np
import pandas as pd
import pytest

from traveling_salesperson import etl


@pytest.fixture()
def bad_filename_fixture():
    """An example of a bad filename"""
    return 'oops.csv'


def test_extract_raises_file_not_found_error_with_filename(bad_filename_fixture):
    """Ensures that the appropriate error is raised when the file does not exist."""
    with pytest.raises(FileNotFoundError):
        _ = etl.extract(filename=bad_filename_fixture)


@pytest.fixture(
    params=[(100, 100, 1), (100, 1, 100), (1, 100, 100), (1, 1, 100), (0.001, 0.001, 10000)]
)
def city_data_dict_fixture(request):
    """An example of raw and transformed city data with different scalings applied"""
    x_scale, y_scale, t_scale = request.param
    return {
        'raw': pd.DataFrame({
            'name': ['a', 'b', 'c'],
            'x': np.arange(0, 15 * x_scale, 5 * x_scale),
            'y': np.arange(0, 30 * y_scale, 10 * y_scale)
        }),
        'transformed': (
            pd.DataFrame({
                'name': ['a', 'b', 'c'],
                'x': np.arange(0, 15 * x_scale * t_scale, 5 * x_scale * t_scale),
                'y': np.arange(0, 30 * y_scale * t_scale, 10 * y_scale * t_scale)
            }), t_scale)
    }


def test_transform_scales_coordinates_correctly(city_data_dict_fixture):
    """Ensures that the transform() method returns the city data, scaled as expected"""
    raw_frame = city_data_dict_fixture['raw']
    expected_frame, expected_scale = city_data_dict_fixture['transformed']
    observed_frame, observed_scale = etl.transform(raw_frame)
    pd.testing.assert_frame_equal(observed_frame, expected_frame)
    assert observed_scale == expected_scale


def test_load_returns_expected_list(city_dataframe_fixture,
                                    cities_fixture):
    """Ensures that the load() method returns the expected list of City tuples"""
    observed_list = etl.load(city_dataframe_fixture)
    assert observed_list == cities_fixture


@pytest.mark.parametrize('series,expected_int',
                         [(pd.Series([0.01, 0.02, 0.03]), -1),
                          (pd.Series([1000, 2000, 3000]), 3)])
def test_whole_number_digits_returns_expected_int(series, expected_int):
    """Ensures that the whole_number_digits() method returns the expected integer"""
    observed_int = etl.whole_number_digits(series)
    assert observed_int == expected_int
