"""
Functions tests for the etl.py module
"""
# pragma pylint: disable=redefined-outer-name
import pandas as pd

from traveling_salesperson import etl


def test_extract_reads_file_correctly(city_dataframe_fixture,
                                      filename_fixture):
    """Ensures that the extract() method reads in the data as expected"""
    observed_frame = etl.extract(filename_fixture)
    pd.testing.assert_frame_equal(observed_frame, city_dataframe_fixture)
