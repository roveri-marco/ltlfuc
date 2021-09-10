import os
import re

def list_all_result_leaf_dirs(root_dir, the_node, tools, verifications):
    leaf_dir_flag = True
    files_in = []
    for f in os.listdir(the_node):
        the_sub_node = the_node+'/'+f
        if os.path.isdir(the_sub_node):
            leaf_dir_flag = False
            (tools, verifications) = list_all_result_leaf_dirs(root_dir, the_sub_node, tools, verifications)
        elif os.path.isfile(the_sub_node):
            files_in.append(the_sub_node)

    if "results" in the_node and leaf_dir_flag:
        # print(the_node)
        tool_name = the_node[the_node.index("results/") + len("results/"):the_node.index("/", the_node.index("results/")+len("results/"))]
        tool_name_index = tool_name.lower()
        tools.add(tool_name_index)

        for test in files_in:
            test_name = test[len(root_dir+"/"):]
            # At times, the tool name is appended at the end of the file name after a hyphen
            test_name = re.sub(r'-[a-zA-Z0-9]+$', '', test_name)
            source_name = test_name.replace("results/" + tool_name, "benchmarks")
            test_name = test_name.replace("results/" + tool_name + "/", "")
            result = open(test, "r").read().replace("Please insert the LTLf formula", "").strip()
            # print(test_name.lower() + " => " + result)
            satisfiability_result = re.sub(r'[^a-zA-Z]', '', result)
            test_name_index = test_name.lower()
            if test_name_index not in verifications:
                verifications[test_name_index] = {'results': {}, 'source': source_name}
            verifications[test_name_index]['results'][tool_name_index] = satisfiability_result

    return (tools, verifications)

def aggregate_verification_results(verifications):
    for (verification_test, verification_result) in verifications.items():
        consensus = 'unknow'
        majority = 0
        aggregates = {}
        for value in verification_result['results'].values():
            if value not in aggregates:
                aggregates[value] = 1
            else:
                aggregates[value] = aggregates[value] + 1
        for key in aggregates.keys():
            if key not in {'', 'timeout', 'unknow'} and aggregates[key] > majority:
                majority = aggregates[key]
                consensus = key
        verification_result['results']['__consensus'] = consensus
        verification_result['results']['__aggregates'] = aggregates
    return verifications


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = current_dir + '/AIJ-artifact'
    (tools, verifications) = list_all_result_leaf_dirs(root_dir, root_dir, set(), {})
    verifications = aggregate_verification_results(verifications)
    f = open(current_dir + '/aggregate-verification-results.txt', 'w')
    for (verification_test, verification_result) in verifications.items():
        f.write('{} => {}\n'.format(verification_test, str(verification_result)))
    f.flush()
    f.close()
    f = open(current_dir + '/aggregate-verification-results-UNSAT.txt', 'w')
    for (verification_test, verification_result) in verifications.items():
        if verification_result['results']['__consensus'] == 'unsat':
            warning_sign = ""
            if not os.path.isfile(root_dir + "/" + verification_result['source']):
                print("WARNING: " + root_dir + "/" + verification_result['source'] + " does not exist or is no readable file")
                warning_sign = "! "
            else:
                f.write('{}{} => {}\n'.format(warning_sign, verification_result['source'], str(verification_result['results'])))
    f.flush()
    f.close()
