#! /usr/bin/env python3

import logging
import os
import tempfile

from utils import limit_virtual_memory
from utils import run_ltlfuc

#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


from config import LTLFUCBIN, LTLFUCBENCHMARKS, LTLFUCBDDBENCHMARKSD, LTLFUCBDDBENCHMARKSE, MAX_VIRTUAL_MEMORY, TIMEOUT


NUSMVSHELLCMDB="set on_failure_script_quits; time; echo; go; time; echo; get_ltlf_ucore; time; echo; quit;"

NUSMVSHELLCMDS="set on_failure_script_quits; time; echo; go; time; echo; get_ltlf_ucore -s -k 50; time; echo; quit;"


if __name__ == '__main__':
    done = set([])
    err = set([])
    SAT=False
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
            with open(LTLFUCBDDBENCHMARKSD, "w") as inf:
                for f in done:
                    inf.write("{}\n".format(f))

        except OSError as error:
            logging.error("Unable to open file {}:{}".format(LTLFUCBDDBENCHMARKSD,str(error)))
            exit(1)
        try:
            with open(LTLFUCBDDBENCHMARKSE, "w") as inf:
                for f in err:
                    inf.write("{}\n".format(f))

        except OSError as error:
            logging.error("Unable to open file {}:{}".format(LTLFUCBDDBENCHMARKSE,str(error)))
            exit(1)
