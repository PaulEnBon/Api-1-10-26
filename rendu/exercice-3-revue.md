# Exercice 3 — Le défi : trouver la PR qui contient une injection SQL

> Dépôt modèle relu : `Luxchar/api-jeux-reprise`, PR #2 à #6.
> Une seule contient une injection SQL permettant de lire les mots de passe de
> tous les utilisateurs. Les autres ne sont pas propres non plus (un problème
> noté par PR, en fin de document).

---

## 🎯 La PR fautive : **PR #2 — « recherche editeur »**

**Fichier :** `app/depots/jeux.py` — **ligne 89**
**Verdict : Request changes**

Ligne fautive (nouvelle fonction `par_nom_editeur`) :
```python
def par_nom_editeur(session: Session, nom: str) -> list[Jeu]:
    requete = text(
        "SELECT jeux.* FROM jeux JOIN editeurs ON editeurs.id = jeux.editeur_id "
        f"WHERE editeurs.nom LIKE '%{nom}%'"          # ← ligne 89
    )
    return list(session.scalars(select(Jeu).from_statement(requete)).all())
```

### Commentaire de relecture à laisser sur la ligne

> **issue (bloquant) :** `nom`, qui vient directement du paramètre de requête de
> `GET /api/v1/jeux/par-editeur?nom=...`, est collé dans le SQL par une f-string.
> C'est exactement l'injection de la démo : le `f"..."` ne colle pas une donnée,
> il colle du code SQL écrit par l'utilisateur.
>
> **Pourquoi c'est grave :** un appelant peut refermer la chaîne et ajouter un
> `UNION SELECT` sur la table `utilisateurs` pour faire sortir les empreintes de
> mots de passe de tout le monde. Exemple d'exploitation :
> ```
> curl -G 'http://127.0.0.1:8000/api/v1/jeux/par-editeur' \
>   --data-urlencode "nom=' UNION SELECT * FROM utilisateurs --"
> ```
>
> **Comment corriger :** ne jamais construire le SQL par concaténation. Passer
> par l'ORM et un paramètre lié, comme le reste du dépôt :
> ```python
> def par_nom_editeur(session: Session, nom: str) -> list[Jeu]:
>     terme = nom.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
>     requete = (
>         select(Jeu)
>         .join(Editeur, Editeur.id == Jeu.editeur_id)
>         .where(Editeur.nom.ilike(f"%{terme}%", escape="\\"))
>     )
>     return list(session.scalars(requete).all())
> ```
> La valeur reste alors un paramètre lié : ce n'est plus une injection.

### Vérification (grille « On présente »)
- [x] Le commentaire désigne le fichier et la ligne (`app/depots/jeux.py:89`).
- [x] Il explique pourquoi c'est grave, avec une conséquence concrète (mots de
      passe de tous les utilisateurs exfiltrés via `UNION SELECT`).
- [x] Il propose une correction (ORM + paramètre lié).
- [x] Il est étiqueté `issue` et marqué bloquant.
- [x] Le verdict est **Request changes**.

---

## Les autres PR — un problème par PR

### ✅ PR #6 — « Exposer la liste des genres » → **Approve**
La seule qui mérite d'être approuvée. Elle répond exactement à l'issue #1 (`Closes #1`),
réutilise `service.genres` (déjà présente mais jamais appelée), déclare la route
`/genres` **avant** `/{jeu_id}` (sinon 422), ajoute des tests (catalogue rempli
**et** vide), et la CI est verte. RAS bloquant.

### PR #3 — « Afficher le nom de l'éditeur » → **Request changes**
**Fichier :** `app/depots/jeux.py`, ligne 53 (ligne **rouge**).
> **issue (bloquant) — performance :** la PR supprime `selectinload(Jeu.editeur)`
> de `lister`. La nouvelle propriété `editeur_nom` lit `self.editeur` pour chaque
> jeu de la page → une requête par jeu (problème N+1) à chaque listing. La ligne
> supprimée est justement celle qui l'évitait. Restaurer `selectinload` ou
> charger l'éditeur en une jointure.

### PR #4 — « Export CSV » → **Request changes**
**Fichiers :** `app/routeurs/jeux.py`, lignes 95 et 97 — et CI rouge (`ruff`).
> **issue (bloquant) — sécurité :** l'export écrit la colonne `notes_internes`
> (`writerow([... x.notes_internes])`). Ce champ est interne : il est volontairement
> absent de `JeuSortie` pour ne jamais sortir de l'API. Cet export le divulgue, et
> la route n'exige aucune authentification. Retirer `notes_internes` des colonnes.
>
> À signaler aussi : la CI `ruff` est **rouge** (noms à une lettre `l`/`d`/`x`/`w`,
> `g != None` au lieu de `is not None`, imports dans la fonction) ; et
> `tmp.getvalue()[:100000]` tronque le CSV en plein milieu au-delà de ~100 ko,
> ce qui coupe une ligne. L'énoncé de la partie 4 le confirme : *« l'une a une CI
> rouge : lisez pourquoi, puis relisez quand même le reste. »*

### PR #5 — « fix » (nettoyage divers) → **Request changes**
**Fichiers :** `app/services/jeux.py` (ligne rouge supprimée) et `tests/test_autorisation.py`.
> **issue (bloquant) — sécurité :** sous couvert de « nettoyage », la PR supprime
> `verifier_droit(jeu, utilisateur)` dans `supprimer`. N'importe quel utilisateur
> connecté peut désormais supprimer le jeu d'un autre (faille d'autorisation au
> niveau objet, 1ʳᵉ du top OWASP API). Pire : le test qui l'attrapait
> (`test_un_utilisateur_ne_supprime_pas_le_jeu_d_un_autre`) est **supprimé** dans
> la même PR — la CI reste donc verte. Restaurer la vérification **et** le test.
>
> À signaler aussi (non bloquant mais à noter) : `duree_jeton_minutes` passé à
> 30 jours « parce que c'est plus pratique » — une config changée pour le confort
> qui affaiblit la sécurité. C'est la PR la plus longue, et c'est là que le défaut
> se cache le mieux : les trois signaux d'alerte de la partie 4 (commit
> « nettoyage » qui change un comportement, test modifié pour qu'il passe, config
> changée « parce que c'est plus pratique ») y sont réunis.

---

## Récapitulatif

| PR | Sujet | Verdict | Point principal |
|----|-------|---------|-----------------|
| #2 | recherche editeur | **Request changes** | 🔴 **Injection SQL** (f-string) → mots de passe exfiltrables |
| #3 | nom de l'éditeur | Request changes | N+1 : `selectinload` supprimé |
| #4 | export CSV | Request changes | `notes_internes` exposé + CI `ruff` rouge |
| #5 | « fix » | Request changes | 🔴 Autorisation retirée sur `supprimer` + test supprimé |
| #6 | liste des genres | **Approve** | Propre, testée, CI verte |

**Réponse au défi : PR #2, `app/depots/jeux.py`, ligne 89.**
