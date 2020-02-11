from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize
import contractions


def parse_trace_links(inputFile):
    """
    parse a links.csv file
    returns a dictionary trace_links where trace_links[high_id] = [low_id1, low_id2, ...]
    """
    trace_links = {}
    for i, line in enumerate(inputFile):
        if i == 0: continue  # ignores the header
        high_id = line.split(',\"')[0]
        low_ids = line.split('\"')[1].split(',')
        if low_ids[0] == '': low_ids = []
        trace_links[high_id] = low_ids
    inputFile.close()
    return trace_links


def parse_and_preprocess_requirements(inputFile):
    """
    parse a high.csv or low.csv file
    removes stop words and stems words
    returns an array [{'id': string, 'tokens': [string]}]
    """
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
    for i, line in enumerate(inputFile):
        if i == 0: continue  # ignores the header
        id = line.split(',\"')[0]

        # takes everything inbetween "" in input file and expands contractions (e.g. couldn't -> could not)
        # stores all alphabetical words in this line in lowercase (only alphabetical to ignore 's, 0000)
        sentence = contractions.fix(line.split('\"')[1])
        tokens = [word.lower() for word in word_tokenize(sentence) if word.isalpha()]

        req_tokens.append({'id': id, 'tokens': tokens})
    inputFile.close()
    return req_tokens


def remove_stop_words(req_tokens):
    """
    remove stop words (words without relevant meaning) from the list of tokens
    """
    stop_words = set(stopwords.words('english'))
    for requirement in req_tokens:
        requirement['tokens'] = [word for word in requirement['tokens'] if not word in stop_words]
    return req_tokens


def stem_words(req_tokens):
    """
    stem words from the list of tokens
    """
    ps = PorterStemmer()
    for requirement in req_tokens: requirement['tokens'] = [ps.stem(word) for word in requirement['tokens']]
    return req_tokens
