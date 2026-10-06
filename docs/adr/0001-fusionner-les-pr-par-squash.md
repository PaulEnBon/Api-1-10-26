# 1. Fusionner les pull requests par squash

- **Date** : 2026-10-06
- **Statut** : Proposée

## Contexte

Tout changement arrive sur `main` par une pull request relue, et la CI
(`ruff check .` et `pytest`) tourne sur chaque PR. Sur une branche, les
commits sont de qualité inégale : un commit de test, un commit de correction,
puis les corrections demandées en relecture (« renommer la variable »,
« ajouter un cas »).

GitHub propose trois façons de fusionner, et le bouton vert propose par défaut
*Create a merge commit*. Sans décision écrite, chaque membre choisit au
hasard, et `main` mélange les styles.

L'historique actuel montre ce qu'on veut éviter : `git log main` contient
`oui` et `2`, deux commits poussés directement, dont le message n'explique
rien. Le correcteur, comme un futur mainteneur, lit cet historique.

La protection de branche n'est pas activée sur ce dépôt : la règle « pas de
push sur `main` » est une règle d'équipe, pas une contrainte de l'outil.

## Options envisagées

1. **Merge commit.** Tous les commits de la branche arrivent sur `main`, plus
   un commit de fusion.
   Pour : historique complet, rien n'est réécrit, c'est l'option par défaut.
   Contre : les commits de travail et de relecture arrivent sur `main` ;
   l'historique n'est plus linéaire et `git log` devient difficile à lire ;
   annuler une PR demande de revenir sur un commit de fusion.
2. **Squash and merge.** Les commits de la branche sont réunis en un seul
   commit sur `main`, dont le message est le titre de la PR.
   Pour : un commit sur `main` égale une PR relue ; l'historique est linéaire
   et lisible ; une PR s'annule en un seul `git revert` ; les commits de la
   branche peuvent rester imparfaits sans salir `main`.
   Contre : le détail des commits disparaît de `main` ; une grosse PR devient
   un gros commit.
3. **Rebase and merge.** Les commits de la branche sont rejoués un par un sur
   `main`, sans commit de fusion.
   Pour : historique linéaire, et chaque étape reste visible.
   Contre : exige des commits déjà propres et atomiques, sinon les commits de
   relecture arrivent sur `main` ; les commits sont réécrits, avec de nouveaux
   identifiants ; demande une pratique de Git que toute l'équipe n'a pas.

## Décision

Nous fusionnons toutes les pull requests vers `main` par **Squash and merge**,
puis nous supprimons la branche.

Le titre de la PR devient le message du commit sur `main` : il décrit le
changement (« Renvoyer des statistiques à zéro au lieu d'une erreur 500 sur un
catalogue vide »), il ne dit pas « fix » ni « modifs ».

Nous la retenons parce qu'elle donne un `main` lisible, une ligne par PR
relue, sans exiger de chaque membre des commits parfaits. La méthode par
rebase donnerait un historique aussi lisible, mais seulement si chaque commit
est propre, ce que nous ne pouvons pas garantir aujourd'hui.

Pour l'appliquer : dans *Settings → General → Pull Requests*, décocher
*Allow merge commits* et *Allow rebase merging*, et cocher *Automatically
delete head branches*. Le bouton vert ne propose alors plus que le squash.

## Conséquences

- `git log --oneline main` donne une ligne par PR relue, avec un message qui
  explique le changement.
- Une PR fautive s'annule par un seul `git revert`.
- Les corrections de relecture ne polluent pas `main`.
- **Inconvénient** : le détail des commits n'existe plus que dans la PR
  fusionnée, sur GitHub. Par exemple, la preuve que le test des statistiques
  a été committé avant la correction ne se voit plus dans `git log main`. Si
  le dépôt quitte GitHub, ce détail est perdu.
- **Inconvénient** : une grosse PR devient un gros commit, et `git bisect` ou
  `git blame` désignent tout le bloc. Cela oblige à garder des PR courtes,
  400 lignes au plus.
- **Inconvénient** : une branche fusionnée ne se réutilise pas. Ses commits ne
  sont pas sur `main`, et continuer dessus provoque des conflits : on repart
  d'un `main` à jour, sur une nouvelle branche.
- À revoir si nos PR dépassent régulièrement 400 lignes avec des étapes
  qu'on veut garder séparées sur `main`, ou si l'équipe écrit des commits
  assez propres pour passer à *Rebase and merge*.
