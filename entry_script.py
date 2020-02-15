import sys
import parser
import probabilistic_model
import vector_representer
import trace_link_generator
import evaluator


def write_output_file(trace_links):
    """
    outputs the trace links in csv format
    """
    file = open('/output/links.csv', 'w')
    file.write("id,links\n")
    for h_id in trace_links:
        file.write(h_id + ",\"" + ','.join(trace_links[h_id]) + "\"\n")
    file.close()


if __name__ == "__main__":
    '''
    Entry point for the script
    '''
    if len(sys.argv) < 2:
        print("Please provide an argument to indicate which matcher should be used")
        exit(1)

    match_type = 0

    try:
        match_type = int(sys.argv[1])
    except ValueError as e:
        print("Match type provided is not a valid number")
        exit(1)

    # Third parameter used for configuration of some of our measures provided
    option = None
    if len(sys.argv) >= 3:
        try:
            option = float(sys.argv[2])
        except ValueError as e:
            print("Extra option is not a valid number")
            exit(1)

    print(f"Running with matchtype {match_type}"
          f"{(' and extra option ' + str(option)) if option is not None else ''}!")

    # Parse and prepare the tokens of both documents
    lem_over_stem = False  # when True uses lemmatization instead of stemming
    low_tokens = parser.parse_and_preprocess_requirements(open("/input/low.csv", "r"), lem_over_stem)
    high_tokens = parser.parse_and_preprocess_requirements(open("/input/high.csv", "r"), lem_over_stem)

    if match_type <= 2:
        # Match type that uses vector matching
        low_tokens, high_tokens = vector_representer.vectorize(low_tokens, high_tokens)
        sim_matrix = vector_representer.calc_similarity_matrix(low_tokens, high_tokens)
    else:
        # Match type that uses probabilistic matching
        sim_matrix = probabilistic_model.calc_similarity_matrix(low_tokens, high_tokens)

    # Generate trace links from the similarity matrix
    predicted_trace_links = trace_link_generator.generate_trace_links(sim_matrix, match_type, option)

    # Write the trace links to the output file
    write_output_file(predicted_trace_links)

    # Parse the file with actual human-made trace links
    true_trace_links = parser.parse_trace_links(open("/input/links.csv", "r"))

    # Create and display the confusion matrix between the produced trace links and the human-made trace links
    conf_matrix = evaluator.create_confusion_matrix(predicted_trace_links, true_trace_links, low_tokens)
    print(conf_matrix)
