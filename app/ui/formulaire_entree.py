# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
)

from app.core.storage import Entree
from app.ui.generator_ui import FenetreGenerateur


class FormulaireEntree(QWidget):
    """Formulaire d'ajout ou de modification d'une entrée.
    Le signal entree_validee transmet l'e-mail et le mot de passe saisis."""

    entree_validee = Signal(str, str)

    def __init__(self, emails_pris: list[str], entree: Entree = None) -> None:
        super().__init__()
        self.emails_pris = [email.lower() for email in emails_pris]
        self.setWindowTitle("Modifier l'entrée" if entree else "Nouvelle entrée")
        self.initialiser_ui(entree)

    def initialiser_ui(self, entree: Entree) -> None:
        disposition = QFormLayout()

        self.champ_email = QLineEdit(entree.email if entree else "")
        self.champ_mot_de_passe = QLineEdit(entree.mot_de_passe if entree else "")

        bouton_generer = QPushButton("Générer")
        bouton_generer.clicked.connect(self.generer)
        ligne_mot_de_passe = QHBoxLayout()
        ligne_mot_de_passe.addWidget(self.champ_mot_de_passe)
        ligne_mot_de_passe.addWidget(bouton_generer)

        bouton_enregistrer = QPushButton("Enregistrer")
        bouton_annuler = QPushButton("Annuler")
        bouton_enregistrer.clicked.connect(self.valider)
        bouton_annuler.clicked.connect(self.close)
        ligne_boutons = QHBoxLayout()
        ligne_boutons.addStretch()
        ligne_boutons.addWidget(bouton_enregistrer)
        ligne_boutons.addWidget(bouton_annuler)

        disposition.addRow("E-mail :", self.champ_email)
        disposition.addRow("Mot de passe :", ligne_mot_de_passe)
        disposition.addRow(ligne_boutons)
        self.setLayout(disposition)

    def generer(self) -> None:
        """Ouvre la fenêtre de génération ; le mot de passe choisi remplit le champ."""
        self.generateur = FenetreGenerateur()
        self.generateur.mot_de_passe_choisi.connect(self.champ_mot_de_passe.setText)
        self.generateur.show()

    def valider(self) -> None:
        """Vérifie la saisie ; en cas d'erreur, le formulaire reste ouvert."""
        email = self.champ_email.text().strip()
        mot_de_passe = self.champ_mot_de_passe.text()

        if "@" not in email:
            QMessageBox.critical(self, "Erreur", "L'e-mail doit contenir un « @ ».")
        elif email.lower() in self.emails_pris:
            QMessageBox.critical(self, "Erreur", "Cet e-mail existe déjà dans le coffre-fort.")
        elif not mot_de_passe:
            QMessageBox.critical(self, "Erreur", "Le mot de passe ne doit pas être vide.")
        else:
            self.entree_validee.emit(email, mot_de_passe)
            self.close()