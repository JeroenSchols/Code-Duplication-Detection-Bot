def calc_similarity_matrix(low_tokens, high_tokens):
    """
    calculates a similarity matrix[h[id], l[id]] based on the probabilistic model
     """
    sim_matrix = {}
    # Construct the vocabulary of all used words
    vocabulary = set()
    for entry in high_tokens + low_tokens:
        for word in entry['tokens']:
            vocabulary.add(word)

    for high in high_tokens:
        sim_vector = dict()
        for low in low_tokens:
            # sim(high, low) = P(high|low) = Product of P(w|high) for all w in low
            document = low['tokens']
            beta = calc_beta(document)
            lambd = calc_lambda(vocabulary, document, beta)
            probability = 1
            for word in high['tokens']:
                probability *= calc_probability(word, document, lambd, beta)
            sim_vector[low['id']] = probability
        sim_matrix[high['id']] = sim_vector

    return sim_matrix


def calc_probability(word, document, lambd, beta):
    """
    Calculate the probability P(word|document)
    with smoothing of the unigram probability distribution to avoid the zero-frequency problem
    """
    # Calculate P(word|document)
    if word in document:
        return lambd + (document.count(word) - beta) / len(document)
    else:
        return lambd


def calc_lambda(vocabulary, document, beta):
    """
    Calculate interpolation term lambda of a document
    """
    # Calculate interpolation term lambda
    vocab_size = len(vocabulary)
    num_words_in_doc = len(document)
    num_unique_words_in_doc = len(set(document))
    return num_unique_words_in_doc / (num_words_in_doc * vocab_size) * beta


def calc_beta(document):
    """
    Calculate beta by definition of Ney and Essen
    """
    occurrences = {}
    for w in document:
        if w in occurrences.keys():
            occurrences[w] += 1
        else:
            occurrences[w] = 1
    num_words_appearing_once = len([w for w in set(document) if document.count(w) == 1])
    num_words_appearing_twice = len([w for w in set(document) if document.count(w) == 2])
    return num_words_appearing_once / (num_words_appearing_once + 2 * num_words_appearing_twice)
