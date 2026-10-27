# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QSlider, QSpinBox,
    QCheckBox, QVBoxLayout, QHBoxLayout
)

from app.core.generator import PasswordGenerator


class FenetreGenerateur(QWidget):
    """Fenêtre de génération de mot de passe.
    Le signal mot_de_passe_choisi transmet le mot de passe à la fenêtre appelante."""

    mot_de_passe_choisi = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générer un mot de passe")
        self.mot_de_passe = ""
        self.initialiser_ui()
        self.generer()

    def initialiser_ui(self):
        disposition = QVBoxLayout()

        ligne_mot_de_passe = QHBoxLayout()
        self.etiquette = QLabel()
        self.etiquette.setObjectName("mot_de_passe")
        self.etiquette.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.bouton_masquer = QPushButton("Masquer")
        self.bouton_masquer.setCheckable(True)
        ligne_mot_de_passe.addWidget(self.etiquette, 1)
        ligne_mot_de_passe.addWidget(self.bouton_masquer)

        ligne_longueur = QHBoxLayout()
        self.curseur = QSlider(Qt.Orientation.Horizontal)
        self.boite = QSpinBox()
        for widget in (self.curseur, self.boite):
            widget.setRange(4, 64)
            widget.setValue(16)
        ligne_longueur.addWidget(QLabel("Longueur"))
        ligne_longueur.addWidget(self.curseur, 1)
        ligne_longueur.addWidget(self.boite)

        ligne_cases = QHBoxLayout()
        self.cases = [QCheckBox(texte) for texte in
                      ("Minuscules", "Majuscules", "Chiffres", "Symboles", "Valider")]
        self.cases[4].setToolTip("Au moins un caractère de chaque type choisi")
        for case in self.cases:
            case.setChecked(True)
            ligne_cases.addWidget(case)

        ligne_boutons = QHBoxLayout()
        bouton_regenerer = QPushButton("Régénérer")
        self.bouton_copier = QPushButton("Copier")
        self.bouton_utiliser = QPushButton("Utiliser")
        self.bouton_utiliser.setObjectName("primaire")
        ligne_boutons.addWidget(bouton_regenerer)
        ligne_boutons.addWidget(self.bouton_copier)
        ligne_boutons.addStretch()
        ligne_boutons.addWidget(self.bouton_utiliser)

        disposition.addLayout(ligne_mot_de_passe)
        disposition.addLayout(ligne_longueur)
        disposition.addLayout(ligne_cases)
        disposition.addLayout(ligne_boutons)
        self.setLayout(disposition)

        self.curseur.valueChanged.connect(self.boite.setValue)
        self.boite.valueChanged.connect(self.curseur.setValue)
        self.boite.valueChanged.connect(self.generer)
        for case in self.cases:
            case.stateChanged.connect(self.generer)
        self.bouton_masquer.clicked.connect(self.afficher)
        bouton_regenerer.clicked.connect(self.generer)
        self.bouton_copier.clicked.connect(self.copier)
        self.bouton_utiliser.clicked.connect(self.utiliser)

    def generer(self):
        """Génère un mot de passe avec les réglages actuels.
        L'ordre des cases est celui des paramètres de PasswordGenerator (Partie 1)."""
        try:
            generateur = PasswordGenerator(self.boite.value(), *[case.isChecked() for case in self.cases])
            self.mot_de_passe = generateur.generer()
        except ValueError:
            self.mot_de_passe = ""
        self.bouton_copier.setText("Copier")
        self.bouton_copier.setEnabled(self.mot_de_passe != "")
        self.bouton_utiliser.setEnabled(self.mot_de_passe != "")
        self.afficher()

    def afficher(self):
        """Affiche le mot de passe en clair ou sous forme d'astérisques selon le bouton Masquer."""
        masque = self.bouton_masquer.isChecked()
        self.bouton_masquer.setText("Afficher" if masque else "Masquer")
        if not self.mot_de_passe:
            self.etiquette.setText("Choisissez au moins un type de caractère")
        elif masque:
            self.etiquette.setText("*" * len(self.mot_de_passe))
        else:
            self.etiquette.setText(self.mot_de_passe)

    def copier(self):
        """Copie le mot de passe (en clair) dans le presse-papiers."""
        QApplication.clipboard().setText(self.mot_de_passe)
        self.bouton_copier.setText("Copié !")

    def utiliser(self):
        """Transmet le mot de passe à la fenêtre appelante, puis ferme la fenêtre."""
        self.mot_de_passe_choisi.emit(self.mot_de_passe)
        self.close()
