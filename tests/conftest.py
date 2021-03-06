import os
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import ixmp
from ixmp.testing import create_local_testdb
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--win_ci_skip", action="store_true", default=False,
        help="weird skips for windows ci"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--win_ci_skip"):
        skip_win_ci = pytest.mark.skip(reason="weird effects on windows ci")
        for item in items:
            if "skip_win_ci" in item.keywords:
                item.add_marker(skip_win_ci)


def pytest_report_header(config, startdir):
    return 'ixmp location: {}'.format(os.path.dirname(ixmp.__file__))


@pytest.fixture(scope='session')
def test_data_path(request):
    """Path to the directory containing test data."""
    return Path(__file__).parent / 'data'


@pytest.fixture
def tutorial_path(request):
    """Path to the directory containing tutorials."""
    return Path(__file__).parent / '..' / 'tutorial'


@pytest.fixture(scope="session")
def test_mp(tmp_path_factory, test_data_path):
    """An ixmp.Platform connected to a temporary, local database.

    *test_mp* is used across the entire test session, so the contents of the
    database may reflect other tests already run.
    """
    db_path = tmp_path_factory.mktemp('test_mp')
    test_props = create_local_testdb(db_path, test_data_path / 'testdb')

    # launch Platform and connect to testdb (reconnect if closed)
    mp = ixmp.Platform(test_props)
    mp.open_db()

    yield mp


@pytest.fixture(scope="session")
def test_mp_props(tmp_path_factory, test_data_path):
    """Path to a database properties file referring to a test database."""
    db_path = tmp_path_factory.mktemp('test_mp_props')
    test_props = create_local_testdb(db_path, test_data_path / 'testdb')

    yield test_props
