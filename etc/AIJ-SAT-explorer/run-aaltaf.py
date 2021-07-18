#! /usr/bin/env python3

import logging
import os
import subprocess

#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

import resource

# Maximal virtual memory for subprocesses (in bytes).
MAX_VIRTUAL_MEMORY = 4 * 1024 * 1024 * 1024 # 4 GB

def limit_virtual_memory():
    # The tuple below is of the form (soft limit, hard limit). Limit only
    # the soft part so that the limit can be increased later (setting also
    # the hard limit would prevent that).
    # When the limit cannot be changed, setrlimit() raises ValueError.
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

AALTAFBIN="../../../aaltaf-uc/aaltaf"
AALTAFBENCHMARKS="aaltafuc.txt"
AALTAFBENCHMARKSD="aaltafuc-done.txt"
AALTAFBENCHMARKSE="aaltafuc-error.txt"

def run_aaltaf(fname, timeout=None, use_blsc=False):
    # subprocess.Popen('ulimit -v 1024; ls', shell=True)
    command = list([AALTAFBIN])
    command.append("-u")
    command.append("-u")
    if use_blsc:
        command.append("-blsc")
    command.append("-f")
    command.append(fname)
    try:
        result = subprocess.run(command,
                                shell=False,
                                stdout=subprocess.PIPE,
                                timeout=timeout,
                                preexec_fn=limit_virtual_memory)
        if (result.returncode != 0):
            logging.error("Failure running {}.".format(fname))
            return 1
        else:
            with open(fname + "_out", "w") as o:
                o.write(result.stdout.decode('utf-8'))
                if result.stderr is not None:
                    o.write(result.stderr.decode('utf-8'))
                logging.info("Succeded in analyzing {}.".format(fname))
    except OSError as error:
        logging.error("Some problems running {}: {}".format(fname, str(error)))
        return 1
    except subprocess.TimeoutExpired as err:
        with open(fname + "_out", "w") as o:
            o.write("Timeout: {}\n".format(timeout))
        logging.warning("Timeout for {}: {}".format(fname, str(err)))
        return 1
    return 0
    pass


if __name__ == '__main__':
    done = set([])
    err = set([])
    TIMEOUT=10*60 # seconds
    USE_BLSC=False
    try:
        with open(AALTAFBENCHMARKS, "r") as inf:
            benchfiles = inf.readlines()
            for b in benchfiles:
                if b not in done:
                    logging.info("Executing aaltaf on file {}".format(b))
                    b = b.strip()
                    r = run_aaltaf(b, timeout=TIMEOUT, use_blsc=USE_BLSC)
                    if r == 0:
                        done.add(b)
                    else:
                        err.add(b)
                else:
                    logging.info("Skipping file {} since already solved".format(b))
                    pass
                pass
            pass
        pass
    except OSError as error:
        logging.error("Unable to open file {}:{}".format(AALTAFBENCHMARKS,str(error)))
        exit(1)
    try:
        with open(AALTAFBENCHMARKSD, "w") as inf:
            for f in done:
                inf.write("{}\n".format(f))

    except OSError as error:
        logging.error("Unable to open file {}:{}".format(AALTAFBENCHMARKSD,str(error)))
        exit(1)
    try:
        with open(AALTAFBENCHMARKSE, "w") as inf:
            for f in err:
                inf.write("{}\n".format(f))

    except OSError as error:
        logging.error("Unable to open file {}:{}".format(AALTAFBENCHMARKSE,str(error)))
        exit(1)
