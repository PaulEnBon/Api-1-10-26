# Exercice 1 — Le backlog en issues

> Brouillon des 5 issues du backlog laissé par l'équipe précédente, prêt à coller
> dans GitHub. Une section = une issue. Le titre va dans le champ **Title**, le
> reste dans le corps. L'étiquette et l'assigné se règlent dans la barre latérale
> de GitHub.
>
> **Reproduction faite le 02/10/2026** contre l'état « équipe précédente »
> (commit initial `e99f2a6`). Les réponses d'API ci-dessous sont copiées telles
> quelles. ⚠️ Voir la note en bas : le `main` actuel (`e43ebb7`) corrige déjà
> les deux bugs — à arbitrer avant le rendu.

Environnement de reproduction : macOS 27.0 (arm64) · Python 3.13.15 · SQLite 3.50.4 ·
FastAPI 0.141.1 · SQLAlchemy 2.0.52 · Pydantic 2.13.5 · branche `main`.

---

## Issue 1 — `GET /api/v1/jeux/recommandes` renvoie 422 au lieu de la liste des jeux recommandés

**Étiquette :** `bug`

### Contexte
La page « jeux recommandés » du front appelle `GET /api/v1/jeux/recommandes` et
n'affiche plus rien : l'API répond une erreur 422 au lieu du catalogue des
mieux notés.

### Étapes pour reproduire
1. Peupler la base : `python scripts/peupler.py`.
2. Lancer l'API : `fastapi dev app/main.py`.
3. Appeler la route, sans authentification :
   ```
   curl http://127.0.0.1:8000/api/v1/jeux/recommandes
   ```

### Comportement attendu
Un statut `200` et la liste des jeux dont la note est ≥ 8.

### Comportement observé
Statut `422`. La chaîne `recommandes` est interprétée comme un `jeu_id` :
```json
{
  "code": "VALIDATION_ECHOUEE",
  "message": "Les données envoyées sont invalides",
  "details": [
    {
      "type": "int_parsing",
      "loc": ["path", "jeu_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer"
    }
  ]
}
```

### Piste (facultative, pour celui qui corrigera)
Les routes sont essayées dans l'ordre de déclaration. `/jeux/{jeu_id}` est
déclarée **avant** `/jeux/recommandes`, donc elle capte `recommandes`. Déplacer
le chemin fixe `/recommandes` au-dessus de `/{jeu_id}` (comme `/statistiques`).

### Environnement
macOS 27.0 (arm64) · Python 3.13.15 · SQLite 3.50.4 · branche `main`.

---

## Issue 2 — Modifier uniquement la note renvoie « le titre existe déjà »

**Étiquette :** `bug`

### Contexte
En modifiant la note d'un jeu via `PATCH /api/v1/jeux/{jeu_id}`, l'API répond
que le titre existe déjà — alors que le titre n'est pas envoyé. Le message est
trompeur et bloque la mise à jour de la note.

### Étapes pour reproduire
1. Peupler la base : `python scripts/peupler.py`.
2. Dans `/docs`, se connecter avec **Authorize** (`admin@example.com` /
   `motdepasse123`).
3. `PATCH /api/v1/jeux/1` avec, dans le corps, **uniquement** la note, hors de
   l'échelle 0–10 :
   ```
   curl -X PATCH http://127.0.0.1:8000/api/v1/jeux/1 \
     -H "Authorization: Bearer <jeton>" \
     -H "Content-Type: application/json" \
     -d '{"note": 50}'
   ```
   Une note normale (`{"note": 8}`) passe et renvoie `200` ; c'est une note
   **hors échelle** qui déclenche le message.

### Comportement attendu
Une erreur de validation `422` qui dit clairement que la note doit être comprise
entre 0 et 10. Rien ne concerne le titre.

### Comportement observé
Statut `409`, erreur sur le titre, qui n'a pourtant pas été touché :
```json
{
  "code": "TITRE_DEJA_UTILISE",
  "message": "Un jeu intitulé 'Hollow Knight' existe déjà",
  "details": { "titre": "Hollow Knight" }
}
```

### Piste (facultative, pour celui qui corrigera)
Le modèle `JeuMiseAJour` accepte `note` jusqu'à `le=100`. Une note entre 11 et
100 passe Pydantic, puis viole la contrainte SQL `ck_jeux_note` (0–10). Le
`IntegrityError` est rattrapé dans `_appliquer` et transformé en
`TitreDejaUtilise`, sans distinguer la vraie cause. Aligner la borne du modèle
sur la base (`le=10`).

### Environnement
macOS 27.0 (arm64) · Python 3.13.15 · SQLite 3.50.4 · branche `main`.

---

## Issue 3 — Lister les éditeurs d'un pays donné

**Étiquette :** `enhancement`

### Contexte
Le client veut parcourir les éditeurs par pays (par exemple « tous les éditeurs
du Japon »). Aujourd'hui `GET /api/v1/editeurs` renvoie tout le monde, sans
filtre : impossible de restreindre à un pays.

### Besoin
Pouvoir filtrer la liste des éditeurs sur leur pays.

### Critères d'acceptation
- [ ] `GET /api/v1/editeurs?pays=Japon` ne renvoie que les éditeurs dont le pays
      vaut « Japon ».
- [ ] Le filtre ignore la casse (`japon` et `Japon` donnent le même résultat).
- [ ] Un pays sans aucun éditeur renvoie `[]` avec un statut `200` (pas une
      erreur), et la pagination (`total`) reflète le filtre.

### Hors périmètre
Le filtre par pays sur les **jeux**. La création d'un référentiel de pays
normalisé (liste fermée).

---

## Issue 4 — Filtrer les jeux entre deux années

**Étiquette :** `enhancement`

### Contexte
Pour mettre en avant une période (« les jeux des années 2010 »), il faut
pouvoir borner le catalogue entre deux années de sortie. Les filtres actuels de
`GET /api/v1/jeux` (genre, note minimale, recherche) ne le permettent pas.

### Besoin
Filtrer la liste des jeux sur une plage d'années de sortie, cumulable avec les
filtres existants.

### Critères d'acceptation
- [ ] `GET /api/v1/jeux?annee_min=2010&annee_max=2019` ne renvoie que les jeux
      dont l'année est comprise entre 2010 et 2019 (bornes incluses).
- [ ] Chaque borne est facultative et utilisable seule (`annee_min` seule,
      `annee_max` seule).
- [ ] `annee_min` supérieure à `annee_max` renvoie une erreur `422` (plage
      incohérente), et le filtre se cumule avec `genre`, `note_min` et le tri.

### Hors périmètre
Un filtre sur une date précise (jour/mois). Le tri par année existe déjà
(`tri=annee`) et n'est pas concerné.

---

## Issue 5 — Gérer les plateformes (PC, Switch, PS5…) sur les jeux

**Étiquette :** `enhancement`

### Besoin
Pouvoir associer une ou plusieurs plateformes (PC, Switch, PS5…) à un jeu, et
filtrer le catalogue par plateforme.

Plusieurs modélisations sont possibles (liste de chaînes façon `tags`, table
dédiée `plateformes` avec relation N-N, énumération fermée…), avec des
conséquences différentes sur le schéma et les requêtes. **On ne tranche pas
ici** : cette issue demande d'abord une décision écrite — un **ADR** (séance 4)
— qui compare les options et acte le choix. L'implémentation suivra une fois
l'ADR validé.

### Hors périmètre
Le choix de modélisation lui-même, qui relève de l'ADR à écrire.

---

## Tri du backlog — à faire dans GitHub (rappel)
- **Étiqueter** chaque issue : `bug` (1, 2) ou `enhancement` (3, 4, 5).
- **Répartir et s'assigner** : une ou deux demandes par membre ; chacun s'assigne
  les issues qu'il écrit.
- **Relier la PR** qui fermera l'issue avec `Closes #N` (en anglais) dans la
  description de la PR.

---

## Pour aller plus loin — les deux signalements oraux

### Issue 6 — Le premier jeu du catalogue a un « jeu précédent » qui ne devrait pas exister

**Étiquette :** `bug` — signalé par Tom (front)

#### Contexte
Sur la fiche du tout premier jeu ajouté (Hollow Knight, `id = 1`), le bouton
« jeu précédent » renvoie vers un autre jeu. Il ne devrait même pas s'afficher :
il n'y a pas de jeu avant le premier.

#### Étapes pour reproduire
1. `python scripts/peupler.py`, puis lancer l'API.
2. `curl http://127.0.0.1:8000/api/v1/jeux/1/voisins`

#### Comportement attendu
`precedent` vaut `null` pour le premier jeu.

#### Comportement observé
`precedent` pointe vers le **dernier** jeu du catalogue :
```json
{
  "precedent": { "id": 9, "titre": "Le jeu de Lea", "genre": "Party", "note": 7 },
  "suivant":   { "id": 2, "titre": "Stardew Valley", "genre": "Simulation", "note": 9 }
}
```

#### Piste
Dans `service.voisins`, `index > 0` au lieu de `index >= 0` : pour le premier
jeu (`index == 0`), `identifiants[-1]` désigne le dernier élément.

#### Environnement
macOS 27.0 (arm64) · Python 3.13.15 · SQLite 3.50.4 · branche `main`.

---

### Issue 7 — « Mes jeux » affiche 1 jeu mais le compteur annonce 9 résultats

**Étiquette :** `bug` — signalé par Léa (test)

#### Contexte
Dans « Mes jeux » (`GET /api/v1/moi/jeux`), un utilisateur qui n'a créé qu'un
seul jeu voit bien un seul jeu dans la liste, mais le compteur `total` annonce 9.
Le total ne tient pas compte du propriétaire.

#### Étapes pour reproduire
1. Peupler la base (8 jeux appartenant à l'admin).
2. S'inscrire comme nouvel utilisateur, créer **un** jeu.
3. `GET /api/v1/moi/jeux` avec le jeton de ce nouvel utilisateur.

#### Comportement attendu
`elements` contient 1 jeu **et** `total` vaut 1.

#### Comportement observé
`elements` contient 1 jeu, mais `total` vaut 9 (tout le catalogue) :
```json
{ "elements": [ { "id": 9, "titre": "Le jeu de Lea", "genre": "Party", "note": 7 } ], "total": 9, "saut": 0, "limite": 20 }
```

#### Piste
Dans `service.lister`, l'appel à `depot.compter(...)` oublie de passer
`proprietaire_id` : le total compte tout le catalogue au lieu des seuls jeux du
propriétaire.

#### Environnement
macOS 27.0 (arm64) · Python 3.13.15 · SQLite 3.50.4 · branche `main`.

---

## ⚠️ Note importante sur l'état du dépôt

Les reproductions ci-dessus ont été faites contre le **commit initial**
(`e99f2a6`), qui est l'état « équipe précédente ».

Le `main` **actuel** de ce dépôt (commit `e43ebb7` « oui ») **corrige déjà** les
quatre bugs (issues 1, 2, 6, 7) :
- `/recommandes` déplacée avant `/{jeu_id}` ;
- `note` du modèle de mise à jour ramenée à `le=10` ;
- `voisins` : `index > 0` ;
- `compter(...)` reçoit bien `proprietaire_id`.

À arbitrer avant le rendu : soit écrire les issues telles quelles puis les
fermer via la PR de correction déjà présente (`Closes #N` + référence au commit),
soit vérifier avec le formateur l'état de départ attendu. Les évolutions
(issues 3, 4, 5), elles, ne sont pas implémentées et restent entièrement valides.
