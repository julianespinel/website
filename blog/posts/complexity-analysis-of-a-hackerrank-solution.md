---
title: Complexity analysis of a HackerRank solution
date: 2018-10-06
categories: programming
tags: java, hackerrank
---

{% extends 'blog/base.html' %}
{% load static %}
{% block content %}

# Complexity analysis of a HackerRank solution

**TL;DR (update 2)**

This blog post is wrong. But I have decided to keep it online because making mistakes is an important part of the learning process. Additionally this blog post will stay here because in Latin America (the region I was born) mistakes are not welcomed and are seen as failure instead of a source of learning and progress. I do not agree with that point of view, so as a form of protest and as a way to remind me what I learned from this, and how I did it, this post will remain public on the Internet.

Why was this post wrong?

Because I tried to make asymptotic analysis of a problem with a fixed input, and according to the book Introduction to algorithms that does not make sense:

> When we look at input sizes large enough to make only the order of growth of the running time relevant, we are studying the asymptotic efficiency of algorithms. That is, we are concerned with how the running time of an algorithm increases with the size of the input in the limit, as the size of the input increases without bound. Usually, an algorithm that is asymptotically more efficient will be the best choice for all but very small inputs.

“3 Growth of Functions.” Introduction to Algorithms, by Thomas H. Cormen, MIT Press, 2009.

In short, asymptotic analysis of a problem with a fixed input can be simplified as O(1). For a longer explanation please see the [amazing feedback](https://www.reddit.com/r/programming/comments/9lxqt9/complexity_analysis_of_a_hackerrank_solution/) some redditors gave me about this post.
___

Recently I have been solving HackerRank problems. After clearing some exercises categorized as easy I decided to move forward and try a medium difficulty problem. That’s when I found an exercise called “Forming a Magic Square”. Here is its description: [Forming a Magic Square](https://www.hackerrank.com/challenges/magic-square-forming/problem).

In this post, I want to show a solution to this problem and perform a basic complexity analysis of the proposed solution. By the end of this post, I will enumerate some common pitfalls to avoid and what to take into account when solving this kind of problems.

Please read the problem statement (click the highlighted text above) before continue reading.

## Solution: structure and implementation

The basic algorithm I imagined was divided into three main parts:

1. Read the given 3 x 3 matrix from stdin
1. Calculate the minimum cost to convert the given matrix into a magic square
1. Write the minimum cost to stdout

Let’s solve each part independently.

### Read the given 3 x 3 matrix from stdin

The most intuitive way to read a matrix from stdin is row by row, element by element:

```java
private static int[][] readNumbers(int lines, BufferedReader reader) throws IOException {
    int[][] matrix = new int[lines][lines];
    for (int i = 0; i < lines; i++) {
        String line = reader.readLine();
        String[] row = line.split(SPACE);
        int[] numbers = new int[lines];
        for (int j = 0; j < row.length; j++) {
            int number = Integer.parseInt(row[j]);
            numbers[j] = number;
        }
        matrix[i] = numbers;
    }
    return matrix;
}
```

~~This way of reading the expected 3 x 3 matrix from stdin has a major problem: its complexity is `O(n^2)` because we have a nested for loop.~~

Can we decrease its time complexity?

We now we are given a 3 x 3 matrix, but it is not mandatory for us to work with a matrix in memory. We could read the given matrix into an array and then use the array for the rest of the solution.

Here is how it is done:

```java
private static int[] readNumbers(int lines, BufferedReader reader) throws IOException {
    String line = "";
    for (int i = 0; i < lines; i++) {
        line += " " + reader.readLine();
    }

    String[] stringNumbers = line.trim().split(SPACE);

    int[] numbers = new int[lines * lines];
    for (int i = 0; i < stringNumbers.length; i++) {
        String stringNumber = stringNumbers[i];
        int number = Integer.parseInt(stringNumber);
        numbers[i] = number;
    }
    return numbers;
}
```

~~This way we perform two for loops, but they are not nested, so the complexity of reading the input of the problem is `O(n)`.~~

**Update 1**

As some friends pointed out, the complexity of reading the matrix from stdin is always the same. Using nested for loops (first approach) or two independent for loops (second approach), we always read 9 elements because the input of the program is a 3 x 3 matrix. So the complexity of reading the matrix could be noted as `O(9)` which solves to `O(1)`.

For the rest of the post we will work assuming the second approach, so the given matrix is contained in a single dimension array.

### Calculate the minimum cost to convert the given matrix into a magic square

Now we have the input matrix in memory represented as an array. How can we transform that array into a 3 x 3 magic square at a minimum cost?

Reading on the internet I found there are only 8 magic squares of dimension 3 x 3. With this information the problem is simple to solve if we perform these steps:

1. Know the 8 magic squares beforehand
1. Compare the given input against each of the 8 valid magic squares to get 8 costs
1. Get the minimum cost from the 8 comparisons

How can we do those three steps in `O(n)` complexity? The following diagram will explain how.

![Forming magic squares](blog/forming-magic-square.png)

We can compare the array representing the matrix given as input, against all 8 magic squares using a single for loop. Here is the implementation:

```java
private static final int ELEMENTS_IN_MAGIC_SQUARE = 9;

private static final int NUMBER_OF_MAGIC_SQUARES = 8;

private static List getMinCostLinear(int[] magicSquares, int[] flatMatrix) {
    List costs = new ArrayList<>();
    int cost = 0;
    assert magicSquares.length == flatMatrix.length * NUMBER_OF_MAGIC_SQUARES;
    for (int i = 0; i < magicSquares.length; i++) {
        int flatMatrixIndex = i % ELEMENTS_IN_MAGIC_SQUARE;
        if (i > 0 && flatMatrixIndex == 0) {
            costs.add(cost);
            cost = 0;
        }
        int elementOne = magicSquares[i];
        int elementTwo = flatMatrix[flatMatrixIndex];
        cost += Math.abs(elementOne - elementTwo);
    }
    costs.add(cost);
    return costs;
}
```

As the code shows, we used only one for loop to compare the input matrix against all possible 3 x 3 magic squares. So the complexity of the previous code fragment is O(n).

By this point, we have a list of costs. That list represents the cost to transform the matrix given as input into each possible magic squares. Now, all we have to do is to get the minimum element (cost) in the list:

```java
private static final int[] MAGIC_SQUARES_LINEAR = new int[]{
        8, 1, 6, 3, 5, 7, 4, 9, 2,
        6, 1, 8, 7, 5, 3, 2, 9, 4,
        4, 9, 2, 3, 5, 7, 8, 1, 6,
        2, 9, 4, 7, 5, 3, 6, 1, 8,
        8, 3, 4, 1, 5, 9, 6, 7, 2,
        4, 3, 8, 9, 5, 1, 2, 7, 6,
        6, 7, 2, 1, 5, 9, 8, 3, 4,
        2, 7, 6, 9, 5, 1, 4, 3, 8
};

private static int convertToMagicSquareAtMinCost(int[] flatMatrix) {
    // Call method to get a list of costs.
    List costs = getMinCostLinear(MAGIC_SQUARES_LINEAR, flatMatrix);
    // Get min cost from list of costs.
    return Collections.min(costs);
}
```
The complexity of the call `Collections.min(costs);` is also `O(n)`.

### Write the minimum cost to stdout

Finally we have to write the minimum cost to the stdout. We can do that by calling: `System.out.println(minCost);`. The print instruction complexity is `O(1)`.

## Solution: code

The complete solution has documentation for each method and constant. Please take a look [here](https://github.com/julianespinel/training/blob/6ba199c5fa4c0a2d14874d2baf4669f6575b6c0a/hackerrank/FormingAMagicSquare.java).

## Complexity analysis

We have seen what is the time complexity of the functions explained up until this point. As a general rule, the time complexity of a program is the maximum time complexity among all the instructions of the program.

Let's see the main function of our solution and find out which of its statements has the maximum time complexity:

```java
public static void main(String[] args) throws IOException {
    // Open a BufferedReader -> O(1)
    try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
        int[] flatMatrix = readNumbers(ROWS, reader); // -> O(1)
        int minCost = convertToMagicSquareAtMinCost(flatMatrix); // -> O(n)
        System.out.println(minCost); -> // O(1)
    }
}
```

Therefore the time complexity of our solution is:

```
max(O(1), O(1), O(n), O(1)) = O(n)
```

## Conclusion

We humans, tend to model problems as they are given to us. For example, if the problem statement talks about a matrix, the natural thing to do is model the given matrix as a two-dimension array in memory. But when thinking about the time complexity of an algorithm, it is worth trying different data structures to model the problem. This might be key to produce more efficient solutions.

As I was writing this post, I realized that explaining the proposed solution was not trivial to me. Not because the solution was complex, it was because I lack experience writing about code using other tools than code itself. This also reminded me about a [tweet from a former boss](https://twitter.com/ykiriki/status/1037388762798415872). Which takes me to the second conclusion of this post:

It is critical to document and explain our solutions as clear as possible. In programming exercises such as those proposed in HackerRank this might not seem important, but it is, and it is critical in our daily job. Ultimately programming is not only about writing correct programs with a decent algorithm complexity, programming is also about communicating our ideas and solutions to our fellow developers.

## References

Magic squares

* [How Many 3×3 Magic Squares Are There? Sunday Puzzle](https://mindyourdecisions.com/blog/2015/11/08/how-many-3x3-magic-squares-are-there-sunday-puzzle/)

Big O notation

* [A beginner's guide to Big O notation](https://rob-bell.net/2009/06/a-beginners-guide-to-big-o-notation/)
* [Big O notation](http://web.mit.edu/16.070/www/lecture/big_o.pdf)
* [Algorithmic Complexity](https://www.cs.cmu.edu/~adamchik/15-121/lectures/Algorithmic%20Complexity/complexity.html)
* [Big-O Cheat Sheet](http://www.bigocheatsheet.com/)

{% endblock %}