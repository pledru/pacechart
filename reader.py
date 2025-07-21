#!/usr/bin/python3

import sys

def read(f):
    entries = []
    with open(f, 'r') as file:
        header = True
        for line in file:
            line = line.strip()
            if header:
                header = False
                continue
            tokens = line.split('\t')
            start = None
            end = None
            distance = None
            stime = None
            for t in tokens:
                if t == '':
                    continue
                if start is None:
                    start = t
                if end is None:
                    end = t
                if distance is None:
                    distance = t
                if stime is None:
                    stime = t
            entry = {'start': start, 'end': end, 'distance': distance, 'stime': stime}
            print(entry)
            entries.append(entry)
    return entries

f = sys.argv[1]
read(f)
