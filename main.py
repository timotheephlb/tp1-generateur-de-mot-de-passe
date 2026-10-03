import argparse

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

    print(utilise_minuscule, utilise_majuscule, utilise_nombre, utilise_symbole)


if __name__ == "__main__":
    main()