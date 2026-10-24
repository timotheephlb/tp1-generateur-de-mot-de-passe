# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb
import json
import os


class ErreurCoffre(Exception):
    """Erreur de lecture ou d'écriture du fichier du coffre-fort."""


class Entree:
    """Un couple e-mail / mot de passe du coffre-fort."""

    def __init__(self, email, mot_de_passe):
        self.email = email
        self.mot_de_passe = mot_de_passe

    def vers_dict(self):
        """Convertit l'entrée en dictionnaire (pour l'écrire en JSON)."""
        return {
            "email": self.email,
            "mot_de_passe": self.mot_de_passe
        }

    @classmethod
    def depuis_dict(cls, donnees):
        """Crée une entrée depuis un dictionnaire. Lève ValueError si les données sont invalides."""
        if not isinstance(donnees, dict):
            raise ValueError("une entrée doit être un dictionnaire")
        for champ in ("email", "mot_de_passe"):
            if not isinstance(donnees.get(champ), str):
                raise ValueError(f"champ « {champ} » manquant ou invalide")
        return cls(donnees["email"], donnees["mot_de_passe"])

    def __repr__(self):
        return f"Entree(email='{self.email}')"


class Coffre:
    """Collection d'entrées, avec sa sauvegarde dans un fichier JSON en texte clair."""

    def __init__(self, chemin="vault.json"):
        self.chemin = chemin
        self.entrees = []

    def email_existe(self, email, ignorer=None):
        """Indique si l'e-mail est déjà utilisé (sans tenir compte de la casse).
        `ignorer` exclut l'entrée en cours de modification."""
        email = email.strip().lower()
        for entree in self.entrees:
            if entree is not ignorer and entree.email.lower() == email:
                return True
        return False

    def ajouter(self, entree):
        if self.email_existe(entree.email):
            raise ValueError("Cet e-mail existe déjà dans le coffre-fort")
        self.entrees.append(entree)

    def modifier(self, entree, email, mot_de_passe):
        if self.email_existe(email, ignorer=entree):
            raise ValueError("Cet e-mail existe déjà dans le coffre-fort")
        entree.email = email
        entree.mot_de_passe = mot_de_passe

    def supprimer(self, entree):
        self.entrees.remove(entree)

    def trier_par_email(self, inverse=False):
        """Retourne les entrées triées par e-mail (ordre alphabétique, sans tenir compte de la casse)."""
        return sorted(self.entrees, key=lambda entree: entree.email.lower(), reverse=inverse)

    def charger(self):
        """Charge le fichier JSON. Un fichier absent donne un coffre vide.
        Lève ErreurCoffre si le fichier est illisible ou invalide."""
        self.entrees = []
        try:
            with open(self.chemin, "r", encoding="utf-8") as fichier:
                donnees = json.load(fichier)
        except FileNotFoundError:
            return
        except PermissionError:
            raise ErreurCoffre(f"Permission refusée pour lire « {self.chemin} »")
        except json.JSONDecodeError as erreur:
            raise ErreurCoffre(f"JSON invalide dans « {self.chemin} » : {erreur}")
        except UnicodeDecodeError as erreur:
            raise ErreurCoffre(f"Erreur d'encodage dans « {self.chemin} » : {erreur}")
        except OSError as erreur:
            raise ErreurCoffre(f"Impossible de lire « {self.chemin} » : {erreur}")

        if not isinstance(donnees, list):
            raise ErreurCoffre(f"« {self.chemin} » doit contenir une liste d'entrées")

        entrees = []
        for i, donnees_entree in enumerate(donnees, start=1):
            try:
                entrees.append(Entree.depuis_dict(donnees_entree))
            except ValueError as erreur:
                raise ErreurCoffre(f"Entrée n° {i} invalide dans « {self.chemin} » : {erreur}")
        self.entrees = entrees

    def sauvegarder(self):
        """Écrit le fichier JSON. On écrit d'abord dans un fichier temporaire, puis on le renomme :
        si l'écriture échoue, l'ancien fichier reste intact."""
        chemin_temporaire = self.chemin + ".tmp"
        try:
            with open(chemin_temporaire, "w", encoding="utf-8") as fichier:
                json.dump([entree.vers_dict() for entree in self.entrees],
                          fichier, indent=4, ensure_ascii=False)
            os.replace(chemin_temporaire, self.chemin)
        except OSError as erreur:
            raise ErreurCoffre(f"Impossible d'écrire « {self.chemin} » : {erreur}")

    def mettre_de_cote_fichier_corrompu(self):
        """Renomme le fichier invalide en « .corrompu » pour ne pas l'écraser à la prochaine sauvegarde.
        Retourne le nouveau chemin."""
        nouveau_chemin = self.chemin + ".corrompu"
        os.replace(self.chemin, nouveau_chemin)
        return nouveau_chemin