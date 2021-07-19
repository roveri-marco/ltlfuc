#! /usr/bin/env python3

import logging
import os
import subprocess
import tempfile

#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

import resource

from config import LTLFUCBIN, LTLFUCBENCHMARKS, LTLFUCSATBENCHMARKSD, LTLFUCSATBENCHMARKSE, MAX_VIRTUAL_MEMORY, TIMEOUT

def limit_virtual_memory():
    # The tuple below is of the form (soft limit, hard limit). Limit only
    # the soft part so that the limit can be increased later (setting also
    # the hard limit would prevent that).
    # When the limit cannot be changed, setrlimit() raises ValueError.
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))


NUSMVSHELLCMDB="set on_failure_script_quits; time; echo; go; time; echo; get_ltlf_ucore; time; echo; quit;"

NUSMVSHELLCMDS="set on_failure_script_quits; time; echo; go; time; echo; get_ltlf_ucore -s -k 50; time; echo; quit;"

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
        with open(fname + "_out", "w") as o:
            o.write("Timeout: {}\n".format(timeout))
        logging.warning("Timeout for {}: {}".format(fname, str(err)))
        return 1
    return 0
    pass


if __name__ == '__main__':
    done = set([])
    err = set([])
    SAT=True
    with tempfile.NamedTemporaryFile(mode="w") as tmp:
        if SAT:
            tmp.write(NUSMVSHELLCMDS + "\n")
        else:
            tmp.write(NUSMVSHELLCMDB + "\n")
        try:
            with open(LTLFUCBENCHMARKS, "r") as inf:
                benchfiles = inf.readlines()
                for b in benchfiles:
                    if b not in done:
                        logging.info("Executing LTLFUC on file {}".format(b))
                        b = b.strip()
                        r = run_ltlfuc(b, tmp.name, timeout=TIMEOUT, use_sat=SAT)
                        if r == 0:
                            done.add(b)
                        else:
                            err.add(b)
                    else:
                        logging.info("Skipping file {} since already solved".format(b))
                    pass
                pass
            pass
        except OSError as error:
            logging.error("Unable to open file {}:{}".format(LTLFUCBENCHMARKS,str(error)))
            exit(1)
        try:
            with open(LTLFUCSATBENCHMARKSD, "w") as inf:
                for f in done:
                    inf.write("{}\n".format(f))

        except OSError as error:
            logging.error("Unable to open file {}:{}".format(LTLFUCSATBENCHMARKSD,str(error)))
            exit(1)
        try:
            with open(LTLFUCSATBENCHMARKSE, "w") as inf:
                for f in err:
                    inf.write("{}\n".format(f))

        except OSError as error:
            logging.error("Unable to open file {}:{}".format(LTLFUCSATBENCHMARKSE,str(error)))
            exit(1)
