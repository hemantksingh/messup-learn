# Algorithms and Complexity

An algorithm's speed is the growth rate of its step count as the input grows. A problem's hardness is the class of the best possible algorithm for it: P if it can be solved in polynomial time, NP if an answer can be checked in polynomial time, NP-complete if it is the hardest kind of checkable problem. Whether solving is harder than checking, P vs NP, is unproven.

"Complexity" as a code metric (cyclomatic complexity) is a different idea, see [Code Quality](Code%20Quality.md).

## Asymptotic notation

Write the steps an algorithm takes as a function of input size, f(n). Only the growth rate matters. The notation compares f against a simpler function g:

* O(g): f grows no faster than g. Upper bound.
* Ω(g): f grows at least as fast as g. Lower bound.
* Θ(g): both. Tight bound.

These bound a *function*. Best, worst and average case decide *which* function you analyse: most steps over all inputs of size n, fewest, or the mean. "Binary search is Θ(log n) in the worst case" is a complete statement. The mistake to avoid: "best case is the lower bound, worst case is the upper bound". A best case of one step does not make Ω(1) the lower bound of the worst case.

The common growth classes, slowest growing first:

| Class | Example |
|---|---|
| Θ(1) constant | reading a stored length |
| Θ(log n) logarithmic | binary search, worst case |
| Θ(n) linear | counting characters one by one |
| Θ(n log n) | comparison sorting, such as merge sort |
| Θ(n²) polynomial | comparing every pair of items |
| Θ(2ⁿ) exponential | trying every subset of n items |
| Θ(n!) factorial | trying every ordering of n items |

O(2n) is not its own class: constants are dropped, so O(2n) = O(n).

## Worked examples

**Constant time.** Counting the characters of a string when the length is stored in a variable, `length = 20`. Reading a variable costs the same whatever the string holds: Θ(1).

**Linear.** Counting the characters by walking the string. Twice the string, twice the steps: Θ(n).

**Linear search.** Checking each element of an unsorted list in turn. Best case, the element is first: Θ(1). Worst case, last or absent: Θ(n). Average, about n/2 checks: still Θ(n).

**Binary search.** Finding an element in a sorted list. Compare with the middle element and discard the half it cannot be in. Each comparison halves the range. After ⌊log₂ n⌋ halvings one candidate is left and one more comparison decides, so the worst case is ⌊log₂ n⌋ + 1 comparisons: 4 for 8 elements, 5 for 16. Doubling the input adds one comparison. Best case Θ(1): the middle element is the one wanted. Worst case Θ(log n).

## Data structures and their costs

**Arrays** hold elements in contiguous memory. Index i is a fixed offset, so indexed lookup is Θ(1). A plain array is fixed size. A *dynamic array* (`List<T>`, `ArrayList`, `vector`) doubles when full: allocate a bigger block and copy. The copy is Θ(n) but happens once per n cheap appends, so each append is Θ(1) *amortised*.

**Linked lists** grow a node at a time and insert at a known position in Θ(1). There is no index arithmetic, so finding an element walks from the head: Θ(n).

**Hash tables** find an element in Θ(1) and still grow. A hash table is an array plus a hash function from key to index. Two keys will eventually share an index: a *collision*. *Chaining* gives each slot a linked list. *Open addressing*, such as linear probing, tries the next slot until a free one is found.

Cost depends on the load factor α = n/m, elements over slots. With a hash function that spreads keys evenly, a chained lookup costs about 1 + α steps and an unsuccessful probing lookup about 1/(1 − α). Both are expected Θ(1) while α stays below a constant. Worst case is Θ(n), when everything collides. Keeping α down is the dynamic-array trick: when the table fills, allocate a bigger one and rehash, amortised Θ(1) per insert. Open addressing needs α below 1, so it must resize; chaining tolerates more. 12 elements over 4 chains is a load factor of 3, an average chain length of 3, not "O(3)".

Hash tables keep no order, so no "next largest" and no range queries. **Binary search trees** do. Invariant: for every node, every key in its left subtree is smaller and every key in its right subtree is larger. Search is binary search down the tree, so the cost is the height. A balanced tree has height Θ(log n); self-balancing variants (red-black, AVL) keep it so. Insert sorted keys into a naive tree and it degenerates into a linked list of height n: Θ(n).

Note, scoped to .NET: the BCL `List<T>`, `Stack<T>` and `Queue<T>` are array-backed and carry array costs.

## P, NP and NP-complete

Complexity classes sort *decision problems* (yes or no answers) by the growth rate of the best algorithm that solves them, with n the size of the written-down instance.

**P**: decision problems solvable in time bounded by a polynomial in n, such as n, n² or 12n⁷ - 6n⁵. Sorting names and multiplying numbers run in polynomial time (strictly, their yes/no versions are in P). Schoolbook multiplication is Θ(n²) in the number of digits.

**NP**: decision problems whose "yes" answers can be *checked* in polynomial time, given a proposed solution. The name is *nondeterministic polynomial* (a machine that guesses the solution, then checks it), not "non-polynomial". P ⊆ NP, because solving is one way of checking. Any NP problem can be solved in exponential time by trying every candidate, so P ⊆ NP ⊆ EXPTIME.

Sudoku: checking that a filled grid has each digit once per row, column and box is fast. Finding the filling is the hard part. *Hard to solve, easy to check* is what puts a problem in NP. A fixed 9x9 board is a single instance, so growth rates say nothing about it; generalised n²xn² sudoku is NP-complete (Yato and Seta, 2003).

A **polynomial-time reduction** from A to B turns any instance of A into an instance of B with the same answer, in polynomial time. Solve B fast and you solve A fast, so B is at least as hard as A. A problem is **NP-hard** if every problem in NP reduces to it. It is **NP-complete** if it is NP-hard *and* in NP. NP-hard problems need not be in NP: the halting problem is NP-hard and not even decidable.

The Cook-Levin theorem (1971) gives the first one: boolean satisfiability, SAT, is NP-complete. Thousands more follow by reduction from SAT. So a polynomial algorithm for any one of them gives one for all of NP.

**P = NP?** asks whether a quick way to check an answer always means a quick way to find one. If P = NP, every NP-complete problem has a polynomial algorithm and cryptography built on hard-to-invert functions collapses (see [Cryptography Basics](../security/Cryptography%20Basics.md)). Most researchers expect P ≠ NP; that is a belief, not a theorem.

**EXPTIME**: problems solvable in time 2 to a polynomial in n. Generalised n x n chess is EXPTIME-complete (Fraenkel and Lichtenstein, 1981), so no polynomial program plays it perfectly. Ordinary 8x8 chess is a single instance; only its constant size makes it hard.

Two talks: [P vs. NP and the Computational Complexity Zoo](https://www.youtube.com/watch?v=YX40hbAHx3s) (hackerdashery) and [Why is P vs NP Important?](https://www.youtube.com/watch?v=9MvbNPQiEE8) (Siraj Raval).

## How to rederive this

* Count steps as f(n), drop constants and lower-order terms. O, Ω, Θ bound a function; best, worst, average pick the function.
* Halving each step gives log₂ n steps: binary search, and the height of a balanced tree.
* A Θ(n) operation once per n cheap ones is Θ(1) amortised: dynamic-array append, hash-table resize.
* P: solve in polynomial time. NP: check in polynomial time. Solving is checking (P ⊆ NP); trying every answer is exponential (NP ⊆ EXPTIME).
* NP-complete: in NP and everything in NP reduces to it. Cook-Levin gives SAT; reductions give the rest.

## Sources

* Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*.
* Sipser, *Introduction to the Theory of Computation*, ch. 7.
* Skiena, *The Algorithm Design Manual*.
* Yato and Seta, 2003 (sudoku). Fraenkel and Lichtenstein, 1981 (chess).
* CS50, [Hash Tables](https://www.youtube.com/watch?v=tjtFkT97Xmc) (video).
