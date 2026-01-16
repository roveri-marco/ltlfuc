# Experiments
This directory contains 
1. a synthesis of the [experimental data](https://drive.google.com/open?id=1eOYGvm3C8sQ-9iyfZ8qx42K54hgrFNTC) taken from the tests run by
Li et al. for their [article published on the Artificial Intelligence journal (2020)](https://doi.org/10.1016/j.artint.2020.103369) to identify **inconsistent specifications**, and
1. the scripts and data used for the **experimental evaluation** of the LTLf unsatisfiable-core detection algorithms shown in the paper entitled “[Computing unsatisfiable cores for LTLf specifications](https://doi.org/10.48550/arXiv.2203.04834)”.

## Inconsistent specifications
The `run-AIJ-SoTA-results-analysis.py` script generates two reports, based on the content of the `AIJ-artifact` directory:
1. `aggregate-verification-results.txt` summarises all the satisfiability checking results;
1. `aggregate-verification-results-UNSAT.txt` lists the sole specifications that the checkers categorise as unsatisfiable.

In `aggregate-verification-results.txt`, every line corresponds to a specification. The data are structured by associating to every specification
(identified by their source file path on the left of ` => `):
1. the results of the satisfiability checking (`sat`, `unsat`, `unknow`, `timeout` or `unknowKilled`) for every tool (under the key `results`), with
   * the number of tools returning any of the aforementioned categories (under the key `__aggregates`) and
   * the consensus (decided by the majority of the tools that return either `sat` or `unsat` – `unknow` otherwise, under the key `__consensus`);
1. the source of the specification file (under the key `source`).
For example:
```
declare/declare-benchmark/re5k.mxml_run_1_alpha_0_apriori_100-ltl.txt => {'results': {'ltl2sat': 'sat', 'aalta': 'timeout', 'nuxmv': 'sat', 'cdlsc': 'sat', 'aaltaf': 'unknow', '__consensus': 'sat', '__aggregates': {'sat': 3, 'timeout': 1, 'unknow': 1}}, 'source': 'declare/benchmarks/DECLARE-benchmark/re5k.mxml_Run_1_Alpha_0_Apriori_100-LTL.txt'}
```

In `aggregate-verification-results.txt`, every line corresponds to a specification such that
1. it is declared as unsatisfiable by the majority of the tools, and 
1. its specification file occurs in the `AIJ-artifact` directory.
The data are structured by associating to every specification (identified by their source file path on the left of ` => `)
the results of the satisfiability checking (`sat`, `unsat`, `unknow`, `timeout` or `unknowKilled`) with
* the number of tools returning any of the aforementioned categories (under the key `__aggregates`) and
* the consensus (decided by the majority of the tools that return either `sat` or `unsat` – `unknow` otherwise, under the key `__consensus`).

## Experimental evaluation
The `run-LTLfUC-results-analysis.py` script generates detailed reports and plots illustrating the performance of four unsatisfiable-core detecting algorithms run on the subset of specifications above (taking only those for which consensus is reached):
1. AALTAF;
1. NuSMV-B;
1. NuSMV-S;
1. TRP++.

It generates output files and plots in [AIJ-analysis-plots](https://github.com/roveri-marco/ltlfuc/tree/aij-check-explorer/etc/AIJ-SAT-explorer/AIJ-analysis-plots).
