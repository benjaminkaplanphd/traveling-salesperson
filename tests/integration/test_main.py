"""
Integration tests for __main__.py
"""
# pragma pylint: disable=redefined-outer-name
from click.testing import CliRunner
import pytest

from traveling_salesperson import __main__ as main


def test_main_runs(mocker, filename_fixture):
    """Ensures that main() runs smoothly over a test file."""
    mock_etl = mocker.spy(main, 'etl')
    mock_distance = mocker.spy(main, 'distance_matrix')
    mock_path = mocker.spy(main, 'determine_path')
    mock_plot = mocker.spy(main, 'plot_path')

    # Test cli interface
    runner = CliRunner()
    result = runner.invoke(main.main, ['-f', filename_fixture])
    assert result.exit_code == 0

    mock_etl.assert_called_once_with(filename_fixture)
    mock_distance.assert_called_once()
    mock_path.assert_called_once()
    mock_plot.assert_called_once()


@pytest.mark.parametrize('arg_list,error_code',
                         [(['-x', 'bad_arg'], 2),  # Command line error
                          (['-m', 'de-sitter'], 2),  # Command line error
                          (['-f', 'bad_file'], 1)])  # File not found error
def test_main_fails_with_bad_argument(arg_list, error_code):
    """Ensures that main() has an error (code -1) when run with unsupported arguments."""
    runner = CliRunner()
    result = runner.invoke(main.main, arg_list)
    assert result.exit_code == error_code
