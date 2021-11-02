# Produces tokens

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
