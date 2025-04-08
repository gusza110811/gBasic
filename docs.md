# gBasic Documentation

## Comment
use # to comment the text after it, can be used in line

## Text output
`print {text}` : Prints {text}

`clean` : Clear the terminal

`dump` : Outputs all variables set

## Variables
`set {name} (value)` Create and set a a variable {name} to (value)

`input {variable name} (prompt)` Ask the user (prompt) and set variable {variable name} to the user's answer

## If statement and Loops
`:{label name}` : set variable {label name}'s value to the current line

`?{condition} {target}` or `if {condition} {target}` or `gotoif {condition} {target}`: Go to {target} if {condition} is true

## Affixes
Use `${variable name}` to get {variable name}'s value

Use `"` or `'` to surround a text to make it one token of data, this also allows spaces in variables. both are interchangeable so you can use `'` to close a `"` and vice versa

# Arithmetics
Supported calculations are
`+`addition `-`subtraction `*`multiplication `/`division and `**`exponentiation

## Comparators
Supported comparators are
`==`equals to `>`more than `<`less than

## Boolean Arithmetics
Supported calculations are
`||`or `&&`and `~~`not

### Note
Each of these symbols above must be seperated from surrounding text with spaces to do their assigned functions, other wise it is considered plain text

for example
`5 ** 2` means 5<sup>2</sup> and is considered as one token `25`. while `5**2` is just `5**2`

`2 == 9` means 2=9 and is considered as one token `False` while `2==9` is just `2==9`

`~~ False` means not(False) and is considered as one token while `True` `~~False` is just `~~False`