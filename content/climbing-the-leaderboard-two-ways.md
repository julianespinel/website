---
title: Climbing the leaderboard, two ways
date: 2021-10-23
category: programming
tags: algorithms, python
description: Solve 'Climbing the leaderboard' using two different implementations in Python. Show its difference in execution time using cProfile.
---

Over the years working as a software engineer, I have noted that
programming languages, frameworks and tools, rarely make a big
impact on skill level. On the other hand, I have seen that going back to
basics has helped me to see problems in a different way and create more
efficient solutions.

By "going back to basics" we are referring to the basics of
programming: algorithms and data structures. That's why in this post we
will show two solutions for the same problem.

We will profile both solutions to show the difference in execution time between
the two approaches. Why? We want to show the impact of having a solution with
lower growth rate when the input is large.

The problem we are going to solve is
[Climbing the Leaderboard](https://www.hackerrank.com/challenges/climbing-the-leaderboard/problem), and the two proposed solutions are:

| Solution | Complexity (Big O) |
|---|---|
| Brute force | `O(scores) * O(ranks log ranks)` |
| Linear | `O(scores) + O(ranks)` |

If you haven't read the problem statement please read it before
continuing. Now, let's get started!

## Brute force solution

The first implementation is brute force. This is what it does:

First, we remove the duplicates in a way that is not efficient for this
problem. Why? Since we know that `ranks` is a list is sorted in descending
order, we can remove the duplicates in a single pass: O(ranks).
This is something we will improve in the next implementation.

Next, we get the position of each score in the ranking. The way we do it
is not optimal because we insert each score by the end of ranks, then we sort
ranks, and finally we search for the score in the sorted ranks to get its
position in the ranking.

The time complexity of this solution is: `O(scores) * O(ranks log ranks)`

Here is the implementation:

```python
def remove_duplicates(ranks: list[int]) -> list[int]:
    '''
    Time complexity: O(n log n)
    '''
    ranks_set = set(ranks)
    return sorted(ranks_set, reverse=True)


def get_positions_per_score(ranks: list[int], scores: list[int]) -> list[int]:
    '''
    Time complexity: O(scores) * O(ranks log ranks)
    '''
    positions = []
    for score in scores:  # O(scores)
        # amortized O(1), why? see: https://stackoverflow.com/a/33045038/2420718
        ranks.append(score)
        ranks = sorted(ranks, reverse=True)  # O(ranks log ranks)
        position = ranks.index(score)  # O(ranks)
        positions.append(position)  # amortized O(1)

    return positions


def solve_problem(ranks: list[int], scores: list[int]) -> list[int]:
    ranks = remove_duplicates(ranks)  # O(ranks log ranks)
    positions = get_positions_per_score(ranks, scores)  # O(scores) * O(ranks log ranks)
    return positions
```

You can find the complete code [here](https://github.com/julianespinel/blog-code/blob/65410ca22d52c922a3a22d38f9360757c9d9f962/python-profiling/brute_force.py).

The following is the result of profiling this implementation with a test case
that gives us 200k ranks, and 100k scores.

```
   400005 function calls in 363.902 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.003    0.003  363.902  363.902 brute_force.py:29(solve_problem)
        1   41.344   41.344  363.866  363.866 brute_force.py:14(get_positions_per_score)
   100001  177.871    0.002  177.871    0.002 {built-in method builtins.sorted}
   100000  144.639    0.001  144.639    0.001 {method 'index' of 'list' objects}
   200000    0.034    0.000    0.034    0.000 {method 'append' of 'list' objects}
        1    0.010    0.010    0.033    0.033 brute_force.py:6(remove_duplicates)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

Most of the execution time was spent sorting and searching for the index
(position) of the given score in the `ranks` list. The algorithm produced a 
solution after 363.902 seconds, which is roughly 6.07 minutes.

## Linear solution

The second implementation uses two pointers to traverse each list only once.
How?

We are given two lists:

1. ranks: a list of the top scores ordered in descending order
1. scores: a list of player scores ordered in ascending order

If we revert the scores list, **then we have both lists sorted in descending order.**
In this way we can compare an element from scores against an element of ranks,
from the beginning to the end of each list. If the element from scores is `>=` 
than the element from ranks, then we have found the position for that score.
Otherwise we need to get the next element from ranks.

Finally, if the scores list was bigger than the ranks list, we need to add the
remaining score positions in our response.

The time complexity of this solution is: `O(scores) + O(ranks)`

This is how it is done:

```python
def remove_duplicates(ranks: list[int]) -> list[int]:
    '''
    Given a list sorted in descending order (ranks),
    remove the duplicates of the list.

    Time complexity: O(n)
    Why? See: https://stackoverflow.com/a/7961390/2420718
    '''
    return list(dict.fromkeys(ranks))


def get_positions_per_score(ranks: list[int], scores: list[int]) -> deque[int]:
    '''
    Return the position of each score in the ranks list
    using a zero-based index.

    ranks: list sorted in **descending** order
    scores: list sorted in **descending** order

    Time complexity: O(scores) + O(ranks)
    '''
    positions = deque()  # why a deque? to make all appends O(1)
    ranks_index = 0  # O(1)
    scores_index = 0  # O(1)

    scores_size = len(scores)  # O(1)
    ranks_size = len(ranks)  # O(1)

    # O(scores) + O(ranks)
    while (scores_index < scores_size) and (ranks_index < ranks_size):
        score = scores[scores_index]  # O(1)
        rank = ranks[ranks_index]  # O(1)
        if score >= rank:  # O(1)
            positions.append(ranks_index)  # O(1)
            scores_index += 1  # O(1)
        else:
            ranks_index += 1  # O(1)

    # add missing scores
    while scores_index < scores_size:  # O(scores) in the worst case
        positions.append(ranks_index)  # O(1)
        scores_index += 1  # O(1)

    positions.reverse()  # O(scores)
    return positions


def solve_problem(ranks: list[int], scores: list[int]) -> list[int]:
    ranks = remove_duplicates(ranks)  # O(ranks)
    scores.reverse()  # O(scores)
    positions = get_positions_per_score(ranks, scores)  # O(ranks) + O(scores)
    one_index_positions = list(map(lambda position: position + 1, positions))
    return one_index_positions
```

You can find the complete code [here](https://github.com/julianespinel/blog-code/blob/65410ca22d52c922a3a22d38f9360757c9d9f962/python-profiling/linear.py).

The following is the result of profiling this implementation with a test case
that gives us 200k ranks, and 100k scores. (The same test case we used to
profile the brute force implementation).

```
   200009 function calls in 0.065 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.008    0.008    0.065    0.065 linear.py:71(solve_problem)
        1    0.028    0.028    0.032    0.032 linear.py:35(get_positions_per_score)
        1    0.003    0.003    0.019    0.019 linear.py:24(remove_duplicates)
        1    0.017    0.017    0.017    0.017 {built-in method fromkeys}
   100000    0.006    0.000    0.006    0.000 linear.py:75(<lambda>)
   100000    0.004    0.000    0.004    0.000 {method 'append' of 'collections.deque' objects}
        1    0.000    0.000    0.000    0.000 {method 'reverse' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'reverse' of 'collections.deque' objects}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

Most of the execution time was spent removing duplicates (done once).
The algorithm produced a solution after 0.065 seconds.

## Conclusion

We know that we should strive to develop algorithms with lower growth rate in
both time and space (aka lower Big O complexity). In this post we want to show
the difference in runtime between two solutions for the same problem with
different time complexities.

How impactful is decreasing the time complexity if we compare the runtime
from one implementation to the other?

| Solution | Complexity (Big O) | Runtime (seconds) |
|---|---|---|
| Brute force | `O(scores) * O(ranks log ranks)` | 363.902 |
| Linear | `O(scores) + O(ranks)` | 0.065 |

The linear implementation is 5.5 thousand times faster for the given test case.