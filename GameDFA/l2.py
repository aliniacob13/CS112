FPATH = __file__.rsplit("/", maxsplit=1)[0] + "/"
def load_automata(filename):
    """
    Loads the automata from the given file.
    The file must contain three sections: [States], [Symbols] and [Rules],
    each separated by a line with a single '#' character.
    """
    states = []
    symbols = []
    rules = []
    
    with open(FPATH + filename, "r") as f:
        content = f.read().strip()
    
    # Split the file into sections by the '#' separator
    sections = content.split("#")
    
    for section in sections:
        # Get each non-empty, stripped line in the section
        lines = [line.strip() for line in section.strip().split("\n") if line.strip()]
        if not lines:
            continue
        header = lines[0]
        if header == "[States]":
            states = lines[1:]  # Every line after the header is a state
        elif header == "[Symbols]":
            symbols = lines[1:]
        elif header == "[Rules]":
            for line in lines[1:]:
                # Assume each rule is formatted as: current_state move next_state
                parts = line.split()
                if len(parts) == 3:
                    rules.append((parts[0], parts[1], parts[2]))
    
    print("States:", states)
    print("Symbols:", symbols)
    print("Rules:", rules)
    return states, symbols, rules


def build_transitions(rules):
    """
    Constructs a dictionary mapping (current_state, symbol) -> next_state.
    """
    transitions = {}
    for current_state, symbol, next_state in rules:
        transitions[(current_state, symbol)] = next_state
    return transitions


def main():
    filename = "joc.lfa"
    states, symbols, rules = load_automata(filename)
    transitions = build_transitions(rules)
    
    # Start at the entrance.
    current_state = "entrance"
    print("\nWelcome to the automata-based room game!")
    print("Use the directions (up, down, left, right) to move through the rooms.\n")
    
    while True:
        print(f"You are in: {current_state}")
        # End the game if the player reaches the exit.
        if current_state == "exit":
            print("Congratulations, you've reached the exit!")
            break
        
        # Determine available moves from the current room.
        available_moves = [move for (state, move) in transitions if state == current_state]
        if available_moves:
            print("You can move:", ", ".join(available_moves))
        else:
            print("No moves available from here. Game over.")
            break
        
        move = input("Enter your move: ").strip()
        
        # Check if the move is among the allowed symbols.
        if move not in symbols:
            print("Invalid direction. Please use one of:", ", ".join(symbols))
            continue
        
        # Check if there is a valid transition.
        key = (current_state, move)
        if key in transitions:
            current_state = transitions[key]
        else:
            print("You can't go that way.")

def run_game():
    filename = "joc_greu.lfa"
    states, symbols, rules = load_automata(filename)
    transitions = build_transitions(rules)
    
    # The game starts at the entrance.
    current_state = "entrance"
    inventory = set()  # To keep track of items (like the spoon)
    
    print("\nWelcome to the updated automata-based room game!")
    print("Available commands: up, down, left, right.")
    print("In the kitchen, you can also type 'pick' to pick up the spoon.\n")
    
    while True:
        print(f"\nYou are in: {current_state}")
        
        # Check win conditions.
        if current_state == "exit":
            print("You have reached the exit. You win!")
            break
        if current_state == "mega_exit":
            print("You have entered the mega exit. Congratulations!")
            break
        
        # List available moves according to the automata rules.
        available_moves = [move for (state, move) in transitions if state == current_state]
        
        if current_state == "kitchen" and "spoon" not in inventory:
            available_moves.append("pick")
        
        print("You can move:", ", ".join(available_moves))
        command = input("Enter your command: ").strip().lower()
        
        if command == "pick":
            if current_state == "kitchen":
                if "spoon" in inventory:
                    print("You already picked up the spoon.")
                else:
                    inventory.add("spoon")
                    print("You picked up the spoon!")
            else:
                print("There's nothing to pick up here.")
            continue
        
        # Validate 
        if command not in available_moves:
            print("Invalid command. Try again.")
            continue
        
        key = (current_state, command)
        if key in transitions:
            next_state = transitions[key]
            if next_state == "mega_exit" and "spoon" not in inventory:
                print("You need the spoon to enter the mega exit!")
                continue
            current_state = next_state
        else:
            print("You can't go that way.")

if __name__ == "__main__":
    run_game()
