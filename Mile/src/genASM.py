import pickle
import os
import sys
with open('scopeTabDump', 'rb') as handle:
    scopeTab  = pickle.load(handle)

with open("code.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]
j=0
codeLines=[]
for i in content:
    codeLines.append([])
    for x in i.split():
        codeLines[j].append(x)
    j+=1
regToVar={}
varToReg={}

f=open('mips.txt', 'wr')

f.write(".text\n.globl main\n")

for code in codeLines:
    if (len(code) == 2 and code[1]==":"):
        f.write(code[0]+code[1]+"\n")






f.close()
