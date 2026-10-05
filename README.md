# API Catalogue de jeux

API REST qui gère un catalogue de jeux vidéo, leurs éditeurs et les comptes de
leurs contributeurs. Elle sert le front du catalogue. Construite avec FastAPI,
SQLAlchemy et Pydantic.

## Prérequis

- **Python 3.12**, la version utilisée par la CI et l'image Docker.
  Vérifiez avec `python3.12 --version` (Windows : `py -3.12 --version`).
- **Git**.
- Aucune base à installer pour démarrer : SQLite est fourni avec Python.
  PostgreSQL 16 n'est utile que pour la variante Docker.

## Démarrage rapide

Toutes les commandes se lancent depuis la racine du dépôt cloné.

```bash
# 1. Créer et activer l'environnement virtuel
python3.12 -m venv .venv         # Windows : py -3.12 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate

# 2. Installer les dépendances (application, tests et linter)
pip install -r requirements-dev.txt

# 3. Créer le fichier de configuration
cp .env.example .env             # Windows : copy .env.example .env
```

Ouvrez `.env` et modifiez deux lignes :

```ini
DATABASE_URL=sqlite:///./app.db
CLE_SECRETE=collez-ici-la-cle-generee
```

La clé se génère avec `python -c "import secrets; print(secrets.token_urlsafe(32))"`.

```bash
# 4. Remplir la base avec le catalogue de démonstration
python scripts/peupler.py

# 5. Lancer l'API
fastapi dev app/main.py
```

Une fois l'environnement activé, `(.venv)` précède l'invite du terminal, et
`python` désigne Python 3.12 sur tous les systèmes.

Résultat attendu :

- l'étape 4 affiche `Administrateur créé : admin@example.com`, puis
  `Jeux créés : 8 — déjà présents : 0` ;
- l'étape 5 affiche `Server started at http://127.0.0.1:8000` ;
- http://127.0.0.1:8000/docs affiche la liste des routes, rangées par
  rubrique : Système, Authentification, Mon compte, Jeux, Éditeurs…

Le compte de démonstration est `admin@example.com` / `motdepasse123`
(rôle `admin`). Ne l'utilisez jamais hors de votre poste.

Si le lancement échoue avec `ValidationError: 2 validation errors for
Configuration` et `Field required`, le fichier `.env` est absent ou n'est pas
à la racine du dépôt.

### Variante : avec Docker

Prérequis : Docker et Docker Compose. Cette variante lance l'API et une base
PostgreSQL 16, sans environnement virtuel.

```bash
docker compose up --build
```

L'API répond sur http://localhost:8000/docs. La base démarre vide.

## Configuration

L'API lit ses variables dans l'environnement, puis dans le fichier `.env`
(voir `app/config.py`). Sans l'une des deux variables obligatoires, l'API
refuse de démarrer.

| Variable | Rôle | Obligatoire | Valeur par défaut |
|---|---|---|---|
| `DATABASE_URL` | Adresse de la base. `sqlite:///./app.db` en local ; `postgresql+psycopg://utilisateur:motdepasse@hote:5432/base` pour PostgreSQL. Une adresse `postgres://` est convertie automatiquement. | oui | aucune |
| `CLE_SECRETE` | Signe les jetons de connexion. Qui la détient peut se fabriquer un jeton d'administrateur : une clé différente par environnement, jamais versionnée. | oui | aucune |
| `ALGORITHME_JETON` | Algorithme de signature des jetons JWT. | non | `HS256` |
| `DUREE_JETON_MINUTES` | Durée de validité d'un jeton, en minutes. | non | `30` |
| `ORIGINES_AUTORISEES` | Origines autorisées par CORS (le front), séparées par des virgules ou en liste JSON. | non | `http://localhost:5173` |
| `ENVIRONNEMENT` | Nom de l'environnement, affiché par `/sante` et dans les journaux. | non | `developpement` |
| `NIVEAU_JOURNAL` | Niveau des journaux : `DEBUG`, `INFO`, `WARNING`, `ERROR`. | non | `INFO` |
| `ECHO_SQL` | `true` affiche chaque requête SQL dans la console. | non | `false` |
| `MAX_TENTATIVES_CONNEXION` | Échecs de connexion tolérés pour un email avant le refus `429`. | non | `5` |
| `FENETRE_TENTATIVES_MINUTES` | Durée, en minutes, pendant laquelle les échecs sont comptés. | non | `15` |

## Utilisation

La documentation complète des routes, avec leurs formats, est générée par
FastAPI : http://127.0.0.1:8000/docs. Le bouton **Authorize** permet d'y
tester les routes protégées.

Les routes métier sont préfixées par `/api/v1`. Trois exemples, API lancée et
base peuplée :

```bash
# Les trois jeux les mieux notés (lecture publique)
curl "http://127.0.0.1:8000/api/v1/jeux?tri=note&limite=3"
# -> {"elements":[{"id":7,"titre":"Portal 2","genre":"Réflexion","note":10}, …],"total":8, …}

# Obtenir un jeton (formulaire OAuth2 : l'email va dans `username`)
curl -X POST http://127.0.0.1:8000/api/v1/connexion \
  -d "username=admin@example.com&password=motdepasse123"
# -> {"access_token":"eyJhbGciOi…","token_type":"bearer"}

# Créer un jeu, avec le jeton obtenu
curl -X POST http://127.0.0.1:8000/api/v1/jeux \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"titre": "Outer Wilds", "genre": "Aventure", "note": 10, "annee": 2019}'
# -> 201, le jeu créé avec son identifiant. Sans jeton : 401 NON_AUTHENTIFIE.
```

Sous Windows, ces commandes écrites pour bash ne passent pas telles quelles
(guillemets, `\` en fin de ligne) : testez les mêmes routes depuis `/docs`.

Des scripts complètent l'API, à lancer depuis la racine, environnement activé :

```bash
python scripts/importer.py donnees/jeux.csv     # 2 lignes invalides, volontairement
python scripts/statistiques.py                  # rapport du catalogue
python scripts/exporter.py sortie.csv --genre RPG
```

## Tests

```bash
pytest          # résultat attendu : « N passed », aucun « failed »
ruff check .    # résultat attendu : « All checks passed! »
```

Les tests utilisent une base SQLite en mémoire : ni `.env` ni `app.db` ne
sont touchés. La CI (`.github/workflows/verifications.yml`) lance les deux sur chaque pull
request et sur chaque push sur `main`.

## Architecture

Une requête traverse quatre couches, toujours dans le même sens. Chaque couche
n'appelle que celle du dessous : un service ne connaît pas HTTP, un dépôt ne
décide de rien.

```mermaid
flowchart LR
    Client["Client HTTP<br/>front, curl, /docs"] -->|JSON| Routeurs
    Scripts["scripts/"] --> Services
    Scripts --> Depots
    Routeurs["routeurs/<br/>routes HTTP"] --> Services["services/<br/>règles métier"]
    Services --> Depots["depots/<br/>requêtes SQL"]
    Depots --> Tables["tables/<br/>modèles SQLAlchemy"]
    Tables --> Base[("SQLite ou<br/>PostgreSQL")]
    Routeurs -. "valident avec" .-> Modeles["modeles/<br/>schémas Pydantic"]
```

| Dossier ou fichier | Rôle |
|---|---|
| `app/main.py` | Assemble l'application : middlewares, format des erreurs, routeurs. |
| `app/routeurs/` | Les routes HTTP : lisent la requête, appellent un service, renvoient la réponse. |
| `app/services/` | Les règles métier ; lèvent les exceptions de `app/exceptions.py`. |
| `app/depots/` | L'accès aux données : lectures et écritures SQL, sans aucune règle métier. |
| `app/tables/` | Les tables de la base (modèles SQLAlchemy). |
| `app/modeles/` | La forme de ce qui entre et sort de l'API (modèles Pydantic). |
| `app/config.py` | La configuration, validée au démarrage. |
| `app/dependances.py` | Ce que FastAPI prépare avant une route : session, utilisateur connecté, pagination. |
| `app/securite.py` | Hachage des mots de passe (bcrypt) et jetons JWT. |
| `scripts/` | Outils en ligne de commande : peupler, importer, exporter, statistiques. |
| `tests/` | Les tests pytest, dont `test_architecture.py` qui vérifie le sens des couches. |

Exception connue : `app/routeurs/administration.py` appelle encore les dépôts
directement, sans passer par un service.

## Contribuer

1. Une issue décrit le besoin ou le bug.
2. Une branche par issue, créée depuis un `main` à jour :
   `type/numero-description`, par exemple `fix/7-tri-par-note`.
3. Des commits au format Conventional Commits : `fix(jeux): trier par note`.
4. Une pull request décrit le contexte, les changements, l'impact et comment
   tester, et ferme l'issue avec `Closes #numero`.
5. Un autre membre de l'équipe la relit ; la CI doit être verte.
6. Fusion par **Squash and merge**, puis suppression de la branche.

On ne pousse jamais directement sur `main`.
