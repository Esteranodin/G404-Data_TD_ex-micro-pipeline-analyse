# Pipeline de départ — tickets support

Travaillez dans l'ordre des fichiers numérotés. L'étape 01 fonctionne ; les
fonctions des étapes 02 à 05 restent à écrire. Les données comportent deux
variables d'analyse (`channel`, `resolution_minutes`) et un identifiant
(`ticket_id`) pour les contrôles et la traçabilité.

La fiche [Python — points de départ](../PYTHON_SNIPPETS.md) donne des exemples
à adapter sur des visites fictives. Elle explicite les opérations une par une.

## Exécuter une étape

Dans VS Code, ouvrez `01_auditer.py` puis utilisez Quick Run avec l'environnement
`.venv` du cours. Ou, depuis ce dossier avec cet environnement activé :

```bash
python 01_auditer.py
```

Inspectez le CSV d'audit et les modalités affichées. L'audit ne prend aucune
décision de nettoyage. Complétez ensuite `preparer_tickets` dans
`02_preparer.py` ; remplacez son `NotImplementedError` par votre code et un
`return` des deux tableaux demandés. Exécutez le fichier, vérifiez ses sorties,
puis passez à l'étape suivante.

## Contrats des cinq étapes

| Étape | Entrée | Travail à réaliser | Sortie |
|---|---|---|---|
| 01 — auditer | CSV brut | Inspecter schéma et structure | `audit_structure.csv` |
| 02 — préparer | CSV brut | Décider, nettoyer et tracer | CSV nettoyé + journal qualité |
| 03 — décrire | CSV nettoyé | Résumer les durées par canal | `resume_par_groupe.csv` |
| 04 — visualiser | CSV nettoyé | Trois histogrammes séparés avec observations en dessous, puis boîte à moustaches | Deux graphiques HTML |
| 05 — mesurer | CSV nettoyé | Compter puis diviser dans chaque canal | `frequences_empiriques_180_minutes.csv` |

Les noms de colonnes de sortie sont fixés pour faciliter les vérifications :

| Tableau | Colonnes, dans l'ordre |
|---|---|
| Données nettoyées | `ticket_id`, `channel`, `resolution_minutes` |
| Journal qualité | `ligne_source`, `ticket_id`, `regle`, `decision`, `justification` |
| Résumé | `channel`, `nombre`, `moyenne`, `mediane`, `ecart_type`, `q1`, `q3`, `minimum`, `maximum` |
| Fréquences | `channel`, `seuil_minutes`, `nombre_queue`, `effectif_groupe`, `frequence_queue` |

`ecart_type` utilise `std(ddof=1)`. `frequence_queue` est une proportion entre
0 et 1 ; le seuil vaut 180 minutes et la comparaison est `>=`.

Les chemins sont déjà définis dans `chemins_projet.py`. Le brut se trouve dans
`../data/raw/tickets_support.csv` et doit rester intact. Les données dérivées
vont dans `../data/processed/` ; tableaux, journal et figures dans `../outputs/`.
Utilisez les mêmes axes et des classes de 10 minutes (5, 15, 25, …) pour les
trois canaux. Une courbe de densité lissée reste optionnelle.
Les graphiques doivent être autonomes : `write_html(..., include_plotlyjs=True)`.

## Contrôler avant de continuer

- **02** : les identifiants sont-ils uniques, les canaux valides et les durées
  numériques positives ou nulles ? Chaque retrait est-il expliqué ?
- **03** : la somme des effectifs par canal égale-t-elle l'effectif nettoyé ?
  Les quartiles et la médiane sont-ils entre le minimum et le maximum ?
- **04** : les deux fichiers s'ouvrent-ils ? Les axes, unités et canaux sont-ils
  lisibles ? Pouvez-vous expliquer la forme observée ?
- **05** : chaque numérateur est-il inférieur ou égal à son dénominateur ? Le
  dénominateur correspond-il au canal concerné ?

## Rejouer et conclure

Quand les cinq étapes fonctionnent séparément :

```bash
python executer_pipeline.py
```

Le lanceur utilise le même interpréteur Python pour chaque étape. Il s'arrête
à la première erreur : corrigez cette étape avant de relancer.

Vous développez cette version jeudi matin et après-midi. Vendredi matin, le
pipeline de référence permettra de comparer les décisions et leur traduction
en code. Des approches différentes restent possibles si elles sont justifiées,
traçables et reproductibles.
