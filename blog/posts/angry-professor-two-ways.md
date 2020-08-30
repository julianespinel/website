---
title: Angry professor, two ways
date: 2020-08-30
categories: programming
tags: algorithms
      java
      haskell
---

# Angry Professor, two ways

2020-08-30

In this entry we are going to show how to solve the same problem from HackerRank using two different programming 
languages: Java and Haskell. The goal of the post **is not to** argue about which programming language is better.
I just want to show the differences in the implementation of the same solution.

The problem we are going to solve is: [Angry professor](https://www.hackerrank.com/challenges/angry-professor/problem).
It is a very simple problem that will allow us to illustrate the implementation differences without making this entry
too long. (Please read the problem description by clicking the link).

First, I will describe the basic algorithm I used to solve this problem, then I will show each step of the algorithm
implemented in both Java and Haskell. By the end of the post I will share the links to the complete code of both
implementations. Finally I will provide the Big O complexity analysis of the solution.

## Algorithm description

The algorithm that I used to solve this problem is as follows. For each case:

1. Count the number of students who arrived early.
1. Compare the number of students who arrived early against the cancellation threshold.
    1. If the number students who arrived early is `>=` cancellation threshold -> print `NO` (the class is not cancelled)
    1. Otherwise -> print `YES` (the class is cancelled)

## Implementation

### Data structures

In both implementations I decided to create classes/data structures that allowed me to represent a test case (`Case`) and
its response (`Answer`). This helped me to encapsulate related information and enforce type safety.

Let's see how they look in Java:

```java
enum Answer {
      YES, NO
}

private class Case {

      private final int totalStudents;
      private final int cancellationThreshold;
      private final int[] arrivals;

      public Case(int totalStudents, int cancellationThreshold, int[] arrivals) {
            this.totalStudents = totalStudents;
            this.cancellationThreshold = cancellationThreshold;
            this.arrivals = arrivals;
      }
      ...
}
```

This is the Haskell counterpart:

```haskell
data Answer = YES | NO deriving (Show)

data Case = Case { totalStudents         :: Int
                 , cancellationThreshold :: Int
                 , arrivals              :: [Int] }
```

Why did we define a type to represent the answer (YES/NO)? We could have used plain strings to represent them, right?
Sure! But that means that we could also return any other random string as answer, for example: `"Hello world"`. By
defining a type to represent the answer we are making sure that the compiler will complain if we return something
different from `YES` or `NO`.

### Validation

Although it is not required in this type of programming problems, I like to validate the input in case there is an
invalid case. Let's see how this simple validation is implemented in Java:

```java
private void validate() {
      if (totalStudents != arrivals.length) {
            String errorMessage = String.format("Total students expected to be %s, but is %s",
                  totalStudents, arrivals.length);
            throw new AssertionError(errorMessage); // Break the program on erroneous input
      }
}
```

The corresponding Haskell code is:

```haskell
validate :: Case -> Case
validate (Case students threshold arrivals)
  | students == length arrivals = Case students threshold arrivals
  | otherwise = error errorMessage -- Break the program on erroneous input
  where errorMessage = printf "Total students expected to be %s, but is %s" (show students) (show $ length arrivals)
```

### Count and compare

To solve the problem we need to count how many students arrived on time and compare that number against the cancellation
threshold defined by our angry professor. If the amount of students who arrived on time is greater or equal than the
cancellation threshold then the class will continue, otherwise it will be cancelled.

Let's see how we can implement this in Java:

```java
private int countEarly() {
      int studentsOnTime = 0;
      for (int arrival : arrivals) {
            studentsOnTime += (arrival <= 0) ? 1 : 0;
      }
      return studentsOnTime;
}

private Answer isClassCancelled() {
      int studentsOnTime = countEarly();
      return (studentsOnTime >= cancellationThreshold) ? Answer.NO : Answer.YES;
}

public Answer solve() {
      validate();
      return isClassCancelled();
}
```

As you can see, the method `solve` verifies if the case is valid and then checks if the class is cancelled or not.
The same logic written in Haskell is as follows:

```haskell
countEarly :: [Int] -> Int
countEarly arrivals = length $ filter (<= 0) arrivals

isClassCancelled :: Case -> Answer
isClassCancelled (Case _ cancellationThreshold arrivals)
  | countEarly arrivals >= cancellationThreshold = NO
  | otherwise = YES

solve :: Case -> Answer
solve = isClassCancelled . validate
```

Note that the methods in the Java version do not receive parameters. This is because those are instance methods,
defined within the class `Case`, therefore they can access the fields of the object.

On the other hand, all the functions in the Haskell implementation receive arguments. This happens because the types we
defined in Haskell does not have any logic themselves. In this case, the types we defined in Haskell are placeholders
used to group related data and give it semantic value.

You can find the complete code of both implementations here: [Java](https://github.com/julianespinel/training/blob/master/hackerrank/AngryProfessor.java), [Haskell](https://github.com/julianespinel/training/blob/master/hackerrank/AngryProfessor.hs).

## Big O complexity analysis

We will use the Haskell version to perform the complexity analysis. I have omitted the code fragments required to read
the input and write the output, those lines of code are usually not included in the complexity analysis.

Let's review the runtime and space complexity of each function that is part of the solution of the problem.

### validate

```haskell
validate :: Case -> Case
validate (Case students threshold arrivals)
  | students == length arrivals = Case students threshold arrivals
  | otherwise = error errorMessage -- Break the program on erroneous input
  where errorMessage = printf "Total students expected to be %s, but is %s" (show students) (show $ length arrivals)
```

Runtime: O(arrivals)

* `length arrivals` -> O(arrivals), why? Please see the explanation on [StackOverflow](https://stackoverflow.com/a/46718612/2420718).
* Compare two numbers: `students == length arrivals` -> O(1)
* `error errorMessage` -> O(1)

Space: O(arrivals)

* The space we use is given by the case we receive as argument `aCase`.
* The `Case` type holds two numbers and one list, therefore the space complexity is defined as: max(O(1), O(1), O(arrivals))

### countEarly

```haskell
countEarly :: [Int] -> Int
countEarly arrivals = length $ filter (<= 0) arrivals
```

Runtime: O(arrivals)

* `filter (<= 0) arrivals` -> O(arrivals)
* `length` of the list returned by `filter` -> O(arrivals)
    * Why? Because in the worst case scenario the filter returns the same list.
* Therefore: 2 * O(arrivals) -> constants are not considered in complexity analysis -> O(arrivals)

Space: O(arrivals)

* Potentially we need to hold arrivals twice: 1) the original argument, 2) the result of `filter`.
    * Therefore: 2 * O(arrivals) -> constants are not considered in complexity analysis -> O(arrivals)

### isClassCancelled

```haskell
isClassCancelled :: Case -> Answer
isClassCancelled (Case _ cancellationThreshold arrivals)
  | countEarly arrivals >= cancellationThreshold = NO
  | otherwise = YES
```

Runtime: O(arrivals)

* `countEarly arrivals` runtime complexity: O(arrivals)
* Compare two numbers: `countEarly arrivals >= cancellationThreshold` -> O(1)
* Therefore: max(O(arrivals), O(1)) -> O(arrivals)

Space: O(arrivals)

* The space we use is given by the case we receive as argument `Case`.
* As we already calculated it, the space required to hold a `Case` is: O(arrivals)

### solve

```haskell
solve :: Case -> Answer
solve = isClassCancelled . validate
```

Runtime: O(arrivals)

* `validate` -> O(arrivals)
* `isClassCancelled` -> O(arrivals)
* Therefore: 2 * O(arrivals) -> constants are not considered in complexity analysis -> O(arrivals)

Space: O(arrivals)

* `validate` -> O(arrivals)
* `isClassCancelled` -> O(arrivals)
* Therefore: 2 * O(arrivals) -> constants are not considered in complexity analysis -> O(arrivals)

### Result

In conclusion, in order to solve a single test case of the Angry Professor problem we need:

* Runtime: O(arrivals), linear time
* Space: O(arrivals), linear space
