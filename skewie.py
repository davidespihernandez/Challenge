#!/usr/bin/python

import sys
import getopt

from algorithm import RPNAlgorithm


# defaults
MAX_EXECUTION_TIME = 995
ALGORITHM = "RPN"
STOP_ON_FIRST = True
VERBOSE = False
ALGORITHMS = {
    "RPN": RPNAlgorithm,
}
USAGE = """python skewie.py <expression> [-t <max execution time ms=1000>] [-g <algorithm=RPN>] [-a] [-v]
-a: return all solutions (not stop on first), by default only the fist is printed
-v: verbose mode, prints more information like elapsed time, total solutions... implies to calculate all solutions
"""


def main(argv):
    max_execution_time = MAX_EXECUTION_TIME
    algorithm = ALGORITHMS.get(ALGORITHM)
    stop_on_first = STOP_ON_FIRST
    verbose = VERBOSE
    try:
        opts, args = getopt.gnu_getopt(
            argv,
            "t:g:av"
        )
    except getopt.GetoptError as e:
        print(USAGE)
        sys.exit(2)
    if len(args) != 1:
        print(USAGE)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-t":
            max_execution_time = int(arg)
        elif opt == "-g":
            algorithm = ALGORITHMS.get(arg)
            if not algorithm:
                print(USAGE)
                sys.exit(2)
        elif opt == "-a":
            stop_on_first = False
        elif opt == "-v":
            verbose = True
    alg = algorithm(max_execution_time, stop_on_first)
    result = alg.solve(args[0])
    print(result.verbose() if verbose else str(result))


if __name__ == "__main__":
    main(sys.argv[1:])
