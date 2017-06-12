#!/usr/bin/env python3

# Do NOT change this file!


import sys
import re
import collections

Head = collections.namedtuple("Head", "file line")

def parse(pn):
    ans = collections.defaultdict(str)

    head = None
    for l in open(pn):
        # ignore comments
        if l.startswith("#"):
            continue

        # found a header
        m = re.match("^\[(\S+):(\d+)\]+.*", l)
        if m:
            head = Head._make(m.groups())
            continue

        # collect descriptions
        if head:
            ans[head] += l

    # chomp
    return dict((h, d.strip()) for (h, d) in ans.items())

def say_pass(reason):
    print("\033[1;32mPASS\033[m", reason)

def say_fail(reason):
    print("\033[1;31mFAIL\033[m", reason)

def stat_summary(ans):
    print("Summary:")
    for (h, d) in ans.items():
        desc = d.split("\n")[0]
        print(" %-8s %+4s | %-30s .." % (h.file, h.line, desc))

    if len(ans) >= 5:
        say_pass("found enough bugs")
    else:
        say_fail("found %s bugs, but need at least 5" % len(ans))
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("usage: %s [ex1-answers.txt]" % sys.argv[0])
        sys.exit(1)
    ans = parse(sys.argv[1])
    stat_summary(ans)


if __name__ == "__main__":
    main()
