class DonneeInvalideError(Exception):
    """Levée quand une donnée (fichier, colonne, valeur) est inutilisable."""

class ModeleIndisponibleError(Exception):
    """Levée quand on utilise un modèle non entraîné ou introuvable."""
