#! /usr/bin/env python3

import logging
import os

from config import trpppBIN, trpppBENCHMARKS, trpppBENCHMARKSD, trpppBENCHMARKSE, MAX_VIRTUAL_MEMORY, TIMEOUT

from utils import limit_virtual_memory
from utils import run_trppp

#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    done = set([])
    err = set([])
    try:
        with open(trpppBENCHMARKS, "r") as inf:
            benchfiles = inf.readlines()
            for b in benchfiles:
                if b not in done:
                    logging.info("Executing trppp on file {}".format(b))
                    b = b.strip()
                    r = run_trppp(b, timeout=TIMEOUT)
                    if r == 0:
                        done.add(b)
                    else:
                        err.add(b)
                else:
                    logging.info("Skipping file {} since already solved".format(b))
                    pass
                exit(1)
                pass
            pass
        pass
    except OSError as error:
        logging.error("Unable to open file {}:{}".format(trpppBENCHMARKS,str(error)))
        exit(1)
    try:
        with open(trpppBENCHMARKSD, "w") as inf:
            for f in done:
                inf.write("{}\n".format(f))

    except OSError as error:
        logging.error("Unable to open file {}:{}".format(trpppBENCHMARKSD,str(error)))
        exit(1)
    try:
        with open(trpppBENCHMARKSE, "w") as inf:
            for f in err:
                inf.write("{}\n".format(f))

    except OSError as error:
        logging.error("Unable to open file {}:{}".format(trpppBENCHMARKSE,str(error)))
        exit(1)
