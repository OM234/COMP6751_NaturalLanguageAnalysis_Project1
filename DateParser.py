import nltk


# This class is used to parse dates
class DateParser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.parser = None
        self.token_subarrays = None

    def parse_dates(self):
        strCFG = buildCFGString()  # the string representation of our CFG
        cfg = getCFG(strCFG)  # the actual nltk CFG
        self.token_subarrays = getTokenSubArrays(self.tokens)  # all subarrays of length 5, which are fed to parser
        self.parser = nltk.RecursiveDescentParser(cfg)  # parser used

    def print_dates(self):
        print_parses('dates', self.parser, self.token_subarrays)  # iterate through subarrays, try to find date parse


# we build the string representation of our CFG
def buildCFGString():
    strCFG = initialCFGString()  # get the base CFG string
    strCFG = addDaysToCFG(strCFG)  # add days to CFG, e.g. 1st
    strCFG = addDaysDigToCFG(strCFG)  # add days to CFG, e.g. 0, 05, 8
    strCFG = addFourDigYearsToCFG(strCFG)  # add years to CFG, e.g. 1990, 1800
    strCFG = addTwoDigYearsToCFG2(strCFG)  # add years to CFG, e.g. 90, 80, 35
    return strCFG


def initialCFGString():
    return (
            "DATE -> YEAR SEP MONTHDIG SEP DAYDIG\n" +  # 1990/01/30

            "DATE -> DAYDIG SEP MONTHDIG SEP YEAR\n" +  # 03/01/1990

            "DATE -> FULLYEAR\n" +  # 2050

            "DATE -> MONTH DAY\n" +  # february 5th

            "DATE -> MONTH\n" +  # june

            "DATE -> ORDINAL OF MONTH\n"  # second of may

            "DATE -> DAY OF MONTH\n"  # 9th of january

            "DATE -> ORDINAL OF MONTH\n"  # fourth of january

            "MONTH -> 'january' | 'february' | 'march' | 'april' | 'may' | 'june' | 'july' | 'august' | "
            "'september' | 'october' | 'november' | 'december'\n" +

            "MONTHDIG -> '01' | '02' | '03' | '04' | '05' | '06' | '07' | '08' | '09' | '10' | '11' | '12'\n" +

            "ORDINAL -> SMALLORDINAL | LARGEORDINAL SMALLORDINAL\n"  # first, twenty-third (dashes removed in tokenizer) 

            "SMALLORDINAL -> 'first' | 'second' | 'third' | 'fourth' | 'fifth' | 'sixth' | 'seventh' | 'eighth' | "
            "'ninth' | 'tenth' | 'eleventh' | 'twelfth' | 'thirteenth' | 'fourteenth' | 'fifteenth' | 'sixteenth' | "
            "'seventeenth' | 'eighteenth' | 'nineteenth'\n" +

            "LARGEORDINAL -> 'twenty' | 'twentieth' | 'thirty' | 'thirtieth' \n"

            "SEP -> '/'\n" +

            "OF -> 'of'\n")


def addDaysToCFG(strCFG):
    strCFG = strCFG + 'DAY -> \'1st\' '
    for day in range(2, 32):
        strCFG = strCFG + '| \'' + str(day)
        if day % 10 == 1:
            strCFG = strCFG + 'st\' '
        elif day % 10 == 2:
            strCFG = strCFG + 'nd\' '
        elif day % 10 == 3:
            strCFG = strCFG + 'rd\' '
        else:
            strCFG = strCFG + 'th\' '
    strCFG = strCFG + "\n"
    return strCFG


def addDaysDigToCFG(strCFG):
    strCFG = strCFG + 'DAYDIG -> \'0\' | \'00\''
    for day in range(1, 32):
        strCFG = strCFG + ' | \'' + str(day) + '\''
        if day < 10:
            strCFG = strCFG + ' | \'0' + str(day) + '\''
    strCFG = strCFG + "\n"
    return strCFG


def addFourDigYearsToCFG(strCFG):
    strCFG = strCFG + 'FULLYEAR -> \'0000\''
    for year in range(1, 3000):
        strCFG = strCFG + ' | '
        if year < 10:
            strCFG = strCFG + '\'000'
        elif year < 100:
            strCFG = strCFG + '\'00'
        elif year < 1000:
            strCFG = strCFG + '\'0'
        else:
            strCFG = strCFG + '\''
        strCFG = strCFG + str(year) + '\''
    strCFG = strCFG + "\n"
    return strCFG


def addTwoDigYearsToCFG2(strCFG):
    strCFG = strCFG + 'YEAR -> \'00\''
    for year in range(1, 100):
        strCFG = strCFG + ' | '
        if year < 10:
            strCFG = strCFG + '\'0'
        else:
            strCFG = strCFG + '\''
        strCFG = strCFG + str(year) + '\''
    strCFG = strCFG + "\n"
    return strCFG


def getCFG(strCFG):
    cfg = nltk.CFG.fromstring(strCFG)
    return cfg


def getTokenSubArrays(tokens):
    limit = 5
    sub_arrays = []
    for i in range(0, len(tokens)):
        subarray = [tokens[i]]
        sub_arrays.append(list(subarray))
        j = i + 1
        while j < len(tokens) and j - i < limit:
            subarray.append(tokens[j])
            sub_arrays.append(list(subarray))
            j = j + 1
    return sub_arrays


def print_parses(name, parser, tokens_subarrays):
    print('\n\n**********', name, '**********')
    for subarray in tokens_subarrays:
        try:
            printParsedTrees(parser, subarray)
        except:
            pass


def printParsedTrees(parser, subarray):
    for tree in parser.parse(subarray):
        print(tree)
