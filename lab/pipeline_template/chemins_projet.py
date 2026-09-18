"""Chemins communs au pipeline étudiant."""

from pathlib import Path

RACINE_PIPELINE = Path(__file__).resolve().parent
RACINE_LAB = RACINE_PIPELINE.parent

CSV_BRUT = RACINE_LAB / "data" / "raw" / "tickets_support.csv"
CSV_NETTOYE = RACINE_LAB / "data" / "processed" / "tickets_support_nettoyes.csv"
CSV_JOURNAL_QUALITE = RACINE_LAB / "outputs" / "journal_decisions_qualite.csv"
CSV_AUDIT = RACINE_LAB / "outputs" / "audit_structure.csv"
CSV_RESUME = RACINE_LAB / "outputs" / "resume_par_groupe.csv"
CSV_FREQUENCES = RACINE_LAB / "outputs" / "frequences_empiriques_180_minutes.csv"
HTML_DISTRIBUTIONS = RACINE_LAB / "outputs" / "distributions_temps_resolution.html"
HTML_BOITE = RACINE_LAB / "outputs" / "boite_temps_resolution.html"

COLONNES_REQUISES = ["ticket_id", "channel", "resolution_minutes"]
CANAUX_ATTENDUS = ["phone", "chat", "email"]
SEUIL_QUEUE_MINUTES = 180


def creer_dossiers_sortie():
    """Créer les dossiers dérivés sans toucher au CSV brut."""
    CSV_NETTOYE.parent.mkdir(parents=True, exist_ok=True)
    CSV_AUDIT.parent.mkdir(parents=True, exist_ok=True)
