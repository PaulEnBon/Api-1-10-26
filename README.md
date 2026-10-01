# api-jeux

API REST du catalogue de jeux (FastAPI, SQLAlchemy, Pydantic).

## Installation

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt
    cp .env.example .env        # puis renseignez DATABASE_URL et CLE_SECRETE

Pour développer sans PostgreSQL, SQLite suffit : `DATABASE_URL=sqlite:///./app.db`.

## Lancer

    fastapi dev app/main.py

Documentation interactive : http://localhost:8000/docs

Avec Docker (API + PostgreSQL) :

    docker compose up --build

## Données de démonstration

    python scripts/peupler.py                       # admin@example.com / motdepasse123 + 8 jeux
    python scripts/importer.py donnees/jeux.csv     # 2 lignes invalides, volontairement
    python scripts/statistiques.py
    python scripts/exporter.py sortie.csv --genre RPG

## Vérifications

    ruff check .
    pytest
