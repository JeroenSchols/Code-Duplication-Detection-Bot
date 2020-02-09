import sys
import parser
import vector_representer
import trace_link_generator


def write_output_file(trace_links):
    """
    outputs the trace links in csv format
    """
    f = open('/output/links.csv', 'w')
    f.write("id,links\n")
    for h in trace_links:
        f.write(h + ",\"" + ','.join(trace_links[h]) + "\"\n")


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
    sim_matrix = vector_representer.calc_similarity_matrix(low_tokens, high_tokens)

    trace_links = trace_link_generator.generate_trace_links(sim_matrix, match_type)

    write_output_file(trace_links)
