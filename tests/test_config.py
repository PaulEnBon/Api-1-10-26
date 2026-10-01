"""Tests de la configuration — séance 7, partie 3."""

import pytest

from app.config import Configuration


@pytest.mark.parametrize(
    "valeur, attendu",
    [
        ("http://localhost:5173", ["http://localhost:5173"]),
        ("http://a.com, http://b.com", ["http://a.com", "http://b.com"]),
        ('["http://a.com", "http://b.com"]', ["http://a.com", "http://b.com"]),
    ],
)
def test_origines_lues_depuis_l_environnement(monkeypatch, valeur, attendu):
    """Le format de `.env.example` et de `docker-compose.yml` doit démarrer."""
    monkeypatch.setenv("ORIGINES_AUTORISEES", valeur)

    assert Configuration(_env_file=None).origines_autorisees == attendu


def test_url_postgres_normalisee(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://u:p@hote:5432/base")

    assert Configuration(_env_file=None).database_url.startswith("postgresql+psycopg://")
