# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QScrollArea, QListWidget, QListWidgetItem, QMessageBox, QMenu
)

from app.core.storage import Entree, Storage
from app.ui.formulaire_entree import FormulaireEntree


class FenetrePrincipale(QMainWindow):
    """Fenêtre principale du coffre-fort."""

    def __init__(self, chemin_coffre: str = "vault.json") -> None:
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.resize(700, 500)

        self.storage = Storage(chemin_coffre)
        self.entrees = []
        self.coffre_valide = True

        self.initialiser_ui()
        self.charger_coffre()

    def initialiser_ui(self) -> None:
        """Assemble la fenêtre : barre de boutons en haut, liste défilante en dessous."""
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        self.liste = QListWidget()
        self.liste.itemDoubleClicked.connect(self.basculer)
        self.liste.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.liste.customContextMenuRequested.connect(self.afficher_menu)

        zone = QScrollArea()
        zone.setWidget(self.liste)
        zone.setWidgetResizable(True)

        disposition = QVBoxLayout(widget_central)
        disposition.addLayout(self.creer_barre_boutons())
        disposition.addWidget(zone)

    def creer_barre_boutons(self) -> QHBoxLayout:
        """Boutons de gestion à gauche, choix du tri à droite."""
        disposition = QHBoxLayout()

        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_ajouter.setObjectName("primaire")
        self.bouton_modifier = QPushButton("Modifier")
        self.bouton_supprimer = QPushButton("Supprimer")
        self.bouton_supprimer.setObjectName("danger")
        self.liste_tri = QComboBox()
        self.liste_tri.addItems(["Trier : E-mail (A → Z)", "Trier : E-mail (Z → A)"])

        self.bouton_ajouter.clicked.connect(self.ajouter)
        self.bouton_modifier.clicked.connect(self.modifier)
        self.bouton_supprimer.clicked.connect(self.supprimer)
        self.liste_tri.currentIndexChanged.connect(self.afficher_liste)

        disposition.addWidget(self.bouton_ajouter)
        disposition.addWidget(self.bouton_modifier)
        disposition.addWidget(self.bouton_supprimer)
        disposition.addStretch()
        disposition.addWidget(self.liste_tri)
        return disposition

    def charger_coffre(self) -> None:
        """Lit vault.json. S'il est illisible, avertit l'utilisateur et affiche un coffre vide."""
        try:
            self.entrees = self.storage.charger()
        except (ValueError, KeyError, TypeError, OSError):
            self.coffre_valide = False
            QMessageBox.critical(self, "Erreur lors du chargement", "Le fichier du coffre-fort est illisible.")
        self.afficher_liste()

    def texte(self, entree: Entree, revele: bool) -> str:
        """Texte d'une ligne : l'e-mail et le mot de passe (masqué ou non)."""
        return f"{entree.email}      {entree.mot_de_passe if revele else '*******'}"

    def afficher_liste(self) -> None:
        """Reconstruit la liste, triée par e-mail."""
        self.liste.clear()
        inverse = self.liste_tri.currentIndex() == 1
        for entree in sorted(self.entrees, key=lambda e: e.email.lower(), reverse=inverse):
            item = QListWidgetItem(self.texte(entree, False))
            item.setData(Qt.ItemDataRole.UserRole, entree)
            self.liste.addItem(item)
        self.statusBar().showMessage(f"{len(self.entrees)} entrée(s)")

    def basculer(self, item: QListWidgetItem) -> None:
        """Double-clic : révèle ou masque le mot de passe de la ligne."""
        entree = item.data(Qt.ItemDataRole.UserRole)
        est_masque = item.text() == self.texte(entree, False)
        item.setText(self.texte(entree, est_masque))

    def afficher_menu(self, position) -> None:
        """Clic droit sur une ligne : menu avec Révéler / Masquer, Modifier et Supprimer."""
        item = self.liste.itemAt(position)
        if item is None:
            return
        self.liste.setCurrentItem(item)

        action_basculer = QAction("Révéler / Masquer", self)
        action_modifier = QAction("Modifier", self)
        action_supprimer = QAction("Supprimer", self)
        action_basculer.triggered.connect(lambda: self.basculer(item))
        action_modifier.triggered.connect(self.modifier)
        action_supprimer.triggered.connect(self.supprimer)

        menu = QMenu(self)
        menu.addAction(action_basculer)
        menu.addAction(action_modifier)
        menu.addAction(action_supprimer)
        menu.exec(self.liste.viewport().mapToGlobal(position))

    def ajouter(self) -> None:
        """Ouvre le formulaire d'ajout."""
        self.formulaire = FormulaireEntree([entree.email for entree in self.entrees])
        self.formulaire.entree_validee.connect(self.ajouter_entree)
        self.formulaire.show()

    def ajouter_entree(self, email: str, mot_de_passe: str) -> None:
        self.entrees.append(Entree(email, mot_de_passe))
        self.afficher_liste()

    def modifier(self) -> None:
        """Ouvre le formulaire de modification pour l'entrée sélectionnée."""
        ligne = self.liste.currentRow()
        if ligne == -1:
            QMessageBox.information(self, "Modifier", "Sélectionnez d'abord une entrée.")
            return
        self.entree_modifiee = self.liste.item(ligne).data(Qt.ItemDataRole.UserRole)
        autres_emails = [entree.email for entree in self.entrees if entree is not self.entree_modifiee]
        self.formulaire = FormulaireEntree(autres_emails, self.entree_modifiee)
        self.formulaire.entree_validee.connect(self.modifier_entree)
        self.formulaire.show()

    def modifier_entree(self, email: str, mot_de_passe: str) -> None:
        self.entree_modifiee.email = email
        self.entree_modifiee.mot_de_passe = mot_de_passe
        self.afficher_liste()

    def supprimer(self) -> None:
        """Supprime l'entrée sélectionnée, après confirmation."""
        ligne = self.liste.currentRow()
        if ligne == -1:
            QMessageBox.information(self, "Supprimer", "Sélectionnez d'abord une entrée.")
            return
        reponse = QMessageBox.question(self, "Supprimer", "Voulez-vous vraiment supprimer cette entrée ?")
        if reponse == QMessageBox.StandardButton.Yes:
            self.entrees.remove(self.liste.item(ligne).data(Qt.ItemDataRole.UserRole))
            self.afficher_liste()

    def closeEvent(self, event) -> None:
        """Enregistre le coffre-fort à la fermeture, sauf si le fichier chargé était illisible."""
        if self.coffre_valide:
            try:
                self.storage.sauvegarder(self.entrees)
            except OSError:
                reponse = QMessageBox.question(
                    self, "Erreur", "Impossible d'enregistrer le coffre-fort. Quitter quand même ?"
                )
                if reponse == QMessageBox.StandardButton.No:
                    event.ignore()
                    return
        event.accept()
        QApplication.quit()
