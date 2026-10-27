# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb
import argparse
import sys

from PySide6.QtWidgets import QApplication

from app.core.generator import PasswordGenerator
from app.ui.main_window import FenetrePrincipale
from app.ui.style import STYLE


def lancer_cli(args) -> None:
    """Mode ligne de commande : affiche un mot de passe généré."""
    utilise_minuscule = not args.no_lower
    utilise_majuscule = not args.no_upper
    utilise_nombre = not args.no_digits
    utilise_symbole = not args.no_symbols

    try:
        gen = PasswordGenerator(args.length, utilise_minuscule, utilise_majuscule,
                                utilise_nombre, utilise_symbole, args.validate)
        print(gen.generer())
    except ValueError as e:
        print(f"Erreur : {e}")
        raise SystemExit(1)


def lancer_gui(chemin_coffre: str) -> None:
    """Mode graphique : ouvre le coffre-fort."""
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    window = FenetrePrincipale(chemin_coffre)
    window.show()
    sys.exit(app.exec())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-gui", action="store_true")
    parser.add_argument("--vault_file", default="vault.json")
    parser.add_argument("--length", type=int, default=16)
    parser.add_argument("--no-lower", action="store_true")
    parser.add_argument("--no-upper", action="store_true")
    parser.add_argument("--no-digits", action="store_true")
    parser.add_argument("--no-symbols", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

    if args.no_gui:
        lancer_cli(args)
    else:
        lancer_gui(args.vault_file)


if __name__ == "__main__":
    main()
