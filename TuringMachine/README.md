# Turing Machines (TM)  
## Table of Contents

1. [Introduction to Turing Machines](#introduction-to-turing-machines)  
2. [Why Unbounded Memory?](#why-unbounded-memory)  
3. [Deterministic vs. Nondeterministic TM](#deterministic-vs-nondeterministic-tm)  
4. [Formal Definition of a TM](#formal-definition-of-a-tm)  
5. [How a TM Operates](#how-a-tm-operates)  
6. [Designing a TM](#designing-a-tm)  
7. [Example: Deciding the Language `{0ⁿ1ⁿ}`](#example-deciding-the-language-0ⁿ1ⁿ)  
8. [Additional Remarks and Tips](#additional-remarks-and-tips)
9. [My python code](#my python code)
---

## Introduction to Turing Machines

In 1936, Alan Turing introduced a mathematical model of a computing device that captures the notion of algorithmic computation. A **Turing Machine** is essentially a finite‐state control coupled with an infinite one-dimensional tape that serves as unbounded read‐write memory. With this machine, one can model any computation that a modern computer can perform (ignoring resource constraints), and thus TMs are central to the theory of computability.

- A TM surpasses finite automata (DFA/NFA) and pushdown automata (PDA) because its tape can store arbitrarily many symbols.  
- TMs recognize **recursively enumerable languages**; deterministic TMs (DTMs) decide exactly the class of **decidable/recursive languages**.  
- In practice, TMs are used as a theoretical yardstick: if a problem is solvable by some Turing Machine, we consider it “computable.”

---

## Why Unbounded Memory?

1. **Beyond Finite Control and Stack**  
   - A DFA can remember only its current state (finitely many possibilities).  
   - A PDA adds a stack, which provides unbounded memory but only in a LIFO (last-in, first-out) manner, so PDAs recognize exactly the class of context‐free languages.  
   - Certain languages (e.g., `{0ⁿ1ⁿ2ⁿ | n ≥ 0}`) are not context‐free and cannot be decided by any PDA. A TM, with its unrestricted tape head movement and read‐write capabilities, can handle such languages.

2. **Arbitrary Read/Write**  
   - The tape of a TM allows reading, writing, and moving left or right arbitrarily, so the machine can implement counters, multiple stacks, or any other finite‐control plus unbounded storage strategy.  
   - This unbounded, random‐access‐via‐head‐moves (left/right steps) memory model makes TMs the canonical model for “any algorithm.”  

3. **Nested or Cross‐Serial Dependencies**  
   - Some recognition tasks require matching symbols in complex ways (e.g., palindromes, equal numbers of multiple different symbols).  
   - The TM tape can serve as scratch space to mark, cross off, copy, and compare arbitrarily, enabling recognition of recursively enumerable and decidable languages.

---

## Deterministic vs. Nondeterministic TM

- **Deterministic TM (DTM)**  
  - At each moment, given the current state and the tape symbol under the head, there is **exactly one** transition.  
  - A DTM either halts in an accepting or rejecting state (deciding a language), or it can run forever on some inputs (semi‐deciding a language).  
  - The class of languages decidable by some DTM is exactly the class of **recursive (decidable) languages**.

- **Nondeterministic TM (NTM)**  
  - In each configuration (state + tape symbol), the machine may have **multiple** possible transitions.  
  - Conceptually, the NTM “branches” into parallel computations; if any branch eventually enters an accepting state, the NTM accepts.  
  - NTMs recognize the class of **recursively enumerable** languages.  
  - It is unknown whether every NTM can be simulated by a DTM with only a polynomial slowdown (this is essentially the P vs. NP question when restricted to polynomial time).

> **Key Point:**  
> In terms of recognition power, DTMs and NTMs are equivalent: a language is recursively enumerable if and only if some DTM semi‐decides it. For decision (total algorithms that always halt), DTMs capture exactly the decidable languages; NTMs do the same.

---

## Formal Definition of a TM

A Turing Machine is a 7‐tuple M = (Q, Σ, Γ, δ, q₀, q_accept, q_reject) where:  
1. **Q** is a finite set of states.  
2. **Σ** is a finite input alphabet (does not include the blank symbol “◻”).  
3. **Γ** is a finite tape alphabet, where `Σ ⊆ Γ` and `◻ ∈ Γ` is the special blank symbol.  
4. **δ : Q × Γ → Q × Γ × {L, R}** is the transition function. Given the current state `q ∈ Q` and the tape symbol `X ∈ Γ` under the head, δ returns a triple `(p, Y, D)` meaning:  
   - Write symbol `Y` in place of `X` on the tape.  
   - Move the head one square left (L) or right (R).  
   - Enter state `p ∈ Q`.  
   There is exactly one such triple for each `(q, X)` if we assume determinism.  
5. **q₀ ∈ Q** is the start state.  
6. **q_accept ∈ Q** is the unique accepting (final) state; **q_reject ∈ Q** is the unique rejecting state, with `q_reject ≠ q_accept`.  
7. **No transitions are defined out of** `q_accept` **or** `q_reject` (both are halting states).

- The tape is conceptually infinite in both directions (or infinite to the right and bounded on the left, depending on the variant), filled with blank symbols `◻` except for a finite region holding the input.  
- The head starts on the leftmost symbol of the input (or on a designated “first” square) in state `q₀`.  

A configuration of `M` is given by `(q, … a b c …)`, where `q ∈ Q` is the current state, and the tape contents are shown with the head pointing at the marked symbol (e.g., the head is on `b` if the configuration is `… a [q:b] c …`). At each step, the machine uses δ to rewrite the current tape cell, move the head, and change state.

---

## How a TM Operates

1. **Initialization**  
   - Place the input string `w = w₁w₂…wₙ` on consecutive tape cells, with the head on the leftmost cell (containing `w₁`).  
   - All other cells are blank (`◻`).  
   - Set the machine’s state to `q₀`.

2. **Transition Steps**  
   - Suppose the machine is in state `q ∈ Q` and the head is scanning symbol `X ∈ Γ`.  
   - Compute `(p, Y, D) = δ(q, X)`.  
     1. **Write** `Y` over the current tape cell.  
     2. **Move** the head one cell either **Left (L)** or **Right (R)**.  
        - If the head moves left from the leftmost tape cell, it either stays in place (for a semi‐infinite model) or “extends” the tape with a new blank cell.  
     3. **Enter** state `p`.  
   - This completes one computation step.  

3. **Halting and Acceptance**  
   - If `q = q_accept`, the machine halts and accepts.  
   - If `q = q_reject`, the machine halts and rejects.  
   - Otherwise, it continues reading δ indefinitely (possibly never halting if the language is recursively enumerable but not decidable).

4. **Tape Behavior**  
   - Cells not yet visited are blank (`◻`).  
   - Once the head moves past the last nonblank symbol, it still sees a blank and can write new nonblank symbols if δ instructs it.

5. **Overall Computation**  
   - The TM’s computation on input `w` is the (possibly infinite) sequence of configurations starting from `(q₀, [w₁]w₂…wₙ ◻ ◻ ◻ …)`, updating according to δ.  
   - If this sequence ever reaches `(q_accept, …)`, we say “`M` accepts `w`.” If it ever reaches `(q_reject, …)`, we say “`M` rejects `w`.” If it never reaches either halting state, `M` runs forever on `w`.

---

## Designing a TM

When building a TM to decide or recognize a language, consider the following guidelines:

1. **Identify the key task**  
   - Determine precisely what the TM must verify, modify, or compute. For a decision problem, the TM must **always** halt and correctly accept or reject. For a recognition (semi‐decision) problem, it may run forever on some inputs.

2. **Choose state names with clear semantics**  
   - Design states that represent distinct “phases” or “modes” of the algorithm. For example, separate the “scan for a 0” phase from the “scan for a matching 1” phase, or from “erase and return” phases.  
   - Each state label should reflect what the TM is checking or modifying at that moment.

3. **Use tape markings and head movement strategically**  
   - To remember which symbols have been processed, you may **overwrite** input symbols with special markers (e.g., replace a `0` with an `X` to mark it as “used”).  
   - Plan how the head will sweep left or right to find the next symbol, and whether you need to return to an earlier position.  

4. **Ensure proper halting**  
   - If deciding a language, include explicit transitions into `q_accept` or `q_reject` once the input is fully processed and the required conditions are met.  
   - Use a dedicated rejecting branch if you encounter any violation of the language’s pattern.

5. **Verify correctness by tracing configurations**  
   - Before writing down δ exhaustively, walk through a few sample inputs and manually trace how the head and tape evolve.  
   - This often reveals edge cases (e.g., empty input, single-symbol input, mismatched patterns) that must be handled.

6. **Keep the tape alphabet Γ minimal**  
   - Let Γ include only the symbols you actually need, plus any special marker symbols (e.g., `X`, `Y`) and the blank `◻`.  
   - A smaller Γ typically makes δ easier to specify and reason about.

---

## Example: Deciding the Language `{ 0ⁿ1ⁿ }`

We will construct a **deterministic TM** `M` that decides L = { 0ⁿ1ⁿ  |  n ≥ 0 }  over Σ = `{0, 1}`. Informally, `M` will verify that there are exactly as many 1s as 0s and that all 0s precede all 1s.  
1. Scan from left to right until you find an unmarked `0`.  
2. Replace that `0` with `X` (a new marker symbol), then move right to find the first unmarked `1`.  
3. If you find an unmarked `1`, replace it with `Y` (another marker), then return left to the leftmost tape cell and repeat.  
4. After marking each pair `(0, 1)`, if at any point you fail to find a matching unmarked `1`, **reject**.  
5. Once all `0`s have been marked (no unmarked `0` remains) and there are no unmarked `1`s remaining, **accept**.  
6. If there is an unmarked symbol in the “wrong region” (e.g., a `1` before all `0`s are marked), **reject**.

### 1. States and Tape Alphabet

- **Q = {  
   q_start,         # initial scanning (look for a 0 to mark)
   q_find1,         # after marking a 0, search for a 1
   q_return,        # return head to leftmost square
   q_check,         # check if any unmarked 0 remains
   q_accept,
   q_reject   }**

- **Σ = { 0, 1 }**  
- **Γ = { 0, 1, X, Y, ◻ }**  
  - `X` marks a “used” 0,  
  - `Y` marks a “used” 1,  
  - `◻` is the blank symbol.

- **q₀ = q_start**  
- **q_accept** is the accepting state; **q_reject** is the rejecting state.  

### 2. Informal δ-Table

Below is a high-level description of δ for each relevant `(state, tape_symbol)` pair. Each line `δ(q, A) = (p, B, D)` means: “In state `q` reading `A`, write `B`, move head in direction `D ∈ {L, R}`, and enter state `p`.”

---

#### State `q_start`  
- **δ(q_start, 0) = (q_find1, X, R)**  
  - Found an unmarked `0`. Mark it as `X`, then switch to `q_find1` to locate a matching `1`.  

- **δ(q_start, X) = (q_start, X, R)**  
  - Already marked `0` (an `X`), skip it and continue scanning right.  

- **δ(q_start, Y) = (q_start, Y, R)**  
  - Already marked `1` (a `Y`), skip it (we are still in the phase of finding an unmarked `0`).  

- **δ(q_start, 1) = (q_reject, 1, R)**  
  - Encountered an unmarked `1` before finding all 0s. This means the string is of form “some 0s, then a 1, then later a 0.” Reject immediately.  

- **δ(q_start, ◻) = (q_check, ◻, L)**  
  - Reached the blank (end of tape) without finding any new `0`. Move to `q_check` to verify that no unmarked `1` remains.

---

#### State `q_find1`  
- **δ(q_find1, 1) = (q_return, Y, L)**  
  - Found an unmarked `1`. Mark it as `Y` and switch to `q_return` to head back to the left end.  

- **δ(q_find1, Y) = (q_find1, Y, R)**  
  - Already marked `1`, skip it.  

- **δ(q_find1, X) = (q_find1, X, R)**  
  - Seen an `X` (a marked `0`), skip it.  

- **δ(q_find1, 0) = (q_find1, 0, R)**  
  - Seen an unmarked `0` that must be to the left of the 1 we want; skip it (we look only for the first unmarked `1`).  

- **δ(q_find1, ◻) = (q_reject, ◻, R)**  
  - Reached the blank without seeing an unmarked `1` to match the `0` we marked. Reject (unequal numbers).

---

#### State `q_return`  
- **δ(q_return, X) = (q_return, X, L)**  
  - While returning left, skip marked `0`s.  

- **δ(q_return, Y) = (q_return, Y, L)**  
  - Skip marked `1`s.  

- **δ(q_return, 0) = (q_return, 0, L)**  
  - Skip any remaining unmarked `0`s (we are simply returning).  

- **δ(q_return, 1) = (q_return, 1, L)**  
  - Skip any unmarked `1`s.  

- **δ(q_return, ◻) = (q_start, ◻, R)**  
  - Reached the leftmost blank. Now go to `q_start` and move right to begin the next marking cycle.

---

#### State `q_check`  
- **δ(q_check, X) = (q_check, X, L)**  
  - Move left over any marked `0`s.  

- **δ(q_check, Y) = (q_check, Y, L)**  
  - Move left over any marked `1`s.  

- **δ(q_check, 0) = (q_reject, 0, R)**  
  - Found an unmarked `0` during final check. That means there was no matching `1` for that `0`. Reject.  

- **δ(q_check, 1) = (q_reject, 1, R)**  
  - Found an unmarked `1` without a corresponding `0` (since all 0s were supposedly marked). Reject.  

- **δ(q_check, ◻) = (q_accept, ◻, R)**  
  - Reached the leftmost blank with no unmarked `0` or `1` found. The string has perfectly matched 0s and 1s in the correct order. Accept.

---

### 3. Operation on a Sample Input

Let us trace `M` on the input `000111`:

1. **Initial configuration**  
   - Tape: `[0 0 0 1 1 1 ◻ ◻ …]`  
   - Head at leftmost `0`, State = `q_start`

2. **Cycle 1 (mark first 0–1 pair)**  
   - `q_start` sees `0` → mark as `X` → go to `q_find1`, head moves right.  
     - Tape: `[X 0 0 1 1 1 ◻ …]`, head on the second cell (`0`).  
   - `q_find1`: skip `0` → skip next `0` → reach first unmarked `1` → mark as `Y` → go to `q_return`.  
     - Tape becomes `[X 0 0 Y 1 1 ◻ …]`, head on the marked `Y`.  
   - `q_return`: move left over Y, 0, 0, X until hitting `◻` on the left edge → then switch to `q_start` and move right.  
     - After return, head is on the first `X`. State = `q_start`.

3. **Cycle 2 (mark second pair)**  
   - `q_start` skips `X` → sees next unmarked `0` → mark as `X`, go to `q_find1`.  
     - Tape: `[X X 0 Y 1 1 ◻ …]`, head on third cell (`0`).  
   - `q_find1`: skip marked cells (`X`, `Y`) until it finds next unmarked `1` → mark as `Y`, go to `q_return`.  
     - Tape: `[X X 0 Y Y 1 ◻ …]`, head on that `Y`.  
   - `q_return`: move left back to blank → switch to `q_start`.

4. **Cycle 3 (mark third pair)**  
   - `q_start` skips `X`, `X` → sees the last unmarked `0` → mark as `X`, go to `q_find1`.  
     - Tape: `[X X X Y Y 1 ◻ …]`, head on third marked cell.  
   - `q_find1`: skip three `X`s and two `Y`s until it finds the last `1` → mark it as `Y`, go to `q_return`.  
     - Tape: `[X X X Y Y Y ◻ …]`, head on that `Y`.  
   - `q_return`: move left to blank → switch to `q_start` (head on the first `X`).

5. **Final Check**  
   - `q_start` now sees only `X` and `Y` and eventually hits blank → moves to `q_check`.  
   - `q_check` moves left across all marked symbols → hits leftmost blank → enters `q_accept`.

Hence `M` accepts `000111`. If at any step a required match was missing or the input had extra symbols out of order, `M` would transition to `q_reject`.

---

## Additional Remarks and Tips

1. **Multiple Tape Tracks and Subroutines**  
   - Some TM designs use a **two‐track tape** or multiple tapes (multi‐tape TM) to simplify the control logic. Because a multi‐tape TM can be simulated by a standard single‐tape TM with only polynomial slowdown, these variants do not expand the class of decidable languages; they only make design neater.  
   - One can view a “subroutine” as a collection of states that perform a specific job (e.g., “scan to the right until you see a 1,” or “erase a block of symbols”). Upon completion, the subroutine enters a distinguished state marked “return.” Then the main TM can link to that return state and continue.

2. **Why This Example Matters**  
   - The language `{0ⁿ1ⁿ}` is context‐free, so a PDA could decide it. The TM approach, however, works similarly by marking and crossing off symbols, illustrating that TMs generalize PDAs.  
   - By using the tape, we effectively implement a two‐stack mechanism: one “stack” is the region of marked `X` symbols on the left, and matching is done by sweeping right for the corresponding `1`s.  

3. **Design Checklist**  
   - **Tape Alphabet**: Include only the symbols you need—here, `{0, 1, X, Y, ◻}`.  
   - **States**: Break down into phases (scan for a 0, scan for a 1, return, check for remaining symbols).  
   - **Transitions**: For each `(state, symbol)` pair, specify exactly one `(next_state, write_symbol, move_direction)`.  
   - **Halting Conditions**: Be explicit about when the TM should accept or reject. In this example, any mismatch or leftover symbol triggers immediate rejection; only when everything lines up do we accept.

4. **Extending to More Complex Languages**  
   - A TM can decide any context‐free language (by first converting a CFG to a PDA, then simulating the PDA with a TM), as well as languages beyond context‐free, such as `{0ⁿ1ⁿ2ⁿ}` or even arbitrary recursive languages.  
   - For `{0ⁿ1ⁿ2ⁿ}`, a TM can cross off one `0`, one `1`, one `2` per cycle. Each cycle marks one triple, returning to the left after each marking.  

5. **Limits of Turing Machines**  
   - Although TMs are extremely powerful, there exist languages they **cannot** decide (e.g., the Halting problem). These are the **undecidable** languages.  
   - The Church‐Turing thesis posits that any effectively computable function (in the intuitive sense) can be computed by a Turing Machine.  

---

**Key Takeaway:**  
A Turing Machine is a finite‐state device equipped with an infinite tape, allowing it to read, write, and move left or right as needed. This extra memory capability makes TMs strictly more powerful than DFAs, NFAs, and PDAs. By carefully designing states and tape‐manipulation rules, one can build a TM that decides the language { 0ⁿ1ⁿ  |  n ≥ 0 }, marking and matching each `0` with a corresponding `1`. The example illustrates how the TM’s infinite tape and head movements enable unbounded counting and arbitrary symbol matching, features that lie at the core of “Turing‐complete” computation.  

---
## My python code:
I implemented a Turing Machine which takes two numbers in unary numeral systems and adds them. For exemple, I will have on the tape, initially, 111+1111$. After, I will have 1111111$.  
Run the following command:  
```
python l6.py
```
---
