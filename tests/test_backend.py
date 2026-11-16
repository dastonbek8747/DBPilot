"""Tests for DBPilot backend.

These tests exercise real code paths: password hashing, session-id
generation, request validation and database connectivity helpers.
They do not call any LLM, so no API key is required.
"""
import os
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from hashing_password import generate_session_id, hashing_password, verify_password  # noqa: E402
from schemas import ChatAgent, LoginUser, RegisterUser  # noqa: E402


def test_password_hash_is_not_plaintext():
    hashed = hashing_password("s3cret-password")
    assert hashed != "s3cret-password"
    assert hashed.startswith("$argon2")


def test_password_verify_roundtrip():
    hashed = hashing_password("s3cret-password")
    assert verify_password("s3cret-password", hashed) is True


def test_password_verify_rejects_wrong_password():
    hashed = hashing_password("s3cret-password")
    assert verify_password("wrong-password", hashed) is False


def test_verify_password_handles_garbage_hash():
    assert verify_password("anything", "not-a-real-hash") is False


def test_session_id_is_unique():
    ids = {generate_session_id() for _ in range(50)}
    assert len(ids) == 50


def test_register_schema_rejects_short_password():
    with pytest.raises(Exception):
        RegisterUser(username="doston", email="a@b.com", password="short")


def test_register_schema_rejects_bad_email():
    with pytest.raises(Exception):
        RegisterUser(username="doston", email="not-an-email", password="longenough1")


def test_register_schema_accepts_valid_payload():
    user = RegisterUser(username="doston", email="a@b.com", password="longenough1")
    assert user.email == "a@b.com"


def test_login_schema_requires_email_and_password():
    with pytest.raises(Exception):
        LoginUser(email="a@b.com")
    ok = LoginUser(email="a@b.com", password="longenough1")
    assert ok.password == "longenough1"


def test_chat_agent_schema_fields():
    req = ChatAgent(session_id="abc", database_url="sqlite:///x.db", request="how many orders?")
    assert req.request == "how many orders?"


def test_check_conn_db_sqlite(tmp_path):
    """check_conn_db must report success for a real SQLite file."""
    from db_conn import check_conn_db

    db_file = tmp_path / "sample.db"
    sqlite3.connect(str(db_file)).close()

    result = check_conn_db(
        db_password="",
        db_name=str(db_file),
        db_user="",
        db_host="",
        db_port="",
        driver_name="sqlite",
    )
    assert result["db_conn"] is True


def test_get_database_returns_sql_database(tmp_path):
    """get_database must wrap a SQLite file into a LangChain SQLDatabase."""
    from db_conn import get_database

    db_file = tmp_path / "sample.db"
    con = sqlite3.connect(str(db_file))
    con.execute("CREATE TABLE dishes (id INTEGER PRIMARY KEY, name TEXT)")
    con.execute("INSERT INTO dishes (name) VALUES ('Osh')")
    con.commit()
    con.close()

    db = get_database(f"sqlite:///{db_file}")
    assert "dishes" in db.get_usable_table_names()
