import importlib
import os
from unittest import mock

import dacoolstore.config


def test_config_defaults():
    # Verify that default values are set when no environment variables are present.
    # We clear the environment dictionary during reload to ensure defaults are checked.
    with mock.patch.dict(os.environ, {}, clear=True):
        importlib.reload(dacoolstore.config)
        assert dacoolstore.config.DB_HOST == "localhost"
        assert dacoolstore.config.DB_USER == "root"
        assert dacoolstore.config.DB_PASSWORD == "######"
        assert dacoolstore.config.DB_NAME == "dacoolstore"


def test_config_custom():
    # Verify environment values override default values.
    custom_env = {
        "DB_HOST": "192.168.1.100",
        "DB_USER": "admin",
        "DB_PASSWORD": "secretpassword",
        "DB_NAME": "store_production",
    }
    with mock.patch.dict(os.environ, custom_env):
        importlib.reload(dacoolstore.config)
        assert dacoolstore.config.DB_HOST == "192.168.1.100"
        assert dacoolstore.config.DB_USER == "admin"
        assert dacoolstore.config.DB_PASSWORD == "secretpassword"
        assert dacoolstore.config.DB_NAME == "store_production"

    # Restore default configurations after test run
    importlib.reload(dacoolstore.config)
