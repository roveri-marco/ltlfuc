#! /usr/bin/env python3

import logging
import os
import subprocess

PROGRAMS = { "aaltaf2aaltafuc" : [ "../../../aaltaf-uc/ltlparser/ltlf2Andltlf/ltlf2Andltlf" ],
             "aaltaf2ltlfuc" : [ "../../../aaltaf-uc/ltlparser/ltlf2Andltlf/ltlf2Andltlf", "-s" ],
             "aaltafuc2trp"    : [ "../../../aaltaf-uc/aaltaf", "-u"],
             "ltlfuc2aaltafuc" : [ "../../../aaltaf-uc/ltlfuc2aaltauc.py"] }

BASEDIR="/home/marco/work/Tools/ltlfuc/etc/AIJ-SAT-explorer/AIJ-artifact"

BENCHMARKS = "aggregate-verification-results-UNSAT.txt"

def aaltaf2aaltafuc(ifile,ofile):
    command = list(PROGRAMS["aaltaf2aaltafuc"])
    command.append(ifile)
    result = subprocess.run(command, stdout=subprocess.PIPE)
    # print(str(result.stdout.decode('utf-8')))
    if (result.returncode != 0):
        logging.error("Error converting aaltaf 2 aaltafuc {}:{}".format(ifile,str(resul.stderr)))
        exit(1)
    try:
        with open(ofile, "w") as of:
            of.write(result.stdout.decode('utf-8'))
    except OSError as error:
        logging.error("Unable to open file {}:{}".format(benchfile,str(error)))
        exit(1)
    pass

def aaltaf2ltfuc(ifile,ofile):
    command = list(PROGRAMS["aaltaf2ltlfuc"])
    command.append(ifile)
    result = subprocess.run(command, stdout=subprocess.PIPE)
    #print(str(result.stdout.decode('utf-8')))
    if (result.returncode != 0):
        logging.error("Error converting aaltaf 2 ltlfuc {}:{}".format(ifile,str(result.stderr)))
        exit(1)
    try:
        with open(ofile, "w") as of:
            of.write(result.stdout.decode('utf-8'))
    except OSError as error:
        logging.error("Unable to open file {}:{}".format(ofile,str(error)))
        exit(1)
    pass

def aaltafuc2trp(ifile,ofile):
    command = list(PROGRAMS["aaltafuc2trp"])
    command.append("-f")
    command.append(ifile)
    command.append("-p")
    command.append(ofile)
    #print(command)
    result = subprocess.run(command, stdout=subprocess.PIPE)
    #print(result.returncode)
    if (result.returncode != 0):
        logging.error("Error converting aaltafuc 2 trp {}:{}".format(ifile,str(result.stderr)))
        exit(1)

    #print(str(result.stdout.decode('utf-8')))
    pass

def prepare(benchfile):
    aaltafuc = []
    ltlfuc = []
    trpuc = []
    try:
        with open(benchfile, "r") as benchf:
            c = 0
            lines = benchf.readlines()
            for line in lines:
                l = line.split(" ")
                bf = l[0]
                cbf = BASEDIR+"/"+bf
                if os.path.isfile(cbf):
                    fn, fe = os.path.splitext(cbf)
                    print("{} File: {}".format(c, cbf))
                    # Generating aaltafuc
                    print("Generating aaltaf-uc file")
                    out = fn+".aaltafuc"
                    #aaltaf2aaltafuc(cbf, out)
                    aaltafuc.append(out)
                    #print(out)
                    # Generating ltlfuc (aka NuSMV)
                    print("Generating LTLFuc (NuSMV) file")
                    out = fn + ".ltlfuc"
                    #aaltaf2ltfuc(cbf, out)
                    ltlfuc.append(out)
                    # Generating trp++
                    print("Generating TRP++ file")
                    out = fn + ".trpuc"
                    #aaltafuc2trp(fn+".aaltafuc", out)
                    trpuc.append(out)
                else:
                    print("File {} does not exists!".format(bf))

    except OSError as error:
        logging.error("Unable to open file {}:{}".format(benchfile,str(error)))
        exit(1)
    return (aaltafuc, ltlfuc, trpuc)
    pass



if __name__ == '__main__':
    (a,l,t) = prepare(BENCHMARKS)

    for (l,fn) in [(a, "aaltafuc.txt"), (l, "ltlfuc.txt"),
                  (t, "trppp.txt")]:
        with open(fn, "w") as f:
            for i in l:
                f.write("{}\n".format(i))
                pass
            pass
        pass
