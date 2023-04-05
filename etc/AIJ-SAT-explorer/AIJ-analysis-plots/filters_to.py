#! /usr/bin/env python3
import pandas as pd

table = pd.read_csv("AIJ-analysis-results-failures.csv",sep=";")

t1 = table[table['timeout']==True]
#print(t1)
t2 = t1[t1['tool'] != 'v_best']
#print(t2)
#print(t2[t2['tool'] == 'trppp'])

base = "/home/marco.roveri/aaai21/ltlfuc.src/etc"
with open('trpppto.txt', 'w') as f:
    for i,r in t2[t2['tool'] == 'trppp'].iterrows():
        f.write(base + r['dir'] + "/" + r['test'] + ".trpuc\n")
        pass
    pass

with open('ltlfuc_bddto.txt', 'w') as f:
    for i,r in t2[t2['tool'] == 'ltlfuc_bdd'].iterrows():
        f.write(base + r['dir'] + "/" + r['test'] + ".ltlfuc\n")
        pass
    pass

with open('ltlfuc_satto.txt', 'w') as f:
    for i,r in t2[t2['tool'] == 'ltlfuc_sat'].iterrows():
        f.write(base + r['dir'] + "/" + r['test'] + ".ltlfuc\n")
        pass
    pass

with open('aaltafucto.txt', 'w') as f:
    for i,r in t2[t2['tool'] == 'aaltafuc'].iterrows():
        f.write(base + r['dir'] + "/" + r['test'] + ".aaltafuc\n")
        pass
    pass
