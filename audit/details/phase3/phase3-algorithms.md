# Phase 3 report: fundamentals/computing/Algorithms and Complexity.md

File rewritten in place (not committed): `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/computing/Algorithms and Complexity.md`

Final length after the owner's tighten pass: 1,400 by `wc -w` (which counts table pipes and symbols such as Θ(1) as words); 1,299 alphabetic words. Target was 1,100 to 1,400, never over. Checks run: one H1, no em or en dashes, no code fences, no `0(`, no `O(2n)` presented as a class, no connective filler words, no `> Own view:` text, British spelling, both relative links resolve, no question marks except the owner's own "P = NP?" label and a video title. Other modified files in `git status` belong to other rewrite agents and were not touched.

## (a) The question the page now answers

How do I reason about how fast an algorithm is, and what does it mean for a problem to be "hard"? The first paragraph answers both in plain words: speed is the growth rate of the step count; hardness is the class (P, NP, NP-complete, EXPTIME) of the best possible algorithm; P vs NP is unproven.

## (b) Kept from the original

- The stored-length `length = 20` constant-time example.
- The count-characters-one-by-one linear example.
- The linear-search "element is first / element is last" cases, now stated as a separate algorithm from counting.
- Binary search on a sorted list with the 8-element / 16-element "doubling adds one comparison" observation (numbers corrected, see (d)).
- The 12 elements over 4 chains hash-table example, restated as load factor 3 / average chain length 3.
- The array, linked list, hash table progression ("find an element in Θ(1) and still grow").
- The collision definition and the two resolution strategies (linear probing, chaining).
- The sudoku "hard to solve, easy to check" framing and the owner's P = NP question ("does a quick way to check an answer mean a quick way to find one?").
- The chess EXPTIME example (qualified, see (d)).
- The owner's polynomial examples, trimmed to n, n² and 12n⁷ - 6n⁵; sorting names and multiplying numbers as polynomial-time examples (worded so that only their yes/no versions are said to be "in P", since P is defined over decision problems).
- The two P vs NP video links, titled and stripped of `&nohtml5=False`: "P vs. NP and the Computational Complexity Zoo" (hackerdashery) and "Why is P vs NP Important?" (Siraj Raval). Titles verified via YouTube oembed. The CS50 "Hash Tables" video was also kept as a titled link under Sources, stripped of its `&ebc=` tracking token; see (f).
- The .NET remark that List, Stack, Queue are array-backed, now one sentence scoped to the .NET BCL, with the Hashtable claim dropped.

## (c) Dropped and why

From the audit's WRONG/BROKEN findings:

- "Best case is the lower bound, worst case is the upper bound" and every "Omega(1) lower bound" remark about best cases (audit L5, L20). Replaced by the bounds-vs-cases explanation.
- The growth-class list with `O(2n)` as polynomial, `O(e n)`, `0(n!)` and broken exponent markup (audit L10-12). Replaced by a table with one example per class and a sentence saying O(2n) = O(n).
- "8 elements takes 3 operations, 16 takes 4" (audit L35-36, off by one). Now ⌊log₂ n⌋ + 1: 4 and 5.
- "Arrays are unable to grow" (audit L50). Replaced by dynamic arrays with amortised doubling.
- "Linear probing O(n)" vs "Chaining O(n/k)" as different classes, and "O(12/4) = O(3)" (audit L60-63). Replaced by the load-factor analysis.
- "List, Stack, Queue, Hashtable all use an underlying array ... linear searching time" as a general truth (audit L65). Scoped to .NET; the searching-time clause dropped.
- The one-sentence "Trees and Graphs" stub (audit L65-67). BST completed; graphs not added.
- "NP: problems that can take exponential time to solve" (audit L9). Replaced by the verifier definition.
- "Sudoku is NP because it gets harder as grids increase" (audit L9). Replaced.
- "Multiplication of even exponential numbers can be performed quickly" (audit L7). Replaced by schoolbook multiplication being Θ(n²) in digits.
- "Perfect chess falls in EXP" for the 8x8 board (audit L16). Qualified to generalised n x n chess.
- "NP Complete: problems reduced to a single task ... NP Complete level traversal" (audit L18). Replaced by reductions, NP-hard, NP-complete, Cook-Levin.
- The `# P = NP` H1 and bare-line question structure (audit L1, L11-14).
- The "log 1 = 0 ... log 8 = 3" list; the halving derivation covers it.

Cut again in the owner's tighten pass (were in my first draft, not in the outline):

- The P ≠ EXPTIME / time hierarchy remark ("at least one inclusion is strict").
- The claim that no comparison sort beats n log n in the worst case (table now just says "comparison sorting, such as merge sort").
- "Inserting in the middle of an array is Θ(n)."
- "Chaining tolerates α above 1" shortened to "chaining tolerates more".
- The "phone multiplies huge numbers instantly" aside.
- Chapter-level detail in Sources (now book titles only, plus Sipser ch. 7).

## (d) Added, with sources for non-obvious claims

- O, Ω, Θ as bounds on a function; best/worst/average as choice of function. CLRS ch. 3.
- Binary search worst case ⌊log₂ n⌋ + 1 comparisons. Standard; matches the audit's suggested fix.
- Dynamic array doubling gives amortised Θ(1) append. CLRS amortised analysis (table doubling); Skiena ch. 3.
- Hash table cost: chaining about 1 + α per lookup; open addressing about 1/(1 − α) probes for an unsuccessful lookup under uniform hashing; both expected Θ(1) with bounded α, Θ(n) worst case; open addressing needs α < 1. CLRS 3rd ed. ch. 11 (Theorems 11.1, 11.2, 11.6). Note: the brief said "expected O(1+α) for both"; CLRS gives 1/(1 − α) for open addressing, so the page states the honest formulas and keeps the brief's intent (same class, both governed by α). Resizing framed as the same amortised-doubling argument as dynamic arrays.
- BST invariant, search cost = height, Θ(log n) balanced (red-black, AVL named), Θ(n) degenerate; BSTs give ordered operations that hash tables lack. CLRS ch. 12 and 13.
- P and NP as classes of decision problems; NP = nondeterministic polynomial; verifier definition; P ⊆ NP ⊆ EXPTIME. Sipser ch. 7.
- Polynomial-time reduction, NP-hard, NP-complete definitions; the halting problem as NP-hard but not in NP (undecidable). Sipser ch. 4 and 7.
- Cook-Levin theorem (1971): SAT is NP-complete. Sipser ch. 7; CLRS ch. 34.
- Generalised n²xn² sudoku is NP-complete: Yato and Seta, 2003. Generalised n x n chess is EXPTIME-complete: Fraenkel and Lichtenstein, 1981 (both cited in the audit's suggested fixes).
- Fixed-size boards (9x9 sudoku, 8x8 chess) are single instances, so asymptotic classes do not apply. Follows from the definitions.
- If P = NP, cryptography built on hard-to-invert functions collapses (one-way functions exist only if P ≠ NP). Linked to `../security/Cryptography%20Basics.md`.
- "Most researchers expect P ≠ NP" stated as a belief, not a theorem.
- Disambiguation sentence pointing to `Code%20Quality.md` for cyclomatic complexity.
- No `> Own view:` blocks: the owner wrote no opinion here and none was invented.

## (e) Diagrams Phase 5 should draw

The original had no images and none were added. Two would earn their place:

1. `growth-rates.drawio.svg`: steps against n for the seven growth classes on one chart (1, log n, n, n log n, n², 2ⁿ, n!), showing how quickly the last two leave the page. Embed under "Asymptotic notation".
2. `complexity-classes.drawio.svg`: nested regions P inside NP inside EXPTIME; NP-complete as the outer ring of NP; NP-hard extending outside NP (halting problem there); SAT and generalised sudoku on the NP-complete ring; generalised chess in EXPTIME. Draw the P/NP boundary dashed because it is unknown whether it is strict. Embed under "P, NP and NP-complete".

## (f) Open questions for the owner

1. The brief said keep "the two video links". The CS50 "Hash Tables" video was also kept, titled, under Sources. Drop it if three is too many.
2. The page is at the 1,400 ceiling by `wc` (1,300 real words). To reach the low end of the range the cheapest further cuts are the .NET note (one sentence), the halting-problem sentence, and the "Two talks" line if the videos move to Sources.
3. No graphs section. The old "Trees and Graphs" heading promised graphs; the outline did not ask for them. About 60 words (adjacency list vs matrix, BFS/DFS Θ(V + E)) would cover it if wanted.
4. The .NET note (`List<T>`, `Stack<T>`, `Queue<T>` array-backed) is true of the BCL to my knowledge but not verified against current .NET source. Low stakes; drop if .NET specifics no longer matter.
5. Skiena is in Sources as the brief asked, but the page leans on CLRS and Sipser. Remove if only sources actually used should be listed.
