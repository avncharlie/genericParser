"""

TODO: research SLR parsers

difference:
https://www.javatpoint.com/parse-tree-and-syntax-tree

"""

from GenericParser.Symbols import *
from GenericParser.Tokeniser import *

# main function: validates grammar
class Grammar:
    def __init__(self, terminals, rules, start):
        self.rules = rules
        self.start = start
        self.terminals = terminals

    def reduce(self, symbol_stack):
        # go through rules to check if reduction possible
        for lhs in self.rules:
            rhs = self.rules[lhs]
            
            # expand top level ORs to alternatives
            alternatives = [rhs] # if not OR, then only 1 alternative
            if isinstance(rhs, grammar_or):
                alternatives = rhs.items

            reductionPossible = False
            for alt in alternatives:
                # expand SEQs to lists
                rhsSeq = [alt] # if not seq, then single item seq
                if isinstance(alt, grammar_seq):
                    rhsSeq = alt.items

                # check if any reduction possible
                if len(rhsSeq) <= len(symbol_stack):
                    reductionPossible = True
                    for i, x in enumerate(reversed(rhsSeq)):
                        if x != symbol_stack[-(i+1)]:
                            reductionPossible = False
                            break

                # if possible, reduce
                if reductionPossible:
                    symbol_stack = symbol_stack[:-len(rhsSeq)] # remove rhsSeq
                    symbol_stack.append(lhs) # replace with lhs

                    print("reduced:", rhsSeq, "-->", lhs)
                    print(symbol_stack, end="\n\n")

                    return symbol_stack


    def parse(self, string):
        # set up tokeniser and stack
        tokeniser = Tokeniser(self.terminals, string)
        symbol_stack = []

        while not tokeniser.atEnd():
            # shift
            symbol_stack.append(tokeniser.nextToken())
            print("shift")
            print(symbol_stack, end="\n\n")

            # reduce
            symbol_stack = self.reduce(symbol_stack)


# OR > SEQ > nonterminals | terminals

