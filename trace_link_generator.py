def generate_trace_links(sim_matrix, match_type, option):
    """
    generate a dictionary of trace links
    trace_links[high_id] = [low_id1, low_id2, ...]
    """
    # Matchings with vector-calculated sim_matrix
    if match_type == 0:
        return non_zero_trace_links(sim_matrix)
    elif match_type == 1:
        return absolute_trace_links(sim_matrix, option)
    elif match_type == 2:
        return relative_trace_links(sim_matrix, option)
    # Matchings with probability-calculated sim_matrix
    elif match_type == 3:
        return top_x_trace_links(sim_matrix, option)
    elif match_type == 4:
        return absolute_trace_links(sim_matrix, option)
    elif match_type == 5:
        return relative_trace_links(sim_matrix, option)
    else:
        print("match type not found")


def non_zero_trace_links(sim_matrix):
    """
    high_id is linked with low_id if and only if their similarity is non-zero
    """
    trace_links = {}
    for h_id in sim_matrix:
        links = []
        for l_id in sim_matrix[h_id]:
            if sim_matrix[h_id][l_id] > 0:
                links.append(l_id)
        trace_links[h_id] = links
    return trace_links


def absolute_trace_links(sim_matrix, threshold):
    """
    high_id is linked with low_id if and only if their similarity is greater than 0.25 (or threshold if provided)
    """
    if threshold is None:
        threshold = 0.25

    trace_links = {}
    for h_id in sim_matrix:
        links = []
        for l_id in sim_matrix[h_id]:
            if sim_matrix[h_id][l_id] >= threshold:
                links.append(l_id)
        trace_links[h_id] = links
    return trace_links


def relative_trace_links(sim_matrix, threshold):
    """
    high_id is linked with low_id if and only if the similarity with low_id is greater than the 0.67 * max_sim
    where max_sim is the highest similarity of any low_id with high_id
    If a different threshold is provided, threshold * max_sim is used
    """
    if threshold is None:
        threshold = 0.67

    trace_links = {}
    for h_id in sim_matrix:
        max_sim = max(list(sim_matrix[h_id].values()))
        links = []
        for l_id in sim_matrix[h_id]:
            if sim_matrix[h_id][l_id] >= threshold * max_sim:
                links.append(l_id)
        trace_links[h_id] = links
    return trace_links


def top_x_trace_links(sim_matrix, amount):
    """
    high_id is linked to exactly {amount} low_ids, namely the ones that have the highest scores in the matrix
    By default amount = 1
    """
    if amount is None:
        amount = 1
    else:
        try:
            amount = int(amount)
        except ValueError as e:
            print("For this match type, the extra option should be an integer; the number of links per document")
            exit(1)

    trace_links = {}
    for h_id in sim_matrix:
        # Sort by value, descending
        options = sorted(sim_matrix[h_id].items(), key=lambda x: x[1], reverse=True)

        # Take the first {amount}
        trace_links[h_id] = [x[0] for x in options[:amount]]
    return trace_links
