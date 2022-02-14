# Wordle solver

Very simple NY-Times wordle solver for python with a provided CLI.

## Usage
no extra packages are required. The CLI accepts an input in the following format:

```
Guess 'aaaaa' > <INPUT>

<INPUT> := <POSITION>,<INCLUDED>

<POSITION> := ααααα   # represent the green tiles
α := <LETTER> | *     # wildcard means no fixed requirement

<INCLUDED> := α<INCLUDED> | ε  # list of letters that must be included, ε is empty word
```

## Contributions
Word list provided by https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
