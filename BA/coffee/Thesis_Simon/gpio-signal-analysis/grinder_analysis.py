import csv
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

with open('grinder_deltas_unfiltered.csv') as grinder_f:
    csv_reader = csv.reader(grinder_f)
    dataset=[]
    next(csv_reader)
    first = next(csv_reader)
    last = {'row': first, 'time': time.mktime(
            time.strptime(first[0], "%a %b %d %H:%M:%S %Y"))}
    
    block=[]
    for row in csv_reader:
        current = {'row': row, 'time': time.mktime(
            time.strptime(row[0], "%a %b %d %H:%M:%S %Y"))}
        delta = abs(int(current['row'][1]) - int(last['row'][1]))
        if delta < 10000000:
            block.append({'delta': delta, 'ts': current['row'][0], 'time': current['time'], 'value': current['row'][2]})
        else:
            dataset.append(block)
            block = [{'delta': delta, 'ts': current['row'][0], 'time': current['time'], 'value': current['row'][2]}]
        last = current

# hypothesis: coffee was ground when grinder signal is 0 for about 1s,
# the rest of the transitions are noise
groups_not_in_spec = []
for group in dataset:
    follows_spec = False
    for event in group:
        if event['value'] == "1" and event['delta'] > 500000 and event['delta'] < 2000000:
            follows_spec = True
            break
    if not follows_spec:
        groups_not_in_spec.append(group)

print("number of groups: {}, number of groups not in spec: {}".format(len(dataset), len(groups_not_in_spec)))