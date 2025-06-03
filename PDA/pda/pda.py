import sys
from pathlib import Path


# INCARCARE PDA
def load_pda(path: str):
    cfg = {k: [] for k in (
        "States", "InputSymbols", "StackSymbols",
        "Start", "StackStart", "Final", "Rules")}
    section = None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if "#" in line:
            line = line.split("#", 1)[0].rstrip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        cfg[section].append(line)

    Q   = set(cfg["States"])
    Σ   = set(cfg["InputSymbols"])
    Γ   = set(cfg["StackSymbols"])
    q0  = cfg["Start"][0]
    Z0  = cfg["StackStart"][0]
    F   = set(cfg["Final"])
    δ   = {q: [] for q in Q}              # listă de tranziţii

    for rule in cfg["Rules"]:
        src, insym, popsym, dst, push = rule.split()
        δ[src].append((insym, popsym, dst, push))
    return Q, Σ, Γ, q0, Z0, F, δ



# SIMULARE PDA (nedeterminista, DFS cu backtracking)
def accepts(word, *, start, z0, finals, δ, max_depth=10000):
    initial_cfg = (start, 0, [z0])        # (state, pos în cuvânt, stack list)
    stack = [initial_cfg]

    while stack:
        state, pos, stiva = stack.pop()
        if pos == len(word) and state in finals:
            return True                   # acceptare prin stare finală
        if len(stack) > max_depth:
            raise RecursionError("Căutare prea adâncă (posibil ciclu infinit)")

        # simbol curent (sau '$' dacă am ajuns la sfârşitul cuvântului)
        a = word[pos] if pos < len(word) else '$'
        top = stiva[-1] if stiva else '$'

        for insym, popsym, dst, push in δ[state]:
            # testăm potrivirea simbolului de intrare
            if insym != '$' and insym != a:
                continue
            # testăm potrivirea simbolului din vârful stivei
            if popsym != '$' and popsym != top:
                continue

            # pregătim noua configuraţie
            new_pos = pos + (0 if insym == '$' else 1)
            new_stack = stiva.copy()
            if popsym != '$':             # „pop” efectiv
                new_stack.pop()
            if push != '$':               # „push” (posibil mai multe simboluri)
                for c in reversed(push):
                    new_stack.append(c)

            stack.append((dst, new_pos, new_stack))
    return False



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizare: python pda.py <automat.pda>")
        sys.exit(1)

    Q, Σ, Γ, q0, Z0, F, δ = load_pda(sys.argv[1])

    print("Introduceţi cuvinte (Enter exit, quit, "" => stop):")
    while True:
        w = input("> ").strip()
        if w in {"quit", "exit", ""}:
            print("Ieșire...")
            break
        verdict = accepts(w, start=q0, z0=Z0, finals=F, δ=δ)
        print("ACCEPTAT" if verdict else "RESPINS")
