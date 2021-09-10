This directory contains a quick synthesis of the [experimental data](https://drive.google.com/open?id=1eOYGvm3C8sQ-9iyfZ8qx42K54hgrFNTC) taken from the tests run by
Li et al. for their [article published on the Artificial Intelligence journal (2020)](https://doi.org/10.1016/j.artint.2020.103369).

The `main.py` script generates two reports, based on the content of the `AIJ-artifact` directory:
1. `aggregate-verification-results.txt` summarises all the satisfiability checking results;
1. `aggregate-verification-results-UNSAT.txt` lists the sole models that the checkers categorise as unsatisfiable.

In `aggregate-verification-results.txt`, every line corresponds to a model. The data are structured by associating to every model
(identified by their source file path on the left of ` => `):
1. the results of the satisfiability checking (`sat`, `unsat`, `unknow`, `timeout` or `unknowKilled`) for every tool (under the key `results`), with
   * the number of tools returning any of the aforementioned categories (under the key `__aggregates`) and
   * the consensus (decided by the majority of the tools that return either `sat` or `unsat` – `unknow` otherwise, under the key `__consensus`);
1. the source of the model file (under the key `source`).
For example:
```
declare/declare-benchmark/re5k.mxml_run_1_alpha_0_apriori_100-ltl.txt => {'results': {'ltl2sat': 'sat', 'aalta': 'timeout', 'nuxmv': 'sat', 'cdlsc': 'sat', 'aaltaf': 'unknow', '__consensus': 'sat', '__aggregates': {'sat': 3, 'timeout': 1, 'unknow': 1}}, 'source': 'declare/benchmarks/DECLARE-benchmark/re5k.mxml_Run_1_Alpha_0_Apriori_100-LTL.txt'}
```

In `aggregate-verification-results.txt`, every line corresponds to a model such that
1. it is declared as unsatisfiable by the majority of the tools 
1. its model file occurs in the `AIJ-artifact` directory.
The data are structured by associating to every model (identified by their source file path on the left of ` => `)
the results of the satisfiability checking (`sat`, `unsat`, `unknow`, `timeout` or `unknowKilled`) with
* the number of tools returning any of the aforementioned categories (under the key `__aggregates`) and
* the consensus (decided by the majority of the tools that return either `sat` or `unsat` – `unknow` otherwise, under the key `__consensus`).
