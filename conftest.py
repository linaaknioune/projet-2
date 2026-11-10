import sys
from pathlib import Path

# Ajouter le dossier src au début du chemin de recherche
RACINE = Path(__file__).resolve().parent
SRC = RACINE / "src"

sys.path.insert(0, str(SRC))
