"""
masina turing
un array 
initial: gol
stare initiala: q0
(qi,a)->(qj,b,{left, right})
daca vreau sa umplu cu 1: (q0,0)->(q1,1,right) - o singura tranzitie
daca vrem 1, spatiu, 1
(q0,0)->(q1,1,right)
(q1," ")->(q0," ",right)
Adunam 2 numere(in unar)
111+1111->1111111
(q0,1)->(q0,1,right)
(q0,+)->(q0,1,right)
(q0," ")->(q1," ",left)
(q1,1)->(q_accept," ",right)
"""

"""
definit limbaj
alfabet, tranzitii, stare initiala, stare finala, emulator
"""



FPATH = __file__.rsplit("/", maxsplit=1)[0] + "/"

def load_automata(filename):
    """
    Încarcă automata din fișierul .lfa cu secțiunile:
      [States], [Symbols] și [Rules], separate prin linia '#'.
    Ignorează comentariile (linii care încep cu '#', dar nu sunt doar '#'),
    elimină comentariile inline (după un '#') și secțiunile goale.
    Returnează tuple (states, symbols, rules).
    """
    raw = open(FPATH + filename).read().splitlines()
    sections, current = [], []
    for ln in raw:
        ln = ln.rstrip("\n")
        if not ln.strip():
            continue
        if ln.strip() == "#":
            sections.append(current)
            current = []
            continue
        if ln.strip().startswith("#"):
            continue
        # eliminăm comentariile inline
        line = ln.split("#")[0].rstrip()
        current.append(line)
    if current:
        sections.append(current)

    states, symbols, rules = [], [], []
    for sec in sections:
        if not sec:
            continue
        header = sec[0].strip()
        content = [s.strip() for s in sec[1:] if s.strip()]
        if header == "[States]":
            states = content
        elif header == "[Symbols]":
            symbols = content
        elif header == "[Rules]":
            for rule in content:
                parts = rule.split()
                if len(parts) == 5:
                    st, sym, new_st, write_sym, move = parts
                    rules.append((st, sym, new_st, write_sym, move))
    return states, symbols, rules

def build_transitions(rules):
    """
    Construiește dicționarul:
      (stare_curentă, simbol_citit) -> (stare_nouă, simbol_scris, direcție)
    """
    return { (st, sym): (new_st, write_sym, move)
             for st, sym, new_st, write_sym, move in rules }

def step(tape, head, state, trans, blank):
    """
    Execută un pas de Turing:
      1. Citește simbolul la poziția `head`.
      2. Aplică regula `trans[(state, simbol)]`.
      3. Scrie simbolul nou și actualizează starea.
      4. Mută capul (R/L/N).
    Returnează (tape, head, new_state, ok).
    """
    key = (state, tape[head])
    if key not in trans:
        return tape, head, state, False
    new_state, write_sym, move = trans[key]
    tape[head] = write_sym
    if move == 'R':
        head += 1
        if head >= len(tape):
            tape.append(blank)
    elif move == 'L':
        head = max(0, head - 1)
    # N = no move
    return tape, head, new_state, True

def run_turing(inp, defs, trans, max_steps=10000):
    """
    Rulează mașina Turing pe șirul `inp` și returnează banda finală,
    inclusiv marcatorul '$'.
    defs = (states, symbols, rules), trans = dicționar de tranziții.
    """
    states, symbols, rules = defs
    blank = '_'   # simbolul blank
    tape = list(inp) + [blank] * 50
    head = 0
    state = states[0]  # q0

    for i in range(max_steps):
        if state == 'q_accept':
            break
        tape, head, state, ok = step(tape, head, state, trans, blank)
        if not ok:
            break

    return ''.join(tape)

def main():
    # 1. Încarcă definiția
    states, symbols, rules = load_automata('masina_turing.lfa')
    # 2. Construiește tranzițiile
    trans = build_transitions(rules)
    # 3. Citește input de la utilizator
    inp = input("Introduceți două șiruri unare separate prin '+', ex. 111+1111: ").strip()
    # 4. Rulează și afișează rezultatul
    result = run_turing(inp, (states, symbols, rules), trans)
    print("Rezultat:", result)

if __name__ == '__main__':
    main()