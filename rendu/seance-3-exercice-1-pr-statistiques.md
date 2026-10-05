# Séance 3 · Exercice 1 — La PR des statistiques

> Kit prêt à copier pour la PR qui corrige l'erreur 500 de
> `GET /api/v1/jeux/statistiques` sur un catalogue vide. Remplacez `N` par le
> numéro de l'issue sur GitHub.
>
> Toutes les commandes et tous les résultats ci-dessous ont été rejoués le
> 05/10/2026 dans un clone neuf : Python 3.12.3, `pytest` 163 tests, `ruff`
> 0.14.6.

---

## ⚠️ À régler avant de commencer : le correctif est déjà sur `main`

Le commit `e43ebb7` (« oui », 01/10) a poussé **directement sur `main`**, sans
PR, le correctif (`app/depots/jeux.py`, ligne 172) **et** son test
(`test_statistiques_sur_un_catalogue_vide`). Une branche créée depuis `main`
aujourd'hui n'aurait donc rien à corriger : la PR serait vide, le test ne
pourrait pas échouer, et l'historique ne pourrait pas montrer « le test avant
la correction ».

Autre constat : **aucune issue n'existe sur GitHub** (0 issue, 0 PR). Le
brouillon de la séance 1 (`rendu/exercice-1-backlog.md`) ne contient pas non
plus d'issue sur les statistiques.

**À faire valider par le formateur.** Deux façons de s'en sortir, sans rien
réécrire de l'historique :

| | Option A : PR de retrait, puis la vraie PR | Option B : on documente et on corrige autre chose |
|---|---|---|
| Principe | Une petite PR retire le correctif arrivé sans relecture et le dit ; la PR de l'exercice le refait proprement, test d'abord. | L'issue est créée puis fermée en citant `e43ebb7` ; l'exercice se fait sur une autre issue encore ouverte (par exemple le filtre par pays). |
| Pour | Suit l'énoncé à la lettre ; tout est visible et expliqué dans les PR. | Aucun retour en arrière sur `main`. |
| Contre | `main` porte de nouveau le bug entre les deux fusions. | Ce n'est pas l'issue demandée par l'énoncé. |

Le reste de ce document suit l'**option A**. Jamais de `push --force` sur
`main` pour « effacer » `e43ebb7` : l'historique doit rester honnête.

---

## Étape 0 — L'issue (à créer si elle n'existe pas)

**Titre :** `GET /api/v1/jeux/statistiques renvoie une erreur 500 quand le catalogue est vide`
**Étiquette :** `bug` · **Assignée à :** le membre qui tiendra le clavier

```markdown
### Contexte
Sur une base neuve, avant la création du premier jeu,
`GET /api/v1/jeux/statistiques` répond une erreur 500 au lieu de statistiques
à zéro. Toute nouvelle installation de l'API tombe dessus.

### Étapes pour reproduire
1. Partir d'une base vide (`DATABASE_URL=sqlite:///./vide.db`, sans lancer
   `scripts/peupler.py`).
2. Lancer l'API : `fastapi dev app/main.py`.
3. `curl http://127.0.0.1:8000/api/v1/jeux/statistiques`

### Comportement attendu
Un statut `200` :
`{"nombre": 0, "moyenne": 0.0, "meilleure_note": null, "par_genre": {}}`

### Comportement observé
Statut `500` :
`{"code": "ERREUR_INTERNE", "message": "Une erreur est survenue"}`

Dans les journaux de l'API :
`TypeError: float() argument must be a string or a real number, not 'NoneType'`
(`app/depots/jeux.py`, fonction `statistiques`).

### Piste (facultative)
Sur une table vide, `AVG(note)` renvoie `NULL` : `float(None)` lève la
`TypeError`.

### Environnement
Python 3.12 · SQLite · branche `main` (état de départ `e99f2a6`).
```

---

## Étape 0 bis (option A) — La PR de retrait

```bash
git switch main
git pull
git switch -c revert/statistiques-hors-relecture
```

Remettre `app/depots/jeux.py` (fin de `statistiques`) dans l'état de départ :

```python
        # `func.avg` renvoie un Decimal sur PostgreSQL : le `float()` est requis.
        "moyenne": round(float(moyenne), 2),
```

et supprimer `test_statistiques_sur_un_catalogue_vide` de
`tests/test_api_jeux.py`. Puis :

```bash
pytest && ruff check .     # tout passe : le test du cas vide n'existe plus
git commit -am "revert(jeux): retirer le correctif des statistiques arrivé sans relecture" \
  -m "Le correctif et son test sont arrivés sur main par e43ebb7, sans pull request.
On les retire pour les refaire passer par une PR relue, test d'abord.

Refs #N"
git push -u origin revert/statistiques-hors-relecture
```

**Titre de la PR :** `Retirer le correctif des statistiques arrivé sur main sans relecture`

```markdown
## Contexte
Le correctif de #N et son test sont arrivés sur `main` par `e43ebb7`, poussé
directement, sans pull request ni relecture. On les retire pour les refaire
passer par la PR de l'issue, relue, avec le test committé avant la correction.

## Changements
- `app/depots/jeux.py` : `statistiques` revient à l'état de départ (`e99f2a6`).
- `tests/test_api_jeux.py` : retrait de `test_statistiques_sur_un_catalogue_vide`.

## Impact
- **Le bug de #N revient sur `main`** jusqu'à la fusion de la PR de correction,
  qui suit immédiatement.
- Aucun autre changement : les autres correctifs de `e43ebb7` restent.

## Comment tester
`pytest` et `ruff check .` passent. `GET /api/v1/jeux/statistiques` sur une base
vide renvoie de nouveau 500 : c'est attendu.

Refs #N
```

Pas de `Closes` ici : c'est la PR suivante qui ferme l'issue.

---

## 1.1 à 1.4 — La correction

Repartir de `main` **après** la fusion de la PR de retrait :

```bash
# 1.1 Un main à jour, puis la branche
git switch main
git pull
git switch -c fix/N-statistiques-catalogue-vide
```

**1.2 — Le test d'abord**, dans `tests/test_api_jeux.py`, juste après
`test_statistiques` :

```python
def test_statistiques_sur_un_catalogue_vide(client):
    """`AVG` renvoie NULL sur une table vide : ce n'est pas une erreur 500."""
    reponse = client.get(f"{BASE}/jeux/statistiques")

    assert reponse.status_code == 200
    assert reponse.json() == {
        "nombre": 0,
        "moyenne": 0.0,
        "meilleure_note": None,
        "par_genre": {},
    }
```

```bash
pytest tests/test_api_jeux.py -k catalogue_vide
# Résultat obtenu : 1 failed
# E   TypeError: float() argument must be a string or a real number, not 'NoneType'
# app/depots/jeux.py:171: TypeError

git add tests/test_api_jeux.py
git commit -m "test(jeux): reproduire l'erreur 500 des statistiques sur un catalogue vide" \
  -m "Sur une table vide, AVG(note) renvoie NULL et float(None) lève une TypeError.
Ce test échoue tant que la correction n'est pas faite.

Refs #N"
```

**1.3 — La correction**, dans `app/depots/jeux.py`, fonction `statistiques` :

```python
        # `func.avg` renvoie un Decimal sur PostgreSQL : le `float()` est requis.
        # Et NULL sur une table vide : `float(None)` lèverait une erreur 500.
        "moyenne": round(float(moyenne), 2) if moyenne is not None else 0.0,
```

```bash
pytest            # résultat obtenu : 163 passed
ruff check .      # résultat obtenu : All checks passed!

# 1.4 Le second commit, puis la publication
git add app/depots/jeux.py
git commit -m "fix(jeux): renvoyer une moyenne de 0.0 quand le catalogue est vide" \
  -m "AVG(note) renvoie NULL sur une table vide. On répond 0.0 au lieu de laisser
float(None) lever une TypeError, transformée en erreur 500.

Refs #N"
git push -u origin fix/N-statistiques-catalogue-vide
```

Historique attendu sur la branche : le commit `test(...)` **avant** le commit
`fix(...)`.

---

## 1.5 — La pull request

Vérifier le sens avant de cliquer : **base `main` ← compare
`fix/N-statistiques-catalogue-vide`**.

**Titre** (il deviendra le message du commit sur `main` avec le squash) :

```
Renvoyer des statistiques à zéro au lieu d'une erreur 500 sur un catalogue vide
```

**Description :**

```markdown
## Contexte
`GET /api/v1/jeux/statistiques` renvoie une erreur 500 tant que le catalogue
ne contient aucun jeu, c'est-à-dire sur toute installation neuve, jusqu'à la
création du premier jeu (#N).

Cause : sur une table vide, `AVG(note)` renvoie `NULL`, et `float(None)` lève
une `TypeError`, transformée en 500 par le gestionnaire d'erreurs.

## Changements
- `tests/test_api_jeux.py` : nouveau test `test_statistiques_sur_un_catalogue_vide`,
  committé seul et avant la correction ; il échouait avec la `TypeError` de l'issue.
- `app/depots/jeux.py` : `statistiques` renvoie `moyenne = 0.0` quand `AVG`
  vaut `NULL`.

## Impact
- API : sur un catalogue vide, la route répond `200` avec
  `{"nombre": 0, "moyenne": 0.0, "meilleure_note": null, "par_genre": {}}`.
  Sur un catalogue non vide, la réponse ne change pas.
- Le format de réponse (`JeuStatistiques`) ne change pas : `meilleure_note`
  était déjà déclarée `null` possible.
- Aucune modification du schéma de base, des performances ni de la sécurité.
- `scripts/statistiques.py` en profite aussi : il affiche `Note moyenne 0.0`
  au lieu de planter.

## Comment tester
Automatique :
    pytest tests/test_api_jeux.py -k statistiques     # 2 passed
    pytest                                            # 163 passed

À la main, sur une base vide :
    DATABASE_URL=sqlite:///./vide.db fastapi dev app/main.py
    curl http://127.0.0.1:8000/api/v1/jeux/statistiques
    # -> 200 {"nombre":0,"moyenne":0.0,"meilleure_note":null,"par_genre":{}}

## Vérifications
- [x] test ajouté, et vu en échec avant la correction
- [x] `pytest` passe en entier
- [x] `ruff check .` sans erreur
- [x] documentation : rien à changer (`/docs` est généré, le format ne change pas)

Closes #N
```

**1.6 — Relecture de la description** : un relecteur qui n'a jamais vu
l'issue sait *pourquoi* (installation neuve → 500), *quoi* (deux fichiers,
une ligne de code), et *comment vérifier* (deux commandes, un `curl`, le
résultat attendu).

---

## 1.7 à 1.10 — Relecture et fusion

**Le relecteur relit lui-même le diff** : ce qui suit est une liste de pistes,
pas des commentaires à recopier. Une approbation sans vraie lecture compte
comme une absence de relecture.

Avant tout commentaire : la CI est verte sur la PR, ou bien
`git fetch`, `git switch fix/N-statistiques-catalogue-vide`, `pytest`.

Pistes réelles trouvées en préparant ce kit :

- **Le choix de `0.0`.** Une moyenne de `0.0` peut se confondre avec un
  catalogue où tous les jeux ont 0. `null` serait plus honnête, mais
  `JeuStatistiques.moyenne` est déclaré `float` non nul : changer le format
  casserait les clients de l'API. Bonne matière pour une `question:`.
- **Le test couvre l'API, pas le dépôt.** `tests/test_services.py` a un
  `test_statistiques` ; il n'a pas de cas vide. Matière pour une `suggestion:`
  (non bloquante).
- **Hors périmètre, à ne pas corriger dans cette PR** :
  `scripts/statistiques.py` affiche `—` pour une meilleure note de `0`
  (`stats['meilleure_note'] or '—'` : `0` est faux en Python). C'est un autre
  bug : on ouvre une issue, on ne l'ajoute pas ici.

Rappel de forme : **Start a review**, au moins deux commentaires étiquetés
sur des lignes (`praise:`, `question:`, `suggestion:`, `issue:`, `nit:`),
dont un `praise:` sincère, puis **Submit review** avec un verdict.

**Côté auteur**, une réponse par commentaire, par exemple :
« Corrigé dans `3f2a1c9` », un argument factuel, ou « Hors périmètre, j'ai
ouvert #M ». Puis `git push` (sans `--force`) et **Re-request review**.

**Fusion** : menu du bouton vert → **Squash and merge** (le défaut est
*Create a merge commit*), puis **Delete branch**.

Pourquoi le squash, à noter pour l'ADR de la séance 4 : un commit sur `main`
égale une PR relue ; `git log` sur `main` reste lisible ; le titre de la PR,
soigné, devient le message. Ce qu'on accepte de perdre : le détail des
commits sur `main` (il reste visible dans la PR fusionnée, où l'on voit le
test avant la correction).

Vérifications finales :
- [ ] l'issue #N est fermée par la PR (pas à la main) ;
- [ ] l'onglet *Commits* de la PR montre `test(jeux)` avant `fix(jeux)` ;
- [ ] la PR montre une relecture avec des commentaires et les réponses de l'auteur ;
- [ ] la CI est verte sur `main` après la fusion ;
- [ ] aucun nouveau commit n'arrive sur `main` en dehors d'une PR.
