---
title: How to read a CSV file using Haskell
date: 2021-09-22
categories: programming
tags: haskell
---

# How to read a CSV file using Haskell

2021-09-22

In this entry we explore how to read a file CSV using Haskell.
If you are new to Haskell the easiest way to install it is
[GHCup](https://www.haskell.org/ghcup/).

## Description

Suppose we want to read a CSV file that contains basic information about
financial instruments (bonds, stocks, funds, etc.) listed in the US stock market.

The CSV file we want to read has the following structure:

![csv](blog/csv.png)

There are two important things we need to take into account about the file:

1. There are different types of financial instruments in the file: Common stock,
   ETF, Fund.
1. The Isin column can be empty.

## Steps

We want to write a Haskell program that reads the file and returns a list
containing financial instruments of type `Common Stock`. In order to do that,
our program needs to perform (at least) the following steps:

1. Receive the CSV file path as argument
2. Check if the CSV file exists
3. Read the CSV file
4. Filter the elements of type `Common Stock`
5. Return the resulting list

Let's see how to do that using Haskell!

## Source code

### Data modeling

Among the first things we usually do before start writing code, is think about the
data we are going to work with. In this case we need to create a data type to
hold the information from the CSV file.

We will model each row of the CSV file using the following data type:

```haskell
-- data type to model a FinancialInstrument
data FinancialInstrument = FinancialInstrument
  { code :: String,
    name :: String,
    country :: String,
    exchange :: String,
    currency :: String,
    instrumentType :: String
  }
  deriving (Show, Eq)
```

We can ignore the value from the column Isin. Why? Because we don't
need it for this exercise.

### How to read a CSV file

The next thing we need to define is how we are going to read the CSV file.
To read the file we are going to use two libraries:

1. [Data.ByteString.Lazy](https://hackage.haskell.org/package/bytestring-0.11.1.0/docs/Data-ByteString-Lazy.html): to read the file as a stream (lazily).
2. [Cassava](https://hackage.haskell.org/package/cassava): to parse a CSV row to a `FinancialInstrument`.

Let's see how to use them:

```haskell
import Prelude hiding (filter)
import qualified Data.ByteString.Lazy as BL
import Data.Csv -- this is from the Cassava library
import qualified Data.Vector as V
import System.Directory (doesFileExist)

-- Define how to get a FinancialInstrument from a record (CSV row)
-- by implementing the FromNamedRecord type class
instance FromNamedRecord FinancialInstrument where
  parseNamedRecord record =
    FinancialInstrument
      <$> record .: "Code"
      <*> record .: "Name"
      <*> record .: "Country"
      <*> record .: "Exchange"
      <*> record .: "Currency"
      <*> record .: "Type"

type ErrorMsg = String
-- type synonym to handle CSV contents
type CsvData = (Header, V.Vector FinancialInstrument)

-- Function to read the CSV
parseCsv :: FilePath -> IO (Either ErrorMsg CsvData)
parseCsv filePath = do
  fileExists <- doesFileExist filePath
  if fileExists
    then decodeByName <$> BL.readFile filePath
    else return . Left $ printf "The file %s does not exist" filePath
```

#### Parse a CSV row

The first five lines of the previous code fragment specify the libraries we
need to read the CSV file.

Then, we make our `FinancialInstrument` data type an instance of the type class
`FromNamedRecord`. Think about this like implementing an interface in Java.

Java:
```java
class FinancialInstrument implements FromNamedRecord { ... }
```

Haskell:
```haskell
instance FromNamedRecord FinancialInstrument where ...
```

In order to be an instance of `FromNamedRecord` we need to implement the
function `parseNamedRecord`. Again, following our Java analogy:

Java:
```java
public Parser<FinancialInstrument> parseNamedRecord(NamedRecord record) { ... }
```

Haskell:
```haskell
parseNamedRecord record = ...
```

In this function we define how we can create a `FinancialInstrument` from a row
in the CSV file.

#### Read and return

Then, we define two type synonyms (aka. type alias):

1. `ErrorMsg` to define an error message.
2. `CsvData` is a tuple to handle the result of reading the CSV file.

Finally, we define the function `parseCsv`. We use it to read the CSV file and
return its contents. The function performs the following steps:

1. Check if the file exists
2. If the file exists read each row and return `IO (Right CsvData)`
3. if the file does not exist return `IO (Left ErrorMsg)`

### Filter stocks

If everything went well, the function `parseCsv` returns an `IO (Right CsvData)`.
We have read the CSV file! But we are not done yet.

Please remember that:

```haskell
type CsvData = (Header, V.Vector FinancialInstrument)
```

Therefore, if we replace `CsvData` by its definition in `IO (Right CsvData)`,
we have:

```haskell
IO (Right (Header, V.Vector FinancialInstrument))
```

Let's drop `IO` and `Right`. Don't worry about them, we will add them back later.

In essence, we have a tuple `(Header, V.Vector FinancialInstrument)` and we want
to have `V.Vector FinancialInstrument`, where the vector only has financial
instruments of type `Common Stock`. Therefore, we are missing two steps:

1. Remove the headers from `(Header, V.Vector FinancialInstrument)`
2. Filter the `V.Vector FinancialInstrument` to only keep the financial
   instruments of type `Common Stock`

#### 1. Remove the headers from CsvData

Our starting point is `(Header, V.Vector FinancialInstrument)` and we
want to remove the headers, meaning that we want `V.Vector FinancialInstrument`.
In Haskell terms we want the following function:

```haskell
someFunction :: (Header, V.Vector FinancialInstrument) -> V.Vector FinancialInstrument
```

We have a tuple, and we need to get its second element.
Fantastic! Haskell has a function for that:

```haskell
:t snd
snd :: (a, b) -> b
```

To have a meaningful name (in the context or our problem), we define a
function that will be equal to `snd`.

```haskell
-- Discard headers from CsvData
removeHeaders :: CsvData -> V.Vector FinancialInstrument
removeHeaders = snd
```

Excellent! We have a function to get the second element of the tuple.

#### 2. Filter the FinancialInstrument vector

Now, we need to filter the `V.Vector FinancialInstrument` to keep the
instruments of type `Common Stock` and discard the rest. Once again, Haskell has
a function for that, the name of the function is [filter](https://hackage.haskell.org/package/base-4.15.0.0/docs/Prelude.html#v:filter):

```haskell
:t filter
filter :: (a -> Bool) -> [a] -> [a]

-- Which means:
-- applied to a predicate (a -> Bool) and a list [a],
-- returns the list [a] of those elements that satisfy the predicate
--
-- For example: filter odd [1, 2, 3] -> [1, 3]
```

We would like to create a function that has a meaning in the context of our
problem:

```haskell
-- Given a list, return only the elements with instrumentType "Common Stock"
filterStocks :: V.Vector FinancialInstrument -> V.Vector FinancialInstrument
filterStocks = filter isStock
  where
    isStock :: FinancialInstrument -> Bool
    isStock instrument = instrumentType instrument == "Common Stock"
```

Great! We have functions to remove the headers and filter the vector.
What happens if we compose these two functions?

```haskell
:t (filterStocks . removeHeaders)
(filterStocks . removeHeaders) :: CsvData -> V.Vector FinancialInstrument
```

We get a function that takes a `CsvData` and returns a filtered vector
`V.Vector FinancialInstrument`. That's almost exactly what we need.
Why almost? Because we have an `IO (Right CsvData)`, not just a `CsvData`.

This takes us to the last question of the exercise. How do we apply the function
`(filterStocks . removeHeaders) :: CsvData -> V.Vector FinancialInstrument` to
`IO (Right CsvData)`?

### Lifting functions

We don't want to explain `IO` and `Either` in this blog post.
However, you can read about them
[here](http://learnyouahaskell.com/input-and-output) and
[here](http://learnyouahaskell.com/for-a-few-monads-more).
For now, let's call them a container or a context.

Taking that into account, `IO (Right CsvData)` means that we have a tuple
(remember, CsvData is a tuple) inside an Either context: `Right CsvData`,
and we have an Either inside an IO context: `IO (Right CsvData)`.
How can we modify our composed function `(filterStocks . removeHeaders)` to operate
on `IO (Right CsvData)`?

There is a simple way we can lift a function to operate on contexts.
Enter `fmap`:

```haskell
:t fmap
fmap :: Functor f => (a -> b) -> (f a -> f b)
```

`fmap` is a function that takes a function from a to b `(a -> b)` and returns
the same function [lifted](https://wiki.haskell.org/Typeclassopedia#Intuition)
to the context f `(f a -> f b)`. Therefore we can apply the initial function in
the context f.

What is `Functor f`? For the sake of this exercise, a functor is a
container or a context. In fact `IO` and `Either` are functors!
For a proper explanation of what a Functor is, please read this chapter:
[Functors, Applicative Functors and Monoids](http://learnyouahaskell.com/functors-applicative-functors-and-monoids).

What happens if we apply `fmap` to `(filterStocks . removeHeaders)`? Let's see:

```haskell
:t fmap (filterStocks . removeHeaders)
fmap (filterStocks . removeHeaders)
  :: Functor f => f CsvData -> f (V.Vector FinancialInstrument)
```

We are close! We lifted the function and we can apply it over one context.
But we have two contexts (`Either` and `IO`). What if we apply `fmap`
again? (aka. lift the function again).

```haskell
:t fmap (fmap (filterStocks . removeHeaders))
fmap (fmap (filterStocks . removeHeaders))
  :: (Functor f1, Functor f2) => f1 (f2 CsvData) -> f1 (f2 (V.Vector FinancialInstrument))

-- which can also be written as:

(fmap . fmap) (filterStocks . removeHeaders)
```

We did it! Now we can apply our function over two nested contexts!
And this is how our program ends:

```haskell
-- Read stocks from a CSV file
readStocks :: FilePath -> IO (Either ErrorMsg (V.Vector FinancialInstrument))
readStocks filePath =
  (fmap . fmap) -- lift the function twice
    (filterStocks . removeHeaders) -- remove headers and filter stocks
      (parseCsv filePath) -- read CSV from file path
```

If you want to check the complete program and run it yourself you can find the
instructions here: [README.md](https://github.com/julianespinel/stockreader/tree/e6de8e7ee43c6f16f10192a188b2c1d5d7ed460c/v2/stockreader#run). The file we have
explained is [Csv.hs](https://github.com/julianespinel/stockreader/blob/e6de8e7ee43c6f16f10192a188b2c1d5d7ed460c/v2/stockreader/src/Csv.hs)

## Tests

We want to add tests to check the behavior of our program.
We created the test cases using [Hspec](https://hspec.github.io/):

```haskell
-- imports are omitted for brevity

spec :: Spec
spec = do
  describe "readStocks" $ do
    it "returns IO (Left ErrorMsg) when the file does not exist" $ do
      let nonExistentFile = "test-resources/no-file.csv"
      let errorMessage = printf "The file %s does not exist" "test-resources/no-file.csv"
      readStocks nonExistentFile `shouldReturn` Left errorMessage

    it "returns 'not enough input' when the file is empty" $ do
      let emptyFile = "test-resources/empty-file.csv"
      let errorMessage = "parse error (not enough input) at \"\""
      readStocks emptyFile `shouldReturn` Left errorMessage

    it "returns the same rows as the file when the file only contains stocks" $ do
      let stocksOnlyFile = "test-resources/stocks-only.csv"
      either <- readStocks stocksOnlyFile
      either `shouldSatisfy` isRight
      length <$> either `shouldBe` Right 5

    it "returns the less rows than the file because filters out non-stocks" $ do
      let stocksAndFundsFile = "test-resources/stocks-and-funds.csv"
      either <- readStocks stocksAndFundsFile
      either `shouldSatisfy` isRight
      length <$> either `shouldBe` Right 7
```

You can find the whole test file here: [CsvSpec.hs](https://github.com/julianespinel/stockreader/blob/e6de8e7ee43c6f16f10192a188b2c1d5d7ed460c/v2/stockreader/test/CsvSpec.hs)

## Closing words

Thanks for reading this far! I hope you have enjoyed this post.
