---
title: An API to provide MILA stock data
date: 2018-07-23
categories: finance, programming
tags: golang, mila, stock market
---

{% load static %}

# An API to provide MILA stock data

Around five years ago, I was structuring my undergraduate thesis around performing heuristic-based analysis over the US stock market. At that time I asked myself the following question: “Given I live in Colombia, can I perform heuristic-based analysis using data from the Colombian stock market?” The answer was simple: the dataset of stocks in Colombia was so small, that it was not worth it. The Colombian stock exchange had 80 companies listed, while the US stock market had +6000 stocks only in NYSE and NASDAQ.

By the beginning of 2018, after monitoring and investing in the US stock market for some time, creating systems to [gather US stock market data](https://github.com/julianespinel/stockreader) and performing analysis over that information; the question came into my mind again: “Given that I live in Colombia, can I perform analysis using data from the Colombian stock market?”, and this time I hoped the answer would be different because now MILA was in place.

## What is MILA?

The Integrated Latin American Exchange known as [MILA](https://en.wikipedia.org/wiki/Mercado_Integrado_Latinoamericano) for its initials in Spanish, is a cooperative initiative that integrates stock markets from Mexico, Colombia, Chile and Peru. MILA started operating in 2011 with three founding members: Colombia, Chile and Peru. Mexico became part of MILA by 2014, making it an exchange with more than 700 listed companies.

## MILA API

Data is the main resource you need in order to perform stock market analysis, specifically historical data; and now it seems we have enough information thanks to MILA. This takes us to a critical step of the analysis process: acquiring information. The US stock market excels at this point because you can find historical stock data in multiple websites such as Yahoo Finance, Google Finance and Quandl, just to name a few. Most of them offer an API to access information and it’s open to the general public.

Taking those websites as inspiration I decided to start creating [MILA API](https://github.com/julianespinel/mila-api), an API to provide MILA stock market data. To simplify the problem I decided to begin the project by offering an API that returns closing data from the previous trading day.

## Design

In general terms, I needed to gather previous day stock data from all four MILA members (Mexico, Colombia, Chile and Peru), store it into a database and expose it using an HTTP API. As I began looking for current day stock market data from Mexico, Colombia, Chile and Peru, I realized there were not websites like Yahoo Finance or Quandl that provide stock data for Latin American exchanges. The lack of a central point where to obtain data from, meant I would have to gather information from each stock exchange individually.

Considering that constraint, my idea was to obtain information from each stock market part of MILA once a day. I would have to perform at least four external requests in order to get the previous day stock data. In the diagram below I show the design of the piece of software created to gather stock data and then offer it through an API.

![MILA api_uml](blog/mila_api.png)

The design was simple, I built an architecture composed of three main layers:

1. **API**: responsible for verifying the input sent in the HTTP requests and serializing the response to be given to the user.
1. **Domain**: responsible for handling the business logic. Part of the business logic is to gather data once a day from each stock exchange.
1. **Persistence**: responsible for communicating with the database. Specifically, it performs CRUD operations of stock data against the database.

There are four clients on the right-hand side of the diagram, each client is responsible for getting stock market data from each stock exchange part of MILA and return that data to the domain layer in the form of business objects.

## Implementation

The implementation of MILA API is not complete yet. It currently downloads stock market data from the Colombian stock exchange, transforms it into valid business objects and stores them in the database. Then it exposes the information using an HTTP API.

Here is an example of an endpoint request and its response:

Request:
```
GET mila/api/colombia
```

Response:
```
{
  "date": "2018-05-26T10:03:58.813141778-05:00",
  "country": "colombia",
  "stocksData": [
    {
      "date": "2018-05-26T10:03:58.812629133-05:00",
      "country": "colombia",
      "symbol": "BCOLOMBIA",
      "name": "Bancolombia",
      "currency": "COP",
      "open": "33000",
      "high": "35100",
      "low": "32900",
      "close": "33200",
      "adjClose": "33200",
      "volume": 891338
    },
    {
      "date": "2018-05-26T10:03:58.812713643-05:00",
      "country": "colombia",
      "symbol": "GRUPOARGOS",
      "name": "Grupo Argos",
      "currency": "COP",
      "open": "19700",
      "high": "21300",
      "low": "19500",
      "close": "20000",
      "adjClose": "20000",
      "volume": 373137
    }
  ]
}
```

The part missing for the project to be complete is to create the clients responsible for gathering market information from the remaining countries: MexicoClient, ChileClient and PeruClient.

The code is available [here](https://github.com/julianespinel/mila-api).

## Lessons learned

By doing this side project I learned new technical implementation details related to the Go programming language, here I list them:

1. `dep` is a great dependency management tool, simple to use. Here is an [overview](https://golang.github.io/dep/docs/daily-dep.html).
1. How to use `go-vcr` to record HTTP requests for testing. Here is an [example](https://github.com/julianespinel/mila-api/blob/c8fa9e8e46d0b66d41acaad52330722b3b68144c/bvc/client_test.go#L14-L27).
3. How to use `gomock` to create mocks and use them in tests. Here is an [example](https://github.com/julianespinel/mila-api/blob/f0a12e5b50c950a36c0b51a4b0bc1813fc7b116a/core/domain_test.go#L29-L30).
1. Although I try to avoid ORMs, this time I used `gorm` because MILA API was a small and simple project. Gorm helped me to reduce the time writing database access code significantly. Here are some examples: [one](https://github.com/julianespinel/mila-api/blob/a0a7f14e8697478f9c4458392c570b29e3d1ca74/models/stock.go#L11-L14) and [two](https://github.com/julianespinel/mila-api/blob/f0a12e5b50c950a36c0b51a4b0bc1813fc7b116a/core/persistence.go).
1. Iris (the web framework) is fast, flexible and simple to use. Here is an [example](https://github.com/julianespinel/mila-api/blob/1777c037212b5dcc1e44267253f026530fe3e058/main.go#L60-L68).

## Next steps

I don’t know if I will finish this project, but the road until this point has been fun. The project still requires [some work](https://github.com/julianespinel/mila-api/issues) and I don’t know if I will use it once it is finished. The primary goal of MILA API was to check if this time I could have a better answer (with respect of the one I had five years ago) to the question: “Given I live in Colombia, can I perform analysis using data from the Colombian stock market?”.

This time the answer was indeed better, now we have enough data and enough companies listed in MILA to be able to perform automated analysis on them. At this moment the problem is different, we have data but we lack the infrastructure to make that data available. Latin America is still behind in terms of financial services that provide access to stock market data to the general public.

A secondary goal I was pursuing when I started this project was to learn a more about Golang. The fact that Golang has a small syntax, one way to do things, and a [clearly defined code style](https://blog.golang.org/go-fmt-your-code); means it will be easier to read and maintain by other people. Taking into consideration that most of the software lifecycle is spent on maintenance, this aspect of a programming language is crucial for me. I’m not an expert in Golang, but this project allowed me to practice and appreciate the Go programming language.
