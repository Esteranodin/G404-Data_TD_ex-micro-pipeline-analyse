"""Étape 05 : mesurer une fréquence observée au-delà d'un seuil."""

import pandas as pd

from chemins_projet import (
    CSV_FREQUENCES,
    CSV_NETTOYE,
    SEUIL_QUEUE_MINUTES,
    creer_dossiers_sortie,
)


def calculer_frequences_queue(tickets_nettoyes):
    """Renvoyer une ligne par canal au seuil SEUIL_QUEUE_MINUTES.

    Colonnes : channel, seuil_minutes, nombre_queue,
    effectif_groupe, frequence_queue.
    """
    lignes_frequences = []

    for canal in tickets_nettoyes["channel"].unique():
        appartient_au_canal = tickets_nettoyes["channel"] == canal
        canaux = tickets_nettoyes.loc[appartient_au_canal]
        atteint_seuil = canaux["resolution_minutes"] >= SEUIL_QUEUE_MINUTES

        nombre_queue = int(atteint_seuil.sum())
        effectif_canal = len(canaux)
        frequence_queue = nombre_queue / effectif_canal

        ligne = {
            "channel": canal,
            "seuil_minutes": SEUIL_QUEUE_MINUTES,
            "nombre_queue": nombre_queue,
            "effectif_groupe": effectif_canal,
            "frequence_queue": frequence_queue,
        }
        lignes_frequences.append(ligne)

    return pd.DataFrame(lignes_frequences)


def main():
    """Mesurer la fréquence des longues durées par canal.

    Lit les tickets nettoyés, calcule la proportion de tickets dont
    la durée atteint ou dépasse le seuil défini, puis enregistre les
    fréquences obtenues au format CSV.
    """

    tickets_nettoyes = pd.read_csv(CSV_NETTOYE)
    frequences = calculer_frequences_queue(tickets_nettoyes)


    # --- Contrôles ---
    assert frequences["effectif_groupe"].sum() == len(tickets_nettoyes)
    assert (frequences["nombre_queue"] >= 0).all()
    assert (
        frequences["nombre_queue"] <= frequences["effectif_groupe"]
    ).all()
    assert frequences["frequence_queue"].between(0, 1).all()

    # Vérification indépendante : recompter à la main, par un autre chemin,
    # pour un canal choisi.
    frequence_email = frequences.loc[
        frequences["channel"] == "email", "frequence_queue"
    ].iloc[0]
    nombre_email_independant = (
        tickets_nettoyes.loc[
            tickets_nettoyes["channel"] == "email", "resolution_minutes"
        ] >= SEUIL_QUEUE_MINUTES
    ).sum()
    effectif_email_independant = (tickets_nettoyes["channel"] == "email").sum()
    assert frequence_email == nombre_email_independant / effectif_email_independant

    print("Contrôles réussis pour les fréquences de queue.")
    creer_dossiers_sortie()
    frequences.to_csv(CSV_FREQUENCES, index=False)
    print(f"Seuil : {SEUIL_QUEUE_MINUTES} minutes")
    print(frequences.to_string(index=False))
    print(f"Sortie : {CSV_FREQUENCES}")
    print("Contrôle : vérifier le numérateur et le dénominateur de chaque ligne.")


if __name__ == "__main__":
    main()
