# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb

import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QScrollArea
)

from app.core.storage import Storage


class FenetrePrincipale(QMainWindow):
    """Fenêtre principale du coffre-fort."""

    def __init__(self, chemin_coffre: str = "vault.json") -> None:
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.resize(700, 500)

        self.storage = Storage(chemin_coffre)
        self.entrees = []

        self.initialiser_ui()

    def initialiser_ui(self) -> None:
        """Assemble la fenêtre : barre de boutons en haut, liste défilante en dessous."""
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        disposition = QVBoxLayout(widget_central)
        disposition.addLayout(self.creer_barre_boutons())
        disposition.addWidget(self.creer_zone_liste())

        self.statusBar().showMessage("0 entrée")

    def creer_barre_boutons(self) -> QHBoxLayout:
        """Boutons de gestion à gauche, choix du tri à droite."""
        disposition = QHBoxLayout()

        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_modifier = QPushButton("Modifier")
        self.bouton_supprimer = QPushButton("Supprimer")
        self.liste_tri = QComboBox()
        self.liste_tri.addItems(["Trier : E-mail (A → Z)", "Trier : E-mail (Z → A)"])

        disposition.addWidget(self.bouton_ajouter)
        disposition.addWidget(self.bouton_modifier)
        disposition.addWidget(self.bouton_supprimer)
        disposition.addStretch()
        disposition.addWidget(self.liste_tri)
        return disposition

    def creer_zone_liste(self) -> QScrollArea:
        """Zone défilante qui contiendra une ligne par entrée."""
        self.conteneur_lignes = QWidget()
        self.disposition_lignes = QVBoxLayout(self.conteneur_lignes)
        self.disposition_lignes.addStretch()

        zone = QScrollArea()
        zone.setWidget(self.conteneur_lignes)
        zone.setWidgetResizable(True)
        return zone


if __name__ == "__main__":
    application = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(application.exec())