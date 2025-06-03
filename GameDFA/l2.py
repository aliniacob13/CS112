FPATH = __file__.rsplit("/", maxsplit=1)[0] + "/"
def load_automata(filename):
    """
    Încarcă automata din fișierul indicat.
    Fișierul trebuie să conțină trei secțiuni: [States], [Symbols] și [Rules],
    fiecare separat de o linie cu un singur caracter '#'.
    """
    states = []
    symbols = []
    rules = []
    
    with open(FPATH + filename, "r") as f:
        content = f.read().strip()
    
    # Împarte conținutul fișierului în secțiuni după separatorul '#'
    sections = content.split("#")
    
    for section in sections:
        # Obține fiecare linie ne-gol, curățată de spații, din secțiune
        lines = [line.strip() for line in section.strip().split("\n") if line.strip()]
        if not lines:
            continue
        header = lines[0]
        if header == "[States]":
            states = lines[1:]  # Fiecare linie după antet este o stare
        elif header == "[Symbols]":
            symbols = lines[1:]
        elif header == "[Rules]":
            for line in lines[1:]:
                # Presupune că fiecare regulă are formatul: stare_curentă simbol stare_următoare
                parts = line.split()
                if len(parts) == 3:
                    rules.append((parts[0], parts[1], parts[2]))
    
    print("States:", states)
    print("Symbols:", symbols)
    print("Rules:", rules)
    return states, symbols, rules


def build_transitions(rules):
    """
    Construiește un dicționar care mapează (stare_curentă, simbol) -> stare_următoare.
    """
    transitions = {}
    for current_state, symbol, next_state in rules:
        transitions[(current_state, symbol)] = next_state
    return transitions


def main():
    filename = "joc.lfa"
    states, symbols, rules = load_automata(filename)
    transitions = build_transitions(rules)
    
    # Începe jocul din starea "entrance".
    current_state = "entrance"
    print("\nBine ai venit la jocul bazat pe automată!")
    print("Folosește direcțiile (up, down, left, right) pentru a te mișca prin camere.\n")
    
    while True:
        print(f"You are in: {current_state}")
        # Încheie jocul dacă jucătorul ajunge la "exit".
        if current_state == "exit":
            print("Felicitări, ai ajuns la ieșire!")
            break
        
        # Determină mișcările disponibile din camera curentă.
        available_moves = [move for (state, move) in transitions if state == current_state]
        if available_moves:
            print("Poți să mergi:", ", ".join(available_moves))
        else:
            print("Nu există mișcări disponibile de aici. Joc terminat.")
            break
        
        move = input("Introdu mișcarea: ").strip()
        
        # Verifică dacă mișcarea se află printre simbolurile permise.
        if move not in symbols:
            print("Direcție invalidă. Te rugăm să folosești una dintre:", ", ".join(symbols))
            continue
        
        # Verifică dacă există o tranziție validă.
        key = (current_state, move)
        if key in transitions:
            current_state = transitions[key]
        else:
            print("Nu poți merge pe acolo.")


def run_game():
    filename = "joc_greu.lfa"
    states, symbols, rules = load_automata(filename)
    transitions = build_transitions(rules)
    
    # Jocul începe în camera "entrance".
    current_state = "entrance"
    inventory = set()  # Pentru a ține evidența obiectelor (de ex. lingura)
    
    print("\nBine ai venit la versiunea actualizată a jocului bazat pe automată!")
    print("Comenzi disponibile: up, down, left, right.")
    print("În bucătărie, poți tasta și 'pick' pentru a lua lingura.\n")
    
    while True:
        print(f"\nYou are in: {current_state}")
        
        # Verifică condițiile de câștig.
        if current_state == "exit":
            print("Ai ajuns la ieșire. Ai câștigat!")
            break
        if current_state == "mega_exit":
            print("Ai intrat în mega_exit. Felicitări!")
            break
        
        # Listează mișcările disponibile conform regulilor automatelor.
        available_moves = [move for (state, move) in transitions if state == current_state]
        
        if current_state == "kitchen" and "spoon" not in inventory:
            available_moves.append("pick")
        
        print("Poți:", ", ".join(available_moves))
        command = input("Introdu comanda: ").strip().lower()
        
        if command == "pick":
            if current_state == "kitchen":
                if "spoon" in inventory:
                    print("Ai luat deja lingura.")
                else:
                    inventory.add("spoon")
                    print("Ai luat lingura!")
            else:
                print("Nu este nimic de luat aici.")
            continue
        
        # Validare comandă
        if command not in available_moves:
            print("Comandă invalidă. Încearcă din nou.")
            continue
        
        key = (current_state, command)
        if key in transitions:
            next_state = transitions[key]
            if next_state == "mega_exit" and "spoon" not in inventory:
                print("Ai nevoie de lingură pentru a intra în mega_exit!")
                continue
            current_state = next_state
        else:
            print("Nu poți merge pe acolo.")


if __name__ == "__main__":
    run_game()
