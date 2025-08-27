from art import text2art

def main():
    print("=== Superhero Banner Generator ===")
    print("Type a hero name (e.g. batman, spiderman, ironman, superman)")
    print("Type 'exit' to quit.\n")

    while True:
        hero = input("Enter hero name: ").strip().lower()
        if hero in ("exit", "quit"):
            print("Goodbye!")
            break

        if hero in ["batman", "spiderman", "ironman", "superman", "hulk", "thor", "captainamerica", "wonderwoman"]:
            banner = text2art(hero, font="block")  # big ASCII text
            print(banner)
        else:
            print("Hero not found! Try another.")

if __name__ == "__main__":
    main()
