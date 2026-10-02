# Exercice 2 — Un message de blocage

> Non noté. La situation : on vient de cloner le dépôt, l'API refuse de démarrer.
> Dans le terminal :
>
> ```
> pydantic_core._pydantic_core.ValidationError: 1 validation error for Configuration
> cle_secrete
>   Field required
> ```
>
> On a créé un `.env` à la main, avec seulement `DATABASE_URL=sqlite:///./jeux.db`.

## Pourquoi le message de départ est mauvais

> `@samir tu peux m'envoyer ton .env ? le mien marche pas`

- Samir ne sait pas **ce qui bloque** : il doit mener l'enquête.
- Ce qui est demandé pose un problème en soi : un `.env` contient des secrets
  (la clé qui permet de forger un jeton d'administrateur). On ne s'échange jamais
  un `.env` — cf. séance 1, partie 2, « Deux conséquences ».

## Message réécrit (les cinq rubriques)

> **Bloqué au démarrage de l'API après un clone propre.**
>
> **Ce que j'essaie de faire :** lancer l'API en local (`fastapi dev app/main.py`)
> pour commencer à travailler.
>
> **Ce qui bloque :** la configuration refuse de se charger, il manque
> `cle_secrete`. Erreur copiée :
> ```
> pydantic_core._pydantic_core.ValidationError: 1 validation error for Configuration
> cle_secrete
>   Field required
> ```
>
> **Ce que j'ai déjà essayé :** j'ai créé un `.env` à la main avec seulement
> `DATABASE_URL=sqlite:///./jeux.db`. Je n'ai pas renseigné `CLE_SECRETE`.
>
> **Mon hypothèse :** `CLE_SECRETE` est obligatoire (elle est dans
> `.env.example`), et comme je ne l'ai pas mise, la config plante au démarrage.
> Je pense qu'il faut que je génère la mienne plutôt que d'en demander une.
>
> **Ce dont j'ai besoin :** @samir peux-tu me confirmer que je dois juste partir
> de `.env.example` (`cp .env.example .env`) et générer ma propre clé avec
> `python -c "import secrets; print(secrets.token_urlsafe(32))"` ? Pas urgent,
> avant demain midi. En attendant je lis le README.

**Ce que ce message ne demande pas :** aucun secret. On ne réclame pas le `.env`
de Samir ni sa clé — chacun génère la sienne, différente en production.

## Variante — « help docker marche pas » (si le temps le permet)

> **Bloqué sur le démarrage via Docker.**
>
> **Ce que j'essaie de faire :** lancer la stack avec `docker compose up --build`.
>
> **Ce qui bloque :** le conteneur de l'API s'arrête aussitôt. Erreur copiée :
> ```
> [l'erreur exacte affichée par docker compose, p. ex. :
>  api | sqlalchemy.exc.OperationalError: could not connect to server: Connection refused]
> ```
>
> **Ce que j'ai déjà essayé :** `docker compose down -v` puis rebuild ;
> [j'ai vérifié que le port 5432 n'est pas déjà pris].
>
> **Mon hypothèse :** l'API démarre avant que PostgreSQL soit prêt à accepter
> les connexions (pas de `depends_on` / healthcheck ?).
>
> **Ce dont j'ai besoin :** @[personne qui a écrit le docker-compose] peux-tu
> confirmer l'ordre de démarrage attendu ? [échéance].

## Grille de vérification (à relire avec un voisin)
- [ ] Les cinq rubriques sont présentes : objectif, erreur copiée, essais,
      hypothèse, besoin.
- [ ] Il y a un destinataire (« de qui ») et une échéance (« pour quand »).
- [ ] Il ne demande **aucun secret** (ni `.env`, ni clé, ni mot de passe).
- [ ] L'erreur est copiée **telle quelle**, pas résumée.
- [ ] La dernière phrase dit à l'équipe que le temps n'est pas perdu
      (« en attendant je… »).
