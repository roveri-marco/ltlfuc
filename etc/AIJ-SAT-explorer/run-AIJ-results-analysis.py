# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import re
import matplotlib.pyplot as plt
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_RESULTS_DIR = CURRENT_DIR + '/AIJ-SAT-explorer-res/AIJ-SAT-explorer'
OUTPUT_FILE_SUFFIX = '_out'
TIMEOUT = 10000
NOTIME = 5000


def count_clauses(specification_file_path):
    '''Count the number of conjuncts 'rr_r_[0-9]*'.
       Notice that the blankspace in the end is necessary '''
    formulae_f_object = open(specification_file_path, 'r')
    formula = formulae_f_object.readline().strip()
    clauses = []
    clauses_count = 0
    while formula:
        try:
            formula = formula[:formula.index('(')] # Remove anything that has to do with formulas. Particularly useful in cases like "rr_r_00000 & rr_r_00001 & rr_r_00002 & […] & rr_r_00022 & […] & rr_r_00027 & (((((( not (rr_r_00022))) | (((( always (( not (p6))))) | (((( not (p6))) […]" as we do not want to count rr_r_00022 twice
        except ValueError:  # substring not found
            pass
        # print("Formula: " + formula)
        clauses = re.findall('rr_r_[0-9]*', formula)
        # print("Clauses: " + str(clauses))
        clauses_count += len(clauses)
        formula = formulae_f_object.readline().strip()

    if not clauses_count:
        raise LookupError("No timing retrieved in file " + specification_file_path)

    return clauses_count


def retrieve_time(results_file_path, pattern="Elapsed time ([0-9\\.]+) *s"):
    result_f_object = open(results_file_path, 'r')
    result_report = result_f_object.read()
    time_pattern = re.compile(pattern)
    timing = time_pattern.search(result_report)
    if timing:
        return float(timing.group(1))
    else:
        raise LookupError("No timing retrieved in file " + results_file_path)


def compute_stats(results={}, tool='aaltafuc', done_tests_file='aaltafuc-done.txt', failed_tests_file="aaltafuc-error.txt", machine_root_path='/home/mroveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/', timing_pattern='-- Checker total time: ([0-9\\.]+)'):
    pre_parsing_solutions = 0
    timeouts = 0
    with open(ANALYSIS_RESULTS_DIR + "/" + done_tests_file, 'r') as f:
        done_test_line = f.readline()
        while done_test_line:
            done_test_line = done_test_line.strip()
            done_test_line = done_test_line[done_test_line.startswith(machine_root_path) and len(machine_root_path):]
            # print(done_test_line)
            specification_file_path = ANALYSIS_RESULTS_DIR + '/' + done_test_line
            clauses_count = count_clauses(specification_file_path)
            results_file_path = specification_file_path + OUTPUT_FILE_SUFFIX
            try:
                timing = retrieve_time(results_file_path, timing_pattern)
            except LookupError as err:
                print("Time not retrieved (due to pre-parsing optimisation?)", err)
                timing = NOTIME
                pre_parsing_solutions += 1

            result_id = specification_file_path[len(ANALYSIS_RESULTS_DIR):specification_file_path.rfind('.')]
            # print(result_id, "=> clauses:", clauses_count, "; timing:", timing)
            if result_id not in results:
                results[result_id] = {}
            results[result_id][tool] = {"count": clauses_count, "timing": timing}
            done_test_line = f.readline()
    f.close()

    with open(ANALYSIS_RESULTS_DIR + "/" + failed_tests_file, 'r') as f:
        failed_test_line = f.readline()
        while failed_test_line:
            failed_test_line = failed_test_line.strip()
            failed_test_line = failed_test_line[failed_test_line.startswith(machine_root_path) and len(machine_root_path):]
            specification_file_path = ANALYSIS_RESULTS_DIR + '/' + failed_test_line
            clauses_count = count_clauses(specification_file_path)

            result_id = specification_file_path[len(ANALYSIS_RESULTS_DIR):specification_file_path.rfind('.')]
            if result_id not in results:
                results[result_id] = {}

            results[result_id][tool] = {"count": clauses_count, "timing": TIMEOUT}

            timeouts += 1

            failed_test_line = f.readline()
    f.close()
    return (results, pre_parsing_solutions, timeouts)


def add_data_to_plot(results, tool='aaltafuc', marker='o', label='aaaltafuc', colour='red'):
    clauses = []
    timings = []
    for test in results:
        if results[test][tool]['timing'] != NOTIME and results[test][tool]['timing'] != TIMEOUT:
            timings.append(results[test][tool]['timing'])
            clauses.append(results[test][tool]['count'])
    plt.scatter(clauses, timings, marker=marker, facecolors='none', edgecolors=colour, alpha=0.25, label=label)
    return



def create_json(results, program="AALTA", tool="aaltafuc", outfile_prefix="AIJ-analysis-results-aaltafuc.json"):
    json_results = {"preamble": {"program": program, "prog_alias": tool, "benchmark": "Li-et-al-AIJ2020-benchmark"},
            "stats": {}}
    json_results_w_preproc = {"preamble": {"program": program, "prog_alias": tool, "benchmark": "Li-et-al-AIJ2020-benchmark"},
            "stats": {}}
    for test in results:
        json_results["stats"][test] =\
            {"status":
                 False if results[test][tool]["timing"] == TIMEOUT or results[test][tool]["timing"] == NOTIME else True,
             "rtime": results[test][tool]["timing"],
             "clauses": results[test][tool]["count"]}
        json_results_w_preproc["stats"][test] = \
            {"status":
                 False if results[test][tool]["timing"] == TIMEOUT else True,
             "rtime": results[test][tool]["timing"],
             "clauses": results[test][tool]["count"]}
    json.dump(obj=json_results, indent=2, fp=open(outfile_prefix+".json", 'w'))
    json.dump(obj=json_results_w_preproc, indent=2, fp=open(outfile_prefix+"_w_preproc.json", 'w'))
    return json.dumps(
        json_results, indent=2
    )



def analyse_results(tool='aaltafuc',
                    results={},
                    program='AALTA',
                    machine_root_path='/home/mroveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
                    timing_pattern='-- Checker total time: ([0-9\\.]+)',
                    marker='t',
                    colour='green'):
    results, pre_parsing_solutions, timeouts = compute_stats(results=results, tool=tool,
                                                             done_tests_file=tool + '-done.txt',
                                                             failed_tests_file=tool + "-error.txt",
                                                             machine_root_path=machine_root_path,
                                                             timing_pattern=timing_pattern)
    # print(results)
    print(
        tool + " ran into a timeout " + str(timeouts) + " times, " +
        "but found a solution via preprocessing " + str(pre_parsing_solutions) + " times")

    add_data_to_plot(results, tool=tool, marker=marker, label=tool, colour=colour)
    print(create_json(results=results, program=program, tool=tool, outfile_prefix=CURRENT_DIR+"/AIJ-analysis-plots/AIJ-analysis-results-"+tool))

    return (results, pre_parsing_solutions, timeouts)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    results = {}
    results, pre_parsing_solutions, timeouts =\
        analyse_results(
            tool='aaltafuc',
            program='AALTA',
            results=results,
            machine_root_path='/home/mroveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
            timing_pattern='-- Checker total time: ([0-9\\.]+)',
            marker='H',
            colour='green')

    results, pre_parsing_solutions, timeouts =\
        analyse_results(
            tool='trppp',
            program='TRP++',
            results=results,
            machine_root_path='/home/marco.roveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
            timing_pattern='Elapsed time ([0-9\\.]+) *s',
            marker='^',
            colour='red')

    # results, pre_parsing_solutions, timeouts = compute_stats(results, tool='trppp', done_tests_file='trppp-done.txt',
    #                         failed_tests_file="trppp-error.txt",
    #                         machine_root_path='/home/marco.roveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
    #                         timing_pattern='Elapsed time ([0-9\\.]+) *s')
    # print(results)

    # print(create_json(results=results, tool="trppp", outfile=CURRENT_DIR+"/AIJ-analysis-plots/AIJ-analysis-results-trppp.json"))

    # add_data_to_plot(results, tool='trppp', marker='x', label='trppp', colour="red")

    plt.style.use('seaborn-whitegrid')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel('Clauses')
    plt.legend()

    # plt.show()

    # figure = plt.figure()
    plt.savefig(fname=CURRENT_DIR+"/AIJ-analysis-plots/AIJ-analysis-results-plot-clauses_v_time.pdf", format='pdf')

### Use mkplot with the commands below. mkplot is downloadable from: https://github.com/alexeyignatiev/mkplot
### (mind that I altered the sources of scatter.py here and there!)
# python /home/cdc08x/Code/LTLfUC/mkplot/mkplot.py -l --legend program -p scatter \
#   -t 600 -b pdf \
#   --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
#   --save-to /home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots/AIJ-analysis-results-plot-scatter.pdf '/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots/AIJ-analysis-results-aaltafuc_w_preproc.json' '/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots/AIJ-analysis-results-trppp_w_preproc.json' ### python mkplot.py -l --legend -p scatter prog_alias -t 600 -b pdf --save-to /home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots/cactus.pdf --xlabel "Instances" '/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots/AIJ-analysis-results-aaltafuc.json' '/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots/AIJ-analysis-results-trppp.json'