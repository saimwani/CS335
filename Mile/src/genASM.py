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
regToVarFloat=[]
for i in range(0,32):
    regToVarFloat.append("free")

varToReg={}
varToRegFloat={}

regReplace=1
regReplaceFloat=0

def getOffset(name):
    for x in scopeTab:
        if (x.table.get(name)==None):
            continue
        return x.table[name]["offset"]

def getReg(a=None):
    if (a==None):
        for i in range(1, 28):
            if (regToVar[i]=="free"):
                return i
        off=getOffset(regToVar[regReplace])
        f.write("sw " + "$"+ str(regReplace) + "," + "-"+str(off)+"($fp)\n")
        del varToReg[regToVar[regReplace]]
        org=regReplace
        regReplace=(regReplace%27) + 1
        return org
    else:
        for i in range(0, 32):
            if (regToVarFloat[i]=="free"):
                return i
        off=getOffset(regToVarFloat[regReplaceFloat])
        f.write("swc1 " + "$f"+ str(regReplaceFloat) + "," + "-"+str(off)+"($fp)\n")
        del varToRegFloat[regToVarFloat[regReplaceFloat]]
        org=regReplaceFloat
        regReplaceFloat=(regReplaceFloat+1)%32
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
                f.write("addi "+"$"+str(reg)+",$0," + str(val)+"\n")
                regToVar[reg]=code[0]
                varToReg[code[0]]=reg


            else:   #float operation
                op=code[3][-5]
                val=eval(code[2]+op+code[4])
                if (val=="True"):
                    val=1
                elif(val=="False"):
                    val=0
                reg=getReg(f)
                f.write("addi "+"$"+str(reg)+",$0," + str(val)+"\n")
                regToVarFloat[reg]=code[0]
                varToRegFloat[code[0]]=reg


        elif(code[2][0]!='t' and code[2][0]!='v' and code[4][0]=='t'):      # constant, temp
                if (code[3][-2]=="n"):  #integer op
                    if(varToReg.get(code[4])==None):
                        reg3=getReg()
                        off=getOffset(code[4])
                        f.write("lw " + "$"+ str(reg3) + "," + "-"+str(off)+"($fp)\n")
                    else:
                        reg2=varToReg[code[4]]

                    reg2=getReg()
                    f.write("addi " + "$"+ str(reg2) + ",$0," +code[2]+"\n")
                    reg1=getReg()
                    




        #if(code[2][0]!='t' and code[2][0]!='v' and code[4][0]='v'):    # constant, vartemp

        #if(code[2][0]=='t' and code[4][0]!='v' and code[4][0]!='t'):       # temp, constant

        #if(code[2][0]=='t' and code[4][0]=='t'):  # temp, temp

        #if(code[2][0]=='t' and code[4][0]=='v' ):  # temp, vartemp

        #if(code[2][0]=='v' and code[4][0]!='v' and code[4][0]='t'):  # vartemp, constant

        #if(code[2][0]=='v' and code[4][0]=='t'):  #vartemp, temp

        #if(code[2][0]=='v' and code[4][0]=='v'):  #vartemp , vartemp


























f.close()
