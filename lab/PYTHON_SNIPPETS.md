# Python — points de départ pour votre pipeline

Ces exemples utilisent de petites données fictives de **visites**, distinctes
des tickets. Ils montrent des opérations simples : lire, sélectionner,
contrôler, décrire et dessiner. Vous choisissez ensuite ce qui convient à votre
analyse et vous justifiez vos choix.

Pour chaque extrait : **prédire → exécuter → inspecter → expliquer**.

Le notebook de préparation, présenté séparément, montre les cinq étapes
sur un petit exemple en dix minutes.
Cette fiche reste le support détaillé à consulter pendant votre projet.

## Utiliser la fiche

Créez `essais_snippets.py` dans `pipeline_template/`, puis utilisez le Python `.venv`
du cours. Ajoutez les extraits dans l'ordre. Ils écrivent uniquement dans
`outputs/exemples_snippets/`. Vous pouvez lancer le fichier après chaque
ajout ; les figures seront remplacées lors d'une nouvelle exécution.

Les sections 1 à 5 illustrent l'audit et une correction. La section 6 fournit
un **nouveau tableau déjà valide** pour les statistiques : elle ne corrige pas
les anomalies de l'exemple précédent.

## 1. Lire les données sans perdre le texte d'origine

`StringIO` permet ici de lire un CSV écrit dans le code. `dtype="string"` garde
les cellules sous forme de texte ; `keep_default_na=False` garde une cellule
vide sous la forme `""`.

```python
from io import StringIO
from pathlib import Path

import pandas as pd
import plotly.express as px

racine_lab = Path(__file__).resolve().parents[1]
dossier_exemples = racine_lab / "outputs" / "exemples_snippets"
dossier_exemples.mkdir(parents=True, exist_ok=True)

csv_exemple = """visit_id,visit_type,duration_minutes
V001,self_guided,25
V002, self_guided ,40
V003,guided,55
V004,guided,80
V005,self_guided,
V006,guided,erreur
V007,self_guided,-5
V003,guided,55
"""

exemple_brut = pd.read_csv(
    StringIO(csv_exemple),
    dtype="string",
    keep_default_na=False,
)
print(exemple_brut)
```

Pour le projet, remplacez la lecture de `StringIO(csv_exemple)` par :

```python
from chemins_projet import CSV_BRUT

donnees_brutes = pd.read_csv(CSV_BRUT, dtype="string", keep_default_na=False)
print(donnees_brutes.head())
```

Le **type chargé** est du texte, même quand la colonne représente une durée.
Il faudra convertir cette mesure avant de la calculer.

## 2. Regarder la structure et les valeurs à examiner

```python
print("Dimensions :", exemple_brut.shape)
print("Types chargés :")
print(exemple_brut.dtypes)
print("Modalités de visite :")
print(exemple_brut["visit_type"].value_counts(dropna=False))

for colonne in exemple_brut.columns:
    valeurs = exemple_brut[colonne]
    cellules_vides = valeurs.str.strip() == ""
    nombre_vides = int(cellules_vides.sum())
    print(colonne, ":", nombre_vides, "cellule(s) vide(s)")

identifiants_repetes = exemple_brut["visit_id"].duplicated(keep=False)
print("Lignes portant un identifiant répété :")
print(exemple_brut.loc[identifiants_repetes])
```

Un *masque*, comme `cellules_vides`, contient un booléen (`True` ou `False`)
par ligne. `loc[masque]` sélectionne les lignes où il vaut `True`.
`duplicated(keep=False)` montre toutes les occurrences d'un identifiant répété.
Vérifiez les autres colonnes avant de décider s'il s'agit d'un doublon exact.

**À adapter :** `visit_id` devient `ticket_id` ; `visit_type` devient `channel`.
La lecture en texte préserve les cellules vides : `isna()` seul ne les détecte
pas à ce stade.

## 3. Convertir une mesure et distinguer les problèmes

```python
travail = exemple_brut.copy()
travail["ligne_source"] = range(2, len(travail) + 2)

texte_duree = travail["duration_minutes"].str.strip()
duree_numerique = pd.to_numeric(texte_duree, errors="coerce")
travail["duration_minutes"] = duree_numerique

cellule_vide = texte_duree == ""
conversion_impossible = (texte_duree != "") & duree_numerique.isna()
duree_negative = duree_numerique < 0

print("Durées absentes :")
print(travail.loc[cellule_vide])
print("Textes non convertibles :")
print(exemple_brut.loc[conversion_impossible])
print("Durées négatives :")
print(travail.loc[duree_negative])
```

`errors="coerce"` transforme ce qui n'est pas convertible en valeur manquante.
La copie `exemple_brut` garde le texte initial pour comprendre le problème.
`&` signifie « et » entre deux masques ; entourez chaque comparaison de
parenthèses lorsqu'elles sont combinées.

`ligne_source` compte l'en-tête du CSV comme ligne 1. Créez-la avant de trier
ou filtrer. Une valeur grande mais possible reste différente d'une durée
négative. Le code ne décide pas de cette différence à votre place.

## 4. Corriger une modalité et expliquer chaque changement

Dans cet exemple, on sait que les espaces extérieurs n'ont aucune signification
pour le type de visite. On peut donc les retirer. On trace seulement les lignes
qui ont changé.

```python
journal = []

for indice in travail.index:
    ancienne_modalite = travail.loc[indice, "visit_type"]
    nouvelle_modalite = ancienne_modalite.strip()

    if ancienne_modalite != nouvelle_modalite:
        travail.loc[indice, "visit_type"] = nouvelle_modalite

        decision = {
            "ligne_source": int(travail.loc[indice, "ligne_source"]),
            "visit_id": travail.loc[indice, "visit_id"],
            "regle": "espaces_exterieurs",
            "decision": "corriger la modalité",
            "justification": "Les espaces ne distinguent pas un type de visite.",
        }
        journal.append(decision)

colonnes_journal = [
    "ligne_source", "visit_id", "regle", "decision", "justification"
]
journal_exemple = pd.DataFrame(journal, columns=colonnes_journal)
journal_exemple.to_csv(dossier_exemples / "journal_exemple.csv", index=False)
print(journal_exemple)
```

**À adapter :** dans le journal des tickets, la colonne d'identifiant s'appelle
`ticket_id`. Une règle de normalisation doit avoir un sens métier ; ne fusionnez
pas deux modalités seulement parce qu'elles se ressemblent.

## 5. Sélectionner des lignes après avoir pris une décision

Voici un filtre de durées numériques positives ou nulles. Il montre la
sélection ; il ne remplace pas un journal expliquant chaque exclusion.

```python
duree_presente = travail["duration_minutes"].notna()
duree_valide = travail["duration_minutes"] >= 0
a_garder = duree_presente & duree_valide

visites_durees_valides = travail.loc[a_garder].copy()
visites_a_examiner = travail.loc[~a_garder].copy()

print("Lignes dont la durée est valide :", len(visites_durees_valides))
print("Lignes à examiner :")
print(visites_a_examiner)
```

`~` inverse un masque. Ce filtre ne traite pas les identifiants répétés et ne
prouve pas la validité des modalités. **À faire dans votre pipeline :** relier
chaque exclusion au journal et contrôler les identifiants et les canaux.

## 6. Calculer dans un groupe avant de généraliser

Ce nouveau tableau contient dix visites valides. Les deux groupes ont des
effectifs différents pour rendre visible le choix du dénominateur.

```python
exemple_analyse = pd.DataFrame({
    "visit_type": [
        "self_guided", "self_guided", "self_guided", "self_guided",
        "guided", "guided", "guided", "guided", "guided", "guided",
    ],
    "duration_minutes": [25, 40, 55, 80, 30, 35, 50, 60, 90, 120],
})

est_visite_libre = exemple_analyse["visit_type"] == "self_guided"
visites_libres = exemple_analyse.loc[est_visite_libre]
durees_libres = visites_libres["duration_minutes"]

print("Effectif :", len(durees_libres))
print("Moyenne :", durees_libres.mean())
print("Médiane :", durees_libres.median())
print("Écart-type :", durees_libres.std(ddof=1))
print("Premier quartile :", durees_libres.quantile(0.25))
print("Troisième quartile :", durees_libres.quantile(0.75))
print("Minimum :", durees_libres.min())
print("Maximum :", durees_libres.max())
```

`std(ddof=1)` calcule l'écart-type d'échantillon, convention retenue ici.
Ne réduisez pas l'interprétation à la moyenne : le centre, la dispersion et
la forme répondent à des questions différentes.

## 7. Répéter le résumé pour chaque groupe

La boucle reprend les opérations précédentes. `return` renvoie le tableau
calculé par la fonction ; il n'écrit pas encore de fichier.

```python
def resumer_visites(donnees):
    lignes_resume = []
    types_visite = donnees["visit_type"].unique()

    for type_visite in types_visite:
        appartient_au_groupe = donnees["visit_type"] == type_visite
        groupe = donnees.loc[appartient_au_groupe]
        durees = groupe["duration_minutes"]

        ligne = {
            "visit_type": type_visite,
            "nombre": len(durees),
            "moyenne": durees.mean(),
            "mediane": durees.median(),
            "ecart_type": durees.std(ddof=1),
            "q1": durees.quantile(0.25),
            "q3": durees.quantile(0.75),
            "minimum": durees.min(),
            "maximum": durees.max(),
        }
        lignes_resume.append(ligne)

    return pd.DataFrame(lignes_resume)


resume_exemple = resumer_visites(exemple_analyse)
resume_exemple.to_csv(dossier_exemples / "resume_exemple.csv", index=False)
print(resume_exemple)

assert resume_exemple["nombre"].sum() == len(exemple_analyse)
```

`assert` arrête l'exécution si le contrôle échoue. Ici, aucun groupe ne doit
être oublié dans le résumé. **À adapter :** noms des deux variables, nom de la
fonction et chemin de sortie de l'étape 03. Gardez la précision pour les calculs ;
un arrondi peut être réservé à l'affichage.

## 8. Comparer les distributions dans deux figures

L'histogramme montre la répartition des durées par classes. Un panneau par groupe
évite les superpositions. Chaque petit trait en bas représente une visite.
Les classes et les échelles sont communes aux groupes. Dix valeurs servent ici
à comprendre le code ; elles ne suffisent pas à reconnaître une loi.

`px.histogram(marginal="rug")` fonctionne avec Plotly 6 et 7.
L'ancien `ff.create_distplot` du cours précédent n'existe plus en version 7.

```python
histogramme = px.histogram(
    exemple_analyse,
    x="duration_minutes",
    color="visit_type",
    facet_col="visit_type",
    marginal="rug",
    template="plotly_white",
    color_discrete_sequence=["#008C95", "#F06B52"],
    title="Durées des visites par type",
    labels={
        "duration_minutes": "Durée (minutes)",
        "visit_type": "Type de visite",
    },
)
histogramme.update_traces(
    xbins=dict(start=0, size=10), marker_line_width=1, marker_line_color="white",
    selector=dict(type="histogram"),
)
histogramme.update_traces(marker_size=12, marker_line_width=2, selector=dict(type="box"))
# Dans chaque panneau : histogramme en haut, observations en bas.
histogramme.update_layout(height=420, font_size=18, showlegend=False)
histogramme.update_yaxes(title_text="Nombre de visites", domain=[0.25, 1], range=[0, 3], dtick=1, row=1)
histogramme.update_yaxes(domain=[0, 0.15], row=2)
histogramme.update_xaxes(range=[0, 130], title=None, showticklabels=False)
histogramme.update_xaxes(title_text="Durée (minutes)", showticklabels=True, row=2)
histogramme.write_html(
    dossier_exemples / "histogramme_exemple.html",
    include_plotlyjs=True,
)

boite = px.box(
    exemple_analyse,
    x="visit_type",
    y="duration_minutes",
    color="visit_type",
    color_discrete_sequence=["#008C95", "#F06B52"],
    points="all",
    title="Centre et dispersion des durées",
    labels={
        "visit_type": "Type de visite",
        "duration_minutes": "Durée (minutes)",
    },
)
boite.write_html(dossier_exemples / "boite_exemple.html", include_plotlyjs=True)
```

Ouvrez les deux fichiers HTML. `include_plotlyjs=True` inclut ce dont chaque
fichier a besoin pour s'afficher hors connexion. Les points restent visibles :
une boîte à moustaches ne décide pas quelles observations supprimer.

**À adapter :** utilisez les colonnes du projet et les chemins fournis dans
l'étape 04. Choisissez des classes et une plage d'axes adaptées aux données
nettoyées. Le projet utilise des classes communes de 10 minutes, avec des bords
à 5, 15, 25… minutes. Vérifiez que l'axe inclut aussi toutes les valeurs rares.

## 9. Compter puis diviser dans chaque groupe

On cherche ici la proportion de visites durant **60 minutes ou plus**.
Le seuil du projet sera **180 minutes**.

```python
seuil_exemple = 60
lignes_frequences = []

for type_visite in exemple_analyse["visit_type"].unique():
    appartient_au_groupe = exemple_analyse["visit_type"] == type_visite
    groupe = exemple_analyse.loc[appartient_au_groupe]
    atteint_seuil = groupe["duration_minutes"] >= seuil_exemple

    nombre_queue = int(atteint_seuil.sum())
    effectif_groupe = len(groupe)
    frequence_queue = nombre_queue / effectif_groupe

    ligne = {
        "visit_type": type_visite,
        "seuil_minutes": seuil_exemple,
        "nombre_queue": nombre_queue,
        "effectif_groupe": effectif_groupe,
        "frequence_queue": frequence_queue,
    }
    lignes_frequences.append(ligne)

frequences_exemple = pd.DataFrame(lignes_frequences)
frequences_exemple.to_csv(
    dossier_exemples / "frequences_exemple.csv", index=False
)
print(frequences_exemple)
```

Vérifiez à la main : pour `self_guided`, une visite sur quatre atteint le seuil ;
pour `guided`, trois sur six l'atteignent. Le dénominateur est l'effectif du
**même groupe**, pas les dix visites du tableau.

**À adapter :** colonnes et seuil dans l'étape 05, puis `return` du tableau.
Les groupes parcourus ici existent dans le tableau et sont donc non vides.

## 10. Vérifier le résultat et expliquer une limite

```python
assert frequences_exemple["effectif_groupe"].sum() == len(exemple_analyse)
assert (frequences_exemple["nombre_queue"] >= 0).all()
assert (
    frequences_exemple["nombre_queue"] <= frequences_exemple["effectif_groupe"]
).all()
assert frequences_exemple["frequence_queue"].between(0, 1).all()

# Un petit exemple permet aussi une vérification indépendante, à la main.
frequence_libre = frequences_exemple.loc[
    frequences_exemple["visit_type"] == "self_guided", "frequence_queue"
].iloc[0]
assert frequence_libre == 1 / 4

print("Contrôles réussis pour l'exemple de visites.")
```

Adaptez les contrôles au contrat de chaque étape. Un programme peut s'exécuter
sans erreur tout en utilisant le mauvais dénominateur ou en supprimant à tort
des valeurs rares.

Terminez par une **observation**, sa **preuve**, une **limite** et la **prochaine
vérification**. Les calculs descriptifs n'établissent pas à eux seuls une cause.

## Où adapter les exemples ?

| Fichier du pipeline | Sections utiles | Travail à faire |
|---|---|---|
| `01_auditer.py` | 1–2 | Lire ses sorties et compléter vos observations |
| `02_preparer.py` | 2–5 | Décider, tracer, contrôler et renvoyer les deux tableaux |
| `03_decrire.py` | 6–7 | Résumer `resolution_minutes` pour chaque `channel` |
| `04_visualiser.py` | 8 | Choisir et exporter deux figures utiles |
| `05_mesurer_frequences.py` | 9–10 | Compter à partir de 180 minutes dans chaque canal |

Les fonctions à compléter ont déjà leurs entrées et sorties définies dans
[pipeline_template/README.md](pipeline_template/README.md). Construisez et expliquez votre version
jeudi ; le pipeline de référence sera comparé aux vôtres vendredi matin.
