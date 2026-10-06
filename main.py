# Nom: PHILIBERT
# Prénom: Timothée
# Numéro d'étudiant: 2507084
# GitHub: timotheephlb
import argparse
from app.core.generator import PasswordGenerator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=16)
    parser.add_argument("--no-lower", action="store_true")
    parser.add_argument("--no-upper", action="store_true")
    parser.add_argument("--no-digits", action="store_true")
    parser.add_argument("--no-symbols", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

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


if __name__ == "__main__":
    main()