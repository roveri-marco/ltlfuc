#! /usr/bin/env python3

# Maximal virtual memory for subprocesses (in bytes).
MAX_VIRTUAL_MEMORY = 4 * 1024 * 1024 * 1024 # 4 GB
# Maximum time per benchmark
TIMEOUT=10*60 # seconds

AALTAFHOME="../../../aaltaf-uc.src/"
LTLFUCHOME="../../../ltlfuc.src/"

AALTAFBIN=AALTAFHOME + "aaltaf"
LTLFUCBIN=LTLFUCHOME + "NuSMV/build/bin/NuSMV"
trpppBIN="../../../trp++/bin/trp++uc"

BASEDIR="/home/marco.roveri/aaai21/ltlfuc.src/etc/AIJ-SAT-explorer/AIJ-artifact"

BENCHMARKS = "aggregate-verification-results-UNSAT.txt"

PROGRAMS = { "aaltaf2aaltafuc" : [ AALTAFHOME + "ltlparser/ltlf2Andltlf/ltlf2Andltlf" ],
             "aaltaf2ltlfuc"   : [ AALTAFHOME + "ltlparser/ltlf2Andltlf/ltlf2Andltlf", "-s" ],
             "aaltafuc2trp"    : [ AALTAFHOME + "aaltaf", "-u"],
             "ltlfuc2aaltafuc" : [ AALTAFHOME + "ltlfuc2aaltauc.py"] }

AALTAFBENCHMARKS="aaltafuc.txt"
AALTAFBENCHMARKSD="aaltafuc-done.txt"
AALTAFBENCHMARKSE="aaltafuc-error.txt"
LTLFUCBENCHMARKS="ltlfuc.txt"
LTLFUCBDDBENCHMARKSD="ltlfucbdd-done.txt"
LTLFUCBDDBENCHMARKSE="ltlfucbdd-error.txt"
LTLFUCSATBENCHMARKSD="ltlfucsat-done.txt"
LTLFUCSATBENCHMARKSE="ltlfucsat-error.txt"
trpppBENCHMARKS="trppp.txt"
trpppBENCHMARKSD="trppp-done.txt"
trpppBENCHMARKSE="trppp-error.txt"
