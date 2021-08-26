# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import re
import matplotlib.pyplot as plt
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_RESULTS_DIR = CURRENT_DIR + '/AIJ-SAT-explorer-res/AIJ-SAT-explorer'
OUTPUT_FILE_SUFFIX = '_out'
TIMEOUT = 10000
NOTIME = -100


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
                print("XXXX", err)
                timing = NOTIME

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

            failed_test_line = f.readline()
    f.close()

    return results


def add_data_to_plot(results, tool='aaltafuc', marker='o', label='aaaltafuc'):
    clauses = []
    timings = []
    for test in results:
        clauses.append(results[test][tool]['count'])
        timings.append(results[test][tool]['timing'])
    plt.scatter(clauses, timings, marker=marker, color='black', alpha=0.25, label=label)
    return



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    results = compute_stats(tool='aaltafuc', done_tests_file='aaltafuc-done.txt',
                            failed_tests_file="aaltafuc-error.txt",
                            machine_root_path='/home/mroveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
                            timing_pattern='-- Checker total time: ([0-9\\.]+)')
    # print(results)
    #

    add_data_to_plot(results, tool='aaltafuc', marker='s', label="aaltafuc")

    results = compute_stats(results, tool='trppp', done_tests_file='trppp-done.txt',
                            failed_tests_file="trppp-error.txt",
                            machine_root_path='/home/marco.roveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/',
                            timing_pattern='Elapsed time ([0-9\\.]+) *s')
    print(results)

    # clauses = []
    # timings = []
    # for test in results:
    #     clauses.append(results[test]['trppp']['count'])
    #     timings.append(results[test]['trppp']['timing'])
    # plt.scatter(clauses, timings, marker='+', color='black')

    add_data_to_plot(results, tool='trppp', marker='x', label='trppp')

    # with open(ANALYSIS_RESULTS_DIR + '/trppp-done.txt', 'r') as f:
    #     TEST_MACHINE_ROOT_PATH = "/home/marco.roveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/"
    #     done_test_line = f.readline()
    #     while done_test_line:
    #         done_test_line = done_test_line.strip()
    #         done_test_line = done_test_line[done_test_line.startswith(TEST_MACHINE_ROOT_PATH) and len(TEST_MACHINE_ROOT_PATH):]
    #         specification_file_path = ANALYSIS_RESULTS_DIR + '/' + done_test_line
    #         results_file_path = specification_file_path + OUTPUT_FILE_SUFFIX
    #         clauses_count = count_clauses(specification_file_path)
    #         try:
    #             timing = retrieve_time(results_file_path, pattern="Elapsed time ([0-9\\.]+) *s")
    #         except LookupError as err:
    #             print("XXXX", err)
    #         print(specification_file_path, "=> clauses:", clauses_count, "; timing:", timing)
    #         done_test_line = f.readline()

    # with open(ANALYSIS_RESULTS_DIR + '/aaltafuc-done.txt', 'r') as f:
    #     machine_root_path = "/home/mroveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/"
    #     done_test_line = f.readline()
    #     while done_test_line:
    #         done_test_line = done_test_line.strip()
    #         done_test_line = done_test_line[done_test_line.startswith(machine_root_path) and len(machine_root_path):]
    #         # print(done_test_line)
    #         specification_file_path = ANALYSIS_RESULTS_DIR + '/' + done_test_line
    #         results_file_path = specification_file_path + OUTPUT_FILE_SUFFIX
    #         clauses_count = count_clauses(specification_file_path)
    #         try:
    #             timing = retrieve_time(results_file_path, pattern="-- Checker total time: ([0-9\\.]+)")
    #         except LookupError as err:
    #             print("XXXX", err)
    #
    #         result_id = specification_file_path[len(ANALYSIS_RESULTS_DIR):specification_file_path.rfind('.')]
    #         print(result_id, "=> clauses:", clauses_count, "; timing:", timing)
    #         if result_id not in results:
    #             results[result_id] = {}
    #         results[result_id]['aaltafuc'] = {"count": clauses_count, "timing": timing}
    #         done_test_line = f.readline()
    # f.close()
    #
    # print(results)

    plt.style.use('seaborn-whitegrid')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Time (s)')
    plt.xlabel('Clauses')
    plt.legend()

    plt.show()