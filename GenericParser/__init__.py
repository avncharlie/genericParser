from GenericParser.Symbols import *
from GenericParser.Tokeniser import *
from GenericParser.Grammar import *

def numberExample():
    num = nonTerminal('num')
    digit = nonTerminal('digit')
    
    numberTerminals = []
    for n in '0123456789':
        numberTerminals.append(terminal(n))
    
    rules = {
            digit: grammar_or(*numberTerminals),             # digit = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
            num: grammar_or(grammar_seq(digit, num), digit)  #   num = (digit num) | digit
    }

    numbers = Grammar(numberTerminals, rules, num)
    numbers.parse('15')

numberExample()
