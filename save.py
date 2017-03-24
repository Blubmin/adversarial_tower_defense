import sys

with open('output.txt','r') as runs:
    with open("{}.csv".format(sys.argv[1]), 'w') as scores:
        for r in runs:
            if "score" not in r:
                continue
            scores.write("{}\n".format(r.split(' ')[-1].split(")")[0]))