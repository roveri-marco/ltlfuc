import math
import os
import re
import matplotlib.pyplot as plt
import json
import sys
from matplotlib.lines import Line2D
from matplotlib import rc
from scipy import interpolate

rc('font', **{'family': 'serif', 'serif': ['Palatino']})
rc('text', usetex=True)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_RESULTS_DIR = CURRENT_DIR + '/AIJ-SAT-explorer-res/AIJ-SAT-explorer'
ANALYSIS_PLOTS_DIR = CURRENT_DIR + '/AIJ-analysis-plots'
TIMEOUT_THRESHOLD = 600
TIMEOUT = 10000
NO_ANSWER_TIME = 5001
NOTIME = 5000
NO_UNSAT_CORE_FOUND = -1
TIMING_SENSITIVITY_THRESHOLD = 0.000001
BELOW_TIMING_SENSITIVITY_THRESHOLD = 0.005
INTERPOLATION_ADJUSTMENT_LIMIT = 0.02
CATEGORIES = [
    # "/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/forobots",
    # "/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska",
    # "/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier",
    # "/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/acacia",
    # "/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/schuppan",
    # "/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/anzu",
    # "/AIJ-artifact/nasa-boeing/benchmarks/nasa-boeing",
    # "/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf"
    #
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/acacia/demo-v3/demo-v3_cl/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska/lift/lift/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska/lift/lift_b/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska/lift/lift_b_f/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska/lift/lift_b_f_l/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska/lift/lift_b_l/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska/lift/lift_f/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska/lift/lift_f_l/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/alaska/lift/lift_l/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/anzu/amba/amba_c/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/anzu/amba/amba_cl/',  # Changed from '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/anzu/amba/amba_c_l/'
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/anzu/genbuf/genbuf/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/anzu/genbuf/genbuf_c/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/anzu/genbuf/genbuf_cl/',  # Changed from '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/anzu/genbuf/genbuf_c_l/'
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/forobots/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/counter/counter/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/counter/counterCarry/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/counter/counterCarryLinear/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/counter/counterLinear/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n',  # Changed from '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n/', to encompass n* directories (hence, larger sets)
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/schuppan/O1formula/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/schuppan/O2formula/',
    '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/schuppan/phltl/',  # Changed from '/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/schuppan/O2formula/phltl/', which had no results of use to us
    '/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/C100/',
    '/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/'
]

OTHER_CATEGORY = "Other"

class Tool:
    def __init__(self, tool_codename, tool_label, tool_filename_id,
                 plot_marker='', plot_colour='',
                 retr_timing_pattern='', retr_uc_cardinality_pattern='', retr_sat_pattern='', retr_unknown_pattern='',
                 retr_outfile_suffix=''):
        self.tool_codename = tool_codename
        self.tool_label = tool_label
        self.tool_filename_id = tool_filename_id
        self.plot_marker = plot_marker
        self.plot_colour = plot_colour
        self.retr_timing_pattern = retr_timing_pattern
        self.retr_uc_cardinality_pattern = retr_uc_cardinality_pattern
        self.retr_sat_pattern = retr_sat_pattern
        self.retr_unknown_pattern = retr_unknown_pattern
        self.retr_outfile_suffix = retr_outfile_suffix


TOOLS = {
    'aaltafuc': Tool(tool_codename='aaltafuc',
                     tool_label='AALTAF',
                     tool_filename_id='AALTAF',
                     plot_marker='^',
                     plot_colour='red',
                     retr_timing_pattern='-- Checker total time: ([0-9\\.]+)',
                     retr_uc_cardinality_pattern='-- unsat core size: ([0-9]+)',
                     retr_sat_pattern='^-- The set of formulas is sat$',
                     retr_unknown_pattern='^-- The set of LTLf formulas is UNKNOWN$',
                     retr_outfile_suffix='_out'),
    'trppp': Tool(tool_codename='trppp',
                  tool_label='TRP++',
                  tool_filename_id='TRPPP',
                  plot_marker='|',
                  plot_colour='brown',
                  retr_timing_pattern='Elapsed time ([0-9\\.]+) *s',
                  retr_uc_cardinality_pattern='^\\(rr_r_[0-9]*\\) & *$',
                  retr_sat_pattern='^Satisfiable$',
                  retr_unknown_pattern='^-- The set of LTLf formulas is UNKNOWN$',
                  retr_outfile_suffix='_out'),
    'ltlfuc_sat': Tool(tool_codename='ltlfuc_sat',
                       tool_label='NuSMV-S',
                       tool_filename_id='NuSMVS',
                       plot_marker='x',
                       plot_colour='blue',
                       retr_timing_pattern='elapse: [0-9\\.]+ seconds, total: ([0-9\\.]+) seconds',
                       retr_uc_cardinality_pattern='UC Prime implicant #0\n[\t ]*(rr_r_[0-9]*.*)',
                       retr_sat_pattern='^Satisfiable$',
                       retr_unknown_pattern='^-- The set of LTLf formulas is UNKNOWN$',
                       retr_outfile_suffix='_sat_out'),
    'ltlfuc_bdd': Tool(tool_codename='ltlfuc_bdd',
                       tool_label='NuSMV-B',
                       tool_filename_id='NuSMVB',
                       plot_marker='D',
                       plot_colour='orange',
                       retr_timing_pattern='elapse: [0-9\\.]+ seconds, total: ([0-9\\.]+) seconds',
                       retr_uc_cardinality_pattern='-- UC Prime implicant #0\n\t(rr_r_[0-9]*=TRUE.*$)',
                       retr_sat_pattern='^Satisfiable$',
                       retr_unknown_pattern='^-- The set of LTLf formulas is UNKNOWN$',
                       retr_outfile_suffix='_bdd_out')
}
V_BEST_TOOL = Tool(tool_codename='v_best',
                   tool_label='Virtual best',
                   tool_filename_id='v_best',
                   plot_colour='green',
                   plot_marker='H')
NO_TOOL = Tool(tool_codename='none',
               tool_label='None',
               tool_filename_id='none',
               plot_colour='grey')


def output_file_suffix(tool='aaltafuc'):
    return TOOLS[tool].retr_outfile_suffix


def count_clauses(specification_file_path):
    '''Count the number of conjuncts 'rr_r_[0-9]*'.
       Notice that the blankspace in the end is necessary '''
    formulae_f_object = open(specification_file_path, 'r')
    formulae = formulae_f_object.readlines()
    clauses = []
    clauses_count = 0
    for formula in formulae:
        formula = formula.strip()
        try:
            formula = formula[:formula.index('(')] # Remove anything that has to do with formulas. Particularly useful in cases like "rr_r_00000 & rr_r_00001 & rr_r_00002 & […] & rr_r_00022 & […] & rr_r_00027 & (((((( not (rr_r_00022))) | (((( always (( not (p6))))) | (((( not (p6))) […]" as we do not want to count rr_r_00022 twice
        except ValueError:  # substring not found
            pass
        # print("Formula: " + formula)
        clauses = re.findall('rr_r_[0-9]*', formula)
        # print("Clauses: " + str(clauses))
        clauses_count += len(clauses)

    if not clauses_count:
        raise LookupError("No clauses retrieved in file " + specification_file_path)

    return clauses_count


def is_result_unknown(result_report, unknown_pattern):
    return len(re.findall(unknown_pattern, result_report, flags=re.MULTILINE)) > 0


def is_specification_declared_as_sat(result_report, sat_pattern):
    return len(re.findall(sat_pattern, result_report, flags=re.MULTILINE)) > 0



def retrieve_time(results_file_path, pattern="Elapsed time ([0-9\\.]+) *s"):
    # print("Looking for time results in file", results_file_path)
    result_f_object = open(results_file_path, 'r')
    result_report = result_f_object.read()
    time_pattern = re.compile(pattern)
    timing = re.findall(pattern, result_report)
    if timing:
        timing = timing[-1]  # There could multiple timings. We catch the last line, in case.
        timing = float(timing)
        return timing
    else:
        raise LookupError("No timing retrieved in file " + results_file_path)


def retrieve_unsat_core_cardinality(results_file_path,
                                    pattern='-- unsat core size: ([0-9]+)',
                                    tool='aaltafuc',
                                    sat_pattern='^-- The set of formulas is sat$',
                                    unknown_pattern='^-- The set of LTLf formulas is UNKNOWN$'):
    result_f_object = open(results_file_path, 'r')
    result_report = result_f_object.read()
    cardinality_pattern = re.compile(pattern)
    unsat_card = NO_UNSAT_CORE_FOUND
    # TODO: This is hardcoding.
    if tool == 'aaltafuc':
        unsat_card = cardinality_pattern.search(result_report)
        if unsat_card and unsat_card.group(1):
            unsat_card = int(unsat_card.group(1))
        else:
            unsat_card = NO_UNSAT_CORE_FOUND
    elif (tool == 'ltlfuc_sat') or (tool == 'ltlfuc_bdd'):
        if is_result_unknown(result_report=result_report, unknown_pattern=unknown_pattern):
            unsat_card = NO_UNSAT_CORE_FOUND
        else:
            unsat_card = re.findall(pattern, result_report, flags=re.MULTILINE)
            if unsat_card:
                unsat_card = unsat_card[0].split(",")
                unsat_card = len(unsat_card)
            else:
                unsat_card = NO_UNSAT_CORE_FOUND
    else:  # (rr_r_00004) &
        unsat_card = re.findall(pattern, result_report, flags=re.MULTILINE)
        if unsat_card:
            unsat_card = len(unsat_card)
        else:
            unsat_card = NO_UNSAT_CORE_FOUND

    # print("In", results_file_path, "the unsat core cardinality is", unsat_card)

    if unsat_card:
        return unsat_card
    else:
        if is_specification_declared_as_sat(result_report=result_report, sat_pattern=sat_pattern):
            raise LookupError("The analysed specification was satisfiable, as per " + results_file_path)
        else:
            raise LookupError("No unsat core cardinality retrieved in file " + results_file_path + " ")


def compute_stats(results={}, tool='aaltafuc',
                  done_tests_file='aaltafuc-done.txt', failed_tests_file="aaltafuc-error.txt",
                  machine_root_path='$HOME/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
                  timing_pattern='-- Checker total time: ([0-9\\.]+)',
                  unsat_core_cardinality_pattern='-- unsat core size: ([0-9]+)',
                  sat_pattern='^-- The set of formulas is sat$',
                  unknown_pattern='^-- The set of LTLf formulas is UNKNOWN$'):
    pre_parsing_solutions = 0
    timeouts = 0
    unknowns = 0
    with open(ANALYSIS_RESULTS_DIR + "/" + done_tests_file, 'r') as f:
        unsat_card = NO_UNSAT_CORE_FOUND
        done_test_line = f.readline()
        while done_test_line:
            done_test_line = done_test_line.strip()
            done_test_line = done_test_line[done_test_line.startswith(machine_root_path) and len(machine_root_path):]
            # print(done_test_line)
            specification_file_path = ANALYSIS_RESULTS_DIR + '/' + done_test_line
            clauses_count = count_clauses(specification_file_path)
            results_file_path = specification_file_path + output_file_suffix(tool)
            try:
                # print("Retrieving time from:", results_file_path, "for tool", tool)
                timing = retrieve_time(results_file_path, timing_pattern)
            except LookupError as err:
                print("Time not retrieved (due to pre-parsing optimisation?) " + str(err), file=sys.stderr)
                timing = NOTIME
                pre_parsing_solutions += 1
            except FileNotFoundError as err:
                print("Time not retrieved (due to missing output file)? " + str(err), file=sys.stderr)
                timing = NOTIME
                unknowns += 1
            if timing != NOTIME:
                try:
                    unsat_card = retrieve_unsat_core_cardinality(
                        results_file_path=results_file_path, pattern=unsat_core_cardinality_pattern, tool=tool,
                        sat_pattern=sat_pattern, unknown_pattern=unknown_pattern)
                    if unsat_card == NO_UNSAT_CORE_FOUND:
                        unknowns += 1
                        # timing = NO_ANSWER_TIME
                except LookupError as err:
                    # print(err, file=sys.stderr)  #  Shush!
                    pass

            result_id = specification_file_path[len(ANALYSIS_RESULTS_DIR):specification_file_path.rfind('.')]
            # print(result_id, "=> clauses:", clauses_count, "; timing:", timing)
            if result_id not in results:
                results[result_id] = {}
            results[result_id][tool] = {'clauses': clauses_count, "timing": timing, "unsat_core_cardinality": unsat_card}
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

            results[result_id][tool] = {
                'clauses': clauses_count,
                "timing": TIMEOUT,
                "unsat_core_cardinality": NO_UNSAT_CORE_FOUND}

            timeouts += 1

            failed_test_line = f.readline()
    f.close()
    return (results, pre_parsing_solutions, timeouts, unknowns)


def compute_virtual_best(results, vbest_tool_name=V_BEST_TOOL.tool_codename, csv_outfile=ANALYSIS_PLOTS_DIR+'/AIJ-results_virtual-best_info.csv'):
    csv_f = open(csv_outfile, 'w')
    csv_f.write('Test;Clauses;BestTime;BestPerformer;MinUnSATCore;MinUnSATFinder\n')
    absolute_minimum_timing = TIMEOUT
    for test in results:
        best_timing = TIMEOUT
        min_unsat_core_cardinality = None
        min_unsat_core_finder = ''
        best_performer = ''
        clauses = 0
        for tool in results[test]:
            if results[test][tool]['unsat_core_cardinality'] != NO_UNSAT_CORE_FOUND and \
                    results[test][tool]['timing'] != TIMEOUT and \
                    (min_unsat_core_cardinality is None or
                     results[test][tool]['unsat_core_cardinality'] < min_unsat_core_cardinality or
                     results[test][tool]['unsat_core_cardinality'] == min_unsat_core_cardinality and
                     results[test][tool]['timing'] != NOTIME and
                     results[test][tool]['timing'] < best_timing
                    ):
                min_unsat_core_cardinality = results[test][tool]['unsat_core_cardinality']
                min_unsat_core_finder = tool
            clauses = results[test][tool]['clauses']
            if results[test][tool]['timing'] != NOTIME and \
                    results[test][tool]['unsat_core_cardinality'] != NO_UNSAT_CORE_FOUND and \
                    results[test][tool]['timing'] != TIMEOUT and \
                    (results[test][tool]['timing'] < best_timing or \
                     results[test][tool]['timing'] == best_timing and \
                     results[test][tool]['unsat_core_cardinality'] < min_unsat_core_cardinality
                    ):
                if best_timing > results[test][tool]['timing']:
                    best_timing = results[test][tool]['timing']
                    best_performer = tool
                if TIMING_SENSITIVITY_THRESHOLD < best_timing < absolute_minimum_timing:
                    absolute_minimum_timing = best_timing
        results[test][vbest_tool_name] = {}
        results[test][vbest_tool_name]['timing'] = best_timing
        results[test][vbest_tool_name]['clauses'] = clauses
        results[test][vbest_tool_name]['unsat_core_cardinality'] = min_unsat_core_cardinality
        results[test][vbest_tool_name]['min_unsat_core_finder'] = min_unsat_core_finder
        results[test][vbest_tool_name]['best_performer'] = best_performer

        # csv_f.write('Test;Clauses;BestTime;BestPerformer;MinUnSATCore;MinUnSATFinder\n')
        csv_f.write(test + ";")
        csv_f.write(str(clauses) + ";")
        csv_f.write(str(best_timing) + ";")
        csv_f.write(best_performer + ";")
        csv_f.write(str(min_unsat_core_cardinality) + ";")
        csv_f.write(min_unsat_core_finder + "\n")
        # print("Test:", test, "- Virtual best:", results[test][vbest_tool_name])

    return (absolute_minimum_timing, results)


def add_data_to_clausesVtime_plot(results, figure_seq_num=1, tool='aaltafuc', marker='o', label='aaaltafuc', colour='red', filename_prefix=''):
    clauses = []
    timings = []
    for test in results:
        if test.startswith(filename_prefix):
            if results[test][tool]['timing'] != NOTIME \
                    and results[test][tool]['timing'] != TIMEOUT \
                    and results[test][tool]['unsat_core_cardinality'] != NO_UNSAT_CORE_FOUND:
                timings.append(results[test][tool]['timing'])
                clauses.append(results[test][tool]['clauses'])

    plt.figure(figure_seq_num)  # Clauses-v-time
    alpha_line = (0.4 if not filename_prefix else 0.5)  # With fewer data points, increase the opacity
    alpha_shapes = (0.75 if not filename_prefix else 0.8)  # With fewer data points, increase the opacity
    if marker in Line2D.filled_markers:
        plt.scatter(clauses, timings, marker=marker, facecolors='none', edgecolors=colour, alpha=alpha_line, label=label, zorder=5)
    else:
        plt.scatter(clauses, timings, marker=marker, color=colour, alpha=alpha_shapes, label=label, zorder=5)


def setup_data_for_unsatcore_scatter_plot(results, tool_0='aaltafuc', tool_1='trppp', figure_num=2, filename_prefix=''):
    x = []
    y = []
    limit_x = 0
    limit_y = 0
    tool_0_wins = 0
    tool_1_wins = 0
    draws = 0
    newx = 0
    newy = 0

    for test in results:
        if test.startswith(filename_prefix):
            # print(test, tool_0, results[test][tool_0], tool_1, results[test][tool_1])
            if results[test][tool_0]['unsat_core_cardinality'] == NO_UNSAT_CORE_FOUND or \
                    results[test][tool_1]['unsat_core_cardinality'] == NO_UNSAT_CORE_FOUND:
                pass  # Exclude pairs in which one of the two tools was unable to find an unsat core
            else:
                newx = results[test][tool_0]['unsat_core_cardinality']
                newy = results[test][tool_1]['unsat_core_cardinality']
                if newx < newy:
                    tool_0_wins += 1
                elif newx == newy:
                    draws += 1
                else:
                    tool_1_wins += 1

                x.append(newx)
                y.append(newy)
                if newx > limit_x:
                    limit_x = newx
                if newy > limit_y:
                    limit_y = newy

                # print(test, tool_0, newx, tool_1, newy)

    plt.figure(figure_num)  # unSAT-core cardinality scatter
    plt.xlim(0, limit_x + 1)
    plt.ylim(0, limit_y + 1)
    plt.scatter(x=x, y=y, alpha=0.15, zorder=5)

    print(filename_prefix+"/" if filename_prefix else "Overall/", tool_0, "Vs", tool_1 + ":",
          "\n  The unSAT core found by", tool_0, "has the lowest cardinality in", tool_0_wins, "cases;",
          "\n  the unSAT core found by", tool_1, "has the lowest cardinality in", tool_1_wins, "cases;",
          "\n  the cardinality of the found unSAT cores is the same for both tools in", draws, "cases.")


def create_json_preamble(program="AALTA", tool="aaltafuc"):
    return {"preamble": {"program": program, "prog_alias": tool, "benchmark": "Li-et-al-AIJ2020-benchmark"},
            "stats": {}}


def create_json(results, program="AALTA", tool="aaltafuc", outfile_prefix="AIJ-analysis-results-aaltafuc",
                test_filename_prefix=''):
    json_results = create_json_preamble(program=program, tool=tool)
    json_results_w_preproc = create_json_preamble(program=program, tool=tool)

    for test in results:
        if test.startswith(test_filename_prefix):
            json_results["stats"][test] =\
                {"status":
                     False if results[test][tool]["timing"] == TIMEOUT or results[test][tool]["timing"] == NOTIME \
                        else True,
                        # or results[test][tool]["unsat_core_cardinality"] == NO_UNSAT_CORE_FOUND else True,
                 "rtime": results[test][tool]["timing"],
                 "clauses": results[test][tool]['clauses']}
            json_results_w_preproc["stats"][test] = \
                {"status":
                     False if results[test][tool]["timing"] == TIMEOUT else True,
                 "rtime": results[test][tool]["timing"] if results[test][tool]["unsat_core_cardinality"] != NO_UNSAT_CORE_FOUND else NO_ANSWER_TIME,
                 "clauses": results[test][tool]['clauses']}
    json.dump(obj=json_results, indent=2, fp=open(outfile_prefix+".json", 'w'))
    json.dump(obj=json_results_w_preproc, indent=2, fp=open(outfile_prefix+"_w_preproc.json", 'w'))
    return json.dumps(
        json_results, indent=2
    )


def create_noresult_json(
        program="NuSMV-B", tool="nusmvb", test="no_test", outfile_prefix="AIJ-analysis-results-nusmvb"):
    json_results = create_json_preamble(program=program, tool=tool)

    json_results["stats"][test] = \
        {"status": True,
         "rtime": TIMEOUT_THRESHOLD,
         "clauses": 0}

    json.dump(obj=json_results, indent=2, fp=open(outfile_prefix+".json", 'w'))


def create_csv(results, output_file):
    csv_f = open(output_file, 'w')
    csv_f.write('dir;test;clauses')
    # Write the header
    for test in results:
        for tool in results[test]:
            csv_f.write(';'+tool+"_unsat_core_cardinality"+";"+tool+'_timing'+";"+tool+"_terminated_OK")
        break
    csv_f.write('\n')

    for test in results:
        clauses = NO_UNSAT_CORE_FOUND
        testdir = test[:test.rindex('/')]
        testname = test[test.rindex('/') + 1:]
        csv_f.write(testdir+";"+testname)

        for tool in results[test]:
            if clauses == NO_UNSAT_CORE_FOUND:
                clauses = results[test][tool]['clauses']
                csv_f.write(';'+str(clauses))

            result_found = results[test][tool]['timing'] != NOTIME and \
                           results[test][tool]['timing'] != TIMEOUT and \
                           results[test][tool]['unsat_core_cardinality'] != NO_UNSAT_CORE_FOUND
            # csv_f.write(';'+tool+"_unsat_core_cardinality"+";"+tool+'_timing'+";"+tool+"_terminated_OK")
            csv_f.write(';' + str(results[test][tool]["unsat_core_cardinality"]))
            csv_f.write(';' + str(results[test][tool]['timing']))
            csv_f.write(';' + str(result_found))

        csv_f.write("\n")


def create_csv_best_per_category(results, test_filename_prefixes=CATEGORIES, vbest_tool_name=V_BEST_TOOL.tool_codename, criteria=['best_performer', 'min_unsat_core_finder'], csv_outfile=ANALYSIS_PLOTS_DIR+'/AIJ-results_virtual-best_info_per-category.csv'):
    all_tools = [x for x in TOOLS.keys()] + [NO_TOOL.tool_codename]  # Including the “None” tool
    min_cl = max_cl = avg_cl = 0

    test_filename_prefixes = [''] + test_filename_prefixes  # Including the “catch-all” category
    total_tests_counter = {x: 0 for x in test_filename_prefixes}
    clauses_stats = {x: {'min': 0, 'max': 0, 'avg': 0} for x in test_filename_prefixes}

    tool_best_counters = {x: {} for x in test_filename_prefixes}
    for test_filename_prefix in test_filename_prefixes:
        tool_best_counters[test_filename_prefix] = {x: {} for x in all_tools}
        for tool in all_tools:
            for criterion in criteria:
                tool_best_counters[test_filename_prefix][tool][criterion] = 0
                tool_best_counters[test_filename_prefix][tool][criterion] = 0

    retrieve_stats = True
    for criterion in criteria:
        for test_filename_prefix in test_filename_prefixes:  # Computational complexity is definitely improvable. I know
            (best_performances_per_tool, total, min_cl, max_cl, avg_cl) = \
                get_best_performers(criterion, results, test_filename_prefix, vbest_tool_name, retrieve_stats)
            for tool in best_performances_per_tool:  # Write
                tool_best_counters[test_filename_prefix][tool][criterion] = best_performances_per_tool[tool]
            total_tests_counter[test_filename_prefix] = total
            if retrieve_stats:
                clauses_stats[test_filename_prefix]['min'] = min_cl
                clauses_stats[test_filename_prefix]['max'] = max_cl
                clauses_stats[test_filename_prefix]['avg'] = avg_cl
        retrieve_stats = False

    csv_f = open(csv_outfile, 'w')
    csv_f.write("category;total;min-clauses;max-clauses;avg-clauses")
    # Write the header
    for tool in all_tools:
        tool_label = NO_TOOL.tool_label if tool not in TOOLS else TOOLS[tool].tool_label
        csv_f.write(";" + tool_label + "@min-UC" +
                    ";" + tool_label + "@min-UC[%]" +
                    ";" + tool_label + "@min-timing" +
                    ";" + tool_label + "@min-timing%")
    csv_f.write('\n')
    for test_filename_prefix in test_filename_prefixes:
        csv_f.write(build_category_label_from_path_prefix(test_filename_prefix))
        csv_f.write(';')
        csv_f.write(str(total_tests_counter[test_filename_prefix]))
        csv_f.write(';')
        csv_f.write(str(clauses_stats[test_filename_prefix]['min']))
        csv_f.write(';')
        csv_f.write(str(clauses_stats[test_filename_prefix]['max']))
        csv_f.write(';')
        csv_f.write("%0.2f" % clauses_stats[test_filename_prefix]['avg'])
        for tool in all_tools:
            csv_f.write(";" + str(tool_best_counters[test_filename_prefix][tool]['min_unsat_core_finder']) +
                        ";%0.2f" % (tool_best_counters[test_filename_prefix][tool]['min_unsat_core_finder'] / total_tests_counter[test_filename_prefix] * 100.0) +
                        ";" + str(tool_best_counters[test_filename_prefix][tool]['best_performer']) +
                        ";%0.2f" % (tool_best_counters[test_filename_prefix][tool]['best_performer'] / total_tests_counter[test_filename_prefix] * 100.0))
        csv_f.write('\n')


def analyse_results(tool='aaltafuc',
                    results={},
                    program='AALTA',
                    machine_root_path='$HOME/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
                    timing_pattern='-- Checker total time: ([0-9\\.]+)',
                    marker='t',
                    colour='green',
                    unsat_core_cardinality_pattern='-- unsat core size: ([0-9]+)',
                    sat_pattern='^-- The set of formulas is sat$',
                    unknown_pattern='^-- The set of LTLf formulas is UNKNOWN$'):
    results, pre_parsing_solutions, timeouts, unknowns =\
        compute_stats(results=results, tool=tool,
                      done_tests_file=tool + '-done.txt',
                      failed_tests_file=tool + "-error.txt",
                      machine_root_path=machine_root_path,
                      timing_pattern=timing_pattern,
                      unsat_core_cardinality_pattern=unsat_core_cardinality_pattern,
                      sat_pattern=sat_pattern,
                      unknown_pattern=unknown_pattern)
    # print(results)
    print(
        tool + " ran into a timeout " + str(timeouts) + " times, " +
        "could not find a solution " + str(unknowns) + " times, " +
        "found a solution via preprocessing " + str(pre_parsing_solutions) + " times")

    # add_data_to_clausesVtime_plot(results, tool=tool, marker=marker, label=program, colour=colour)
    # print(create_json(results=results, program=program, tool=tool, outfile_prefix=ANALYSIS_PLOTS_DIR+"/AIJ-analysis-results-"+tool))
    # create_json(results=results, program=program, tool=tool,
    #             outfile_prefix=ANALYSIS_PLOTS_DIR+"/AIJ-analysis-results-" + tool)

    return (results, pre_parsing_solutions, timeouts, unknowns)



def setup_figure_common():
    plt.grid(True, zorder=5, linestyle='dotted', color='black')


def setup_clauses_v_time_figure(figure_num=1):
    plt.figure(figure_num)  # Clauses-v-time
    setup_figure_common()
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel('\# input LTL$_\\textrm{f}$ clauses')
    plt.xlim(7.25/10, 1.425*TIMEOUT/10)  # Forged the hard way
    plt.ylim(200*TIMING_SENSITIVITY_THRESHOLD, 1.125*TIMEOUT/10)  # Forged the hard way
    ax = plt.gca()
    lg = ax.legend(loc=4, fancybox=True, shadow=True, framealpha=None)
    for lh in lg.legendHandles:
        lh.set_alpha(1)
    fr = lg.get_frame()
    fr.set_lw(1)
    fr.set_alpha(1.0)
    fr.set_edgecolor('black')


def setup_unsat_core_scatter_figure(tool_0='aaltafuc', tool_1='trppp', figure_num=2):
    plt.figure(figure_num)  # unSAT-core cardinality scatter
    setup_figure_common()
    plt.xlabel(tool_0)
    plt.ylabel(tool_1)
    ax = plt.gca()
    ax.axline([0, 0], [1, 1], color='black', linestyle='dotted')



def replace_timings_under_sensitivity_threshold_with_minimum(results, min_timing):
    for test in results:
        for tool in results[test]:
            if results[test][tool]['timing'] < TIMING_SENSITIVITY_THRESHOLD:
                print("The reported timing for tool " + tool + " on " + test +
                      " goes below the sensitivity threshold (" + str(results[test][tool]['timing']) +
                      "). Approximating to interpolation: " + str(float(min_timing)))
                results[test][tool]['timing'] = float(min_timing)
    return results


def interpolate_timings_under_sensitivity_threshold(results, categories):
    # Forces the interpolation to be a value below 0.01 (the actual sensitivity threshold for NuSMV-S and NuSMV-B)
    def adjust_interpolation(interpolation):
        if interpolation >= INTERPOLATION_ADJUSTMENT_LIMIT:
            interpolation = re.sub('0\.0?', '', str(interpolation))
            interpolation = interpolation.replace('.', '')
            interpolation = float("0.00" + interpolation)
        if math.isnan(interpolation) or interpolation == 0.0:
            interpolation = BELOW_TIMING_SENSITIVITY_THRESHOLD
        return interpolation

    category_sequences = {x: {} for x in categories+[OTHER_CATEGORY]}
    category_tool_interpolators = {x: {} for x in categories+[OTHER_CATEGORY]}

    def find_category(test_filename):
        for category in categories:
            if test_filename.startswith(category):
                return category
        print(test_filename + " belongs to no category!")
        return OTHER_CATEGORY

    # Build up the data structure to interpolate values
    for test in results:
        category = find_category(test)
        for tool in results[test]:
            if results[test][tool]['timing'] >= TIMING_SENSITIVITY_THRESHOLD and \
                    results[test][tool]['timing'] <= TIMEOUT_THRESHOLD:
                if tool not in category_sequences[category]:
                    category_sequences[category][tool] = {'clauses': [], 'timing': []}
                category_sequences[category][tool]['clauses'].append(results[test][tool]['clauses'])
                category_sequences[category][tool]['timing'].append(results[test][tool]['timing'])

    # Create interpolators
    for category in categories+[OTHER_CATEGORY]:
        for tool in category_sequences[category]:
            if len(category_sequences[category][tool]['timing']) > 5:
                category_tool_interpolators[category][tool] = interpolate.interp1d(
                    category_sequences[category][tool]['clauses'],
                    category_sequences[category][tool]['timing'],
                    fill_value="extrapolate"
                )

    # Interpolate whenever necessary
    for test in results:
        category = find_category(test)
        for tool in results[test]:
            if results[test][tool]['timing'] < TIMING_SENSITIVITY_THRESHOLD:
                if tool in category_sequences[category]:
                    try:
                        interpolation = abs(category_tool_interpolators[category][tool](results[test][tool]['clauses']))
                        # Refactoring values that are equal to 0.01 or above
                        interpolation = adjust_interpolation(interpolation)

                    except ValueError as err:
                        print("WARNING: " + tool + " on " + test + " does not provide a value for " + str(results[test][tool]['clauses']) + " \n" + " from " + str(category_sequences[category][tool]) + " -- error: " + str(err))
                        interpolation = BELOW_TIMING_SENSITIVITY_THRESHOLD
                else:
                    interpolation = BELOW_TIMING_SENSITIVITY_THRESHOLD
                print("The reported timing for tool " + tool + " on " + test +
                      " goes below the sensitivity threshold (" + str(results[test][tool]['timing']) +
                      "). Approximating to interpolation: " + str(float(interpolation)))
                results[test][tool]['timing'] = float(interpolation)

    return results

def main():
    results = {}

    for tool in TOOLS.values():
        results, pre_parsing_solutions, timeouts, unknowns = \
            analyse_results(
                tool=tool.tool_codename,
                program=tool.tool_label,
                results=results,
                machine_root_path='$HOME/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
                timing_pattern=tool.retr_timing_pattern,
                marker=tool.plot_marker,
                colour=tool.plot_colour,
                unsat_core_cardinality_pattern=tool.retr_uc_cardinality_pattern,
                sat_pattern=tool.retr_sat_pattern,
                unknown_pattern=tool.retr_unknown_pattern)
        create_json(results=results, program=tool.tool_label, tool=tool.tool_codename,
                    outfile_prefix=ANALYSIS_PLOTS_DIR+"/AIJ-analysis-results-" + tool.tool_codename)

    # Interpolate timings falling under the sensitivity threshold
    # results = interpolate_timings_under_sensitivity_threshold(results, CATEGORIES)

    (absolute_minimum_timing, results) = compute_virtual_best(results, vbest_tool_name=V_BEST_TOOL.tool_codename)

    # Replace timings falling under the sensitivity threshold with the absolute minimum timing
    results = replace_timings_under_sensitivity_threshold_with_minimum(results=results,
                                                                       min_timing=absolute_minimum_timing)

    create_json(results=results, program=V_BEST_TOOL.tool_label, tool=V_BEST_TOOL.tool_codename,
                outfile_prefix=ANALYSIS_PLOTS_DIR+"/AIJ-analysis-results-" + V_BEST_TOOL.tool_codename)

    # create_noresult_json(program="NuSMV-B", tool="nusmvb", test="no_test",
    #                      outfile_prefix=ANALYSIS_PLOTS_DIR+"/AIJ-analysis-results-nusmvb")

    create_csv(results=results, output_file=ANALYSIS_PLOTS_DIR+"/AIJ-analysis-results.csv")
    create_csv_best_per_category(results=results)

    figure_seq_num = 0

    # Cross-categorical plot

    # Best performers' pie charts
    best_performance_piechart_filename_template = ANALYSIS_PLOTS_DIR + \
                                               '/AIJ-analysis-results-plot-best-performance-pie_%s.pdf'
    figure_seq_num += 1
    plot_best_piechart(figure_seq_num=figure_seq_num, results=results,
                       best_piechart_filename_template=best_performance_piechart_filename_template,
                       # test_filename_prefix=category,
                       vbest_tool_name=V_BEST_TOOL.tool_codename,
                       criterion='best_performer')

    best_uc_finder_piechart_filename_template = ANALYSIS_PLOTS_DIR + \
                                              '/AIJ-analysis-results-plot-best-ucs-pie_%s.pdf'
    figure_seq_num += 1
    plot_best_piechart(figure_seq_num=figure_seq_num, results=results,
                       best_piechart_filename_template=best_uc_finder_piechart_filename_template,
                       # test_filename_prefix=category,
                       vbest_tool_name=V_BEST_TOOL.tool_codename,
                       criterion='min_unsat_core_finder')

    # Best performers' stacked bar charts
    best_stacked_bar_per_category_filename_template = ANALYSIS_PLOTS_DIR + \
                                                   '/AIJ-analysis-results-plot-best-per-category_%s.pdf'
    figure_seq_num += 1
    plot_best_stacked_bar_per_category(figure_seq_num, results,
                                       best_stacked_bar_per_category_filename_template,
                                       test_filename_prefixes=CATEGORIES,
                                       vbest_tool_name=V_BEST_TOOL.tool_codename,
                                       criterion='best_performer')
    figure_seq_num += 1
    plt.clf()  # Avoids that the previous plot oddly overlaps the next one.

    plot_best_stacked_bar_per_category(figure_seq_num, results,
                                       best_stacked_bar_per_category_filename_template,
                                       test_filename_prefixes=CATEGORIES,
                                       vbest_tool_name=V_BEST_TOOL.tool_codename,
                                       criterion='min_unsat_core_finder')
    plt.clf()  # Avoids that the previous plot oddly overlaps the next one.

    # Overall and category-specific plots

    if not 1:  # Something awful to stop the computation upon need? Comment this line and uncomment the one below.
    # if not 0:
        print(results)
        return

    CATEGORIES.insert(0, '')
    figure_seq_num += 1

    for category in CATEGORIES:
        cat_dir_name = build_category_name_from_path_prefix(category)
        if category and not os.path.isdir(ANALYSIS_PLOTS_DIR + "/" + cat_dir_name):
            os.mkdir(ANALYSIS_PLOTS_DIR + "/" + cat_dir_name)

        print("Analysing", cat_dir_name if category else "overall results")

        uc_cardinality_scatter_filename_template = ANALYSIS_PLOTS_DIR + \
                                                   ('/' + cat_dir_name if category != '' else '') + \
                                                   '/AIJ-analysis-results-plot-unsat-core-cardinality-scatter_%s-v-%s.pdf'
        # best_performance_piechart_filename_template = ANALYSIS_PLOTS_DIR + \
        #                                            ('/' + cat_dir_name if category != '' else '') + \
        #                                            '/AIJ-analysis-results-plot-best-performance-pie_%s.pdf'
        # best_uc_finder_piechart_filename_template = ANALYSIS_PLOTS_DIR + \
        #                                           ('/' + cat_dir_name if category != '' else '') + \
        #                                           '/AIJ-analysis-results-plot-best-ucs-pie_%s.pdf'
        clauses_v_time_filename = ANALYSIS_PLOTS_DIR + \
                                  ('/' + cat_dir_name if category != '' else '') + \
                                  '/AIJ-analysis-results-plot-clauses_v_time.pdf'

        # JSON files
        if category:
            json_filename_prefix = ANALYSIS_PLOTS_DIR + '/' + cat_dir_name + "/AIJ-analysis-results-"
            for tool in TOOLS.values():
                create_json(results=results, program=tool.tool_label, tool=tool.tool_codename,
                            outfile_prefix=json_filename_prefix + tool.tool_codename,
                            test_filename_prefix=category)
            create_json(results=results, program=V_BEST_TOOL.tool_label, tool=V_BEST_TOOL.tool_codename,
                        outfile_prefix=json_filename_prefix + V_BEST_TOOL.tool_codename,
                        test_filename_prefix=category)

        # Plots
        plt.figure(figure_seq_num)  # Clauses-v-time
        for tool in TOOLS.values():
            add_data_to_clausesVtime_plot(results=results,
                                          figure_seq_num=figure_seq_num,
                                          tool=tool.tool_codename,
                                          marker=tool.plot_marker,
                                          label=tool.tool_label,
                                          colour=tool.plot_colour,
                                          filename_prefix=category)
        setup_clauses_v_time_figure(figure_seq_num)
        plt.savefig(fname=clauses_v_time_filename, format='pdf')
        plt.close(figure_seq_num)

        figure_seq_num += 1
        tool_0 = 'aaltafuc'; tool_1 = 'trppp' # unSAT-core cardinality scatter: AALTAF vs TRP++
        plot_unsat_core_cardinality_scatter(figure_seq_num, results, tool_0, tool_1, uc_cardinality_scatter_filename_template, category)

        figure_seq_num += 1
        tool_0 = 'aaltafuc'; tool_1 = 'ltlfuc_sat'  # unSAT-core cardinality scatter: AALTAF vs NuSMV-S
        plot_unsat_core_cardinality_scatter(figure_seq_num, results, tool_0, tool_1, uc_cardinality_scatter_filename_template, category)

        figure_seq_num += 1
        tool_0 = 'aaltafuc'; tool_1 = 'ltlfuc_bdd'  # unSAT-core cardinality scatter: AALTAF vs NuSMV-B
        plot_unsat_core_cardinality_scatter(figure_seq_num, results, tool_0, tool_1, uc_cardinality_scatter_filename_template, category)

        figure_seq_num += 1
        tool_0 = 'trppp'; tool_1 = 'ltlfuc_sat'  # unSAT-core cardinality scatter: NuSMV-S vs TRP++
        plot_unsat_core_cardinality_scatter(figure_seq_num, results, tool_0, tool_1, uc_cardinality_scatter_filename_template, category)

        figure_seq_num += 1
        tool_0 = 'trppp'; tool_1 = 'ltlfuc_bdd'  # unSAT-core cardinality scatter: NuSMV-B vs TRP++
        plot_unsat_core_cardinality_scatter(figure_seq_num, results, tool_0, tool_1, uc_cardinality_scatter_filename_template, category)

        figure_seq_num += 1
        tool_0 = 'ltlfuc_sat'; tool_1 = 'ltlfuc_bdd'  # unSAT-core cardinality scatter: NuSMV-B vs NuSMV-S
        plot_unsat_core_cardinality_scatter(figure_seq_num, results, tool_0, tool_1, uc_cardinality_scatter_filename_template, category)

    # print(results)


def build_category_name_from_path_prefix(category):
    return (category[:-1] if category.endswith("/") else category).replace('/AIJ-artifact/', '')\
        .replace('benchmarks/', '').replace('/', '_')


def build_category_label_from_path_prefix(category):
    return (category[:-1] if category.endswith("/") else category).replace('/AIJ-artifact/', '')\
        .replace('benchmarks/', '').replace('_', ':')


def plot_unsat_core_cardinality_scatter(figure_seq_num, results, tool_0, tool_1,
                                        uc_cardinality_scatter_filename_template,
                                        category):
    plt.figure(figure_seq_num)
    setup_data_for_unsatcore_scatter_plot(results=results, tool_0=tool_0, tool_1=tool_1, figure_num=figure_seq_num,
                                          filename_prefix=category)
    setup_unsat_core_scatter_figure(tool_0=TOOLS[tool_0].tool_label, tool_1=TOOLS[tool_1].tool_label,
                                    figure_num=figure_seq_num)
    tool_filename_ids = sorted([TOOLS[tool_0].tool_filename_id, TOOLS[tool_1].tool_filename_id])
    plt.savefig(fname=uc_cardinality_scatter_filename_template % (tool_filename_ids[0], tool_filename_ids[1]),
                format='pdf')
    plt.close(figure_seq_num)


def plot_best_piechart(figure_seq_num, results, best_piechart_filename_template, test_filename_prefix='',
                       vbest_tool_name=V_BEST_TOOL.tool_codename, criterion='best_performer'):
    plt.figure(figure_seq_num)
    (best_performances_per_tool, total, _, _, _) = get_best_performers(criterion, results, test_filename_prefix, vbest_tool_name)

    labels = [TOOLS[tool].tool_label for tool in best_performances_per_tool.keys() if tool != NO_TOOL.tool_codename]
    labels.append(NO_TOOL.tool_label)
    sizes = [best_performances_per_tool[tool] for tool in best_performances_per_tool.keys()]
    colours = [TOOLS[tool].plot_colour for tool in best_performances_per_tool.keys() if tool != NO_TOOL.tool_codename]
    colours.append(NO_TOOL.plot_colour)
    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    def show_total_in_place_of_percentage(p):
        return round(p * total / 100)

    plt.pie(sizes, labels=labels, colors=colours, startangle=0,
            autopct=show_total_in_place_of_percentage, shadow=True)
    plt.axis('equal')

    plt.savefig(fname=best_piechart_filename_template % (criterion),
                format='pdf')
    plt.close(figure_seq_num)


def get_best_performers(criterion, results, test_filename_prefix, vbest_tool_name, retrieve_stats=False):
    best_performances_per_tool = {}
    total = 0
    min_cl = -1
    max_cl = avg_cl = tot_clauses = 0

    for test in results.keys():
        if test.startswith(test_filename_prefix):
            total += 1
            best_tool = results[test][vbest_tool_name][criterion]
            if not best_tool:
                best_tool = NO_TOOL.tool_codename
            if best_tool not in best_performances_per_tool.keys():
                best_performances_per_tool[best_tool] = 1
            else:
                best_performances_per_tool[best_tool] += 1
            if retrieve_stats:
                clauses = results[test][vbest_tool_name]['clauses']
                tot_clauses += clauses
                if min_cl < 0 or clauses < min_cl:
                    min_cl = clauses
                if max_cl < clauses:
                    max_cl = clauses
    avg_cl = tot_clauses * 1.0 / total
    return (best_performances_per_tool, total, min_cl, max_cl, avg_cl)


def plot_best_stacked_bar_per_category(figure_seq_num, results, best_stacked_bar_per_category_filename_template, test_filename_prefixes=[''],
                       vbest_tool_name=V_BEST_TOOL.tool_codename, criterion='best_performer'):
    plt.figure(figure_seq_num)

    x_labels = list(map(lambda x: build_category_label_from_path_prefix(x), test_filename_prefixes))
    tool_best_counters = {x: [] for x in TOOLS.keys()}
    tool_best_counters[NO_TOOL.tool_codename] = []
    i = 0
    for test_filename_prefix in test_filename_prefixes:  # Computational complexity is definitely improvable. I know
        (best_performances_per_tool, total, _, _, _) = \
            get_best_performers(criterion, results, test_filename_prefix, vbest_tool_name)
        for tool in tool_best_counters:  # Init
            tool_best_counters[tool].append(0)
        for tool in best_performances_per_tool:  # Write
            tool_best_counters[tool][i] = best_performances_per_tool[tool]
        i += 1
    fig, (ax, ax2) = plt.subplots(2, 1, sharex=True)
    width = 0.4  # the width of the bars: can also be len(x) sequence
    ax.grid(visible=True, zorder=5, axis='y', linestyle='dotted', which='both')
    ax2.grid(visible=True, zorder=5, axis='y', linestyle='dotted', which='both')

    bottoms = [0 for _ in tool_best_counters[NO_TOOL.tool_codename]]
    for tool in tool_best_counters:
        tool_label = TOOLS[tool].tool_label if tool != NO_TOOL.tool_codename else NO_TOOL.tool_label
        bar_colour = TOOLS[tool].plot_colour if tool != NO_TOOL.tool_codename else NO_TOOL.plot_colour
        ax.bar(x_labels, tool_best_counters[tool], width, label=tool_label, color=bar_colour,
               bottom=bottoms)
        ax2.bar(x_labels, tool_best_counters[tool], width, label=tool_label, color=bar_colour,
               bottom=bottoms)
        for i in range(0, len(tool_best_counters[tool])):
            bottoms[i] += tool_best_counters[tool][i]

    ax.set_ylim(100, 520)  # RandomConjunction
    ax2.set_ylim(0, 50)  # most of the data

    ax.spines['bottom'].set_visible(False)  # Hide the boundary line below in the plot above
    ax.tick_params(axis='x', which='both', bottom=False)  # Do not show x-ticks in the plot above
    ax2.spines['top'].set_visible(False)  # Hide the boundary line above the plot below

    d = .015  # To be used do draw the cutting lines
    kwargs = dict(transform=ax.transAxes, color='k',  clip_on=False, lw=0.5)
    # ax.plot((-d, +d), (-d, +d), **kwargs)  # Draw cutting lines on the left border line
    ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # Draw cutting lines on the right border line
    kwargs.update(transform=ax2.transAxes)
    # ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # Draw cutting lines on the left border line
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # Draw cutting lines on the right border line

    ax.legend(loc='upper left')
    # ax.set_xticklabels(x_labels, rotation=45)  # For readability purposes
    # Rotate the tick labels and set their alignment.
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    # ax.set_yscale("log")  # For readability purposes
    # ax.set_ylim(bottom=1, top=6*100)
    plt.savefig(fname=best_stacked_bar_per_category_filename_template % criterion, format='pdf', bbox_inches="tight")
    plt.close(figure_seq_num)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    ### Then, use mkplot with the commands below. mkplot is downloadable from: https://github.com/alexeyignatiev/mkplot
    ### (mind that we altered the sources of scatter.py here and there, hence mkplotalt*.py and scatteralt*.py)
