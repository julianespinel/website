---
title: Solving a HackerRank problem using Haskell
date: 2018-09-22
categories: programming
tags: haskell, functional programming, hackerrank
---

{% extends 'blog/base.html' %}
{% load static %}
{% block content %}

# Solving a HackerRank problem using Haskell

I have been learning Haskell with this great book: [Learn You a Haskell for Great Good!](http://learnyouahaskell.com/)<br>
When I learn something new, I split the learning process in two parts:

1. Theoretical: typically by reading a book.
1. Practical: typically by creating a project or solving HackerRank exercises.

In this blog post I want to show how Haskell can be used to solve HackerRank problems. I will present my solution written in Haskell for the “Diagonal Difference” problem. Please see the problem statement here: [Diagonal Difference](https://www.hackerrank.com/challenges/diagonal-difference/problem)

I will show the solution in parts, explaining each part separately. By the end of the post I will show the solution as a whole. If you see something that could be done better I will greatly appreciate your feedback.

## Solution general description

The solution will be shown following a top-down approach, starting with the main function, which is the entry point of the program, and then explaining each function until we reach the complete solution.

The implementation of the main function is as follows:

```haskell
main = do
  number <- readLn :: IO Int
  matrix <- getIntSquareMatrix number
  let (antiDiagonal, mainDiagonal) = getDiagonals(matrix)
  let result = absDiagonalDifference antiDiagonal mainDiagonal
  print result
```

The main function presents a high level view of how we are going to solve the problem:

1. Read expected input from stdin: lines 25 and 26
1. Give us a data structure to work with: line 26
1. Perform logic to solve the problem: lines 27 and 28
1. Print result to standard output: line 29

Now let's analyse what each function does to complete the solution.

### getIntSquareMatrix

This is the implementation of `getIntSquareMatrix`:

```haskell
getIntSquareMatrix :: Int -> IO([[Int]])
getIntSquareMatrix rows = do
  lines <- replicateM rows getLine
  let intMatrix = (map . map) read $ map words lines
  return intMatrix
```

The function `getIntSquareMatrix` receives an `Int` as paramenter and returns a matrix of Int elements, inside an IO "wrapper" `IO([[Int]])`. Allow me to explain this function line by line:

Line 6 reads a line from stdin N times, where N is defined by the parameter `rows`, then it binds the result to `lines`.

What is the type of `lines`?

> `replicateM rows getLine` returns a type `IO([String])`
> -> Replace by type in line 6
> `lines <- IO([String])`
> -> Left arrow `<-` binds the `[String]` contained in the `IO` "wrapper" to lines
> Then `lines` is of type `[String]`

Line 7 applies some functions to `lines` and defines `intMatrix` of type `[[Int]]`.

Finally line 8 wraps the `intMatrix` into the `IO` "wrapper" so the function returns a value of type `IO([[Int]])`.

### getDiagonals

The implementation of the function `getDiagonals` is as follows:

```haskell
getDiagonals :: [[Int]] -> ([Int], [Int])
getDiagonals matrix =
  let size = length(matrix) - 1
      indices = [0..size]
      antiDiagonal = zipWith (!!) matrix indices
      mainDiagonal = zipWith (!!) matrix (reverse indices)
   in (antiDiagonal, mainDiagonal)
```

Given a matrix as parameter, this function returns a tuple with the anti diagonal and the main diagonal of the matrix. The anti diagonal goes from bottom left to top right. The main diagonal goes from top left to bottom right.

### absDiagonalDifference

This is the implementation of the function `absDiagonalDifference`:

```haskell
absDiagonalDifference :: [Int] -> [Int] -> Int
absDiagonalDifference diagonalOne diagonalTwo =
  let oneSum = foldr (+) 0 diagonalOne
      twoSum = foldr (+) 0 diagonalTwo
   in abs (oneSum - twoSum)
```

This function takes the two lists of Int elements `[Int]` as parameters. Each list represents one diagonal of the matrix. Then it sums the contents of each list. Finally it returns the absolute value of the difference between the sums.

## Complete solution

This is the complete solution of the problem. It contains the same functions we have explained in a single file.

```haskell
import Control.Monad(replicateM)
import Data.List.Split(splitOn)

getIntSquareMatrix :: Int -> IO([[Int]])
getIntSquareMatrix rows = do
  matrix <- replicateM rows getLine
  let intMatrix = (map . map) read $ map words matrix
  return intMatrix

getDiagonals :: [[Int]] -> ([Int], [Int])
getDiagonals matrix =
  let size = length(matrix) - 1
      indices = [0..size]
      antiDiagonal = zipWith (!!) matrix indices
      mainDiagonal = zipWith (!!) matrix (reverse indices)
   in (antiDiagonal, mainDiagonal)

absDiagonalDifference :: [Int] -> [Int] -> Int
absDiagonalDifference diagonalOne diagonalTwo =
  let oneSum = foldr (+) 0 diagonalOne
      twoSum = foldr (+) 0 diagonalTwo
   in abs (oneSum - twoSum)

main = do
  number <- readLn :: IO Int
  matrix <- getIntSquareMatrix number
  let (antiDiagonal, mainDiagonal) = getDiagonals(matrix)
  let result = absDiagonalDifference antiDiagonal mainDiagonal
  print result
```

## Final messages

* With this post I wanted to show that Haskell could be used to solve HackerRank problems and that in fact it is a great language for doing it!
* Why I did not use the word "Monad" in this post? I want this entry to be simple and easy to understand for Haskell newcomers.
* Please DO NOT copy and paste the solution of the problem, I uploaded it here for educational purposes only.

## Resources

* [do notation](https://en.wikibooks.org/wiki/Haskell/do_notation)
* [Equal VS Left arrow](https://stackoverflow.com/questions/28624408/equal-vs-left-arrow-symbols-in-haskell)
* [let VS where](https://wiki.haskell.org/Let_vs._Where)
* [Dot operator](https://stackoverflow.com/questions/631284/dot-operator-in-haskell-need-more-explanation)
* [Matrix diagonal and anti diagonal](https://en.wikipedia.org/wiki/Main_diagonal)
* [What does return do?](https://stackoverflow.com/a/15324633/2420718)

{% endblock %}