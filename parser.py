from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize
import contractions


def parse_trace_links(inputFile):
    trace_links = {}
    for cnt, line in enumerate(inputFile):
        if cnt == 0: continue  # ignores the header
        high_id = line.split(',\"')[0]
        low_ids = line.split('\"')[1].split(',')
        if low_ids[0] == '': low_ids = []
        trace_links[high_id] = low_ids
    inputFile.close()
    return trace_links


def parse_and_preprocess_requirements(inputFile):
    req_tokens = parse_requirements(inputFile)
    req_tokens = remove_stop_words(req_tokens)
    req_tokens = stem_words(req_tokens)
    return req_tokens


def parse_requirements(inputFile):
    """
    parse a high.csv or low.csv file and tokenize it
    returns an array [{'id': string, 'tokens': [string]}]
    """
    req_tokens = []
    for cnt, line in enumerate(inputFile):
        if cnt == 0: continue  # ignores the header
        id = line.split(',\"')[0]
        sentence = contractions.fix(str(line.split('\"')[1]))
        tokens = [word.lower() for word in word_tokenize(sentence) if word.isalpha()]
        req_tokens.append({'id': id, 'tokens': tokens})
    inputFile.close()
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
