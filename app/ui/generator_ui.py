# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb
import sys

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QSlider, QSpinBox,
    QCheckBox, QVBoxLayout, QHBoxLayout, QGridLayout
)

from app.core.generator import PasswordGenerator

LONGUEUR_MIN = 4
LONGUEUR_MAX = 64
LONGUEUR_DEFAUT = 16
MESSAGE_COPIE = "Copié dans le presse-papiers"


class FenetreGenerateur(QWidget):
    """Fenêtre de génération de mot de passe (réutilise PasswordGenerator de la Partie 1).

    Le signal mot_de_passe_choisi est émis quand l'utilisateur clique sur « Utiliser »,
    pour transmettre le mot de passe à la fenêtre appelante.
    """

    mot_de_passe_choisi = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Générer un mot de passe")
        self.setMinimumWidth(460)

        self.mot_de_passe = ""
        self.est_affiche = True

        self.initialiser_ui()
        self.generer()

    def initialiser_ui(self) -> None:
        """Assemble l'interface à partir de ses différentes zones."""
        disposition = QVBoxLayout()
        disposition.addLayout(self.creer_zone_affichage())
        disposition.addLayout(self.creer_zone_longueur())
        disposition.addLayout(self.creer_zone_types())
        disposition.addLayout(self.creer_zone_boutons())

        self.etiquette_message = QLabel()
        self.etiquette_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        disposition.addWidget(self.etiquette_message)

        self.setLayout(disposition)
        self.connecter_signaux()

    def creer_zone_affichage(self) -> QHBoxLayout:
        """Étiquette large et sélectionnable à la souris, avec le bouton masquer/afficher."""
        disposition = QHBoxLayout()
        self.etiquette_mdp = QLabel()
        self.etiquette_mdp.setMinimumHeight(60)
        self.etiquette_mdp.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.bouton_masquer = QPushButton("Masquer")
        disposition.addWidget(self.etiquette_mdp, 1)
        disposition.addWidget(self.bouton_masquer)
        return disposition

    def creer_zone_longueur(self) -> QVBoxLayout:
        """Curseur et boîte numérique pour choisir la longueur."""
        disposition = QVBoxLayout()
        disposition.addWidget(QLabel("Longueur"))

        ligne = QHBoxLayout()
        self.curseur = QSlider(Qt.Orientation.Horizontal)
        self.curseur.setRange(LONGUEUR_MIN, LONGUEUR_MAX)
        self.curseur.setValue(LONGUEUR_DEFAUT)
        self.boite_longueur = QSpinBox()
        self.boite_longueur.setRange(LONGUEUR_MIN, LONGUEUR_MAX)
        self.boite_longueur.setValue(LONGUEUR_DEFAUT)
        ligne.addWidget(QLabel(str(LONGUEUR_MIN)))
        ligne.addWidget(self.curseur, 1)
        ligne.addWidget(QLabel(str(LONGUEUR_MAX)))
        ligne.addWidget(self.boite_longueur)
        disposition.addLayout(ligne)
        return disposition

    def creer_zone_types(self) -> QVBoxLayout:
        """Cases à cocher pour les types de caractères et la validation."""
        disposition = QVBoxLayout()

        grille = QGridLayout()
        self.case_minuscule = QCheckBox("Minuscules")
        self.case_majuscule = QCheckBox("Majuscules")
        self.case_nombre = QCheckBox("Chiffres")
        self.case_symbole = QCheckBox("Symboles")
        self.case_valide = QCheckBox("Valider (au moins un caractère de chaque type)")
        self.cases = [self.case_minuscule, self.case_majuscule, self.case_nombre,
                      self.case_symbole, self.case_valide]
        for case in self.cases:
            case.setChecked(True)
        grille.addWidget(self.case_minuscule, 0, 0)
        grille.addWidget(self.case_majuscule, 0, 1)
        grille.addWidget(self.case_nombre, 1, 0)
        grille.addWidget(self.case_symbole, 1, 1)

        disposition.addLayout(grille)
        disposition.addWidget(self.case_valide)
        return disposition

    def creer_zone_boutons(self) -> QHBoxLayout:
        """Boutons Régénérer, Copier, Utiliser et Fermer."""
        disposition = QHBoxLayout()
        self.bouton_regenerer = QPushButton("Régénérer")
        self.bouton_copier = QPushButton("Copier")
        self.bouton_utiliser = QPushButton("Utiliser")
        self.bouton_fermer = QPushButton("Fermer")
        disposition.addWidget(self.bouton_regenerer)
        disposition.addWidget(self.bouton_copier)
        disposition.addStretch()
        disposition.addWidget(self.bouton_utiliser)
        disposition.addWidget(self.bouton_fermer)
        return disposition

    def connecter_signaux(self) -> None:
        """Relie les widgets à leurs méthodes (signaux et slots)."""
        self.curseur.valueChanged.connect(self.boite_longueur.setValue)
        self.boite_longueur.valueChanged.connect(self.curseur.setValue)

        self.boite_longueur.valueChanged.connect(self.generer)
        for case in self.cases:
            case.stateChanged.connect(self.generer)

        self.bouton_masquer.clicked.connect(self.basculer_affichage)
        self.bouton_regenerer.clicked.connect(self.generer)
        self.bouton_copier.clicked.connect(self.copier)
        self.bouton_utiliser.clicked.connect(self.utiliser)
        self.bouton_fermer.clicked.connect(self.close)

    def generer(self) -> None:
        """Génère un mot de passe avec les réglages actuels, ou affiche l'erreur si ceux-ci sont invalides.
        Sans mot de passe valide, les boutons Copier et Utiliser sont désactivés."""
        try:
            generateur = PasswordGenerator(
                self.boite_longueur.value(),
                self.case_minuscule.isChecked(),
                self.case_majuscule.isChecked(),
                self.case_nombre.isChecked(),
                self.case_symbole.isChecked(),
                self.case_valide.isChecked()
            )
            self.mot_de_passe = generateur.generer()
            self.afficher_message("")
        except ValueError as erreur:
            self.mot_de_passe = ""
            self.afficher_message(str(erreur), est_erreur=True)

        est_valide = self.mot_de_passe != ""
        self.bouton_copier.setEnabled(est_valide)
        self.bouton_utiliser.setEnabled(est_valide)
        self.rafraichir_affichage()

    def rafraichir_affichage(self) -> None:
        """Affiche le mot de passe en clair ou sous forme d'astérisques.
        La police est réduite pour les longs mots de passe, afin qu'ils tiennent dans la fenêtre."""
        if self.est_affiche:
            texte = self.mot_de_passe
        else:
            texte = "*" * len(self.mot_de_passe)

        if len(texte) <= 24:
            taille = 24
        elif len(texte) <= 40:
            taille = 16
        else:
            taille = 11
        self.etiquette_mdp.setStyleSheet(f"font-size: {taille}px; font-weight: bold; font-family: monospace;")
        self.etiquette_mdp.setText(texte)

    def basculer_affichage(self) -> None:
        """Alterne entre l'affichage en clair et les astérisques."""
        self.est_affiche = not self.est_affiche
        if self.est_affiche:
            self.bouton_masquer.setText("Masquer")
        else:
            self.bouton_masquer.setText("Afficher")
        self.rafraichir_affichage()

    def copier(self) -> None:
        """Copie le mot de passe (en clair) dans le presse-papiers."""
        QGuiApplication.clipboard().setText(self.mot_de_passe)
        self.afficher_message(MESSAGE_COPIE)
        QTimer.singleShot(2000, self.effacer_message_copie)

    def utiliser(self) -> None:
        """Transmet le mot de passe à la fenêtre appelante, puis ferme la fenêtre."""
        self.mot_de_passe_choisi.emit(self.mot_de_passe)
        self.close()

    def afficher_message(self, texte: str, est_erreur: bool = False) -> None:
        """Affiche un message en vert, ou en rouge s'il s'agit d'une erreur."""
        couleur = "#dc2626" if est_erreur else "#15803d"
        self.etiquette_message.setStyleSheet(f"color: {couleur};")
        self.etiquette_message.setText(texte)

    def effacer_message_copie(self) -> None:
        """Efface le message de copie, mais pas un éventuel message d'erreur."""
        if self.etiquette_message.text() == MESSAGE_COPIE:
            self.etiquette_message.setText("")


if __name__ == "__main__":
    application = QApplication(sys.argv)
    fenetre = FenetreGenerateur()
    fenetre.show()
    sys.exit(application.exec())