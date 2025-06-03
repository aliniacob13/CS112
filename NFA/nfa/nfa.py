"""
nfa.py  –  Simulator pentru NFA-uri cu λ-tranziții (ε)

FORMAT .nfa:

[States]     # fiecare stare pe linia ei
q0
q1
...

[Symbols]    # alfabetul propriu-zis (nu include ‘$’)
a
b
...

[Start]      # O singură stare
q0

[Final]      # Una sau mai multe stări acceptoare
q2
...

[Rules]      # Linii:  FROM  SYMBOL  TO
q0 a q0      # pot exista una sau mai multe tranziții pentru același (q, a)
q0 $ q1      # simbolul ‘$’ indică tranziție λ (epsilon)
q1 b q2
...
"""

import sys
from pathlib import Path


# Parsare fișier .nfa și încărcarea elementelor NFA-ului
def load_nfa(filepath: str):
    """
    Încarcă automata din fișierul indicat.
    Fișierul trebuie să conțină secțiunile: [States], [Symbols], [Start], [Final], [Rules],
    separate de comentariul '#' sau de linii goale.
    """
    # Inițializăm un dicționar gol pentru a păstra conținutul fiecărei secțiuni
    cfg = {k: [] for k in ("States", "Symbols", "Start", "Final", "Rules")}
    section = None  # Variabilă pentru a ști în ce secțiune ne aflăm

    # Deschidem fișierul .nfa și citim linie cu linie
    with open(filepath, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()

            # Eliminăm comentariile inline (orice după '#') și sărim liniile goale
            if "#" in line:
                line = line.split("#", 1)[0].rstrip()
            if not line:
                continue

            # Detectăm anteturile de secțiuni [States], [Symbols] etc.
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]  # Extragem numele secțiunii fără paranteze
                if section not in cfg:
                    # Dacă secțiunea nu e recunoscută, raportăm eroare
                    raise ValueError(f"Secțiune necunoscută: {section}")
                continue

            # Adăugăm linia la lista potrivită din cfg
            cfg[section].append(line)

    # După parsare, extragem elementele NFA-ului
    Q   = set(cfg["States"])       # Mulțimea stărilor
    Σ   = set(cfg["Symbols"])      # Alfabetul
    q0  = cfg["Start"][0]          # Starea inițială (primul element din [Start])
    F   = set(cfg["Final"])        # Mulțimea stărilor finale
    # Inițializăm funcția de tranziție δ cu un dicționar gol pentru fiecare stare
    δ   = {q: {} for q in Q}       

    # Parsăm fiecare regulă de tranziție din secțiunea [Rules]
    for rule in cfg["Rules"]:
        try:
            src, sym, dst = rule.split()
        except ValueError:
            # Dacă regula nu are exact 3 token-uri, e invalidă
            raise ValueError(f"Regulă invalidă: «{rule}»")

        # Verificăm că simbolul e fie '$' (epsilon) sau face parte din alfabet
        if sym != '$' and sym not in Σ:
            raise ValueError(f"Simbol «{sym}» lipsește din [Symbols]")

        # Pentru epsilon și pentru simboluri valide, adăugăm starea destinație
        # în mulțimea tranzițiilor pentru starea sursă și simbolul respectiv
        δ[src].setdefault(sym, set()).add(dst)

    return Q, Σ, q0, F, δ


# Operații auxiliare: λ-închidere și move fără λ
def epsilon_closure(states, δ):
    """
    Calculează λ-închiderea (epsilon-closure) a mulțimii de stări 'states'.
    Adică toate stările care pot fi atinse din oricare stare din 'states' urmând
    tranziții λ ('$') de orice lungime (inclusiv zero pași).
    """
    stack   = list(states)         # Vom face DFS/BFS pe tranziții ε
    closure = set(states)          # Începem cu stările date
    while stack:
        s = stack.pop()
        # Pentru fiecare tranziție ε din starea s
        for nxt in δ[s].get('$', set()):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure


def move(states, symbol, δ):
    """
    Returnează mulțimea stărilor atinse din 'states' urmând tranziții pe 'symbol',
    fără să aplicăm λ-închidere (adică doar pasul propriu-zis pe symbol).
    """
    nxt = set()
    for s in states:
        nxt.update(δ[s].get(symbol, set()))
    return nxt



# Funcție de acceptare a unui șir (word)
def accepts(word, *, start, finals, δ):
    """
    Returnează True dacă NFA-ul (start, δ, finals) acceptă șirul 'word'.
    Vom parcurge fiecare caracter, aplicând move apoi epsilon_closure la fiecare pas.
    Dacă la final există vreun element comun între stările curente și cele finale,
    șirul e ACCEPTAT; altfel e RESPINS.
    """
    # Începem cu ε-închiderea stării inițiale
    current = epsilon_closure({start}, δ)
    # Pentru fiecare caracter din cuvânt
    for ch in word:
        # Mai întâi mutăm pe ch, apoi aplicăm iar ε-închidere
        current = epsilon_closure(move(current, ch, δ), δ)
        # Dacă niciun traseu nu a supraviețuit (current devine vid), respingem
        if not current:
            return False
    # La final, dacă există vreo stare finală printre stările curente, acceptăm
    return not finals.isdisjoint(current)



# Rularea interactivă a simulării NFA
if __name__ == "__main__":
    # Verificăm argumentele din linia de comandă
    if len(sys.argv) != 2:
        print("Utilizare: python nfa.py <automat.nfa>")
        sys.exit(1)

    # Încărcăm NFA-ul din fișierul specificat
    Q, Σ, q0, F, δ = load_nfa(sys.argv[1])

    print("Introduceți cuvinte (quit, exit sau linie goală => oprire):")
    while True:
        w = input("> ").strip()
        # Dacă utilizatorul scrie „quit”/„exit” sau apasă Enter pe linie goală, întrerupem
        if w == "" or w.lower() in {"quit", "exit"}:
            break

        # Verificăm dacă NFA acceptă șirul w și afișăm rezultat
        verdict = accepts(w, start=q0, finals=F, δ=δ)
        print("ACCEPTAT" if verdict else "RESPINS")