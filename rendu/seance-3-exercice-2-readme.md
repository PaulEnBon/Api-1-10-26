# Séance 3 · Exercice 2 — Le README

> Le nouveau `README.md` est à la racine de cette branche. Il a été suivi à la
> lettre le 05/10/2026 dans un dossier vide (clone neuf, Python 3.12.3) :
> installation, `.env` en SQLite, `scripts/peupler.py`, `fastapi dev`, `/docs`,
> connexion, création d'un jeu, scripts, `pytest` et `ruff`. Tout fonctionne.
> Le schéma Mermaid a été rendu avec `mermaid-cli` : la syntaxe est valide.
>
> **Non testé** : la variante `docker compose up --build` (pas de démon Docker
> dans l'environnement de test) et les variantes Windows. À vérifier avant de
> pousser, ou à retirer.

---

## 2.1 — Les défauts relevés à l'oral

### Le README actuel du dépôt (avant cette séance)

1. **Le démarrage rapide échoue tel quel.** `cp .env.example .env` garde
   `DATABASE_URL` sur un PostgreSQL local que le lecteur n'a pas : `/docs`
   s'affiche, mais `/sante` répond 503 et `GET /api/v1/jeux` répond 500
   (testé). L'astuce SQLite arrive *après*, en une phrase, sans dire quelle
   ligne modifier.
2. **Aucun résultat attendu.** Après `fastapi dev`, rien ne dit à quoi
   ressemble la réussite ; le lecteur ne sait pas s'il a réussi.
3. **Ni prérequis ni Windows.** Aucune version de Python (la CI et l'image
   Docker utilisent 3.12), et `source .venv/bin/activate` ne fonctionne pas
   sous Windows.

Manquent aussi : la configuration (aucune variable expliquée en dehors de
`.env.example`), l'architecture et la façon de contribuer. Le mot de passe de
démonstration est donné sans avertissement.

### Le second mauvais README (« API Jeux 🎮🎮🎮 »)

Les trois plus graves :

1. **Des secrets réels publiés.** Une `DATABASE_URL` de **production** avec
   son mot de passe (`admin:Jeux2024!@db.monprojet.fr/prod`) et une
   `CLE_SECRETE` qui a l'air vraie : quiconque lit le dépôt peut ouvrir la
   base et se fabriquer un jeton d'administrateur. Il faut changer ces deux
   secrets tout de suite ; les retirer du README ne suffit pas, ils restent
   dans l'historique Git.
2. **Des commandes fausses.** `pip install fastapi uvicorn sqlalchemy` ignore
   `requirements.txt` et ses versions ; `uvicorn main:app` vise un module qui
   n'existe pas (l'application est `app/main.py`). Et « il suffit de » fait
   croire au lecteur que l'échec vient de lui.
3. **Il recopie ce qui est généré, et raconte au lieu d'expliquer.** Quarante
   lignes de routes, déjà fournies par FastAPI à `/docs`, qui seront fausses
   à la prochaine route ajoutée ; un historique (« en 2024… Flask… ») qui
   relève d'un ADR ; et un résultat attendu en capture d'écran, qu'on ne peut
   ni copier ni chercher.

---

## 2.2 à 2.6 — Ce que contient le nouveau README

| Section de la partie 4 | Où | Contenu |
|---|---|---|
| Titre et une phrase | en tête | ce que c'est, pour qui |
| Prérequis | `## Prérequis` | Python 3.12, Git ; aucune base à installer |
| Démarrage rapide | `## Démarrage rapide` | 5 étapes testées, variantes Windows, résultat attendu, erreur la plus probable |
| Configuration | `## Configuration` | les 10 variables de `app/config.py` : rôle, obligatoire, défaut |
| Utilisation | `## Utilisation` | lien vers `/docs`, 3 requêtes avec leur réponse, les scripts |
| Tests | `## Tests` | `pytest`, `ruff check .`, ce que lance la CI |
| Architecture | `## Architecture` | schéma Mermaid du sens des dépendances, un rôle par dossier |
| Contribuer | `## Contribuer` | issue, branche, Conventional Commits, PR relue, squash |

Les trois premières sections tiennent sur un écran. Aucun « simplement » ni
« il suffit de ». Aucun secret : `CLE_SECRETE=collez-ici-la-cle-generee`.

---

## 2.7 — Répartition et publication

Proposition de répartition (un seul membre pousse, les autres lui envoient
leur texte ou relisent le sien) :

| Sections | Membre |
|---|---|
| Titre, prérequis, démarrage rapide | … |
| Configuration | … |
| Utilisation et tests | … |
| Architecture et contribuer | … |

La branche `docs/readme` part d'un `main` à jour et ne reçoit **que** le
README :

```bash
git switch main
git pull
git switch -c docs/readme
git checkout origin/claude/nice-dijkstra-uy8f1a -- README.md
git commit -m "docs(readme): réécrire le README pour lancer l'API en cinq minutes" \
  -m "Prérequis, démarrage rapide testé sur un clone neuf avec le résultat attendu,
tableau des variables de configuration, exemples de requêtes, tests,
schéma des couches et règles de contribution."
git push -u origin docs/readme
```

Puis sur GitHub, sur la branche `docs/readme` : vérifier que le schéma
s'affiche dans la section Architecture.

**N'ouvrez pas encore la PR du README** : elle se fait en séance 4, après
l'échange avec l'autre groupe.
