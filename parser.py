def parse_requirements(inputFile):
    """
    parse a high.csv or low.csv file and tokenize it
    returns an array [{'id': string, 'tokens': [string]}]
    """
    req_tokens = []
    for cnt, line in enumerate(inputFile):
        if (cnt == 0): continue ## ignores the header
        tokens = []
        req = {'id': line.split(',')[0], 'tokens': tokens}
        for word in line.split(',')[1].split():
            tokens.append(word.replace('\"', '')) ## removes " character for first and last word in the string
        req_tokens.append(req)
    return req_tokens
