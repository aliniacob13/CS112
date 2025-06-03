import sys
from pathlib import Path

# ------------------------------------------------------------
# Funcție: load_dfa
#
# Citește descrierea unui DFA dintr-un fișier și returnează componentele sale:
#   - Q: lista stărilor
#   - Σ: lista simbolurilor (alfabetul)
#   - q0: starea de start
#   - F: mulțimea stărilor finale (acceptatoare)
#   - δ: funcția de tranziție, ca dicționar ce mapează (stare, simbol) -> stare următoare
#
# Formatul fișierului așteptat utilizează secțiuni între paranteze pătrate, de exemplu:
#   [States]
#   q0
#   q1
#   ...
#   [Symbols]
#   0
#   1
#   ...
#   [Start]
#   q0
#   [Final]
#   q1
#   [Rules]
#   q0 0 q1
#   q0 1 q0
#   ...
#
# Comentariile din fișier încep cu “#” și sunt ignorate. Liniile goale sunt sărite.
#
def load_dfa(filepath: str):
    # Inițializează un dicționar pentru a reține liniile fiecărei secțiuni
    cfg = {
        "States": [],    # Lista tuturor stărilor (Q)
        "Symbols": [],   # Lista simbolurilor de intrare (Σ)
        "Start": [],     # Exact o stare de start
        "Final": [],     # Zero sau mai multe stări finale (F)
        "Rules": []      # Lista regulilor de tranziție (neparse)
    }

    section = None  # Ține evidența secțiunii curente în timpul parsării

    # Deschide fișierul DFA și citește linie cu linie
    with open(filepath, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()

            # Elimină comentariile inline care încep cu “#”
            if "#" in line:
                line = line.split("#", 1)[0].rstrip()

            # Sare peste liniile goale sau cele care erau doar comentarii
            if not line or line.startswith("#"):
                continue

            # Detectează un antet de secțiune, de forma “[States]”
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]  # Extrage textul fără paranteze
                if section not in cfg:
                    # Dacă numele secțiunii nu este recunoscut, aruncă eroare
                    raise ValueError(f"Secțiune necunoscută: {section}")
                continue

            # Dacă suntem într-o secțiune permisă, adaugă linia la lista ei
            cfg[section].append(line)

    # După citirea fișierului, extrage componentele DFA-ului
    Q   = cfg["States"]                # Toate stările
    Σ   = cfg["Symbols"]               # Simbolurile alfabetului
    # Dacă nu s-a specificat nicio stare de start, se folosește prima stare din Q
    q0  = cfg["Start"][0] if cfg["Start"] else Q[0]
    # Transformă stările finale într-un set pentru verificări rapide; implicit, set vid
    F   = set(cfg["Final"] if cfg["Final"] else [])

    # Construiește dicționarul de tranziții δ
    δ   = {}  # Cheile vor fi tupluri (stare, simbol), iar valorile vor fi starea următoare

    # Parcurge fiecare linie din secțiunea [Rules], format “src sym dst”
    for rule in cfg["Rules"]:
        try:
            src, sym, dst = rule.split()
        except ValueError:
            # Dacă împărțirea nu produce exact trei părți, regula este invalidă
            raise ValueError(f"Regulă invalidă: »{rule}«")

        # Verifică dacă simbolul apare în alfabetul Σ
        if sym not in Σ:
            raise ValueError(f"Simbol «{sym}» nu e listat în [Symbols]")

        key = (src, sym)

        # Asigură determinismul: nu poate exista mai multe tranziții pentru același (src, sym)
        if key in δ:
            raise ValueError(f"DFA trebuie să fie determinist – dublă tranziție pentru {key}")

        δ[key] = dst

    # Verifică completitudinea DFA-ului: pentru orice stare și orice simbol trebuie să existe o tranziție
    for q in Q:
        for sym in Σ:
            if (q, sym) not in δ:
                raise ValueError(f"Lipsește tranziția ({q}, {sym}) în [Rules]")

    # Returnează componentele DFA-ului (lista stărilor, alfabet, stare de start, stări finale, funcția δ)
    return Q, Σ, q0, F, δ


# ------------------------------------------------------------
# Funcție: accepts
#
# Dat fiind un șir (word) și componentele unui DFA, decide dacă
# DFA-ul acceptă șirul. Întoarce True dacă este acceptat, False altfel.
#
def accepts(word: str, *, start: str, finals: set, delta: dict):
    state = start  # Începe în starea de start

    # Procesează fiecare caracter din cuvânt, pe rând
    for ch in word:
        key = (state, ch)
        if key not in delta:
            # Dacă nu există tranziție pentru (state, ch), cuvântul este respins
            return False
        # Treci în starea următoare conform funcției δ
        state = delta[key]

    # După procesarea tuturor simbolurilor, acceptă dacă starea curentă e finală
    return state in finals


# ------------------------------------------------------------
# Punctul de intrare principal: când scriptul este rulat direct
#
if __name__ == "__main__":
    # Verifică argumentele din linia de comandă: se așteaptă exact un argument (fișierul .dfa)
    if len(sys.argv) != 2:
        print("Utilizare: python dfa.py <automat.dfa>")
        sys.exit(1)

    # Încarcă definiția DFA din fișierul specificat
    Q, Σ, q0, F, δ = load_dfa(sys.argv[1])

    print("Introduceți cuvinte (Enter „”, stop, exit => ieșire):")
    while True:
        w = input("> ").strip()

        # Dacă utilizatorul introduce un șir gol sau „stop”/„exit” (indiferent de majuscule), se oprește
        if w == "" or w.lower() in {"stop", "exit"}:
            break

        # Verifică acceptarea cuvântului w și afișează rezultatul
        verdict = accepts(w, start=q0, finals=F, delta=δ)
        print("ACCEPTAT" if verdict else "RESPINS")