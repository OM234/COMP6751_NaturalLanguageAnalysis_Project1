import nltk

from DateParser import getCFG, getTokenSubArrays, print_parses


class WrittenNumberParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.parser = None
        self.token_subarrays = None

    def parse_numbers(self):
        strCFG = getCFGString()
        cfg = getCFG(strCFG)
        self.token_subarrays = getTokenSubArrays(self.tokens)
        self.parser = nltk.RecursiveDescentParser(cfg)

    def print_numbers(self):
        print_parses('numbers', self.parser, self.token_subarrays)


def getCFGString():
    return (
        "NUMBER -> SMALLCARDINAL\n"  # four, forty

        "NUMBER -> MEDIUMCARDINAL\n"  # ninety

        "NUMBER -> MEDIUMCARDINAL SMALLCARDINAL\n"  # forty four

        "NUMBER -> SMALLCARDINAL LARGECARDINAL AND SMALLCARDINAL\n"  # one hundred and one

        "NUMBER -> SMALLCARDINAL LARGECARDINAL AND MEDIUMCARDINAL\n"  # fifteen million and forty

        "NUMBER -> SMALLCARDINAL LARGECARDINAL AND MEDIUMCARDINAL SMALLCARDINAL\n"  # one hundred and twenty four

        "SMALLCARDINAL -> 'one'| 'two' |'three' |'four'| 'five' |'six' |'seven' |'eight' |'nine'| "
        "'ten' |'eleven' |'twelve' |'thirteen' |'fourteen' |'fifteen' |'sixteen' |'seventeen'| "
        "'eighteen' |'nineteen'\n"

        "MEDIUMCARDINAL -> 'twenty' |'thirty' |'forty' |'fifty' |'sixty' |'seventy' |'eighty' "
        "|'ninety'\n"

        "LARGECARDINAL -> 'hundred' |'thousand' |'million' |'billion' |'trillion'\n"

        "AND -> 'and'")

