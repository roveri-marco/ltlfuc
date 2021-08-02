#!/usr/bin/env python3

import subprocess
import resource
import logging

from config import MAX_VIRTUAL_MEMORY
from config import AALTAFBIN
from config import LTLFUCBIN
from config import trpppBIN

def read_done(filename):
    done = set([])
    with open(filename, "r") as f:
        d = f.readlines()
        for l in d:
            done.add(l.strip())
            pass
    return done

def limit_virtual_memory():
    # The tuple below is of the form (soft limit, hard limit). Limit only
    # the soft part so that the limit can be increased later (setting also
    # the hard limit would prevent that).
    # When the limit cannot be changed, setrlimit() raises ValueError.
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

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


def run_ltlfuc(fname, script, timeout=None, use_sat=False):
    # subprocess.Popen('ulimit -v 1024; ls', shell=True)
    command = list([LTLFUCBIN])
    command.append("-int")
    command.append("-dynamic")
    command.append("-source")
    command.append(script)
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
        nfn = ""
        if use_sat:
            nfn = fname + "_sat_out"
        else:
            nfn = fname + "_bdd_out"
        with open(nfn, "w") as o:
            o.write("Timeout: {}\n".format(timeout))
        logging.warning("Timeout for {}: {}".format(fname, str(err)))
        return 1
    return 0
    pass


def run_trppp(fname, timeout=None):
    # subprocess.Popen('ulimit -v 1024; ls', shell=True)
    command = list([trpppBIN])
    command.append("-f")
    command.append("ltl")
    command.append("-u")
    command.append("-g")
    command.append("ltl")
    command.append("-a")
    command.append("proof")
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
