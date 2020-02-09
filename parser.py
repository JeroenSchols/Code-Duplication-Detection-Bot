from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer


def parse_requirements(inputFile):
    """
    parse a high.csv or low.csv file and tokenize it
    returns an array [{'id': string, 'tokens': [string]}]
    """
    req_tokens = []
    for cnt, line in enumerate(inputFile):
        if (cnt == 0): continue  ## ignores the header
        tokens = RegexpTokenizer(r'\w+').tokenize(line.split(',')[1])
        req_tokens.append({'id': line.split(',')[0], 'tokens': [token.lower() for token in tokens]})
    return req_tokens


def remove_stop_words(req_tokens):
    """
    remove stop words (words without relevant meaning) from the list of tokens
    """
    stop_words = set(stopwords.words('english'))
    for req in req_tokens:
        req['tokens'] = [w for w in req['tokens'] if not w in stop_words]
    return req_tokens


def stem_words(req_tokens):
    """
    stem words from the list of tokens
    """
    ps = PorterStemmer()
    for req in req_tokens: req['tokens'] = [ps.stem(w) for w in req['tokens']]
    return req_tokens