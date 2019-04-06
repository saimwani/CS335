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

regToVar=[]
for i in range(0,28):
    regToVar.append("free")

varToReg={}

regReplace=1

def getOffset(name):
    for x in scopeTab:
        if (x.table.get(name)==None):
            continue
        return x.table[name]["offset"]

def getReg():
    for i in range(1, 28):
        if (regToVar[i]=="free"):
            return i
    off=getOffset(regToVar[regReplace])
    f.write("sw " + "$"+ str(regReplace) + "," + "-"+str(off)+"($fp)\n")
    del varToReg[regToVar[regReplace]]
    org=regReplace
    regReplace=(regReplace%27) + 1
    return org




f=open('mips.txt', 'wr')

f.write(".text\n.globl main\n")

for code in codeLines:
    if (len(code) == 2 and code[1]==":"):
        f.write(code[0]+code[1]+"\n")
        if (scopeTab[0].table.get(code[0])!= None):
            scope=scopeTab[0].table[code[0]]["Scope"]
            f.write("addi "+"$sp,"+"$sp,"+"-"+str(scopeTab[scope].table["#total_size"]["type"])+"\n")

    if (len(code) == 5):
        if(code[2][0]!='t' and code[2][0]!='v' and code[4][0]!='t' and code[4][0]!='v'):   #constant, constant
            if (code[3][-2]=="n"):  #integer op
                op=code[3][:-3]
                val=eval(code[2]+op+code[4])
                if (val=="True"):
                    val=1
                elif(val=="False"):
                    val=0

                reg=getReg()
                f.write("addi "+"$"+str(reg)+",$0," + str(val))
                regToVar[reg]=code[0]
                varToReg[code[0]]=reg

            else:   #float operation
                xx=0

        #if(code[2][0]!='t' and code[2][0]!='v' and code[4][0]=='t'):      # first constant second temp

        #if(code[2][0]!='t' and code[2][0]!='v' and code[4][0]='v'):    # first constant second vartemp

        #if(code[2][0]=='t' and code[4][0]!='v' and code[4][0]!='t'):       # first temp second constant

        #if(code[2][0]=='t' and code[4][0]=='t'):  # first temp secoand temp

        #if(code[2][0]=='t' and code[4][0]=='v' ):  # temp, vartemp

        #if(code[2][0]=='v' and code[4][0]!='v' and code[4][0]='t'):  # vartemp, constant

        #if(code[2][0]=='v' and code[4][0]=='t'):  #vartemp, temp

        #if(code[2][0]=='v' and code[4][0]=='v'):  #vartemp , vartemp


























f.close()
