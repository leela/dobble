# Dobble

Dobble is a card game in which players try to find a common image between any two cards. You can create dobble cards using this package.

Here are the rules to create dobble cards:

- Each card has equal number of symbols/images.
- No two symbols on a card are same.
- There will be exactly one common symbol between any two cards (common symbol rule).

This package is primarily created to create educational card games for kids who is learning language building blocks like letter sounds and names. In this version only text symbols are supported instead of images unlike standard dobble.

## Installation

Make sure that your Python version is 3.11 or greater.

Installation and usage:

```
$ git clone https://github.com/leela/dobble
$ cd dobble
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python -m dobble --help
```

Look at `python -m dobble --help` to find all the available command line options.

Display card wise symbols using `list-cards` sub-command.

```
python -i -m dobble list-cards -n 4 -s a,b,c,d,e,f,g,h,i,j,k,l,m
```

Generate PDF with dobble cards using `create-cards` sub-command.

```
python -i -m dobble create-cards -n 4 -s a,b,c,d,e,f,g,h,i,j,k,l,m
```

PS: Programme generates Jolly Phonic sound cards by default(when not given any options).

## How Code Works

Here is how the Dobble cards are created.

- Lets start with the first card, that contains 0 to n-1 symbols (where n is symbols per card).
- Any card that we create from now on, should have one symbol from first card(according to common symbol rule). So, we need to create set of cards for each symbol of the first card.
- How can we make a set of cards for "one symbol"?
  - We know that, one symbol from first card will be in all cards in that specific set, with (n-1)\*(n-1) new symbols we can make (n-1) cards in a set.
  - By transposing and shifting/rolling those (n-1)\*(n-1) symbols, we can make (n-1) cards for every symbol from the first card and those obey common symbol rule.
