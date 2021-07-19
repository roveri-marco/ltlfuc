#! /usr/bin/env python3

# Maximal virtual memory for subprocesses (in bytes).
MAX_VIRTUAL_MEMORY = 4 * 1024 * 1024 * 1024 # 4 GB
# Maximum time per benchmark
TIMEOUT=10*60 # seconds

AALTAFBIN="../../../aaltaf-uc/aaltaf"
LTLFUCBIN="../../../ltlfuc/NuSMV/build/bin/NuSMV"
trpppBIN="../../../trp++uc-v2.1-20150628/bin/trp++uc"

BASEDIR="/home/marco/work/Tools/ltlfuc/etc/AIJ-SAT-explorer/AIJ-artifact"

BENCHMARKS = "aggregate-verification-results-UNSAT.txt"

PROGRAMS = { "aaltaf2aaltafuc" : [ "../../../aaltaf-uc/ltlparser/ltlf2Andltlf/ltlf2Andltlf" ],
             "aaltaf2ltlfuc" : [ "../../../aaltaf-uc/ltlparser/ltlf2Andltlf/ltlf2Andltlf", "-s" ],
             "aaltafuc2trp"    : [ "../../../aaltaf-uc/aaltaf", "-u"],
             "ltlfuc2aaltafuc" : [ "../../../aaltaf-uc/ltlfuc2aaltauc.py"] }

AALTAFBENCHMARKS="aaltafuc.txt"
AALTAFBENCHMARKSD="aaltafuc-done.txt"
AALTAFBENCHMARKSE="aaltafuc-error.txt"
LTLFUCBENCHMARKS="ltlfuc.txt"
LTLFUCBDDBENCHMARKSD="ltlfucbdd-done.txt"
LTLFUCBDDBENCHMARKSE="ltlfucbdd-error.txt"
LTLFUCSATBENCHMARKSD="ltlfucbdd-done.txt"
LTLFUCSATBENCHMARKSE="ltlfucbdd-error.txt"
trpppBENCHMARKS="trppp.txt"
trpppBENCHMARKSD="trppp-done.txt"
trpppBENCHMARKSE="trppp-error.txt"
