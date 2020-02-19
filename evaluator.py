def create_confusion_matrix(predicted_trace_links, true_trace_links, low_tokens):
    """
    calculates a confusion matrix based on correctness of predicted trace links and documented trace links
    """
    conf_matrix = {'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0}
    for h_id in predicted_trace_links:
        for low_req in low_tokens:
            l_id = low_req['id']
            if (l_id in predicted_trace_links[h_id]) & (l_id in true_trace_links[h_id]):
                conf_matrix['TP'] += 1
            elif l_id in predicted_trace_links[h_id]:
                conf_matrix['FP'] += 1
            elif l_id in true_trace_links[h_id]:
                conf_matrix['FN'] += 1
            else:
                conf_matrix['TN'] += 1

    conf_matrix['recall'] = conf_matrix['TP'] / (conf_matrix['TP'] + conf_matrix['FN'] + 0.0000000001)
    conf_matrix['precision'] = conf_matrix['TP'] / (conf_matrix['TP'] + conf_matrix['FP'] + 0.0000000001)
    conf_matrix['f-measure'] = 2 * conf_matrix['precision'] * conf_matrix['recall'] / (conf_matrix['precision'] + conf_matrix['recall'] + 0.0000000001)

    return conf_matrix


def print_generated_links(predicted_trace_links, true_trace_links, match_type):
    """"
    Print the generated correct, incorrect and missed trace links as a latex table
    """
    max_links = max([len(set(h + true_trace_links[h_id])) for h_id, h in predicted_trace_links.items()])

    print(f"\\begin{{longtable}}{{c|{'c' * max_links}}}")
    for h_id, h in predicted_trace_links.items():
        line = f"\t{h_id} "
        items = set(h + true_trace_links[h_id])
        items = sorted(items, key=lambda l_id: int(l_id[2:]))
        for l_id in items:
            found = l_id in h
            correct = found and l_id in true_trace_links[h_id]
            line += f" & \\color{{{'green' if correct else 'red' if found else 'black'}}}{{{l_id[2:]}}}"
        line += " \\\\"
        print(line)
    print(f"\t\\caption{{Correctly (green) and incorrectly (red) generated and missed (black) links "
          f"using matching type {match_type} on dataset x}}")
    print("\\end{longtable}")
