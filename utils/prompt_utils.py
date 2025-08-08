def prompt_continue():
    while True:
        choice = input("\nWhat would you like to do next?\n[1] Return to main menu\n[2] Exit\n> ").strip()
        if choice == '1':
            return True
        elif choice == '2':
            print("Exiting.")
            return False
        else:
            print("Invalid input. Please enter 1 or 2.")
