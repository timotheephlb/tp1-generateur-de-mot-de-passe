# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb
import json


class Entree:
    def __init__(self, email: str, mot_de_passe: str):
        self._email = None
        self._mot_de_passe = None
        self.email = email  # Utilise le setter pour valider
        self.mot_de_passe = mot_de_passe

    @property
    def email(self) -> str:
        """Retourne l'adresse e-mail."""
        return self._email

    @email.setter
    def email(self, valeur: str):
        """Définit l'adresse e-mail avec validation."""
        if not isinstance(valeur, str):
            raise TypeError("L'e-mail doit être une chaîne de caractères")
        valeur = valeur.strip()
        if "@" not in valeur:
            raise ValueError(f"L'e-mail « {valeur} » doit contenir un @")
        self._email = valeur

    @property
    def mot_de_passe(self) -> str:
        """Retourne le mot de passe."""
        return self._mot_de_passe

    @mot_de_passe.setter
    def mot_de_passe(self, valeur: str):
        """Définit le mot de passe avec validation."""
        if not isinstance(valeur, str):
            raise TypeError("Le mot de passe doit être une chaîne de caractères")
        if valeur == "":
            raise ValueError("Le mot de passe ne peut pas être vide")
        self._mot_de_passe = valeur

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
