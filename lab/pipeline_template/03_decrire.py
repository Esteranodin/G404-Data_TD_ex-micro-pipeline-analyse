"""Étape 03 : décrire la durée de résolution dans chaque canal."""

import pandas as pd

from chemins_projet import CSV_NETTOYE, CSV_RESUME, creer_dossiers_sortie


def decrire_par_groupe(tickets_nettoyes):
    """Renvoyer une ligne par canal.

    Colonnes : channel, nombre, moyenne, mediane, ecart_type,
    q1, q3, minimum, maximum.
    """

    lignes_resume = []
    canaux = tickets_nettoyes["channel"].unique()

    for canal in canaux:
        appartient_au_groupe = tickets_nettoyes["channel"] == canal
        tickets_du_canal = tickets_nettoyes.loc[appartient_au_groupe]
        durees = tickets_du_canal["resolution_minutes"]

        ligne = {
            "channel": canal,
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



def main():
    """Décrire les durées de résolution pour chaque canal.

    Lit les tickets nettoyés, calcule les statistiques descriptives
    par canal, vérifie les effectifs, puis enregistre le résumé au
    format CSV.
    """
    
    tickets_nettoyes = pd.read_csv(CSV_NETTOYE)
    resume = decrire_par_groupe(tickets_nettoyes)

    assert resume["nombre"].sum() == len(tickets_nettoyes)
    
    creer_dossiers_sortie()
    resume.to_csv(CSV_RESUME, index=False)
    print(resume.to_string(index=False))
    print(f"Sortie : {CSV_RESUME}")
    print("Contrôle : la somme des effectifs égale le nombre de lignes nettoyées.")


if __name__ == "__main__":
    main()
