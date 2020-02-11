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

    print(f"Hello world, running with matchtype {match_type}!")

    # Read input low-level requirements and count them (ignore header line).
    with open("/input/low.csv", "r") as inputfile:
        print(f"There are {len(inputfile.readlines()) - 1} low-level requirements")

    '''
    This is where you should implement the trace level logic as discussed in the 
    assignment on Canvas. Please ensure that you take care to deliver clean,
    modular, and well-commented code.
    '''

    low_tokens = parser.parse_and_preprocess_requirements(open("/input/low.csv", "r"))
    high_tokens = parser.parse_and_preprocess_requirements(open("/input/high.csv", "r"))

    low_tokens, high_tokens = vector_representer.vectorize(low_tokens, high_tokens)

    if match_type <= 2 and False:
        sim_matrix = vector_representer.calc_similarity_matrix(low_tokens, high_tokens)
    else:
        sim_matrix = probabilistic_model.calculate_probabilistic_similarity_matrix(low_tokens, high_tokens)

    # if match_type <= 3:
    predicted_trace_links = trace_link_generator.generate_trace_links(sim_matrix, match_type)
    # else:
    #     predicted_trace_links = trace_link_generator.generate_trace_links_probablistic(low_tokens, high_tokens, match_type)
    write_output_file(predicted_trace_links)

    true_trace_links = parser.parse_trace_links(open("/input/links.csv", "r"))

    conf_matrix = evaluator.create_confusion_matrix(predicted_trace_links, true_trace_links, low_tokens)
    print(conf_matrix)
