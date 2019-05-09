import sys
from subprocess import run
import os

SEEN_TXT = "data/seen.txt"

def get_agg_res():
    a = 0
    with open(SEEN_TXT, 'r') as f:
        for num in f:
            a += int(num)
    return a

def run_exp(cores, vars=None):

    vars = vars if vars else {}

    env = {
        **os.environ,
        "JAVA_HOME": "/usr/lib/jvm/java-8-openjdk-amd64",
        "OHUA_CORES": str(cores),
        "TEST_TIME": "600", # 10 minutes
        **vars
    }

    run(["./stream-bench.sh", "OHUA_TEST"], env=env)



def main(lo, hi):
    with open('aggregate-results.txt', 'w') as f:
        def report(ty, cores, val):
            print(f"{ty} {cores} {val}", file=f)
        run_exp(1, {"SEQUENTIAL": "true"})
        report('seq', 1, get_agg_res())

        for i in range(lo, hi + 1, 1 if lo <= hi else -1) :
            run_exp(i)
            report('par', i, get_agg_res())


if __name__ == '__main__':
    _,lo, hi = sys.argv
    main(int(lo), int(hi))
