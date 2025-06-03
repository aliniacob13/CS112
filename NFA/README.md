# Nondeterministic Finite Automaton (NFA)



## Table of Contents

1. [Introduction to NFAs](#introduction-to-nfas)  
2. [Nondeterminism vs. Determinism](#nondeterminism-vs-determinism)  
3. [Formal Definition of an NFA](#formal-definition-of-an-nfa)  
4. [How an NFA Operates](#how-an-nfa-operates)  
5. [Designing an NFA](#designing-an-nfa)  
6. [Example: Recognizing Strings That Contain “ab”](#example-recognizing-strings-that-contain-ab)  
7. [Additional Remarks and Tips](#additional-remarks-and-tips)

---

## Introduction to NFAs

A **Nondeterministic Finite Automaton (NFA)** extends the concept of a Deterministic Finite Automaton (DFA) by allowing multiple possible transitions for the same-state and input-symbol pair, as well as ε-transitions (sometimes called λ-transitions). In practical terms, an NFA can “branch” into several possible next states on a given input, or even move to a new state without consuming any input symbol (via an ε-transition).

- NFAs recognize exactly the same class of languages as DFAs (the regular languages). However, NFAs can sometimes be more concise or more intuitive to construct than equivalent DFAs.
- In an NFA, an input string is accepted if at least one of the possible “branches” of execution ends in an accepting state after reading the entire string.

---

## Nondeterminism vs. Determinism

1. **Deterministic Model (DFA)**  
   - At each step in the computation, there is exactly one possible transition to follow for the current state and the next input symbol.  
   - If the unique path of transitions ends in an accepting state, the input is accepted; otherwise, it is rejected.

2. **Nondeterministic Model (NFA)**  
   - At each step, there may be **multiple** possible transitions for the same (state, input-symbol) pair.  
   - Additionally, ε-transitions allow the automaton to change state without reading an input symbol.  
   - The input is accepted if **any one** of the possible computation paths leads to an accepting state after the entire input has been consumed.

> **Key Point:** Although NFAs can “branch” into multiple possibilities, they do **not** recognize more languages than DFAs. Every NFA has an equivalent DFA, though the DFA may have exponentially more states in the worst case.

---

## Formal Definition of an NFA

Formally, an NFA is a 5-tuple N = (Q, Σ, δ, q₀, F)  
where:

1. **Q** is a finite set of states.  
2. **Σ** is a finite input alphabet (a set of symbols).  
3. **δ : Q × (Σ ∪ {ε}) → 𝒫(Q)** is the transition function, mapping a state and either an input symbol or ε to a **set** of possible next states.  
4. **q₀ ∈ Q** is the start state.  
5. **F ⊆ Q** is the set of accepting (final) states.

- **δ(q, a) = {r₁, r₂, …}** means that from state `q`, upon reading symbol `a`, the NFA may transition nondeterministically to any of the states in that set.
- **δ(q, ε) = {r₃, …}** represents ε-transitions (also commonly written as δ(q, λ) or δ(q, $)), which move from `q` to any of those states without consuming any input symbol.

When processing an input string `w = a₁ a₂ … aₙ`, the NFA keeps track of all possible current states simultaneously. At each position in the input:

1. First, apply all ε-closures (i.e., follow any number of ε-transitions) from each current state.  
2. Then, read the next symbol `ai` and move into every reachable state via δ on that symbol.  
3. Apply ε-closure again before reading the next input symbol.  
4. At the end of the string, if **any** of the possible current states belongs to `F`, the NFA accepts.

---

## How an NFA Operates

1. **Initialization**  
   - Start from the initial state `q₀`.  
   - Compute the ε-closure of `{q₀}`, which is the set of all states reachable from `q₀` using only ε-transitions (including `q₀` itself). This is the set of “active” states before reading any input.

2. **Processing Each Input Symbol**  
   For each symbol `a` in the input string, do the following in sequence:  
   - Let `Current` be the set of active states from the previous step (or ε-closure).  
   - Compute `Move = ⋃ { δ(q, a) | q ∈ Current }`. In other words, take all possible transitions on `a` from every state in `Current`.  
   - Compute `Next = ε-closure(Move)`. Follow ε-transitions from each state in `Move` to form the new set of active states.  
   - Set `Current ← Next` and proceed to the next symbol.

3. **Acceptance Check**  
   - After the last symbol has been consumed and ε-closure has been applied, check if `Current ∩ F ≠ ∅`.  
   - If there is at least one accepting state in the set of current states, the NFA accepts the string; otherwise, it rejects.

> **Note on ε-closure:**  
> - The ε-closure of a set `S ⊆ Q` is defined as the smallest set `C ⊆ Q` such that:  
>   1. `S ⊆ C`, and  
>   2. for every state `p ∈ C`, if `δ(p, ε) = {r₁, r₂, …}`, then all those `rᵢ` are also in `C`.  
> - In practice, one computes ε-closure by repeatedly adding states reachable via ε until no new states appear.

---

## Designing an NFA

When constructing an NFA for a specific regular-language recognition task, keep these guidelines in mind:

1. **Identify Key Subtasks or Patterns**  
   - Determine the minimal “building blocks” of behavior needed to recognize the language.  
   - For example, if the language is “all strings containing the substring `ab`,” then one subtask is “detect an `a` and then check whether a `b` follows.”

2. **Introduce ε-Transitions to Handle “Nondeterministic Guesses”**  
   - Use ε-transitions when you wish to “branch” into a new computation path without consuming input.  
   - This is especially helpful for languages that require checking multiple overlapping conditions (e.g., multiple substrings) in parallel.

3. **Keep Track of Partial Progress**  
   - Assign each state a clear semantic meaning, such as “we have read one `a` and are awaiting a `b`,” or “we have recognized the substring and can now loop freely.”  
   - Avoid introducing extraneous states; each state should correspond to a necessary distinction in the process of recognition.

4. **Multiple Transitions on the Same Symbol**  
   - In an NFA, it is valid for `δ(q, a)` to contain two or more different next states.  
   - This means that upon reading `a` from state `q`, the machine can nondeterministically follow any of those outgoing edges.

5. **Use ε-Transitions to Reset or “Forget”**  
   - If part of your recognition requires “abandoning” a partial match and restarting, an ε-transition can move you back to an initial or intermediate state without consuming a new symbol.  
   - This simplifies the design of many regular-language recognizers by avoiding complicated loops.

---

## Example: Recognizing Strings That Contain “ab”

Below is a step-by-step description for constructing an NFA that accepts all strings over the alphabet `{a, b}` which contain the substring `ab` at least once.

### 1. Define States

- **q₀**: the start state. In this state, no part of the substring `ab` has been recognized so far.  
- **q₁**: an intermediate state meaning “an `a` has just been read, so if a `b` follows immediately, we complete `ab`.”  
- **q₂**: an accepting (final) state meaning “we have recognized `ab`.” Once this state is reached, the string should be accepted—regardless of any further symbols.

### 2. Define the Alphabet

- Σ = `{a, b}`.

### 3. Define the Transition Function δ

We construct δ as a mapping from `(state, symbol/ε)` to a set of possible next states.

1. **From q₀**  
   - On `a`:  
     - Stay in q₀ (to allow skipping over `a` if it is not the start of the first `ab`).  
       ```
       δ(q₀, a) includes q₀
       ```  
     - Move to q₁ (to guess that this `a` might be the start of `ab`).  
       ```
       δ(q₀, a) includes q₁
       ```  
   - On `b`:  
     - Stay in q₀ (since `b` by itself does not help form `ab`, but we can continue scanning).  
       ```
       δ(q₀, b) includes q₀
       ```

2. **From q₁**  
   - On `b`:  
     - Move to q₂ (we successfully recognized `ab`).  
       ```
       δ(q₁, b) = {q₂}
       ```  
   - On `a`:  
     - (No direct `a`→ transition required, since if we see another `a`, we can still consider that new `a` as the start of a fresh `ab`. In practice, we will use an ε-transition to fall back.)  
   - On ε:  
     - Move back to q₀ (so that if we guessed “start of `ab`” but then saw something else, we can reset to q₀ and try again nondeterministically).  
       ```
       δ(q₁, ε) = {q₀}
       ```

3. **From q₂**  
   - q₂ is a final state. We can choose to loop on `a` or `b` and remain in q₂, because once `ab` is found, the string should be accepted regardless of what comes next:  
     ```
     δ(q₂, a)  = {q₂}
     δ(q₂, b)  = {q₂}
     δ(q₂, ε)  = ∅   (no need for ε here, since we already accept)
     ```  
   - By including loops on both `a` and `b` from q₂ to q₂, we ensure that any suffix after the first `ab` does not cause rejection.

### 4. Summarize δ in Tabular Form

| Current State | Input Symbol | Next State(s)   |
|:-------------:|:------------:|:---------------:|
| q₀            | a            | { q₀, q₁ }      |
| q₀            | b            | { q₀ }          |
| q₀            | ε            | ∅               |
| q₁            | b            | { q₂ }          |
| q₁            | ε            | { q₀ }          |
| q₁            | a            | ∅               |
| q₂            | a            | { q₂ }          |
| q₂            | b            | { q₂ }          |
| q₂            | ε            | ∅               |

- Note that δ is defined on Σ ∪ {ε}.  
- When δ(p, x) is empty (∅), it means no transition exists for symbol x from state p.

### 5. Start and Accepting States

- **Start state:** q₀  
- **Accepting (final) state:** q₂ (only)

### 6. Operation Walk-Through

1. **Initialization**  
   - Active states = ε-closure({q₀}) = {q₀} (since q₀ has no incoming ε from itself).

2. **Reading an input string**  
   - Suppose the input is `b a b a`. We simulate step by step:  
     1. **Symbol** `b` from q₀:  
        - Move: δ(q₀, b) = {q₀}.  
        - ε-closure({q₀}) = {q₀}.  
     2. **Symbol** `a` from q₀:  
        - Move: δ(q₀, a) = {q₀, q₁}.  
        - ε-closure({q₀, q₁}) = {q₀, q₁, (and from q₁ you get ε→q₀ which is already in the set)} = {q₀, q₁}.  
     3. **Symbol** `b` from the set {q₀, q₁}:  
        - Move from q₀ on b → {q₀}.  
        - Move from q₁ on b → {q₂}.  
        - Combined Move = {q₀, q₂}.  
        - ε-closure({q₀, q₂}) = {q₀, q₂} (no additional ε transitions apply).  
     4. **Symbol** `a` from {q₀, q₂}:  
        - Move from q₀ on a → {q₀, q₁}.  
        - Move from q₂ on a → {q₂}.  
        - Combined Move = {q₀, q₁, q₂}.  
        - ε-closure({q₀, q₁, q₂}) = {q₀, q₁, q₂}.  

   - After the final input symbol, the active set contains q₂, which is accepting, so the NFA accepts `baba`.

3. **Key Observation**  
   - As soon as the NFA reaches q₂ at any intermediate step, it can remain in q₂ forever (or move back via ε if we had chosen that path—but since q₂ loops on every input, that branch will remain accepting).  
   - If one computational branch dies (no valid transition at some symbol), other branches may still survive and possibly accept.

---

## Additional Remarks and Tips

1. **Conversion to DFA (Subset Construction)**  
   - Every NFA can be converted to an equivalent DFA using the subset (powerset) construction.  
   - In that construction, each DFA state corresponds to a set of NFA states (an “ε-closure set”).  
   - Although conceptually straightforward, the resulting DFA may have up to 2^|Q| states in the worst case.

2. **Use of ε-Transitions**  
   - ε-transitions make certain regular expressions (e.g., `(a|b)*ab(a|b)*`) easier to implement directly.  
   - However, one can always eliminate ε-transitions by computing ε-closures and adjusting δ accordingly, yielding an NFA without ε’s.

3. **Design Strategy**  
   - Identify “landmark” substrings or conditions in your target language—for example, “`ab` appears somewhere,” or “the string ends with `01`,” etc.  
   - Model each landmark as a distinct state (or set of states).  
   - Use ε-transitions to “reset” or branch when multiple possibilities must be pursued simultaneously.

4. **Nondeterministic “Guess and Check”**  
   - An NFA can guess (via nondeterministic branching) that a certain position in the input might be the start of a pattern. If that guess fails later, the automaton can fall back (via ε) and continue from a different point.  
   - This approach often leads to a smaller, more intuitive NFA than a directly constructed DFA.

5. **Limitation of Branches**  
   - While we think of NFAs as splitting into many “parallel branches,” an actual implementation typically does a breadth-first or depth-first search over the state graph.  
   - In theoretical terms, those branches do not require extra memory—nondeterminism is a conceptual tool, not a literal duplication of computations.

---

