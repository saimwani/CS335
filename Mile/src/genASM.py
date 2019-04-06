import pickle
import os
import sys
with open('scopeTabDump', 'rb') as handle:
    scopeTab  = pickle.load(handle)

with open("code.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]
j=0
content2=[]
for i in content:
    content2.append([])
    for x in i.split():
        content2[j].append(x)
    j+=1

