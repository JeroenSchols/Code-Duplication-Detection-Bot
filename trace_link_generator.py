def generate_trace_links(sim_matrix, match_type):
    if match_type == 1:
        return non_zero_trace_links(sim_matrix)
    elif match_type == 2:
        return absolute_trace_links(sim_matrix)
    elif match_type == 3:
        return relative_trace_links(sim_matrix)
    else:
        print("match type not found")


def non_zero_trace_links(sim_matrix):
    trace_links = {}
    for h in sim_matrix:
        links = []
        for l in sim_matrix[h]:
            if sim_matrix[h][l] > 0:
                links.append(l)
        trace_links[h] = links
    return trace_links


def absolute_trace_links(sim_matrix):
    trace_links = {}
    for h in sim_matrix:
        links = []
        for l in sim_matrix[h]:
            if sim_matrix[h][l] >= 0.25:
                links.append(l)
        trace_links[h] = links
    return trace_links


def relative_trace_links(sim_matrix):
    trace_links = {}
    for h in sim_matrix:
        max_sim = max(list(sim_matrix[h].values()))
        links = []
        for l in sim_matrix[h]:
            if sim_matrix[h][l] >= 0.67 * max_sim:
                links.append(l)
        trace_links[h] = links
    return trace_links
