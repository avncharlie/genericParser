"""

CFG grammar parser

rules: nonterminal -> anything 

given a grammar object

    1. randomly generate valid expression
    2. validate string

"""

# classes used to represent production rules
class nonTerminal:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

class terminal:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        if isinstance(other, terminal):
            return self.name == other.name
        return False

class grammar_or:
    def __init__(self, *args):
        self.items = [*args]

class grammar_seq:
    def __init__(self, *args):
        self.items = [*args]

    def __repr__(self):
        return str(self.items)

class Tokeniser:
    def __init__(self, terminals, string):
        self.tokenised = self.tokenise(string, terminals)
        self.curr = 0

    def nextToken(self):
        n = self.tokenised[self.curr]
        self.curr += 1
        return n

    def getCurrentState(self):
        return self.curr

    def setState(self, state):
        self.curr = state

    def atEnd(self):
        return self.curr == len(self.tokenised)

    # returns (false, part of string not tokenisable) if cannot be tokenised
    def tokenise(self, string, terminals):
        tokenised = []

        currIndex = 0
        canBeTokenised = True
        restOfString = string
        while currIndex < len(string) and canBeTokenised:
            restOfString = string[currIndex:]

            # will stay false if no terminal works with rest of the string
            canBeTokenised = False 
            for term in terminals:
                if self.tryTerminal(restOfString, term):
                    tokenised.append(term)
                    canBeTokenised = True
                    currIndex += len(term.name)
                    break

        if not canBeTokenised:
            return (False, restOfString)

        return tokenised

    def tryTerminal(self, string, terminal):
        if len(string) < len(terminal.name):
            return False

        return string[:len(terminal.name)] == terminal.name


class Grammar:
    def __init__(self, terminals, rules, start):
        self.rules = rules
        self.start = start
        self.terminals = terminals

    def validate(self, string):
        # sets up tokeniser
        self.tokeniser = Tokeniser(self.terminals, string)
        return self.satisfiesRule(self.start)

    # really just expands OR
    # moves token state forward to where rule finished if successful
    def satisfiesRule(self, ruleLeftSide, noLeftOver=True):
        production = self.rules[ruleLeftSide]

        alternatives = [production] # will be terminal, nonterminal, or sequence
        if isinstance(production, grammar_or):
            alternatives = production.items

        foundAlternative = False
        for alternative in alternatives:
            if self.checkAlternative(alternative, noLeftOver=noLeftOver):
                foundAlternative = True
                break

        return foundAlternative

    # really just makes everything a seq and handles passes to seq handler
    def checkAlternative(self, alternative, noLeftOver=True): 
        seq = [alternative] # will be terminal or nonterminal
        if isinstance(alternative, grammar_seq):
            seq = alternative.items

        return self.checkSequence(seq, noLeftOver=noLeftOver)

    def checkSequence(self, sequence, noLeftOver=True):
        # on failure, reset token state to start state
        startState = self.tokeniser.getCurrentState()

        for item in sequence:
            # if no more tokens but rule not finished then fail
            if self.tokeniser.atEnd():
                self.tokeniser.setState(startState)
                return False

            # if terminal, just check if next token matches
            if isinstance(item, terminal):
                if not self.tokeniser.nextToken() == item:
                    self.tokeniser.setState(startState)
                    return False

            # if nonTerminal, use satisfiesRule
            elif isinstance(item, nonTerminal):
                if not self.satisfiesRule(item, noLeftOver=False):
                    self.tokeniser.setState(startState)
                    return False

        if noLeftOver:
            # even if parsed, return false if tokens remaining
            if not self.tokeniser.atEnd():
                return False
        return True


def numberExample():
    num = nonTerminal('num')
    digit = nonTerminal('digit')
    
    numberTerminals = []
    for n in '0123456789':
        numberTerminals.append(terminal(n))
    
    rules = {
            digit: grammar_or(*numberTerminals),
            num: grammar_or(grammar_seq(digit, num), digit)
    }
    
    numbers = Grammar(numberTerminals, rules, num)
    print(numbers.validate('6299485'))

def AAAAexample():
    aTerm = nonTerminal('aTerm')
    a = terminal('a')
    
    rules = {
            aTerm: grammar_or(
                    grammar_seq(a, aTerm),
                    a
                )
    }
    
    aGrammar = Grammar([a], rules, aTerm)
    print(aGrammar.validate('aaaaaaaaaaaaa'))

def mathExample():
    exp = nonTerminal('exp')
    num = nonTerminal('num')
    digit = nonTerminal('digit')
    opp = nonTerminal('opp')
    
    numberTerminals = [terminal(n) for n in '0123456789']
    operationTerminals = [terminal(n) for n in '+-*/']
    
    rules = {
            opp: grammar_or(*operationTerminals),
            digit: grammar_or(*numberTerminals),
            num: grammar_or(grammar_seq(digit, num), digit),
            exp:grammar_or(grammar_seq(exp, opp, exp), num)
    }

    terminals = numberTerminals + operationTerminals
    start = exp
    
    numbers = Grammar(terminals, rules, start)
    print(numbers.validate('629+4'))

mathExample()

#tokeniser = Tokeniser(numberTerminals, '123')

"""
for each thing in seq:
    if terminal:
        check if matching, if not fail

    if nonTerminal:
        check if matching, if not fail

    if out of tokens, fail

if tokens remaining, fail
"""
        



"""
todo:
        has to satisfy one of:
            alt1 (digit):
                isDigit:
            alt2 (digit num):
                isDigit:
                    isNum

    56
    doesn't satisfy alt1
    consume isDigit amount
    check that rest is num

        digit -> 0|1|2|3|4|5|6|7|8|9
        num -> digit num | digit

    https://www.freecodecamp.org/news/beyond-regular-expressions-an-introduction-to-parsing-context-free-grammars-ee77bdab5a92/
    https://en.wikipedia.org/wiki/Parsing_expression_grammar

    document

    MAKE WRAPPER FOR:
        generating rules to not have to manually generate terminal list, etc
        (infer terminals from rules)
    
    rules:
        digit -> 0|1|2|3|4|5|6|7|8|9
        num -> digit num | digit

    start:
        num -> digit num | digit

    isNum:



    given string,
    asks:
        is it first nonTerminal described by first rule?
        if it is, consume and move to next thing
        else, is it second nonTerminal described by second rule?
"""

