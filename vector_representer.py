import math
from scipy import spatial


def vectorize(low_tokens, high_tokens):
    master_vocab = create_master_vocab(low_tokens, high_tokens)
    low_tokens = set_vector_repesentation(low_tokens, master_vocab)
    high_tokens = set_vector_repesentation(high_tokens, master_vocab)
    return low_tokens, high_tokens

def create_master_vocab(low_tokens, high_tokens):
    """
    creates a dictionary of words present in low and high- tokens
    for every word in low_tokens union high_tokens
    master_vocab[word] = log2 (n / d)
    where n is the total number of requirements
    where d is the number of requirements containing word
    """
    n = len(low_tokens) + len(high_tokens)
    count = {}
    for req in low_tokens + high_tokens:
        for token in set(req['tokens']):
            if token in count:
                count[token] = count[token] + 1
            else:
                count[token] = 1

    master_vocab = {}
    for token in count:
        master_vocab[token] = math.log2(float(n) / float(count[token]))

    return master_vocab


def set_vector_repesentation(req_tokens, master_vocab):
    """
    sets a vector representation for each requirement in correspondence with the master vocabulary
    req['vector'][word] = tf * master_vocab[word]
    where tf is the frequency of word in req
    """
    for req in req_tokens:
        vector = {}
        for word in master_vocab:
            count = 0
            for token in req['tokens']:
                if token == word:
                    count = count + 1
            vector[word] = count * master_vocab[word]
        req['vector'] = vector
    return req_tokens


def calc_similarity_matrix(low_tokens, high_tokens):
    """
    calculates a similarity matrix[h[id], l[id]] based on cosine similarity
    """
    sim_matrix = {}
    for h in high_tokens:
        sim_vector = {}
        for l in low_tokens:
            sim_vector[l['id']] = 1 - spatial.distance.cosine(list(l['vector'].values()), list(h['vector'].values()))
        sim_matrix[h['id']] = sim_vector
    return sim_matrix