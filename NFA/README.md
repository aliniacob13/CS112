# Lab.2 - Deterministic finite automaton (DFA)  
## Table of Contents

1. [DFAs, Informally](#dfas-informally)  
2. [Designing DFAs](#designing-dfas)  
3. [Example: Even Number of 1’s](#example-even-number-of-1s)  
4. [Additional Design Considerations](#additional-design-considerations)  

---

## DFAs, Informally

- **Alphabet (Σ):**  
  A DFA operates over a finite set of symbols called the alphabet, denoted Σ. For instance, Σ might be `{0, 1}` for a binary automaton or `{a, b, c}` for a ternary system. Each symbol in Σ must be accounted for in every state transition.

- **Deterministic Transitions:**  
  In a DFA, each state has exactly one outgoing transition for every symbol in Σ. This property ensures that for a given state and input symbol, the next state is uniquely determined. The absence of nondeterminism means there is no ambiguity in the transition function.

- **Start State:**  
  A DFA possesses a single start state, often referred to as the initial state. Before reading any input, the automaton resides in this start state. It is typically denoted by an arrow pointing to the state without originating from another state.

- **Accepting (Final) States:**  
  One or more states may be designated as accepting (final) states. If, after processing an entire input string, the DFA ends in an accepting state, the string is considered accepted. Accepting states are usually indicated by drawing a double circle around the state.

---

## Designing DFAs

When constructing a DFA, it is important to remember that the only memory available to the machine is its current state. The following principles should guide the design process:

1. **State Semantics:**  
   - Each state should correspond to a specific piece of information that the automaton must retain about the portion of the input that has been processed.  
   - By associating each state with a well‐defined memory interpretation, it becomes easier to verify correctness and completeness.

2. **Transitions as Updates:**  
   - A transition represents an update to the internal “snapshot” of what has been read so far.  
   - Upon reading a symbol from Σ, the DFA moves to a state whose semantics reflect the new information, given the previous state and the input symbol.

3. **Completeness and Determinism:**  
   - Verify that every state has exactly one outgoing edge labeled with each symbol in Σ.  
   - If any transition is missing, the automaton is not well‐defined. On the other hand, multiple transitions on the same symbol from a single state would introduce nondeterminism.

4. **Finite Memory Constraint:**  
   - Since a DFA has only finitely many states, it can remember only a finite number of distinct “cases.”  
   - Identify exactly which distinctions are essential to the language to be recognized. Unnecessary distinctions will lead to an overinflated state set.

---

## Example: Even Number of 1’s

**Objective:** Construct a DFA that accepts all binary strings containing an even number of `1` symbols.

1. **Relevant Information to Keep:**  
   - The parity (even or odd) of the number of `1’s encountered so far.

2. **State Definitions:**  
   - **q_even:** Indicates that an even number of `1’s has been seen (including zero).  
   - **q_odd:** Indicates that an odd number of `1’s has been seen.  

3. **Transition Function (Σ = `{0, 1}`):**  
   - From **q_even:**  
     - On input `0`, remain in **q_even** (the count of `1’s` does not change).  
     - On input `1`, transition to **q_odd** (the count of `1’s` becomes odd).  
   - From **q_odd:**  
     - On input `0`, remain in **q_odd** (the count of `1’s` does not change).  
     - On input `1`, transition to **q_even** (the count of `1’s` becomes even).  

4. **Start and Accepting States:**  
   - **Start state:** `q_even` (since zero `1’s` is an even count).  
   - **Accepting state:** `q_even` (strings with an even number of `1’s` should be accepted).

```text
        ┌───────────┐       1        ┌──────────┐
   ────▶│  q_even   │──────────────▶│  q_odd   │
        │(start,   )│◀──────────────│ (       )│
        │ accepting)│    1         └──────────┘
        └───────────┘                ▲   │
          ▲      │                   │   │
          │      └─0 (loop)          │   └─0 (loop)
          └──────────────────────────┘
