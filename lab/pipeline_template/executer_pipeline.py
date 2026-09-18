"""Rejouer les étapes après les avoir terminées et vérifiées séparément."""

import subprocess
import sys
from pathlib import Path

RACINE_PIPELINE = Path(__file__).resolve().parent
ETAPES = [
    "01_auditer.py",
    "02_preparer.py",
    "03_decrire.py",
    "04_visualiser.py",
    "05_mesurer_frequences.py",
]


def main():
    for etape in ETAPES:
        chemin_script = RACINE_PIPELINE / etape
        print(f"\nExécution de {etape}", flush=True)
        # Réutiliser le même Python ; s'arrêter dès qu'une étape échoue.
        subprocess.run([sys.executable, str(chemin_script)], check=True)


if __name__ == "__main__":
    main()
