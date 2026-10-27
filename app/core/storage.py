# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb
import json


class Entree:
    """Un couple e-mail / mot de passe du coffre-fort."""

    def __init__(self, email: str, mot_de_passe: str) -> None:
        self.email = email
        self.mot_de_passe = mot_de_passe

    def vers_dict(self) -> dict:
        """Convertit l'entrée en dictionnaire (pour l'écrire en JSON)."""
        return {
            "email": self.email,
            "mot_de_passe": self.mot_de_passe
        }

    @classmethod
    def depuis_dict(cls, donnees: dict) -> "Entree":
        """Crée une entrée depuis un dictionnaire lu dans le fichier JSON."""
        return cls(donnees["email"], donnees["mot_de_passe"])


class Storage:
    """Lit et écrit les entrées du coffre-fort dans un fichier JSON."""

    def __init__(self, chemin: str = "vault.json") -> None:
        self.chemin = chemin

    def charger(self) -> list[Entree]:
        """Lit le fichier JSON et retourne la liste des entrées.
        Retourne une liste vide si le fichier n'existe pas.
        Lève ValueError si le contenu du fichier est invalide."""
        try:
            with open(self.chemin, "r", encoding="utf-8") as fichier:
                donnees = json.load(fichier)
            return [Entree.depuis_dict(donnees_entree) for donnees_entree in donnees]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as erreur:
            raise ValueError(f"JSON invalide dans « {self.chemin} » : {erreur}")

    def sauvegarder(self, entrees: list[Entree]) -> None:
        """Écrit la liste des entrées dans le fichier JSON.
        Lève OSError si l'écriture échoue."""
        with open(self.chemin, "w", encoding="utf-8") as fichier:
            json.dump([entree.vers_dict() for entree in entrees],
                      fichier, indent=4, ensure_ascii=False)
