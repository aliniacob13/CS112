# Pushdown Automata (PDA)

---

## Table of Contents

1. [Introduction to PDAs](#introduction-to-pdas)  
2. [Why Stack-Based Memory?](#why-stack-based-memory)  
3. [Determinism vs. Nondeterminism](#determinism-vs-nondeterminism)  
4. [Formal Definition of a PDA](#formal-definition-of-a-pda)  
5. [How a PDA Operates](#how-a-pda-operates)  
6. [Designing a PDA](#designing-a-pda)  
7. [Example: Recognizing Balanced Strings `0ⁿ1ⁿ`](#example-recognizing-balanced-strings-0ⁿ1ⁿ)  
8. [Additional Remarks and Tips](#additional-remarks-and-tips)
9. [My python code](#my-python-code)

---

## Introduction to PDAs

A **Pushdown Automaton (PDA)** is a finite automaton augmented with a stack—an unbounded memory device that can be used to store and retrieve symbols in a last‐in, first‐out (LIFO) fashion. Whereas a DFA/NFA can only “remember” its current state, a PDA can also record an unbounded amount of information on its stack. This additional power enables PDAs to recognize exactly the class of **context‐free languages (CFLs)**, such as the language { 0ⁿ1ⁿ  |  n ≥ 0 } which cannot be recognized by any finite automaton alone.  
which cannot be recognized by any finite automaton alone.

---

## Why Stack-Based Memory?

1. **Unbounded counting**  
   Some languages (e.g., `{ 0ⁿ1ⁿ | n ≥ 0 }`) require matching the number of symbols in one part of the input with another part. A finite‐state control has only finitely many states, so it cannot count arbitrarily large `n`. By pushing each `0` onto the stack and then popping for each `1`, the PDA effectively “counts” the number of 0s before expecting exactly the same number of 1s.

2. **Nested and recursive structure**  
   Many context‐free languages (like balanced parentheses or palindromes) have nested or recursive patterns. A stack naturally represents nested contexts: when you see an opening symbol (e.g., `(` or `0`), you push it; when you see a closing symbol (e.g., `)` or `1`), you pop and verify that it matches.  

3. **Finite control + stack = unbounded memory**  
   - The finite‐state control (`Q`) can compare the current input symbol with the top of the stack symbol.  
   - Transitions can push new symbols or pop the top symbol as needed.  
   - As long as there is space on the stack, the PDA can store arbitrarily many symbols, enabling recognition of CFLs.

---

## Determinism vs. Nondeterminism

- **Deterministic PDA (DPDA)**  
  - For any combination of (current state, input symbol or ε, top‐of‐stack symbol), there is at most one possible transition.  
  - At most one transition may be taken at each step.  
  - ε‐moves (stack‐only moves) are allowed, provided they do not conflict with any input‐consuming move.  
  - DPDAs can recognize only a **proper subset** of CFLs (called deterministic context‐free languages, DCFLs). Balanced parentheses and many programming‐language grammars are DCFLs.

- **Nondeterministic PDA (NPDA)**  
  - There may be multiple transitions defined for the same (state, input‐symbol‐or‐ε, top‐of‐stack) combination.  
  - When faced with multiple choices, the NPDA “branches” into parallel computational paths (each path has its own stack).  
  - If **any** branch leads to an accepting state (with the input consumed), the NPDA accepts the input.  
  - NPDAs can recognize **all** context‐free languages. For example, palindromes over `{0,1}` require nondeterminism to guess the midpoint; no DPDA can handle that language.

---

## Formal Definition of a PDA

A Pushdown Automaton is formally defined as a 7‐tuple P = (Q, Σ, Γ, δ, q₀, Z₀, F) 
 where:

1. **Q** is a finite set of states.  
2. **Σ** is the finite input alphabet.  
3. **Γ** is the finite stack alphabet (symbols that may appear on the stack).  
4. **δ : Q × (Σ ∪ {ε}) × Γ → 𝒫(Q × Γ*)** is the transition function. For each triple `(q, a, X)` (where `a` is either an input symbol or ε, and `X` is the current stack top), δ returns a set of pairs `(p, w)`, meaning “from state q, reading symbol a (or no symbol if a=ε), and seeing X on top of the stack, go to state p, pop X, and push the (possibly empty) string w ∈ Γ* onto the stack.”  
5. **q₀ ∈ Q** is the unique start state.  
6. **Z₀ ∈ Γ** is the initial stack symbol (marks the bottom of the stack).  
7. **F ⊆ Q** is the set of accepting (final) states.

- **Computation**  
  - At each step, if the PDA is in state `q ∈ Q`, the next unread input symbol is either `a ∈ Σ` or no symbol if we choose an ε‐transition.  
  - Let `X ∈ Γ` be the top of the stack. If `(p, w) ∈ δ(q, a, X)`, then the machine can nondeterministically:  
    1. Consume input symbol `a` (unless `a=ε`),  
    2. Pop `X` from the stack,  
    3. Push the string `w = Y₁ Y₂ … Yₖ` (where each `Yᵢ ∈ Γ`) onto the stack (so `Y₁` becomes the new top, then `Y₂`, and so on).  
    4. Enter state `p`.  

- **Acceptance**  
  - By **final state**: The PDA accepts if, after consuming the entire input string, it is in a state `q ∈ F` (regardless of what remains on the stack).  
  - (Alternatively, one can define acceptance by empty stack, but this README will assume acceptance by final state for clarity, though the two definitions are equivalent up to slight modifications.)

---

## How a PDA Operates

1. **Initialization**  
   - The PDA begins in state `q₀`, with input tape positioned at the first symbol, and the stack initialized to contain only `Z₀` (the bottom‐of‐stack marker).  

2. **ε‐Closure (Optional ε‐Moves)**  
   - At any point, if there is a transition of the form `(q, ε, X) → {(p, w₁), (r, w₂), …}`, the PDA can choose to take an ε‐move. This means it does not consume any input; it only pops `X` from the stack and pushes the replacement `wᵢ`, then moves to the corresponding next state.  
   - In practice, one repeatedly applies ε‐transitions (on any active configuration) until no more ε‐moves are possible before proceeding to consume the next input symbol.

3. **Reading an Input Symbol**  
   - Suppose the current input symbol is `a` and the current state is `q`. Let `X` be the symbol on top of the stack.  
   - If `(p, w) ∈ δ(q, a, X)`, then the PDA may choose that transition:  
     1. Pop `X`.  
     2. Push the string `w = Y₁Y₂…Yₖ` back onto the stack (so `Y₁` becomes the new top, then `Y₂`, etc.; if `w` is empty, nothing is pushed).  
     3. Enter state `p`.  
     4. Advance the input head by one position (consuming `a`).  

4. **Nondeterministic Branching**  
   - If more than one transition is possible from `(q, a, X)`, the PDA “branches.” Each branch continues its own computation independently, each with its own copy of the stack. If **any** branch eventually ends in an accepting state after consuming all input, the entire PDA accepts the input.  
   - If no transition is possible (including ε‐moves) for a given branch, that branch “dies” (rejects).  

5. **Acceptance**  
   - After the final input symbol is consumed (or earlier, if the PDA chooses a sequence of ε‐moves that lead it to a final state with the input empty), if at least one branch ends in `q ∈ F`, the input is accepted. Otherwise, it is rejected.

---

## Designing a PDA

When constructing a PDA for a context‐free language, one generally follows these steps:

1. **Identify the fundamental pattern**  
   - Determine what part of the input needs to be “remembered” on the stack. For example, if the language is `{0ⁿ1ⁿ}`, you must remember how many 0s have been seen to ensure exactly the same number of 1s follow.

2. **Decide on states and stack alphabet (Γ)**  
   - Choose states that represent distinct phases of recognition (e.g., “reading 0s,” “reading 1s”).  
   - Let Γ include any symbols you need to push (for `{0ⁿ1ⁿ}`, Γ can simply be `{0, Z₀}`, where `0` on the stack counts how many 0s remain to be matched).

3. **Outline transitions**  
   - For each symbol in Σ, specify how the stack should be updated.  
   - Include ε‐transitions if you need to switch phases (e.g., from “pushing” to “popping”).

4. **Ensure proper acceptance condition**  
   - If accepting by final state, make sure the PDA can reach an accepting state exactly when the input is fully consumed and, if needed, the stack is in the correct condition (often `Z₀` only).  
   - If accepting by empty stack, ensure that after consuming all input, the stack is empty (or contains only the bottom marker `Z₀`).

5. **Check for completeness and nondeterministic choices**  
   - At each configuration `(q, a, X)`, list all possible transitions.  
   - Add transitions that handle unexpected symbols (if your design requires rejecting immediately when something is out of place).  
   - If the PDA must “guess” a split point (e.g., for palindromes or even‐length languages), include an ε‐transition that moves to a new state and begins the next phase.

---

## Example: Recognizing Balanced Strings `0ⁿ1ⁿ`

Consider the language L = { 0ⁿ1ⁿ  |  n ≥ 0 } over the alphabet Σ = `{0, 1}`. We want a PDA that accepts exactly those strings that consist of some number of 0s followed by the same number of 1s (e.g., ε, `01`, `0011`, `000111`, etc.).  
### 1. States and Stack Alphabet

- **Q = { q_push, q_pop, q_accept }**  
  - `q_push`: the phase where we read all the 0s and push them onto the stack.  
  - `q_pop`: the phase where we read 1s and pop the corresponding 0s from the stack.  
  - `q_accept`: an accepting sink state (optional, or we can accept in `q_pop` if stack only has `Z₀`).

- **Σ = { 0, 1 }**  

- **Γ = { 0, Z₀ }**  
  - `Z₀` is the bottom‐of‐stack marker.  
  - We push `0` on the stack once for each input 0.

- **q₀ = q_push** (start state)  
- **Z₀** is initially on the stack.  
- **F = { q_accept }** (the set of accepting states). We will move to `q_accept` once all matching is done and the stack has returned to `Z₀` only.

### 2. Transition Function δ

We define δ in terms of rules of the form δ(current_state, input_symbol or ε, top_of_stack) → set of (next_state, string_to_push) where “string_to_push” is a (possibly empty) concatenation of symbols from Γ.  
1. **From q_push** (reading zeros)  
   - On input `0`, with top marker `Z₀`:  
     ```
     δ(q_push, 0, Z₀) = { (q_push, 0Z₀) }
     ```  
     Meaning: pop `Z₀`, push `0Z₀` (so `0` is now on top, with `Z₀` below). Stay in `q_push`.  
   - On input `0`, with top `0`:  
     ```
     δ(q_push, 0, 0) = { (q_push, 00) }
     ```  
     Meaning: for each additional `0`, pop the current top `0` and push `00` (stack gains one more `0` on top).  
   - To switch phases once we see the first `1` (ε‐transition):  
     ```
     δ(q_push, ε, Z₀) = { (q_pop, Z₀) }
     δ(q_push, ε, 0 ) = { (q_pop, 0) }
     ```  
     Explanation: As soon as the next input symbol is not `0` (we’ve read all the 0s we want), the PDA can nondeterministically choose to move from `q_push` to `q_pop` without consuming any symbol. We keep the entire stack intact (pop and push the same top symbol) and change to `q_pop`.  

2. **From q_pop** (reading ones and popping zeros)  
   - On input `1`, with top `0`:  
     ```
     δ(q_pop, 1, 0) = { (q_pop, ε) }
     ```  
     Meaning: when we see a `1`, pop exactly one `0` from the stack (push ε, effectively removing it). Remain in `q_pop`.  
   - If the stack is back to `Z₀` (i.e., all 0s have been matched) and no more input remains, we can accept:  
     ```
     δ(q_pop, ε, Z₀) = { (q_accept, Z₀) }
     ```  
     Meaning: once the top of stack is `Z₀` and there are no more unmatched 0s, move to the accepting state `q_accept` without pushing anything.

3. **From q_accept** (accepting sink)  
   - We do not need any further transitions. Once in `q_accept`, the machine has accepted.  

There are no transitions on input `1` from `q_push` (so if the first symbol is `1` or if 1 appears before all 0s have been processed, the only possible way is to take the ε‐transition to `q_pop` and attempt popping, which will fail unless the stack has a `0` at the top).

### 3. Operation on Input `000111`

1. **Initial configuration**  
   - State: `q_push`  
   - Input: `000111` (head at first `0`)  
   - Stack: `[Z₀]`

2. **Reading the first `0` in q_push**  
   - Top of stack = `Z₀`  
   - Transition: δ(q_push, 0, Z₀) → (q_push, 0Z₀)  
   - New state: `q_push`  
   - Input remaining: `00111` (head advanced)  
   - Stack: `[0, Z₀]`

3. **Reading the second `0` in q_push**  
   - Top of stack = `0`  
   - Transition: δ(q_push, 0, 0) → (q_push, 00)  
   - New state: `q_push`  
   - Input remaining: `0111`  
   - Stack: `[0, 0, Z₀]`

4. **Reading the third `0` in q_push**  
   - Top of stack = `0`  
   - Transition: δ(q_push, 0, 0) → (q_push, 00)  
   - New state: `q_push`  
   - Input remaining: `111`  
   - Stack: `[0, 0, 0, Z₀]`

5. **Now the next symbol is `1`. We must switch to q_pop**  
   - In `q_push`, no δ(q_push, 1, 0) is defined.  
   - We take the ε‐move: δ(q_push, ε, 0) → (q_pop, 0)  
   - State: `q_pop`  
   - Input still: `111` (head has not moved because ε‐move consumes no input)  
   - Stack remains: `[0, 0, 0, Z₀]`

6. **Reading the first `1` in q_pop**  
   - Top of stack = `0`  
   - Transition: δ(q_pop, 1, 0) → (q_pop, ε) (pop one `0`)  
   - New state: `q_pop`  
   - Input remaining: `11`  
   - Stack: `[0, 0, Z₀]`

7. **Reading the second `1` in q_pop**  
   - Top of stack = `0`  
   - δ(q_pop, 1, 0) → (q_pop, ε)  
   - State: `q_pop`  
   - Input remaining: `1`  
   - Stack: `[0, Z₀]`

8. **Reading the third `1` in q_pop**  
   - Top of stack = `0`  
   - δ(q_pop, 1, 0) → (q_pop, ε)  
   - State: `q_pop`  
   - Input now exhausted (`""`)  
   - Stack: `[Z₀]`

9. **Stack is back to `Z₀` and input is empty. Move to accept**  
   - δ(q_pop, ε, Z₀) → (q_accept, Z₀)  
   - State: `q_accept` (accepting)  
   - Input: empty  
   - Stack: `[Z₀]`

Since we have reached `q_accept` with no input left, the machine accepts `000111`.

### 4. Summary of Transitions

- **q_push**  
  - (0, Z₀) → (q_push, 0Z₀)  
  - (0, 0)  → (q_push, 00)  
  - (ε, Z₀) → (q_pop, Z₀)  
  - (ε, 0)  → (q_pop, 0)

- **q_pop**  
  - (1, 0)  → (q_pop, ε)  
  - (ε, Z₀) → (q_accept, Z₀)

- **q_accept**  
  - No outgoing transitions (sink).

---

## Additional Remarks and Tips

1. **Acceptance by Empty Stack vs. Final State**  
   - Some textbooks define PDA acceptance by requiring the stack be empty (i.e., contain only `Z₀`) at the end of input, regardless of the current state. That variant is equivalent (up to slight modifications) to accepting by final state. In our design, we explicitly transition to `q_accept` once the stack has returned to `Z₀`.

2. **Nondeterministic Guessing**  
   - Our design uses an ε‐transition from `q_push` to `q_pop` to guess the moment when the last `0` has been read. If an input 1 appears while in `q_push`, the PDA must (nondeterministically) take that ε‐transition immediately, or else it would have no valid transition on input 1.  
   - In more complex languages (e.g., palindromes), one might need multiple ε‐moves to guess splitting points or midpoints.

3. **DPDA vs. NPDA**  
   - The `{0ⁿ1ⁿ}` language is deterministic: there is never a genuine branching choice, because once a `1` is seen, the PDA must move to `q_pop` immediately. Therefore, this PDA can be implemented deterministically (a DPDA) if one prohibits any other conflicting transitions at the point of switching from pushing to popping.  
   - However, for languages such as palindromes, nondeterminism is required to guess the midpoint: no DPDA can handle all palindromes.

4. **Converting a CFG to a PDA**  
   - There is a general construction that, given any context‐free grammar (CFG), produces an equivalent NPDA (the “predict/match” parser):  
     1. The stack initially holds the start symbol of the grammar.  
     2. An ε‐transition expands a nonterminal on the stack by pushing the right‐hand side of one of its productions.  
     3. A transition that matches a terminal symbol in the input consumes that terminal and pops it from the stack.  
     4. Once the input is exhausted and the stack holds only `Z₀` (or an equivalent marker), the machine enters an accepting state.  
   - This proves that CFLs ⟷ PDAs are equivalent in recognition power.

5. **Why PDAs Matter**  
   - PDAs occupy the next step in the Chomsky hierarchy after finite automata. They precisely capture the class of context‐free languages, which includes many “balanced” or “nested” structures that arise in programming languages (e.g., matched parentheses, nested if/else, call stacks).  
   - Understanding PDAs is essential for parsing and compiler design, as most parser generators (LL, LR, etc.) implement variants of deterministic PDAs.

---
 ## My python code  
 I use a PDA to check balanced strings `0ⁿ1ⁿ`. Run the following command:
```
python pda.py file.pda
```
---
