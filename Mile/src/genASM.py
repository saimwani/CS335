import pickle
import os
import sys
with open('scopeTabDump', 'rb') as handle:
    scopeTab  = pickle.load(handle)
basicTypes=["int","float","rune","string","bool"]

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
        if (scopeTab[x].table.get(name)==None):
            continue
        return scopeTab[x].table[name]["offset"]

def getVarOffset(vartemp):
    for x in scopeTab:
        if (scopeTab[x].table.get(vartemp)==None):
            continue
        return scopeTab[x].table[scopeTab[x].table[vartemp]["type"]]["offset"], x

def getType(vartemp):
    for x in scopeTab:
        if (scopeTab[x].table.get(vartemp)==None):
            continue
        if(scopeTab[x].table[scopeTab[x].table[vartemp]["type"]]["type"][0] not in basicTypes):
            return 1
        else:
            return 0


def getReg(a=None):
    if (a==None):
        for i in range(2, 24):
            if (regToVar[i]=="free"):
                return i
        off=getOffset(regToVar[regReplace])
        if(varToReg[regReplace][0]=='t' or not getType(varToReg[regReplace]) ):
            f.write("sw " + "$"+ str(regReplace) + "," + "-"+str(off)+"($fp)\n")
        del varToReg[regToVar[regReplace]]
        org=regReplace
        regReplace=(regReplace%24) + 2
        return org
    else:
        for i in range(0, 32):
            if (regToVarFloat[i]=="free"):
                return i
        off=getOffset(regToVarFloat[regReplaceFloat])
        if(varToRegFloat[regReplaceFloat][0]=='t' or not getType(varToRegFloat[regReplaceFloat]) ):
            f.write("swc1 " + "$f"+ str(regReplaceFloat) + "," + "-"+str(off)+"($fp)\n")
        del varToRegFloat[regToVarFloat[regReplaceFloat]]
        org=regReplaceFloat
        regReplaceFloat=(regReplaceFloat+1)%32
        return org

def writeInstrBin(reg1, reg2, reg3, op):
    if(op=="||" or op=="|"):
        f.write("or "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n")
    elif(op=="&&" or op=="&"):
        f.write("and "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n")
    elif(op=="+"):
        f.write("add "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n")
    elif(op=="-"):
        f.write("sub "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n")
    elif(op=="*"):
        f.write("mult "+"$" +str(reg2)+",$" +str(reg3)+"\n"+ "mflo " +"$"+str(reg1)+"\n")
    elif(op=="/"):
        f.write("div "+"$"+str(reg2)+",$" +str(reg3)+"\n"+"mflo "+"$" + str(reg1)+"\n")
    elif(op=="%"):
        f.write("div "+"$"+str(reg2)+",$" +str(reg3)+"\n"+"mfhi "+"$" + str(reg1)+"\n")
    elif(op==">>"):
        f.write("srav "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n")
    elif(op=="<<"):
        f.write("sllv "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n")
    elif(op=="^"):
        f.write("xor "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n")
    elif(op=="<"):
        f.write("slt "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n")
    elif(op==">"):
        f.write("slt "+"$"+str(reg1)+",$" +str(reg3)+",$" +str(reg2)+"\n")
    elif(op=="<="):
        f.write("slt "+"$"+str(reg1)+",$" +str(reg3)+",$" +str(reg2)+"\n"+"xori " +"$" + str(reg1)+",$"+ str(reg1)+ "1"+ "\n")
    elif(op==">="):
        f.write("slt "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n"+"xori " +"$" + str(reg1)+",$"+ str(reg1)+ "1"+ "\n")
    elif(op=="=="):
        reg4=getReg()
        regToVar[reg4]="free"
        f.write("slt "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n"+"slt " +"$" + str(reg4)+",$"+ str(reg3)+ ",$"+str(reg2)+ "\n")
        f.write("xori " +"$" + str(reg1)+",$"+ str(reg1)+ "1"+ "\n" + "xori " +"$" + str(reg4)+",$"+ str(reg4)+ "1"+ "\n")
        f.write("and "+"$"+str(reg1)+",$" +str(reg4)+",$" +str(reg1)+"\n")
    elif(op=="!="):
        reg4=getReg()
        regToVar[reg4]="free"
        f.write("slt "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n"+"slt " +"$" + str(reg4)+",$"+ str(reg3)+ ",$"+str(reg2)+ "\n")
        f.write("or "+"$"+str(reg1)+",$" +str(reg4)+",$" +str(reg1)+"\n")


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
            if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-3]=='o'):  #integer op
                op=code[3][:-3] if code[3][-3]=="i" else code[3][:-4]
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
                op=code[3][:-5]
                val=eval(code[2]+op+code[4])
                if (val=="True"):
                    val=1
                elif(val=="False"):
                    val=0
                reg=getReg(f)
                f.write("addi "+"$"+str(reg)+",$0," + str(val)+"\n")
                regToVarFloat[reg]=code[0]
                varToRegFloat[code[0]]=reg


        elif(code[2][0]!='t' and code[2][0]!='v' and (code[4][0]=='t' or code[4][0]=='v')):   # constant, temp or constant, vartemp
                if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-3]=='o'):  #integer op or rune op
                    op=code[3][:-3] if code[3][-3]=="i" else code[3][:-4]
                    if(varToReg.get(code[4])==None):
                        reg3=getReg()
                        if(code[4][0]=='t'):
                            off=getOffset(code[4])
                            f.write("lw " + "$"+ str(reg3) + "," + "-"+str(off)+"($fp)\n")
                        else:
                            off, control=getVarOffset(code[4])
                            if(not getType(code[4])):
                                if(control==0):
                                    f.write("lw " + "$"+ str(reg3) + "," + "-"+str(off)+"($gp)\n")
                                else:
                                    f.write("lw " + "$"+ str(reg3) + ","+"-" +str(off)+"($fp)\n")

                            else:
                                if(control==0):
                                    f.write("subi " + "$"+ str(reg3) + "," + "$gp," + str(off)+"\n")
                                else:
                                    f.write("subi " + "$"+ str(reg3) + "," + "$fp," + str(off)+"\n")
                        regToVar[reg3]=code[4]
                        varToReg[code[4]]=reg3
                    else:
                        reg3=varToReg[code[4]]

                    reg2=getReg()
                    f.write("addi " + "$"+ str(reg2) + ",$0," +code[2]+"\n")
                    regToVar[reg2]="free"
                    reg1=getReg()
                    regToVar[reg1]=code[0]
                    varToReg[code[0]]=reg1
                    writeInstrBin(reg1, reg2, reg3, op)


                else:
                    xxxyyy=0



        elif(code[4][0]!='t' and code[4][0]!='v' and (code[2][0]=='t' or code[2][0]=='v')):   # temp, constant or vartemp, constant
                if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-3]=='o'):  #integer op or rune op
                    op=code[3][:-3] if code[3][-3]=="i" else code[3][:-4]
                    if(varToReg.get(code[2])==None):
                        reg2=getReg()
                        if(code[2][0]=='t'):
                            off=getOffset(code[2])
                            f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($fp)\n")
                        else:
                            off, control=getVarOffset(code[2])
                            if(not getType(code[2])):
                                if(control==0):
                                    f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($gp)\n")
                                else:
                                    f.write("lw " + "$"+ str(reg2) + ","+"-" +str(off)+"($fp)\n")

                            else:
                                if(control==0):
                                    f.write("subi " + "$"+ str(reg2) + "," + "$gp," + str(off)+"\n")
                                else:
                                    f.write("subi " + "$"+ str(reg2) + "," + "$fp," + str(off)+"\n")

                        regToVar[reg2]=code[2]
                        varToReg[code[2]]=reg2
                    else:
                        reg2=varToReg[code[2]]

                    reg3=getReg()
                    f.write("addi " + "$"+ str(reg3) + ",$0," +code[4]+"\n")
                    regToVar[reg3]="free"
                    reg1=getReg()
                    regToVar[reg1]=code[0]
                    varToReg[code[0]]=reg1
                    writeInstrBin(reg1, reg2, reg3, op)


                else:
                    xxxyyy=0



        else:  # t,t or t,v, or v,t, or v,v
            if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-3]=='o'):  #integer or rune  op
                op=code[3][:-3] if code[3][-3]=="i" else code[3][:-4]
                if(varToReg.get(code[2])==None):
                    reg2=getReg()
                    if(code[2][0]=='t'):
                        off=getOffset(code[2])
                        f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[2])
                        if(not getType(code[2])):
                            if(control==0):
                                f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($gp)\n")
                            else:
                                f.write("lw " + "$"+ str(reg2) + ","+"-" +str(off)+"($fp)\n")
                        else:
                            if(control==0):
                                f.write("subi " + "$"+ str(reg2) + "," + "$gp," + str(off)+"\n")
                            else:
                                f.write("subi " + "$"+ str(reg2) + "," + "$fp," + str(off)+"\n")
                    regToVar[reg2]=code[2]
                    varToReg[code[2]]=reg2
                else:
                    reg2=varToReg[code[2]]
                if(varToReg.get(code[4])==None):
                    reg3=getReg()
                    if(code[4][0]=='t'):
                        off=getOffset(code[4])
                        f.write("lw " + "$"+ str(reg3) + "," + "-"+str(off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[4])
                        if(not getType(code[4])):
                            if(control==0):
                                f.write("lw " + "$"+ str(reg3) + "," + "-"+str(off)+"($gp)\n")
                            else:
                                f.write("lw " + "$"+ str(reg3) + ","+"-" +str(off)+"($fp)\n")

                        else:
                            if(control==0):
                                f.write("subi " + "$"+ str(reg3) + "," + "$gp," + str(off)+"\n")
                            else:
                                f.write("subi " + "$"+ str(reg3) + "," + "$fp," + str(off)+"\n")
                    regToVar[reg3]=code[4]
                    varToReg[code[4]]=reg3
                else:
                    reg3=varToReg[code[4]]
                reg1=getReg()
                regToVar[reg1]=code[0]
                varToReg[code[0]]=reg1
                writeInstrBin(reg1, reg2, reg3, op)
            else:
                xxxyyy=0

    if (len(code)==3 and (code[0][0]=='t' or code[0][0]=='v') and code[2][0]!="*"):
        reg1=getReg()
        regToVar[reg1]=code[0]
        varToReg[code[0]]=reg1
        if(code[2][0]!='t' and code[2][0]!='v'): #constant
            reg2=getReg()
            f.write("addi "+ "$" +str(reg2)+",$0," + code[2] +"\n")
        else:
            if(varToReg.get(code[2])==None):
                reg2=getReg()
                if(code[2][0]=='t'):
                    off=getOffset(code[2])
                    f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($fp)\n")
                else:
                    off, control=getVarOffset(code[2])
                    if(not getType(code[2])):
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+"-" +str(off)+"($fp)\n")
                    else:
                        if(control==0):
                            f.write("subi " + "$"+ str(reg2) + "," + "$gp," + str(off)+"\n")
                        else:
                            f.write("subi " + "$"+ str(reg2) + "," + "$fp," + str(off)+"\n")
                regToVar[reg2]=code[2]
                varToReg[code[2]]=reg2
            else:
                reg2=varToReg[code[2]]
            f.write("addi "+"$"+str(reg1)+ ",$" + str(reg2) + ","+ "0\n")

    if(len(code)==4 and code[0]=="*"):
        if(code[3][0]!='t' and code[3][0]!='v'): #constant
            reg2=getReg()
            f.write("addi "+ "$" +str(reg2)+",$0," + code[3] +"\n")
        else:
            if(varToReg.get(code[3])==None):
                reg2=getReg()
                if(code[3][0]=='t'):
                    off=getOffset(code[3])
                    f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($fp)\n")
                else:
                    off, control=getVarOffset(code[3])
                    if(not getType(code[3])):
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+"-" +str(off)+"($fp)\n")
                    else:
                        if(control==0):
                            f.write("subi " + "$"+ str(reg2) + "," + "$gp," + str(off)+"\n")
                        else:
                            f.write("subi " + "$"+ str(reg2) + "," + "$fp," + str(off)+"\n")
                regToVar[reg2]=code[3]
                varToReg[code[3]]=reg2
            else:
                reg2=varToReg[code[3]]
        if(varToReg.get(code[1])==None):
            reg1=getReg()
            if(code[1][0]=='t'):
                off=getOffset(code[1])
                f.write("lw " + "$"+ str(reg1) + "," + "-"+str(off)+"($fp)\n")
            regToVar[reg1]=code[1]
            varToReg[code[1]]=reg1
        else:
            reg1=varToReg[code[1]]
        f.write("sw $"+str(reg2)+",0($"+str(reg1)+")\n")

    if(len(code)==4 and code[2]=="*"):
        reg1=getReg()
        regToVar[reg1]=code[0]
        varToReg[code[0]]=reg1
        if(varToReg.get(code[3])==None):
            reg2=getReg()
            if(code[3][0]=='t'):
                off=getOffset(code[3])
                f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($fp)\n")
            else:
                off, control=getVarOffset(code[3])
                if(not getType(code[3])):
                    if(control==0):
                        f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($gp)\n")
                    else:
                        f.write("lw " + "$"+ str(reg2) + ","+"-" +str(off)+"($fp)\n")
                else:
                    if(control==0):
                        f.write("subi " + "$"+ str(reg2) + "," + "$gp," + str(off)+"\n")
                    else:
                        f.write("subi " + "$"+ str(reg2) + "," + "$fp," + str(off)+"\n")
            regToVar[reg2]=code[3]
            varToReg[code[3]]=reg2
        else:
            reg2=varToReg[code[3]]
        f.write("lw "+"$"+str(reg1)+ ",0"+"($" + str(reg2) + ")"+ "\n")

    if(len(code)==4 and code[2]=="&"):
        reg1=getReg()
        regToVar[reg1]=code[0]
        varToReg[code[0]]=reg1
        if(varToReg.get(code[3])==None):
            reg2=getReg()
            if(code[3][0]=='t'):
                off=getOffset(code[3])
                f.write("lw " + "$"+ str(reg2) + "," + "-"+str(off)+"($fp)\n")
            else:
                off, control=getVarOffset(code[3])
                if(control==0):
                   f.write("subi " + "$"+ str(reg2) + "," + "$gp," + str(off)+"\n")
                else:
                    f.write("subi " + "$"+ str(reg2) + "," + "$fp," + str(off)+"\n")
            regToVar[reg2]=code[3]
            varToReg[code[3]]=reg2
        else:
            reg2=varToReg[code[3]]
        f.write("addi $"+str(reg1)+",$"+str(reg2)+",0\n")


f.close()
