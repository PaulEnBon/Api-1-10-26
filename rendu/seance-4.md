# Séance 4 — Valider le README, écrire un ADR

> Kit prêt à copier pour les trois exercices. L'ADR est déjà rédigé :
> `docs/adr/0001-fusionner-les-pr-par-squash.md`, au statut **Proposée**.

---

## ⚠️ État du dépôt GitHub le 06/10 : rien n'est encore en ligne

Vérifié sur `PaulEnBon/Api-1-10-26` ce matin :

| Attendu par le rendu | État |
|---|---|
| Les issues des séances 1 et 2 | **0 issue** |
| La PR des statistiques (séance 3), fusionnée | **0 PR** ; `main` est toujours à `a6fb28e` (« 2 ») |
| La branche `docs/readme` | **absente** : seules `main` et `claude/nice-dijkstra-uy8f1a` existent |
| La protection de `main` | non activée (`protected: false`) |

La séance 4 s'appuie sur tout cela : l'autre groupe ne pourra pas tester le
README sans branche `docs/readme` (point 1.1 de l'énoncé), et l'ADR doit
décrire la méthode « appliquée à la PR des statistiques ».

**Ordre de rattrapage, avant le rendu du mardi 13 octobre à 23 h 59 :**

1. **Tout de suite, avant l'échange** : pousser `docs/readme` (commandes dans
   `rendu/seance-3-exercice-2-readme.md`, partie 2.7). Sinon, prévenir
   l'enseignant.
2. Créer les issues sur GitHub à partir de `rendu/exercice-1-backlog.md`,
   plus l'issue des statistiques (`rendu/seance-3-exercice-1-pr-statistiques.md`,
   étape 0). Étiquettes, et un membre assigné sur chacune.
3. Faire la PR des statistiques, relue, fusionnée par **squash**
   (après accord de l'enseignant sur l'option A de la fiche séance 3).
4. La PR du README (exercice 2), puis celle de l'ADR (exercice 3).

Chaque membre doit être auteur ou relecteur d'au moins une des trois PR.

---

## Exercice 1 — L'échange des README

### 1.1 Tester le README de l'autre groupe

Un membre, dans un dossier neuf, sans parler au groupe testé :

```bash
git clone <url-du-depot-de-l-autre-groupe> test-readme
cd test-readme
git switch docs/readme
```

Puis il suit **leur** README à la lettre, sans rien ajouter de lui-même,
nouvel environnement virtuel compris. À chaque blocage : copier la commande
et l'erreur exacte, puis noter ce qu'il a fallu deviner pour continuer.

### 1.2 L'issue à ouvrir sur leur dépôt

**Titre :** `Test du README sur une machine vierge : <n> blocage(s)`
(ou `Test du README sur une machine vierge : aucun blocage`)

```markdown
## Contexte
Test de la branche `docs/readme` le 06/10/2026, dans un dossier neuf, en
suivant le README à la lettre, sans aide du groupe.

Environnement : <système et version> · Python <version> · commit `<sha>`

## Résultat
<L'API a démarré / L'API n'a pas démarré>.

## Blocages

### 1. <étape du README, par exemple « Démarrage rapide, étape 4 »>
Commande :
    <commande copiée du README>
Erreur obtenue :
    <message d'erreur copié tel quel>
Ce qu'il a fallu deviner pour continuer : <…, ou « bloqué ici »>

### 2. …

## Remarques non bloquantes
- <ce qui a ralenti sans bloquer : résultat attendu absent, variante Windows…>
```

S'il n'y a aucun blocage, l'issue le dit en une phrase, avec l'environnement
et le commit testé.

### 1.3 Quand l'issue de l'autre groupe arrive chez vous

Corriger **chaque** blocage sur `docs/readme`, un commit par correction :

```bash
git switch docs/readme
git pull
# corriger le README, puis :
git commit -am "docs(readme): <ce que la correction change>" -m "Refs #<issue reçue>"
git push
```

Répondre dans l'issue, pour chaque blocage : « Corrigé dans `<sha>` ». Ne
pas fermer l'issue à la main : la PR du README la fermera.

Notre README a été suivi à la lettre dans un clone neuf le 05/10 (Python
3.12.3). Points à surveiller, **non testés** : la variante Docker, et les
commandes Windows (`py -3.12`, `.venv\Scripts\activate`, `copy`).

---

## Exercice 2 — La PR du README

### 2.1 Ouvrir la PR

*Pull requests → New pull request*, **base `main` ← compare `docs/readme`**.

**Titre :**

```
Réécrire le README pour lancer l'API en cinq minutes sur une machine vierge
```

**Description :**

```markdown
## Contexte
L'ancien README ne permettait pas de lancer l'API : `cp .env.example .env`
gardait une adresse PostgreSQL que le lecteur n'a pas, et l'API répondait
500 sur `GET /api/v1/jeux`. Il ne donnait ni version de Python, ni résultat
attendu, ni variante Windows.

Le nouveau README a été testé par un autre groupe sur une machine vierge
(#<issue de l'échange>) ; chaque blocage signalé est corrigé dans cette PR.

## Changements
- Titre et phrase de présentation, prérequis (Python 3.12 ou 3.13).
- Démarrage rapide en cinq étapes, en SQLite, avec le résultat attendu,
  les variantes Windows et l'erreur la plus probable.
- Configuration : les 10 variables de `app/config.py`, avec leur rôle, si
  elles sont obligatoires, et leur valeur par défaut.
- Utilisation (trois requêtes, lien vers `/docs`), Tests, Architecture
  (schéma Mermaid des couches), Contribuer.
- Corrections issues de l'échange : <une ligne par blocage corrigé>.

## Impact
- Documentation seulement : aucun fichier de code, de test ou de
  configuration n'est modifié.

## Comment tester
Dans un dossier neuf :
    git clone <url-du-depot> && cd <dossier> && git switch docs/readme
puis suivre la section « Démarrage rapide ». Résultat attendu :
http://127.0.0.1:8000/docs affiche la liste des routes, et
`GET /api/v1/jeux` renvoie les 8 jeux de démonstration.

Vérifier aussi que le schéma de la section Architecture s'affiche sur GitHub.

## Vérifications
- [x] testé sur une machine vierge par un autre groupe
- [x] aucun secret, même en exemple
- [x] les commandes modifiées depuis l'échange ont été relancées sur un clone neuf

Closes #<issue de l'échange>
```

### 2.2 et 2.3 — La relecture

Le relecteur n'a pas écrit le README, et de préférence n'a encore eu aucun
rôle sur une PR. **Start a review**, au moins trois commentaires, chacun
rattaché à un critère :

| Critère | Ce que le relecteur fait |
|---|---|
| Exacte | relance, dans un dossier neuf, les commandes **modifiées depuis l'échange** (onglet *Files changed*, ou les commits poussés après l'issue) |
| Complète | se demande ce qui manquerait à un lecteur qui n'a jamais vu le projet |
| Claire | repère les phrases longues, et deux mots pour une même notion |
| À jour | compare le tableau de configuration avec `app/config.py` |
| Sans secret | aucune valeur réaliste de mot de passe ou de clé |
| Liens valides | les suit, y compris `/docs` et `/sante` |

Forme des commentaires, comme en séance 2 : `issue:`, `suggestion:`,
`question:`, `nit:`, `praise:`. Puis **Submit review** avec un verdict.

### 2.4 — Converger et fusionner

L'auteur répond à chaque commentaire (« Corrigé dans `<sha>` », ou un
argument), pousse sans `--force`, et clique sur **Re-request review**. Une
fois la PR approuvée et toutes les conversations résolues : **Squash and
merge**, puis **Delete branch**.

Vérification : le README est sur `main`, et la PR montre au moins trois
commentaires de relecture, tous résolus.

---

## Exercice 3 — L'ADR

### 3.1 À l'oral : quelles décisions méritent un ADR ?

| Décision | ADR ? | Une phrase de justification |
|---|---|---|
| Hacher les mots de passe avec bcrypt | **Oui** | Structurante pour la sécurité et coûteuse à défaire : changer d'algorithme oblige à garder l'ancien tant que chaque utilisateur ne s'est pas reconnecté. Elle a d'ailleurs été débattue (`passlib` abandonné, voir `app/securite.py`). |
| Nommer la table `jeux` plutôt que `games` | Non | Une convention de nommage : une ligne dans le README ou un commentaire suffit. |
| Fusionner les PR par squash | **Oui** | Une décision d'équipe, débattue entre trois options, et surprenante pour un nouvel arrivant qui ne voit qu'un commit par PR. |
| Renommer la fonction `lister` en `rechercher` | Non | Un renommage sans conséquence durable : le message de commit et la PR suffisent. |
| Stocker les tags d'un jeu dans une colonne JSON | **Oui** | Structurante pour le schéma et les requêtes, coûteuse à défaire (migration des données), et une alternative existe : une table dédiée avec relation N-N, la même question que l'issue sur les plateformes. |

### 3.2 à 3.4 — La branche, la PR, la fusion

L'ADR suppose que la PR des statistiques a été fusionnée par **squash**. Si
le groupe a utilisé une autre méthode, l'ADR doit dire celle-là, avec ses
vraies raisons.

```bash
git switch main
git pull
git switch -c docs/adr-fusion
mkdir -p docs/adr
git checkout origin/claude/nice-dijkstra-uy8f1a -- docs/adr/0001-fusionner-les-pr-par-squash.md
git commit -m "docs(adr): proposer de fusionner les pull requests par squash" \
  -m "Premier ADR du dépôt, au statut Proposée. Compare les trois méthodes de
fusion de GitHub et consigne celle appliquée à la PR des statistiques."
git push -u origin docs/adr-fusion
```

Ouvrir la PR par le lien du terminal ou le bandeau *Compare & pull request*.

**Titre :**

```
Proposer l'ADR 0001 : fusionner les pull requests par squash
```

**Description (courte, comme le demande l'énoncé) :**

```markdown
## Décision proposée
Fusionner toutes les PR vers `main` par **Squash and merge**, puis supprimer
la branche. Le titre de la PR devient le message du commit sur `main`.

## Pourquoi maintenant
La PR des statistiques vient d'être fusionnée par squash, et deux autres PR
suivent : sans décision écrite, chacun choisirait au hasard, et le bouton vert
propose par défaut *Create a merge commit*. L'historique de `main` contient
déjà `oui` et `2`, deux messages qui n'expliquent rien : c'est ce que la
décision évite.

Statut : **Proposée**. Il passera à Acceptée dans le dernier commit de cette
PR, après relecture.
```

Après la relecture (un autre membre, Start a review) et les ajustements, le
**dernier commit** change le statut :

```bash
sed -i 's/\*\*Statut\*\* : Proposée/**Statut** : Acceptée/' docs/adr/0001-fusionner-les-pr-par-squash.md
# macOS : sed -i '' 's/\*\*Statut\*\* : Proposée/**Statut** : Acceptée/' docs/adr/0001-fusionner-les-pr-par-squash.md
git commit -am "docs(adr): accepter l'ADR 0001 après relecture"
git push
```

Puis **Squash and merge** et **Delete branch**. Si le groupe applique la
mise en œuvre décrite dans l'ADR, cocher les réglages de *Settings → General
→ Pull Requests* après la fusion.

Vérification : l'ADR est sur `main`, au statut Acceptée, et ses conséquences
contiennent trois points négatifs (le détail des commits perdu de `main`,
les grosses PR qui deviennent de gros commits, les branches fusionnées
inutilisables).

### Qui fait quoi (à remplir)

| PR | Auteur | Relecteur |
|---|---|---|
| Statistiques (séance 3) | … | … |
| README (exercice 2) | … | … |
| ADR (exercice 3) | … | … |

Chaque membre apparaît au moins une fois.

---

## Avant de passer au tableau : notre README face à la grille

| Critère | Où c'est dans notre README |
|---|---|
| On comprend ce que c'est en trente secondes | titre et deux phrases d'ouverture |
| Les prérequis donnent des versions précises | Python 3.12 ou 3.13 ; PostgreSQL 16 pour Docker |
| Commandes dans l'ordre, et le résultat attendu | « Démarrage rapide », 5 étapes, puis « Résultat attendu » |
| Variables listées, sans valeur qui ressemble à un secret | tableau « Configuration » ; `CLE_SECRETE=collez-ici-la-cle-generee` |
| Utilisation et tests : quoi appeler, comment vérifier | 3 requêtes avec leur réponse ; `pytest` et `ruff` avec le résultat attendu |
| Le schéma montre le sens des dépendances | routeurs → services → dépôts → tables → base |
| L'autre groupe a lancé l'API sans question | à compléter avec l'issue de l'échange |

« Qu'auriez-vous enlevé ? » : le mot de passe de démonstration apparaît en
clair (`motdepasse123`). C'est un compte local créé par `scripts/peupler.py`,
et le README dit de ne jamais l'utiliser ailleurs ; c'est la question qu'on
risque de vous poser.

---

## Le rendu : ce que lira le correcteur

- [ ] les issues des séances 1 et 2, étiquetées et assignées
- [ ] la PR des statistiques : test avant la correction, relue, `Closes #N`, squash
- [ ] la PR du README : ferme l'issue de l'échange, 3 commentaires résolus
- [ ] la PR de l'ADR : Proposée, puis Acceptée dans le dernier commit
- [ ] chaque membre auteur ou relecteur d'au moins une PR
- [ ] aucun nouveau commit sur `main` en dehors d'une PR
- [ ] le dépôt reste **public**
