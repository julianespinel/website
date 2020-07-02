---
title: Should parking fares work like Uber?
date: 2018-04-14
categories: economics
tags: uber
      pricing
      opinion
---

# Should parking fares work like Uber?

2018-04-14

Recently I was having lunch with some friends, one of them let us now that the current major of our city (Bogotá, Colombia) had been talking about deregulating the parking fares<sup>1</sup> and, according to my friend, if that happens parking prices will skyrocket. During the discussion two points of views were presented, the first was about the current major of the city being involved in the parking business, so he has conflict of interests. The second argument was about if it was ok or not to deregulate the parking price and let the free market do its job.

This post is about the second point of view. I pretend to analyse how parking lot owners could employ a model similar to Uber’s, adjust the parking fares dynamically according to supply and demand. Simple economic theory, right?

## How do parking lots work today?

Most parking lots in Bogotá have two main business models:

1. Charge the customer a price per minute the car is parked.
1. Charge the customer a monthly price for unlimited time of parking within the month.

Until the publication of this post, Bogotá still has a regulated parking fare. According to law, an underground or elevated parking lot in Bogotá should charge a maximum rate for cars of 105 COP per minute<sup>2</sup>. So when a parking lot is almost empty, parking your car there costs maximum 105 COP per minute. And what’s the cost when the parking lot is almost full in a friday night? You guessed it right, the maximum cost is the same. Can parking lot owners change the rate dynamically according to demand, within the rate interval defined by law? Would that be legal?

## How could parking lots work?

Colombia is a country with a predominantly paternalistic government. I support the state involvement in aspects related to human rights and access to primary needs such as education, health and public transportation, but I don’t see what is the role of the state in regulating things such as parking lot fares.

So what alternatives do parking lots owners have? In a free market, at least theoretically, they should be able to define their fares, as well as their schedule and working days.

### Dynamic fare model for parking fares

I would like to suggest a model where parking lots define the fare to pay according to supply and demand.

Lets create a simple example, based on the following assumptions:

1. You are the owner of a parking lot with 100 car spaces.
1. You have a minimum fare and a maximum fare you must respect.<br>
   The interval is `[48 COP, 105 COP]`.

We could define a linear function<sup>3</sup>: dynamicFare = f(x) = ceil(a + bx), where:

* x is the number of car spaces occupied in the parking lot.
* a equals to 48 COP
* b equals to 0.57 COP

So in case the parking lot has 99 car spaces occupied the dynamicFare would be:

```
dynamicFare = f(x) = ceil(a + bx)
dynamicFare = f(99) = ceil(48 + (0.57*99))
dynamicFare = f(99) = ceil(104.43) = 105
```

Using this linear equation you should be able to adjust the parking fare per minute, according to the occupancy of the parking spaces. In theory every time a car leaves or enters, the fare is adjusted, that leaves us the question: what fare should I charge a customer if, while her car was parked, 10 cars left the parking lot? To make things simple to understand for customers I would suggest to publish the current fare at the entrance of the parking lot and freeze the fare for each car when the car enters. Here is an example:

| Time  | Current fare/minute (COP) | Minutes parked | Total (COP) |
| ----- | ------------------------- | -------------- | ----------- |
| 06:00 | 48 | 60 | 2880 |
| 12:01 | 66 | 60 | 3960 |
| 19:00 | 95 | 60 | 5700 |

This model increases the parking fare linearly according to the occupancy of the parking lot. If you would like to increase the fare faster or slower you have to look for a function that offers the properties you are looking for<sup>4</sup>.

The pricing model can be as complex as you want. For example you could add more variables to represent things such as weather, the occurrence of a popular event (like a concert or a sports event) taking place near to the parking lot, the number of parking options nearby, etc.

## Why?
This debate is important because we need to clearly define and delimit the role of the state and its relationship with the citizens. As a free market advocate I think it is crucial to allow business owners define the variables that impact the operation of their companies. Variables that in this case could promote competition, efficiency and innovation.

Being able to park a car in the city is not a primary need for the average citizen. Someone could argue that parking space access is a primary need for people with special mobility requirements, that could be correct and the state should regulate those specific cases. But for the majority of the population parking space is a luxury not a necessity. Let’s allow the free market handle luxuries and remove inefficiencies.

## Sources

1. [Que los parqueaderos cobren lo que quieran, estudia Peñalosa](https://www.elespectador.com/noticias/bogota/que-los-parqueaderos-cobren-lo-que-quieran-estudia-penalosa-articulo-707171)
1. [Distrito busca aumentar tarifas de parqueaderos públicos en Bogotá](https://www.elespectador.com/noticias/bogota/distrito-busca-aumentar-tarifas-de-parqueaderos-publicos-en-bogota-articulo-733795)
1. [Linear Functions](http://www.columbia.edu/itc/sipa/math/linear.html)
1. [Reference - Graphs of eight basic types of functions](http://mathonweb.com/help_ebook/html/functions_4.htm)
