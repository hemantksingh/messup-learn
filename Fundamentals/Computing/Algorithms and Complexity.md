# Algorithms and Complexity

## Computational complexity: P, NP and NP-complete

P - Set of all problems that can be solved in polynomial time. Polynomial time means that the time measured as the number of steps (S) required to solve a problem is a polynomial function of the input size (n).

S = f(n).

Polynomials are functions involving n + 5 or 2n + 5 or n^2 or 12n^7 - 6n^5 i.e they can be computed in reasonably fast time, e.g multiplication and sorting a collection of names alphabetically. Multiplication of even exponential numbers can be performed quickly even on a phone.

NP - Set of all problems that can take exponential time to solve. e.g. 2^n as n increases the time required grows exponentially. Solution to a sudoku is an NP problem because as the number of grids increase on a sudoku grid it gets harder and harder for a computer to solve it in quick time.

P = NP
*Does being able to quickly verify the answer to a problem mean there is a quick way to solve it too ?*

For example figuring out a solution to sudoku takes time but verifying the correctness of a sudoku solution is relatively quicker *(Hard to solve, easy to check)*. Does that mean we should be able to find a solution to Sudoku quicker too? or is NP = P ? No body has been able to prove or disprove this.

For playing absolutely perfect chess there is no fast program. It falls in the EXP set of problems.

NP Complete Problems - Set of problems that could be reduced to solving a single task. Solving the really hard part would result in solving all the problems, as they are connected to the same NP Complete level traversal.

[P vs NP](https://www.youtube.com/watch?v=YX40hbAHx3s&nohtml5=False)

https://www.youtube.com/watch?v=9MvbNPQiEE8&nohtml5=False

## Asymptotic notation

Measuring the complexity of a program (Big Oh notation). It is a means of analyzing how fast a program's run-time grows asymptotically. i.e. as the size of the input to a program increases towards infinity how does the time to run the program grow?

Best case performance of an algorithm is called the **lower bound** and the worst case performance called the **upper bound**. Algorithms usually fall into the following performance classes:

* constant-time O(1)
* logarithmic O(log n) - slow growth (opposite of exponential)
* linear O(n) - a linear function is a polynomial of degree one or less (with no exponents), including the zero polynomial. It follows a straight line if plotted on a graph
* polynomial O (2n) or O(n`2` )
* exponential O (e `n` )
* factorial 0(n!)

### Constant-time

Eg. counting the number of characters of a string if the length is stored in a variable. `length = 20`

Finding the length of the string does not depend on how long the string is. Checking the value of a variable is considered as an asymptotically constant time operation or O(1)

The upper and lower bound of the algorithm will be the same regardless of the size of the input. **Omega**(1)

Best case constant time =  Worst case constant time = O(1).

Since the best and worst case are the same this can be said to run in **Theta**(1).


### Linear
Eg. counting  the number of characters in a string. As the string length grows the time taken to count the number of characters will grow linearly. i.e the program run-time is proportional to the number of inputs. Denoted as O(n).

Lower bound - Omega(1) The element being searched is the first one in the list. Upper bound - O(n) The element being searched is last in the list.


### Binary search

Finding an element in an already sorted list using [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm). A list with 8 elements takes 3 operations to find a specific element.
A list of 16 elements takes 4 operations to find a specific element. Doubling the input size only increases the time by 1.

* log 1 = 0
* log 2 = 1
* log 4 = 2
* log 8 = 3

log n denoted as O(log n).

Lower bound - the element to find is located in the middle of the list and happens to be the first one being interrogated. No matter what the size of the input the element in this case will be found in 1 operation. The asymptotic complexity is denoted by Omega(1).
Upper bound - The asymptomatic complexity is denoted as explained above is denoted by O(log n).

## Data Structures

**Arrays** - store elements in contiguous memory and have a fixed size. They provide random access to elements with indexes. Due to fixed size arrays are unable to grow as it is difficult to find adjacent contiguous memory.

**Linked lists** - can grow dynamically over time. Finding an element is O(n) as the entire list needs to be traversed to search a particular element.

O(n) isn't great in terms of efficiency. Can we do better than O(n)and while still allowing our data structure to grow over time? Hash tables is the answer.

**[Hash Tables](https://www.youtube.com/watch?v=tjtFkT97Xmc&ebc=ANyPxKoC9kkoTtcCSl4Kf133win8mxqWdnEZ_yfeH6tf1kE1htRp-aGiyYd7l0gGmPz93k5wIWRLKqUI6mWME8A6uVX224w9ng)** - allow the list to grow dynamically with better performance while searching an element. Speedy insertion, deletion and lookup.

A hash table is an array with a hash function. The result of the hash function is used to determine which index an element is stored in the array. With the growth of the hash table the hash function is bound to produce the same result for 2 different values. This results in a **collision**. There are 2 approaches that can be used for resolving collisions:

* Linear probing - O(n) Finds the next available free index in the array to store the element. This could end up in traversing the entire array in worst case scenario.
* Chaining - O(n/k) where k is the size of the hash table. Chaining involves using a linked list for each array index, with the array index storing a pointer to the head of the linked list.

For 12 elements spread over 4 linked lists with each linked list containing 3 elements. Complexity = O(No of inputs/Size of the hash table or No of linked lists) = O(12/4) = O(3).

**Trees and Graphs** - The List, Stack, Queue, Hashtable all use an underlying array as the means by which their data is stored. This means that, under the covers, these data structures are bound by the limitations imposed by an array. An array is stored linearly in memory, requires explicit resizing when the array's capacity is reached, and suffers from linear searching time.

*Binary Search Tree* is a collection of nodes and edges that imposes certain rules on how the nodes are arranged.
