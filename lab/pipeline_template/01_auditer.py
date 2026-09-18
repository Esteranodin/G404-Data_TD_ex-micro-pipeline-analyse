import pandas as pd

from chemins_projet import (
    COLONNES_REQUISES,
    CSV_AUDIT,
    CSV_BRUT,
    creer_dossiers_sortie,
)


def construire_audit_structure(donnees_brutes):
    """Décrire chaque colonne, sans corriger les données."""
    lignes_audit = []

    for colonne in donnees_brutes.columns:
        valeurs = donnees_brutes[colonne]
        cellules_vides = valeurs.str.strip() == ""
        valeurs_non_vides = valeurs.loc[~cellules_vides]

        ligne = {
            "colonne": colonne,
            "nombre_lignes": len(donnees_brutes),
            "cellules_vides": int(cellules_vides.sum()),
            "valeurs_distinctes_non_vides": valeurs_non_vides.nunique(),
            "type_detecte": str(valeurs.dtype),
        }
        lignes_audit.append(ligne)

    return pd.DataFrame(lignes_audit)


def main():
    """Auditer la structure du fichier de tickets bruts.

    Lit les données brutes, vérifie la présence des colonnes requises,
    décrit les colonnes sans modifier les données, puis enregistre
    l'audit structurel au format CSV.
    """

    # Lire en texte permet d'inspecter les valeurs avant de les convertir.
    donnees_brutes = pd.read_csv(CSV_BRUT, dtype="string", keep_default_na=False)

    for colonne in COLONNES_REQUISES:
        if colonne not in donnees_brutes.columns:
            raise ValueError(f"Colonne manquante : {colonne}")

    audit = construire_audit_structure(donnees_brutes)
    creer_dossiers_sortie()
    audit.to_csv(CSV_AUDIT, index=False)

    print(donnees_brutes.head())
    print(audit.to_string(index=False))
    print("Modalités observées :")
    print(donnees_brutes["channel"].value_counts(dropna=False))
    print(f"Sortie : {CSV_AUDIT}")
    print("À examiner ensuite : identifiants répétés et validité des durées.")


if __name__ == "__main__":
    main()