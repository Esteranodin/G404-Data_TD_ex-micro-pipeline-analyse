# Projet individuel — temps de résolution par canal

## Mission

Une responsable support veut décrire les durées de résolution selon le canal
de contact. Elle vous confie un export à contrôler avant de l'analyser.

> Comment les durées de résolution varient-elles entre les canaux, et quelles
> observations faut-il vérifier avant de faire confiance aux comparaisons ?

Les données sont simulées. Les mécanismes qui les ont générées seront révélés
vendredi, avec le pipeline de référence.

## Dictionnaire des données

Une ligne représente un enregistrement de ticket. L'audit doit vérifier si
chaque ticket n'apparaît qu'une fois.

| Colonne | Rôle | Sens attendu |
|---|---|---|
| `ticket_id` | Identifiant de suivi | Retrouver un ticket et repérer un identifiant répété |
| `channel` | Variable qualitative de groupe | `phone` (téléphone), `chat` ou `email` |
| `resolution_minutes` | Variable quantitative | Durée de résolution en minutes, positive ou nulle |

Il y a **deux variables à analyser** : le canal et la durée. L'identifiant est
un outil de traçabilité ; sa moyenne n'aurait aucun sens.

## Règles

- Travail individuel, jeudi matin et après-midi.
- Conservez le CSV brut intact.
- Gardez les noms des trois colonnes tels qu'ils sont fournis.
- Écrivez du code lisible : une étape explicite vaut mieux qu'une formule opaque.
- Justifiez chaque correction, exclusion ou conservation signalée.
- Une durée inhabituelle peut être plausible : elle mérite une investigation.
- Décrivez d'abord les observations, sans imposer une loi théorique.

## 1. Cadrer et auditer

Avant les calculs, précisez l'unité d'observation, la population que l'on
voudrait étudier, la mesure et les groupes. Le fichier simulé permet de
s'exercer ; il ne représente pas une population réelle documentée.

Contrôlez :

- dimensions, noms des colonnes et types chargés ;
- identifiants vides ou répétés ;
- cellules vides ;
- modalités de canal ;
- conversion et validité des durées.

Un identifiant répété signifie-t-il que deux lignes sont identiques ou qu'elles
se contredisent ? Une durée très grande est-elle impossible ou seulement rare ?
Écrivez votre décision avant de la programmer.

## 2. Préparer et tracer

Produisez `data/processed/tickets_support_nettoyes.csv` avec les trois colonnes
initiales, et des durées numériques. Ne laissez aucune ligne invalide entrer
silencieusement dans les calculs.

Dans `outputs/journal_decisions_qualite.csv`, utilisez les colonnes :

```text
ligne_source, ticket_id, regle, decision, justification
```

`ligne_source` désigne le numéro de ligne dans le CSV brut, en comptant
l'en-tête comme ligne 1. Créez ce repère avant tout tri ou filtre. Documentez
les observations signalées et conservées dans le journal ou dans la section
« Observations inhabituelles » du rapport. Il n'est pas nécessaire d'ajouter
une variable analytique au CSV nettoyé.

## 3. Décrire par canal

Produisez `outputs/resume_par_groupe.csv` avec une ligne par canal : effectif,
moyenne, médiane, écart-type, premier et troisième quartiles, minimum et maximum.

Expliquez ce que chaque indicateur apporte. Comparez le centre, la dispersion
et la forme ; une différence de moyennes ne résume pas toute la distribution.

## 4. Visualiser

Créez deux fichiers HTML :

- trois histogrammes séparés de `resolution_minutes`, un panneau par `channel`,
  avec les mêmes axes, des classes de 10 minutes (5, 15, 25, …) et un trait par
  observation en dessous ;
- une vue qui facilite la comparaison des médianes, dispersions et observations
  inhabituelles.

Une densité lissée est une exploration optionnelle, après les histogrammes.

Rendez visibles les canaux et l'unité. Justifiez les classes de l'histogramme
et utilisez des axes comparables. Ouvrez les deux fichiers pour vérifier que
les figures s'affichent aussi hors connexion.

## 5. Mesurer une fréquence dans chaque canal

Utilisez le seuil commun de **180 minutes**, avec une comparaison **supérieure
ou égale** au seuil :

> Parmi les tickets analysables de ce canal, quelle proportion a une durée de
> résolution de 180 minutes ou plus ?

```text
fréquence observée dans le canal
= nombre de tickets du canal à 180 minutes ou plus
  / nombre de tickets analysables de ce même canal
```

Donnez le numérateur, le dénominateur et la fréquence. Ne remplacez pas le
dénominateur par l'effectif du fichier entier. Cette fréquence est observée
dans les données ; aucun modèle théorique n'est nécessaire pour la calculer.

## Livrables et vérification finale

- Les cinq étapes du pipeline et son lanceur.
- Un CSV nettoyé et un journal des décisions.
- Un résumé descriptif et un tableau des fréquences par canal.
- Deux graphiques HTML lisibles hors connexion.
- Une conclusion courte suivant [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md).

Rejouez le pipeline. Vérifiez les effectifs, rapprochez chaque retrait du
journal, puis expliquez une statistique, un graphique et une limite à une autre
personne. Une association observée entre canal et durée ne suffit pas à
conclure que le canal provoque cette différence.
