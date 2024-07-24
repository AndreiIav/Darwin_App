import logging
import os
from unittest.mock import Mock

import pytest
from flask import current_app

import application
from application import init_app, run_warm_up_queries


def test_run_warm_up_queries_runs(test_client, caplog):
    caplog.set_level(logging.INFO)

    run_warm_up_queries(current_app, "test.db")

    assert "warm_up query 1 executed" in caplog.text
    assert "warm_up query 2 executed" in caplog.text


def test_run_warm_up_queries_error(test_client, monkeypatch, tmp_path, caplog):
    caplog.set_level(logging.INFO)
    # Set the DATABASE_FOLDER to use tmp_path
    monkeypatch.setitem(current_app.config, "DATABASE_FOLDER", tmp_path)

    run_warm_up_queries(current_app, "not_existing.db")

    assert (
        "warm_up queries not executed in run_warm_up_queries() because of sqlite3.Error:"
        in caplog.text
    )


run_warm_up_queries_configs = [
    ("config.DevelopmentConfig"),
    ("config.ProductionConfig"),
]


@pytest.mark.parametrize("configs", run_warm_up_queries_configs)
def test_init_app_calls_run_warm_up_queries(monkeypatch, configs):
    run_warm_up_queries_mock = Mock()
    monkeypatch.setattr(application, "run_warm_up_queries", run_warm_up_queries_mock)
    os.environ["CONFIG_TYPE"] = configs

    init_app()

    run_warm_up_queries_mock.assert_called()


do_not_run_warm_up_queries_configs = [
    ("config.TestingConfig"),
    ("config.DemoConfig"),
]


@pytest.mark.parametrize("configs", do_not_run_warm_up_queries_configs)
def test_init_app_does_not_call_run_warm_up_queries(monkeypatch, configs):
    run_warm_up_queries_mock = Mock()
    monkeypatch.setattr(application, "run_warm_up_queries", run_warm_up_queries_mock)
    os.environ["CONFIG_TYPE"] = configs

    init_app()

    run_warm_up_queries_mock.assert_not_called()
