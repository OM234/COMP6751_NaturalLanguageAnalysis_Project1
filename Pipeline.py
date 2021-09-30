import nltk
from DateParser import DateParser
from WrittenNumberParser import WrittenNumberParser


# Pipeline used to preprocess and print relevant values
class Pipeline:
    def __init__(self, corpus, fileID):
        self.corpus = corpus
        self.fileID = fileID
        self.tokens = None
        self.number_parser = None
        self.sentences = None
        self.pos_tags = None
        self.date_parser = None

    def preprocess(self):
        print_preprocessing(self.fileID)  # print current file id
        self.tokens = tokenize(self.corpus.raw(self.fileID))
        self.tokens = normalize_numbers(self.tokens)
        self.number_parser = parse_written_numbers(self.tokens)
        self.sentences = split_sentences(self.corpus.raw(self.fileID))
        self.pos_tags = pos_tagging(self.tokens)
        self.date_parser = parse_dates(self.tokens)

    def print_tokens(self):
        print_tokens(self.tokens)

    def print_sentences(self):
        print_sentences(self.sentences)

    def print_pos_tags(self):
        print_pos_tags(self.pos_tags)

    def print_written_numbers(self):
        self.number_parser.print_numbers(self.number_parser)

    def print_dates(self):
        self.date_parser.print_dates()


# print file id
def print_preprocessing(file_id):
    print("\n\n\npreprocessing: {}\n".format(file_id))


def tokenize(raw_text):
    tokens = nltk.word_tokenize(raw_text)  # use nltk to tokenize
    tokenizeToLowerCase(tokens)  # convert tokens to lower case
    tokens = splitTokensAroundForwardSlash(tokens)  # tokenize around forward slashes (for date parsing)
    return tokens


def tokenizeToLowerCase(tokens):
    for i in range(0, len(tokens)):
        lower_case_token = tokens[i].lower()
        tokens[i] = lower_case_token


# for date processing, we may have a token in the form ['01/01/1900']. We convert this to the form
# ['01', '/', '01', '/', '1990', '//'] for date processing. The double slash at the end indicates
# the end of a date
def splitTokensAroundForwardSlash(tokens):
    new_tokens = []
    for i in range(0, len(tokens)):
        token = tokens[i]
        if '/' in token and token.split('/')[0].isdigit():
            tokens_split = token.split('/')
            for splitted in tokens_split:
                new_tokens.append(splitted)
                new_tokens.append('/')
            new_tokens.pop()
            new_tokens.append('//')
        else:
            new_tokens.append(tokens[i])
    return new_tokens


# for number normalization, nltk does an excellent job of preserving numbers with decimals, e.g. ['1.2'], as a single
# token. There is no need to correct for this. Rather, we normalize in order to eventually parse numbers as written
# words. We do this by splitting tokens of numbers with dashes into separate tokens. For example, ['seventy-six']
# becomes ['seventy', 'six']
def normalize_numbers(tokens):
    tokens = splitWordNumbersAroundDashes(tokens)
    return tokens


def splitWordNumbersAroundDashes(tokens):
    split_tokens = []
    for token in tokens:
        if '-' in token:  # if a token contains '-', we check if this needs to be split
            split_token_if_necessary(token, split_tokens)
        else:
            split_tokens.append(token)
    return split_tokens


def split_token_if_necessary(token, tokens):
    split = token.split('-')
    if len(split) > 2:  # either not a number, or not a number which is handled here
        tokens.append(token)
    elif split[1] in getWrittenNumbersBetween1and9():
        tokens.extend((split[0], split[1]))  # add the 2 tokens to the list of tokens, e.g. ('seventy', 'five')


def getWrittenNumbersBetween1and9():
    return ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth',
            'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


# We use the class WrittenNumberParser to parse for written numbers
def parse_written_numbers(tokens):
    writtenNumberParser = WrittenNumberParser(tokens)
    writtenNumberParser.parse_numbers()
    return writtenNumberParser


# nltk is used to tokenize sentences
def split_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences


# nltk is used to tokenize POS tags
def pos_tagging(tokens):
    pos_tags = nltk.pos_tag(tokens)
    return pos_tags


# We use the class DateParser to parse for dates
def parse_dates(tokens):
    date_parser = DateParser(tokens)
    date_parser.parse_dates()
    return date_parser


def print_tokens(tokens):
    print("********** tokens **********")
    for i in range(len(tokens)):
        if i % 10 == 9:
            print('|\n')
        print('|', tokens[i], end=' ')


def print_sentences(sentences):
    print("\n\n********** sentences **********")
    for i in range(0, len(sentences)):
        print('{}) {}'.format(i + 1, sentences[i]))


def print_pos_tags(pos_tags):
    print("\n\n********** POS tags **********")
    for i in range(len(pos_tags)):
        if i % 6 == 5:
            print('\n')
        print(pos_tags[i], end=' ')

