import pandas as pd

from chemins_projet import (
    CSV_BRUT,
    CSV_JOURNAL_QUALITE,
    CSV_NETTOYE,
    creer_dossiers_sortie,
)


def preparer_tickets(donnees_brutes):
    """Renvoyer deux tableaux : tickets_nettoyes, journal_qualite.

    CSV nettoyé : ticket_id, channel, resolution_minutes.
    Journal : ligne_source, ticket_id, regle, decision, justification.
    """
    travail = donnees_brutes.copy()
    travail["ligne_source"] = range(2, len(travail) + 2)

    journal = []
    lignes_a_exclure = pd.Series(False, index=travail.index)

# *****************************************************************************************
# ------------- Normaliser les canaux -------------
# *****************************************************************************************
    canal_avant = travail["channel"]
    canal_apres = canal_avant.str.strip().str.casefold()
    masque_canal_corrige = canal_avant != canal_apres

    for indice in travail.index[masque_canal_corrige]:
        journal.append({
            "ligne_source": int(travail.loc[indice, "ligne_source"]),
            "ticket_id": travail.loc[indice, "ticket_id"],
            "regle": "modalite_channel",
            "decision": "corrigee",
            "justification": (
                f"Le canal « {canal_avant.loc[indice]} » est normalisé en "
                f"« {canal_apres.loc[indice]} »."
            ),
        })

    travail["channel"] = canal_apres

# *****************************************************************************************
# ------------- Convertir et contrôler les durées -------------
# *****************************************************************************************

    texte_duree = travail["resolution_minutes"].str.strip()
    duree_numerique = pd.to_numeric(texte_duree, errors="coerce")
    travail["resolution_minutes"] = duree_numerique

    masque_duree_absente = texte_duree == ""
    masque_duree_non_numerique = (
        (texte_duree != "") & duree_numerique.isna()
    )
    masque_duree_negative = duree_numerique < 0

    for indice in travail.index[masque_duree_absente]:
        journal.append({
            "ligne_source": int(travail.loc[indice, "ligne_source"]),
            "ticket_id": travail.loc[indice, "ticket_id"],
            "regle": "duree_absente",
            "decision": "exclue",
            "justification": "La durée est vide.",
        })

    for indice in travail.index[masque_duree_non_numerique]:
        journal.append({
            "ligne_source": int(travail.loc[indice, "ligne_source"]),
            "ticket_id": travail.loc[indice, "ticket_id"],
            "regle": "duree_non_numerique",
            "decision": "exclue",
            "justification": "La durée ne peut pas être convertie en nombre.",
        })

    for indice in travail.index[masque_duree_negative]:
        ancienne_valeur = travail.loc[indice, "resolution_minutes"]
        nouvelle_valeur = abs(ancienne_valeur)
        travail.loc[indice, "resolution_minutes"] = nouvelle_valeur

        journal.append({
            "ligne_source": int(travail.loc[indice, "ligne_source"]),
            "ticket_id": travail.loc[indice, "ticket_id"],
            "regle": "duree_negative",
            "decision": "corrigee",
            "justification": (
                f"{ancienne_valeur} est corrigée en {nouvelle_valeur}."
            ),
        })

    lignes_a_exclure |= (
        masque_duree_absente | masque_duree_non_numerique
    )

# *****************************************************************************************
# ------------- Vérifier le format des identifiants -------------
# *****************************************************************************************
    
    schema_ticket_id = r"TKT-[0-9]{4}"
    masque_ticket_invalide = ~travail["ticket_id"].str.fullmatch(
        schema_ticket_id,
        na=False,
    )

    for indice in travail.index[masque_ticket_invalide]:
        journal.append({
            "ligne_source": int(travail.loc[indice, "ligne_source"]),
            "ticket_id": travail.loc[indice, "ticket_id"],
            "regle": "format_ticket_id",
            "decision": "exclue",
            "justification": (
                "L'identifiant ne respecte pas le format TKT- suivi de "
                "quatre chiffres."
            ),
        })

    lignes_a_exclure |= masque_ticket_invalide

# *****************************************************************************************
# ------------- Suppression -------------
# *****************************************************************************************
    # Exclure les lignes déjà invalides avant de chercher les doublons
    travail = travail.loc[~lignes_a_exclure].copy()

    # Supprimer la deuxième occurrence des identifiants répétés
    masque_a_supprimer = travail["ticket_id"].duplicated(
        keep="first"
    )

    for indice in travail.index[masque_a_supprimer]:
        journal.append({
            "ligne_source": int(travail.loc[indice, "ligne_source"]),
            "ticket_id": travail.loc[indice, "ticket_id"],
            "regle": "identifiant_duplique",
            "decision": "exclue",
            "justification": (
                "Deuxième occurrence du ticket ; première occurrence conservée."
            ),
        })

    travail = travail.loc[~masque_a_supprimer].copy()

    colonnes_sortie = [
        "ticket_id",
        "channel",
        "resolution_minutes",
    ]
    tickets_nettoyes = travail[colonnes_sortie]

    colonnes_journal = [
        "ligne_source",
        "ticket_id",
        "regle",
        "decision",
        "justification",
    ]
    journal_qualite = pd.DataFrame(journal, columns=colonnes_journal)

    return tickets_nettoyes, journal_qualite


def main():
    """Charger les tickets bruts, les préparer et enregistrer les résultats.

    Lit le fichier CSV brut, nettoie les données avec `preparer_tickets`,
    puis enregistre :
    - le fichier CSV des tickets nettoyés ;
    - le journal des décisions de qualité.

    Affiche également un résumé du traitement.
    """
    
    donnees_brutes = pd.read_csv(CSV_BRUT, dtype="string", keep_default_na=False)
    tickets_nettoyes, journal_qualite = preparer_tickets(donnees_brutes)

    creer_dossiers_sortie()
    tickets_nettoyes.to_csv(CSV_NETTOYE, index=False)
    journal_qualite.to_csv(CSV_JOURNAL_QUALITE, index=False)

    print(f"Lignes brutes : {len(donnees_brutes)}")
    print(f"Lignes analysables : {len(tickets_nettoyes)}")
    print(f"Données nettoyées : {CSV_NETTOYE}")
    print(f"Journal : {CSV_JOURNAL_QUALITE}")
    print("Contrôle : justifier chaque ligne retirée à l'aide du journal.")


if __name__ == "__main__":
    main()