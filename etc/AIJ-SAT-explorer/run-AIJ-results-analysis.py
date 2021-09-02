# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import re
import matplotlib.pyplot as plt
import json
import sys
from matplotlib.lines import Line2D
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Palatino']})
rc('text', usetex=True)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_RESULTS_DIR = CURRENT_DIR + '/AIJ-SAT-explorer-res/AIJ-SAT-explorer'
OUTPUT_FILE_SUFFIX = '_out'
TIMEOUT_THRESHOLD = 600
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


def retrieve_unsat_core_cardinality(results_file_path, pattern='-- unsat core size: ([0-9]+)', tool='aaltafuc', sat_pattern='^-- The set of formulas is sat$'):
    result_f_object = open(results_file_path, 'r')
    result_report = result_f_object.read()
    cardinality_pattern = re.compile(pattern)
    unsat_card = 0
    # TODO: This is hardcoding.
    if tool == 'aaltafuc':
        unsat_card = cardinality_pattern.search(result_report)
        if unsat_card and unsat_card.group(1):
            unsat_card = int(unsat_card.group(1))
        else:
            unsat_card = 0
    else: # (rr_r_00004) &
        unsat_card = re.findall(pattern, result_report, flags=re.MULTILINE)
        if unsat_card:
            unsat_card = len(unsat_card)
        else:
            unsat_card = 0

    # print("In", results_file_path, "the unsat core cardinality is", unsat_card)

    if unsat_card:
        return unsat_card
    else:
        if re.findall(sat_pattern, result_report, flags=re.MULTILINE):
            raise LookupError("The analysed specification was satisfiable, as per " + results_file_path)
        else:
            raise LookupError("No unsat core cardinality retrieved in file " + results_file_path + " ")


def compute_stats(results={}, tool='aaltafuc',
                  done_tests_file='aaltafuc-done.txt', failed_tests_file="aaltafuc-error.txt",
                  machine_root_path='/home/mroveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
                  timing_pattern='-- Checker total time: ([0-9\\.]+)',
                  unsat_core_cardinality_pattern='-- unsat core size: ([0-9]+)',
                  sat_pattern='^-- The set of formulas is sat$'):
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
                # print("Time not retrieved (due to pre-parsing optimisation?) " + err, file=sys.stderr)
                timing = NOTIME
                pre_parsing_solutions += 1
            if timing != NOTIME:
                try:
                    unsat_card = retrieve_unsat_core_cardinality(
                        results_file_path=results_file_path, pattern=unsat_core_cardinality_pattern, tool=tool,
                        sat_pattern=sat_pattern)
                except LookupError as err:
                    print(err, file=sys.stderr)
                    unsat_card = 0

            result_id = specification_file_path[len(ANALYSIS_RESULTS_DIR):specification_file_path.rfind('.')]
            # print(result_id, "=> clauses:", clauses_count, "; timing:", timing)
            if result_id not in results:
                results[result_id] = {}
            results[result_id][tool] = {"count": clauses_count, "timing": timing, "unsat_core_cardinality": unsat_card}
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


def compute_virtual_best(results, vbest_tool_name='v_best'):
    for test in results:
        best_timing = TIMEOUT
        clauses = 0
        for tool in results[test]:
            if not clauses:
                clauses = results[test][tool]['count']
            if results[test][tool]['timing'] != NOTIME and results[test][tool]['timing'] != TIMEOUT:
                if best_timing > results[test][tool]['timing']:
                    best_timing = results[test][tool]['timing']
        results[test][vbest_tool_name] = {}
        results[test][vbest_tool_name]['timing'] = best_timing
        results[test][vbest_tool_name]['count'] = clauses
    return results


def add_data_to_plot(results, tool='aaltafuc', marker='o', label='aaaltafuc', colour='red'):
    clauses = []
    timings = []
    for test in results:
        if results[test][tool]['timing'] != NOTIME and results[test][tool]['timing'] != TIMEOUT:
            timings.append(results[test][tool]['timing'])
            clauses.append(results[test][tool]['count'])
    if marker in Line2D.filled_markers:
        plt.scatter(clauses, timings, marker=marker, facecolors='none', edgecolors=colour, alpha=0.25, label=label, zorder=3)
    else:
        plt.scatter(clauses, timings, marker=marker, color=colour, alpha=0.3, label=label, zorder=3)
    return


def create_json_preamble(program="AALTA", tool="aaltafuc"):
    return {"preamble": {"program": program, "prog_alias": tool, "benchmark": "Li-et-al-AIJ2020-benchmark"},
            "stats": {}}


def create_json(results, program="AALTA", tool="aaltafuc", outfile_prefix="AIJ-analysis-results-aaltafuc"):
    json_results = create_json_preamble(program=program, tool=tool)
    json_results_w_preproc = create_json_preamble(program=program, tool=tool)

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


def create_noresult_json(program="NuSMV-B", tool="nusmvb", test="no_test", outfile_prefix="AIJ-analysis-results-nusmvb"):
    json_results = create_json_preamble(program=program, tool=tool)

    json_results["stats"][test] = \
        {"status": True,
         "rtime": TIMEOUT_THRESHOLD,
         "clauses": 0}

    json.dump(obj=json_results, indent=2, fp=open(outfile_prefix+".json", 'w'))


def analyse_results(tool='aaltafuc',
                    results={},
                    program='AALTA',
                    machine_root_path='/home/mroveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
                    timing_pattern='-- Checker total time: ([0-9\\.]+)',
                    marker='t',
                    colour='green',
                    unsat_core_cardinality_pattern='-- unsat core size: ([0-9]+)',
                    sat_pattern='^-- The set of formulas is sat$'):
    results, pre_parsing_solutions, timeouts =\
        compute_stats(results=results, tool=tool,
                      done_tests_file=tool + '-done.txt',
                      failed_tests_file=tool + "-error.txt",
                      machine_root_path=machine_root_path,
                      timing_pattern=timing_pattern,
                      unsat_core_cardinality_pattern=unsat_core_cardinality_pattern,
                      sat_pattern=sat_pattern)
    # print(results)
    print(
        tool + " ran into a timeout " + str(timeouts) + " times, " +
        "but found a solution via preprocessing " + str(pre_parsing_solutions) + " times")

    add_data_to_plot(results, tool=tool, marker=marker, label=program, colour=colour)
    # print(create_json(results=results, program=program, tool=tool, outfile_prefix=CURRENT_DIR+"/AIJ-analysis-plots/AIJ-analysis-results-"+tool))
    create_json(results=results, program=program, tool=tool,
                outfile_prefix=CURRENT_DIR + "/AIJ-analysis-plots/AIJ-analysis-results-" + tool)

    return (results, pre_parsing_solutions, timeouts)

def main():
    results = {}
    # AALTAF
    results, pre_parsing_solutions, timeouts =\
        analyse_results(
            tool='aaltafuc',
            program='AALTAF',
            results=results,
            machine_root_path='/home/mroveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
            timing_pattern='-- Checker total time: ([0-9\\.]+)',
            marker='^',
            colour='red',
            unsat_core_cardinality_pattern='-- unsat core size: ([0-9]+)',
            sat_pattern='^-- The set of formulas is sat$')

    results, pre_parsing_solutions, timeouts =\
        analyse_results(
            tool='trppp',
            program='TRP++',
            results=results,
            machine_root_path='/home/marco.roveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
            timing_pattern='Elapsed time ([0-9\\.]+) *s',
            marker='x',
            colour='blue',
            unsat_core_cardinality_pattern='^\\(rr_r_[0-9]*\\) & *$',
            sat_pattern='^Satisfiable$')

    tool = 'v_best'
    results = compute_virtual_best(results, vbest_tool_name=tool)
    create_json(results=results, program='Virtual best', tool=tool,
                outfile_prefix=CURRENT_DIR + "/AIJ-analysis-plots/AIJ-analysis-results-" + tool)
    # print(create_json(results=results, program='V.Best', tool=tool, outfile_prefix=CURRENT_DIR+"/AIJ-analysis-plots/AIJ-analysis-results-"+tool))
    create_json(results=results, program='Virtual best', tool=tool,
                outfile_prefix=CURRENT_DIR + "/AIJ-analysis-plots/AIJ-analysis-results-" + tool)

    create_noresult_json(program="NuSMV-B", tool="nusmvb", test="no_test",
                         outfile_prefix=CURRENT_DIR+"/AIJ-analysis-plots/AIJ-analysis-results-nusmvb")
    create_noresult_json(program="NuSMV-S", tool="nusmvs", test="no_test",
                         outfile_prefix=CURRENT_DIR+"/AIJ-analysis-plots/AIJ-analysis-results-nusmvs")


    plt.grid(True, zorder=5, linestyle='dotted', color='black')
    plt.figure(1)
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel('Clauses')
    ax = plt.gca()
    lg = ax.legend(loc=4, fancybox=True, shadow=True, framealpha=None)
    for lh in lg.legendHandles:
        lh.set_alpha(1)
    fr = lg.get_frame()
    fr.set_lw(1)
    fr.set_alpha(1.0)
    fr.set_edgecolor('black')

    plt.savefig(fname=CURRENT_DIR+"/AIJ-analysis-plots/AIJ-analysis-results-plot-clauses_v_time.pdf", format='pdf')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    ### Then, use mkplot with the commands below. mkplot is downloadable from: https://github.com/alexeyignatiev/mkplot
    ### (mind that I altered the sources of scatter.py here and there!)