def calculate_probabilistic_similarity_matrix(low_tokens, high_tokens):
    """
    calculates a similarity matrix[h[id], l[id]] based on the probabilistic model
     """
    sim_matrix = {}
    print('------')
    print(low_tokens)
    print('------')
    print(high_tokens)
    print('------')
    vocabulary = set()
    for e in high_tokens + low_tokens:
        for w in e['tokens']:
            vocabulary.add(w)

    for h in high_tokens:
        sim_vector = {}
        for l in low_tokens:
            # sim(h, l) = Prod_w in l{P(w|h)}
            pos = 1
            for w in h['tokens']:
                # if w in vocabulary:
                pos *= calc_probability(vocabulary, w, l['tokens'])
            sim_vector[l['id']] = pos
        sim_matrix[h['id']] = sim_vector

    print(sim_matrix)
    print('------')
    return sim_matrix


def calc_probability(vocabulary, word, document):
    occurrences = dict()
    for w in document:
        if w in occurrences.keys():
            occurrences[w] += 1
        else:
            occurrences[w] = 1
    num_words_appearing_once = len([w for w in set(document) if document.count(w) == 1])
    num_words_appearing_twice = len([w for w in set(document) if document.count(w) == 2])
    beta = num_words_appearing_once / (num_words_appearing_once + 2 * num_words_appearing_twice)

    vocab_size = len(vocabulary)
    num_words_in_doc = len(document)
    num_unique_words_in_doc = len(set(document))
    lambd = num_unique_words_in_doc / (num_words_in_doc * vocab_size) * beta

    if word in document:
        return lambd + (document.count(word) - beta) / num_words_in_doc
    else:
        return lambd
