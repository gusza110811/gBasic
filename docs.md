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