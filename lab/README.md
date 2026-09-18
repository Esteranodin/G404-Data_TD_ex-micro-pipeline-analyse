# Projet individuel — temps de résolution par canal

Ce dossier contient les points de départ du projet du jeudi 17 septembre 2026.
Vous construisez votre pipeline pendant la matinée et l'après-midi. Un pipeline
de référence sera présenté vendredi matin pour comparer les approches.

## Commencer ici

1. Lire la mission et le dictionnaire dans [PROJECT_BRIEF.md](PROJECT_BRIEF.md).
2. Ouvrir `data/raw/tickets_support.csv` sans le modifier.
3. Exécuter `pipeline_template/01_auditer.py` puis inspecter son tableau de sortie.
4. Compléter une étape à la fois en suivant [pipeline_template/README.md](pipeline_template/README.md).
5. Rédiger l'interprétation avec [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md).

La fiche [Python — points de départ](PYTHON_SNIPPETS.md) contient du code simple
et commenté sur de petites données de visites. Choisissez les exemples utiles,
expliquez-les, puis adaptez-les aux tickets.

## Deux variables à analyser

- `channel` : le canal de contact (`phone`, `chat` ou `email`).
- `resolution_minutes` : la durée de résolution, en minutes.

`ticket_id` sert uniquement à identifier une observation, repérer les doublons
et retrouver une décision de qualité. Ce n'est pas une mesure à résumer.

## Les cinq étapes

```text
01_auditer.py              → regarder les données brutes
02_preparer.py             → appliquer et tracer les décisions de qualité
03_decrire.py              → résumer les durées par canal
04_visualiser.py           → comparer les distributions
05_mesurer_frequences.py   → mesurer une fréquence dans chaque canal
```

L'étape 01 est exécutable. Les étapes 02 à 05 donnent des chemins, des contrats
et des fonctions à compléter. Lorsque chaque étape fonctionne, utilisez
`executer_pipeline.py` pour rejouer l'ensemble.

Le dossier `pipeline_template/` est le point de départ du jeudi. La version
complète sera distribuée séparément vendredi matin.

## Organisation du jeudi

- **Lancement collectif** : rappeler les principes, lire la mission et essayer
  les points de départ.
- **Matinée individuelle** : auditer, justifier les décisions de qualité,
  préparer les données et commencer les résumés.
- **Après-midi individuelle** : compléter les résumés, figures et fréquences,
  vérifier le pipeline et écrire une conclusion argumentée.

Gardez une trace de ce que vous avez compris, de vos choix et de ce qui reste
incertain. Les checkpoints servent à expliquer votre raisonnement.

## Environnement

Décompressez l'archive, puis ouvrez le dossier extrait dans VS Code.
Sélectionnez l'environnement Python du cours. Si les bibliothèques manquent,
installez-les dans cet environnement :

```bash
python -m pip install pandas plotly
```

Depuis le dossier extrait, lancez la première étape :

```bash
python pipeline_template/01_auditer.py
```

Le tableau d'audit apparaît dans `outputs/audit_structure.csv`. Les chemins
sont calculés depuis les scripts ; le CSV brut reste dans `data/raw/`.
Les étapes 02 à 05 sont à compléter avant de lancer tout le pipeline.

Les données sont **simulées**. Une différence entre canaux dans ce fichier ne
démontre pas un effet causal du canal et ne décrit pas la performance d'un vrai
service support. Les modèles générateurs et la correction restent dans les
supports du formateur jusqu'au débrief du vendredi.
