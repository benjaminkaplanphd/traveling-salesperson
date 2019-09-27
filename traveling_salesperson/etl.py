"""
Module to extract, transform and load city data
"""
import math
from typing import List, Tuple

import pandas as pd

from traveling_salesperson import City


def etl(filename: str, target_digits: int = 3) -> Tuple[List[City], int]:
    """Extract, transform and load the city data

    Args:
        filename: The name of the csv file with the name of each city as well as the x and y
            coordinates
        target_digits: The target number of digits of the whole number part of the coordinates.
            See the README for more discussion on this.
    Returns:
        A tuple with
            (1) a list of cities to be visited
            (2) the scaling used to transform the data
    """
    raw_frame = extract(filename)
    transformed_frame, scale = transform(raw_frame, target_digits)
    cities = load(transformed_frame)
    return cities, scale


def extract(filename: str) -> pd.DataFrame:
    """Extract the raw city data from a local file.

    Args:
        filename: The name of the local csv file
    Returns:
        A Pandas DataFrame with the raw city data
    """
    return pd.read_csv(filename)


def transform(raw_frame: pd.DataFrame, target_digits: int = 3) -> Tuple[pd.DataFrame, int]:
    """Transform the raw city data into a usable format.  Notably, scale the x and y coordinates to
    have the desired number of hole number digits.

    Args:
        raw_frame: A Pandas DataFrame with the raw city data
        target_digits: The target number of digits of the whole number part of the coordinates.
    Returns:
        A tuple with
            (1) a Pandas DataFrame with the transformed city data
            (2) the scaling used to transform the data
    """

    # 1. Determine the lesser number of whole number digits for the two coordinates
    min_digits = min(whole_number_digits(raw_frame['x']),
                     whole_number_digits(raw_frame['y']))

    # 2. We only want to scale the data up
    log10_scale = max(target_digits - min_digits, 0)
    scale = pow(10, log10_scale)

    # 3. Construct the transformed DataFrame
    transformed_frame = raw_frame.assign(
        x=raw_frame['x'] * scale,
        y=raw_frame['y'] * scale
    )

    return transformed_frame, scale


def load(transformed_frame: pd.DataFrame) -> List[City]:
    """Load the transformed data into the format needed by the TSP algorithm.

    Args:
        transformed_frame: A Pandas DataFrame with the transformed city data
    Returns:
        A list of cities to be visited
    """
    cities = transformed_frame.apply(lambda row: City(*row), axis=1).to_list()
    return cities


def whole_number_digits(series: pd.Series) -> int:
    """Determine the relevant number of whole number digits for the given series.  The standard
    deviation, as a measure of the variation of the data, is used.

    Args:
        series: A Pandas Series (of floats)
    Returns:
        The number of whole number digits associated with this series
    """
    stddev = series.std(ddof=0)
    digits = int(math.log10(stddev)) + 1
    return digits
