#! /usr/bin/env python3

import logging
import os

from utils import limit_virtual_memory
from utils import run_aaltaf

#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

from config import AALTAFBIN, AALTAFBENCHMARKS, AALTAFBENCHMARKSD, AALTAFBENCHMARKSE, MAX_VIRTUAL_MEMORY, TIMEOUT

if __name__ == '__main__':
    done = set([])
    err = set([])
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
