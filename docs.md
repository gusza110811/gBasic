# gBasic Documentation

## Comment
use # to comment the text after it, can be used in line

## Text output
`print {text}` : Prints {text}

`clean` : Clear the terminal

`dump` : Outputs all variables set

# File I/O
`write {filename} {text}` : write {text} to file {filename}, overwriting anything still in it
`awrite {filename} {text}` : add {text} to the end of file {filename}
`read {filename} {variable}`: save data of file {filename} to {variable}

## Variables
`set {name} (value)` Create and set a a variable {name} to (value)

`input {variable name} (prompt)` Ask the user (prompt) and set variable {variable name} to the user's answer

## If statement and flow control
`:{label name}` : set variable {label name}'s value to the current line number

`?{condition} ${target}` or `if {condition} ${target}` or `gotoif {condition} ${target}`: Go to line {target} if {condition} is true

`jump ${target}`: jump to {target}

## Affixes
Use `${variable name}` to get {variable name}'s value

Use `"` or `'` to surround a text to make it one token of data, this also allows spaces in variables. both are interchangeable so you can use `'` to close a `"` and vice versa

# Arithmetics
Supported calculations are
`+`addition `-`subtraction `*`multiplication `**`exponentiation `/`division `//`floor division and `%`modulo

## Comparators
Supported comparators are
`==`equals to `<`less than `>`more than 

## Boolean Arithmetics
Supported calculations are
`||`or `&&`and `~~`not

### Note
Each of these symbols above must be seperated from surrounding text with spaces to do their assigned functions, otherwise it is simply plain text

for example
`5 ** 2` means 5<sup>2</sup> and is considered as one token `25`. while `5**2` is just `5**2`

`2 == 9` means 2=9 and is equal to `False` while `2==9` is just `2==9`

`~~ False` means not(False) and is equal to `True` while `~~False` is just `~~False`

###### \*Compiled and Interpreted gBasic may be slightly different
