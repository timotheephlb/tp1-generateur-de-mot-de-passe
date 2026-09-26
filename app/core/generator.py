import string


class PasswordGenerator:
    TYPES_CARACTERES={
        "minuscule": string.ascii_lowercase,
        "majuscule": string.ascii_uppercase,
        "nombre":string.digits,
        "symbole":string.punctuation
    }
    def __init__(self,longueur,utilise_minuscule,utilise_majuscule,utilise_nombre,utilise_symbole,valide):
        self.longueur=longueur
        self.utilise_minuscule=utilise_minuscule
        self.utilise_majuscule=utilise_majuscule
        self.utilise_nombre=utilise_nombre
        self.utilise_symbole=utilise_symbole
        self.valide=valide

