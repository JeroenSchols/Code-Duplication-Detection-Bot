def create_confusion_matrix(predicted_trace_links, true_trace_links, low_tokens):
    conf_matrix = {'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0}
    for h in predicted_trace_links:
        for low_req in low_tokens:
            l = low_req['id']
            if (l in predicted_trace_links[h]) & (l in true_trace_links[h]):
                conf_matrix['TP'] += 1
            elif (l in predicted_trace_links[h]) & (l not in true_trace_links[h]):
                conf_matrix['FP'] += 1
            elif l in true_trace_links[h]:
                conf_matrix['TN'] += 1
            else:
                conf_matrix['FN'] += 1
    conf_matrix['recall'] = conf_matrix['TP'] / (conf_matrix['TP'] + conf_matrix['FN'])
    conf_matrix['precision'] = conf_matrix['TP'] / (conf_matrix['TP'] + conf_matrix['FP'])
    conf_matrix['f-measure'] = 2 * conf_matrix['precision'] * conf_matrix['recall'] / (conf_matrix['precision'] + conf_matrix['recall'])
    return conf_matrix
