from src.vaca import vaca_diz

def main() -> None:
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <phrase>")
        sys.exit(1)

    frase = sys.argv[1]
    vaca_diz(frase)

if __name__ == "__main__":
    main()
