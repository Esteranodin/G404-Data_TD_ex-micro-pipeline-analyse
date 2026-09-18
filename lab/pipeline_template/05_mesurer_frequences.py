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

    À FAIRE : compter les tickets à 180 minutes ou plus dans un canal, puis
    diviser par l'effectif analysable de ce même canal. Répéter par canal.
    frequence_queue est une proportion entre 0 et 1.
    Aide : section 9 de ../PYTHON_SNIPPETS.md.
    """
    raise NotImplementedError("À FAIRE : calculer les fréquences par canal.")


def main():
    """Mesurer la fréquence des longues durées par canal.

    Lit les tickets nettoyés, calcule la proportion de tickets dont
    la durée atteint ou dépasse le seuil défini, puis enregistre les
    fréquences obtenues au format CSV.
    """

    tickets_nettoyes = pd.read_csv(CSV_NETTOYE)
    frequences = calculer_frequences_queue(tickets_nettoyes)

    creer_dossiers_sortie()
    frequences.to_csv(CSV_FREQUENCES, index=False)
    print(f"Seuil : {SEUIL_QUEUE_MINUTES} minutes")
    print(frequences.to_string(index=False))
    print(f"Sortie : {CSV_FREQUENCES}")
    print("Contrôle : vérifier le numérateur et le dénominateur de chaque ligne.")


if __name__ == "__main__":
    main()
