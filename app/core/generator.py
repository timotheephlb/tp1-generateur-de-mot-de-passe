# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb
import string
import random


class PasswordGenerator:
    """Génère des mots de passe aléatoires selon la longueur et les types de caractères choisis."""
    TYPES_CARACTERES = {
        "minuscule": string.ascii_lowercase,
        "majuscule": string.ascii_uppercase,
        "nombre": string.digits,
        "symbole": string.punctuation
    }

    def __init__(self, longueur, utilise_minuscule, utilise_majuscule, utilise_nombre, utilise_symbole, valide):
        if longueur <= 0:
            raise ValueError("La longueur doit être positive")
        if not (utilise_minuscule or utilise_majuscule or utilise_nombre or utilise_symbole):
            raise ValueError("Au moins un type de caractère doit être sélectionné")

        nb_types = sum([utilise_minuscule, utilise_majuscule, utilise_nombre, utilise_symbole])
        if valide and longueur < nb_types:
            raise ValueError("La longueur est trop petite pour satisfaire la validation")

        self.longueur = longueur
        self.utilise_minuscule = utilise_minuscule
        self.utilise_majuscule = utilise_majuscule
        self.utilise_nombre = utilise_nombre
        self.utilise_symbole = utilise_symbole
        self.valide = valide

    def _generer_un_essai(self):
        """Construit un mot de passe aléatoire à partir des caractères autorisés (sans validation)."""
        chaine = ""
        if self.utilise_minuscule:
            chaine += self.TYPES_CARACTERES["minuscule"]
        if self.utilise_majuscule:
            chaine += self.TYPES_CARACTERES["majuscule"]
        if self.utilise_nombre:
            chaine += self.TYPES_CARACTERES["nombre"]
        if self.utilise_symbole:
            chaine += self.TYPES_CARACTERES["symbole"]
        if chaine == "":
            raise ValueError("Le mot de passe ne peut être vide")
        mot_de_passe = ""
        for i in range(self.longueur):
            mot_de_passe += random.choice(chaine)
        return mot_de_passe

    def generer(self):
        """Retourne un mot de passe. Si la validation est activée, régénère jusqu'à obtenir un mot de passe valide."""
        mot_de_passe = self._generer_un_essai()
        while self.valide and not self.valider(mot_de_passe):
            mot_de_passe = self._generer_un_essai()
        return mot_de_passe

    def valider(self, mot_de_passe):
        """Retourne True si le mot de passe contient au moins un caractère de chaque type sélectionné."""
        contient_minuscule=False
        contient_majuscule=False
        contient_nombre=False
        contient_symbole=False
        for c in mot_de_passe:
            if c in self.TYPES_CARACTERES["minuscule"]:
                contient_minuscule=True
            if c in self.TYPES_CARACTERES["majuscule"]:
                contient_majuscule=True
            if c in self.TYPES_CARACTERES["nombre"]:
                contient_nombre=True
            if c in self.TYPES_CARACTERES["symbole"]:
                contient_symbole=True

        if self.utilise_majuscule and not contient_majuscule:
            return False
        elif self.utilise_minuscule and not contient_minuscule:
            return False
        elif self.utilise_nombre and not contient_nombre:
            return False
        elif self.utilise_symbole and not contient_symbole:
            return False
        else :
            return True
