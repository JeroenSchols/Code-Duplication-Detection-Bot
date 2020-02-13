def generate_trace_links(sim_matrix, match_type):
    """
    generate a dictionary of trace links
    trace_links[high_id] = [low_id1, low_id2, ...]
    """
    return personal_trace_links(sim_matrix, match_type)

    if match_type == 0:
        return non_zero_trace_links(sim_matrix)
    elif match_type == 1:
        return absolute_trace_links(sim_matrix)
    elif match_type == 2:
        return relative_trace_links(sim_matrix)
    elif match_type >= 3:
        return personal_trace_links(sim_matrix, match_type)
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


def absolute_trace_links(sim_matrix):
    """
    high_id is linked with low_id if and only if their similarity is greater than 0.25
    """
    trace_links = {}
    for h_id in sim_matrix:
        links = []
        for l_id in sim_matrix[h_id]:
            if sim_matrix[h_id][l_id] >= 0.25:
                links.append(l_id)
        trace_links[h_id] = links
    return trace_links


def relative_trace_links(sim_matrix):
    """
    high_id is linked with low_id if and only if the similarity with low_id is greater than the 0.67 * max_sim
    where max_sim is the highest similarity of any low_id with high_id
    """
    trace_links = {}
    for h_id in sim_matrix:
        max_sim = max(list(sim_matrix[h_id].values()))
        links = []
        for l_id in sim_matrix[h_id]:
            if sim_matrix[h_id][l_id] >= 0.67 * max_sim:
                links.append(l_id)
        trace_links[h_id] = links
    return trace_links


def personal_trace_links_top_percentage(sim_matrix, match_type):
    trace_links = {}
    for h_id in sim_matrix:
        max_sim = max(list(sim_matrix[h_id].values()))
        links = []
        for l_id in sim_matrix[h_id]:
            if sim_matrix[h_id][l_id] >= match_type / 100.0 * max_sim:
                links.append(l_id)
        trace_links[h_id] = links
    return trace_links


def personal_trace_links_top_x(sim_matrix, match_type):
    trace_links = {}
    for h_id in sim_matrix:
        # Sort by value, descending
        options = sorted(sim_matrix[h_id].items(), key=lambda x: x[1], reverse=True)

        # Take the first few
        trace_links[h_id] = [x[0] for x in options[:match_type]]
    return trace_links


def personal_trace_links(sim_matrix, match_type):
    personal_trace_links_top_x(sim_matrix, match_type)
