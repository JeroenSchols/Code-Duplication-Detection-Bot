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
            elif (l_id in predicted_trace_links[h_id]) & (l_id not in true_trace_links[h_id]):
                conf_matrix['FP'] += 1
            elif l_id in true_trace_links[h_id]:
                conf_matrix['TN'] += 1
            else:
                conf_matrix['FN'] += 1

    conf_matrix['recall'] = conf_matrix['TP'] / (conf_matrix['TP'] + conf_matrix['FN'])
    conf_matrix['precision'] = conf_matrix['TP'] / (conf_matrix['TP'] + conf_matrix['FP'])
    conf_matrix['f-measure'] = 2 * conf_matrix['precision'] * conf_matrix['recall'] / (conf_matrix['precision'] + conf_matrix['recall'])

    return conf_matrix
