import pickle
import os
import sys
with open('scopeTabDump', 'rb') as handle:
    scopeTab  = pickle.load(handle)
basicTypes=["int","float","rune","string","bool"]

with open("code.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]

## To Remove Concurrent Returns ##
index=1
while(index<len(content)):
    if(content[index]=="return" and content[index-1]=="return"):
        del(content[index])
    else:
        index=index+1

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

currentFunc=""
currentLabel=""

msgCount=0

def newMsg(a=None):
    global msgCount
    newm="msg"+str(msgCount)
    msgCount+=1
    return newm

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

def getReg(a,b=None):
    global regReplace
    if (a==0):
        if(b!=None):
            if(varToReg.get(b)!=None):
                return varToReg[b]
        for i in range(2, 26):
            if (regToVar[i]=="free"):
                return i
        while(regToVar[regReplace]=="const"):
            regReplace+=1
        if(regToVar[regReplace][0]=='t'):
            off=getOffset(regToVar[regReplace])
            f.write("sw " + "$"+ str(regReplace) + "," + str(-off)+"($fp)\n")
        elif(not getType(varToReg[regToVar[regReplace]])):
            off, control=getVarOffset(regToVar[regReplace])
            if(not control):
                f.write("sw " + "$"+ str(regReplace) + "," + str(-off)+"($gp)\n")
            else:
                f.write("sw " + "$"+ str(regReplace) + "," + str(-off)+"($fp)\n")
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
            f.write("swc1 " + "$f"+ str(regReplaceFloat) + "," + str(-off)+"($fp)\n")
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
        f.write("slt "+"$"+str(reg1)+",$" +str(reg3)+",$" +str(reg2)+"\n"+"xori " +"$" + str(reg1)+",$"+ str(reg1)+ ",1"+ "\n")
    elif(op==">="):
        f.write("slt "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n"+"xori " +"$" + str(reg1)+",$"+ str(reg1)+ ",1"+ "\n")
    elif(op=="=="):
        reg4=getReg(0)
        regToVar[reg4]="free"
        f.write("slt "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n"+"slt " +"$" + str(reg4)+",$"+ str(reg3)+ ",$"+str(reg2)+ "\n")
        f.write("xori " +"$" + str(reg1)+",$"+ str(reg1)+ ",1"+ "\n" + "xori " +"$" + str(reg4)+",$"+ str(reg4)+ ",1"+ "\n")
        f.write("and "+"$"+str(reg1)+",$" +str(reg4)+",$" +str(reg1)+"\n")
    elif(op=="!="):
        reg4=getReg(0)
        regToVar[reg4]="free"
        f.write("slt "+"$"+str(reg1)+",$" +str(reg2)+",$" +str(reg3)+"\n"+"slt " +"$" + str(reg4)+",$"+ str(reg3)+ ",$"+str(reg2)+ "\n")
        f.write("or "+"$"+str(reg1)+",$" +str(reg4)+",$" +str(reg1)+"\n")

def saveReg(index):
    if(regToVar[index]=="free"):
        return
    if(regToVar[index][0]=='t'):
        off=getOffset(regToVar[index])
        f.write("sw " + "$"+ str(index) + "," + str(-off)+"($fp)\n")
    elif(not getType(regToVar[index])):
        off,control=getVarOffset(regToVar[index])
        if (not control):
            f.write("sw " + "$"+ str(index) + "," + str(-off)+"($gp)\n")
        else:
            f.write("sw " + "$"+ str(index) + "," + str(-off)+"($fp)\n")
    if(varToReg.get(regToVar[index])!=None):
        del varToReg[regToVar[index]]
    regToVar[index]="free"

def reset(a=None):
    if(a==None):
        for i in range(2,26):
            if(regToVar[i]=="free"):
                continue
            saveReg(i)
    else:
        xxxyyy=0

def resetF(a=None):
    if(a==None):
        for i in range(2,26):
            if(regToVar[i]!="free"):
                del varToReg[regToVar[i]]
            regToVar[i]=="free"
    else:
        xxxyyy=0

f=open('mips.txt', 'wr')

f.write(".data\n .text\n.globl main\n")
for code in codeLines:
    temp=""
    for x in code:
        temp=temp+x+" "
    # f.write(temp+"\n")
    # f.write("...........................\n")
    if (len(code) == 2 and code[1]==":"):
	if(code[0]=="main"):
            currentLabel="main"
            f.write(code[0]+code[1]+"\n")
            f.write("addi "+ "$fp,$sp,0\n")
        else:
            f.write(code[0]+code[1]+"\n")
        if (scopeTab[0].table.get(code[0])!= None):
            scope=scopeTab[0].table[code[0]]["Scope"]
            f.write("addi "+"$sp,"+"$sp,"+"-"+str(scopeTab[scope].table["#total_size"]["type"])+"\n")

    if (len(code) == 5):
        if(code[2][0]!='t' and code[2][0]!='v' and code[4][0]!='t' and code[4][0]!='v'):   #constant, constant
            if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-3]=='o'):  #integer op
                op=code[3][:-3] if code[3][-3]=="i" else code[3][:-4]
                val=eval(code[2]+op+code[4])
                if (val==True):
                    val=1
                elif(val==False):
                    val=0
                reg=getReg(0,code[0])
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
                reg=getReg(1,code[0])
                f.write("addi "+"$"+str(reg)+",$0," + str(val)+"\n")
                regToVarFloat[reg]=code[0]
                varToRegFloat[code[0]]=reg
        elif(code[2][0]!='t' and code[2][0]!='v' and (code[4][0]=='t' or code[4][0]=='v')):   # constant, temp or constant, vartemp
                if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-3]=='o'):  #integer op or rune op
                    op=code[3][:-3] if code[3][-3]=="i" else code[3][:-4]
                    if(varToReg.get(code[4])==None):
                        reg3=getReg(0)
                        if(code[4][0]=='t'):
                            off=getOffset(code[4])
                            f.write("lw " + "$"+ str(reg3) + "," + str(-off)+"($fp)\n")
                        else:
                            off, control=getVarOffset(code[4])
                            if(not getType(code[4])):
                                if(control==0):
                                    f.write("lw " + "$"+ str(reg3) + "," +str(-off)+"($gp)\n")
                                else:
                                    f.write("lw " + "$"+ str(reg3) + ","+str(-off)+"($fp)\n")

                            else:
                                if(control==0):
                                    f.write("addi " + "$"+ str(reg3) + "," + "$gp," + str(-off)+"\n")
                                else:
                                    f.write("addi " + "$"+ str(reg3) + "," + "$fp," + str(-off)+"\n")
                        regToVar[reg3]=code[4]
                        varToReg[code[4]]=reg3
                    else:
                        reg3=varToReg[code[4]]

                    reg2=getReg(0)
                    f.write("addi " + "$"+ str(reg2) + ",$0," +code[2]+"\n")
                    regToVar[reg2]="const"
                    reg1=getReg(0,code[0])
                    regToVar[reg1]=code[0]
                    varToReg[code[0]]=reg1
                    writeInstrBin(reg1, reg2, reg3, op)
                    regToVar[reg2]="free"
                else:
                    xxxyyy=0

        elif(code[4][0]!='t' and code[4][0]!='v' and (code[2][0]=='t' or code[2][0]=='v')):   # temp, constant or vartemp, constant
                if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-3]=='o'):  #integer op or rune op
                    op=code[3][:-3] if code[3][-3]=="i" else code[3][:-4]
                    if(varToReg.get(code[2])==None):
                        reg2=getReg(0)
                        if(code[2][0]=='t'):
                            off=getOffset(code[2])
                            f.write("lw " + "$"+ str(reg2) + "," +str(-off)+"($fp)\n")
                        else:
                            off, control=getVarOffset(code[2])
                            if(not getType(code[2])):
                                if(control==0):
                                    f.write("lw " + "$"+ str(reg2) + "," +str(-off)+"($gp)\n")
                                else:
                                    f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                            else:
                                if(control==0):
                                    f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
                                else:
                                    f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
                        regToVar[reg2]=code[2]
                        varToReg[code[2]]=reg2
                    else:
                        reg2=varToReg[code[2]]

                    reg3=getReg(0)
                    f.write("addi " + "$"+ str(reg3) + ",$0," +code[4]+"\n")
                    regToVar[reg3]="const"
                    reg1=getReg(0,code[0])
                    regToVar[reg1]=code[0]
                    varToReg[code[0]]=reg1
                    writeInstrBin(reg1, reg2, reg3, op)
                    regToVar[reg3]="free"
                else:
                    xxxyyy=0
        else:  # t,t or t,v, or v,t, or v,v
            if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-3]=='o'):  #integer or rune  op
                op=code[3][:-3] if code[3][-3]=="i" else code[3][:-4]
                if(varToReg.get(code[2])==None):
                    reg2=getReg(0)
                    if(code[2][0]=='t'):
                        off=getOffset(code[2])
                        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[2])
                        if(not getType(code[2])):
                            if(control==0):
                                f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                            else:
                                f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                        else:
                            if(control==0):
                                f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
                            else:
                                f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
                    regToVar[reg2]=code[2]
                    varToReg[code[2]]=reg2
                else:
                    reg2=varToReg[code[2]]
                if(varToReg.get(code[4])==None):
                    reg3=getReg(0)
                    if(code[4][0]=='t'):
                        off=getOffset(code[4])
                        f.write("lw " + "$"+ str(reg3) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[4])
                        if(not getType(code[4])):
                            if(control==0):
                                f.write("lw " + "$"+ str(reg3) + "," + str(-off)+"($gp)\n")
                            else:
                                f.write("lw " + "$"+ str(reg3) + ","+str(-off)+"($fp)\n")

                        else:
                            if(control==0):
                                f.write("addi " + "$"+ str(reg3) + "," + "$gp," + str(-off)+"\n")
                            else:
                                f.write("addi " + "$"+ str(reg3) + "," + "$fp," + str(-off)+"\n")
                    regToVar[reg3]=code[4]
                    varToReg[code[4]]=reg3
                else:
                    reg3=varToReg[code[4]]
                reg1=getReg(0,code[0])
                regToVar[reg1]=code[0]
                varToReg[code[0]]=reg1
                writeInstrBin(reg1, reg2, reg3, op)
            else:
                xxxyyy=0

    if (len(code)==3 and (code[0][0]=='t' or code[0][0]=='v') and code[2][0]!="*" and code[2][0]!="r"):  #CHECK
        reg1=getReg(0,code[0])
        regToVar[reg1]=code[0]
        varToReg[code[0]]=reg1
        if(code[2][0]!='t' and code[2][0]!='v'): #constant
            reg2=getReg(0)
            f.write("addi "+ "$" +str(reg2)+",$0," + code[2] +"\n")
            regToVar[reg2]="free"
        else:
            if(varToReg.get(code[2])==None):
                reg2=getReg(0)
                if(code[2][0]=='t'):
                    off=getOffset(code[2])
                    f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                else:
                    off, control=getVarOffset(code[2])
                    if(not getType(code[2])):
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                    else:
                        if(control==0):
                            f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
                        else:
                            f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
                regToVar[reg2]=code[2]
                varToReg[code[2]]=reg2
            else:
                reg2=varToReg[code[2]]
        f.write("addi "+"$"+str(reg1)+ ",$" + str(reg2) + ","+ "0\n")

    if(len(code)==4 and code[0]=="*"):
        if(code[3][0]!='t' and code[3][0]!='v'): #constant
            reg2=getReg(0)
            f.write("addi "+ "$" +str(reg2)+",$0," + code[3] +"\n")
            regToVar[reg2]="free"
        else:
            if(varToReg.get(code[3])==None):
                reg2=getReg(0)
                if(code[3][0]=='t'):
                    off=getOffset(code[3])
                    f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                else:
                    off, control=getVarOffset(code[3])
                    if(not getType(code[3])):
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                    else:
                        if(control==0):
                            f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
                        else:
                            f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
                regToVar[reg2]=code[3]
                varToReg[code[3]]=reg2
            else:
                reg2=varToReg[code[3]]
        if(varToReg.get(code[1])==None):
            reg1=getReg(0)
            if(code[1][0]=='t'):
                off=getOffset(code[1])
                f.write("lw " + "$"+ str(reg1) + "," + str(-off)+"($fp)\n")
            regToVar[reg1]=code[1]
            varToReg[code[1]]=reg1
        else:
            reg1=varToReg[code[1]]
        f.write("sw $"+str(reg2)+",0($"+str(reg1)+")\n")

    if(len(code)==4 and code[2]=="*"):
        reg1=getReg(0,code[0])
        regToVar[reg1]=code[0]
        varToReg[code[0]]=reg1
        if(varToReg.get(code[3])==None):
            reg2=getReg(0)
            if(code[3][0]=='t'):
                off=getOffset(code[3])
                f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
            else:
                off, control=getVarOffset(code[3])
                if(not getType(code[3])):
                    if(control==0):
                        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                    else:
                        f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                else:
                    if(control==0):
                        f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
                    else:
                        f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
            regToVar[reg2]=code[3]
            varToReg[code[3]]=reg2
        else:
            reg2=varToReg[code[3]]
        f.write("lw "+"$"+str(reg1)+ ",0"+"($" + str(reg2) + ")"+ "\n")

    if(code[0]=="reset"):
        reset()

    if(code[0]=="resetF"):
        resetF()

    if (code[0]=="ifnot"):
        if (code[1]=='0'):
            f.write("j "+code[3]+"\n")
        elif (code[1]=='1'):
            xxxyyy=0
        else:
            if(code[1][0]!='t' and code[1][0]!='v'):
                reg1=getReg(0,code[1])
                regToVar[reg1]=code[1]
                varToReg[code[1]]=reg1
                f.write("addi " + "$"+str(reg1)+ ",$0,"+ code[1]+"\n")
            else:
                if(varToReg.get(code[1])==None):
                    reg2=getReg(0)
                    if(code[1][0]=='t'):
                        off=getOffset(code[1])
                        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[1])
                        if(not getType(code[1])):
                            if(control==0):
                                f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                            else:
                                f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                        else:
                            if(control==0):
                                f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
                            else:
                                f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
                    regToVar[reg2]=code[1]
                    varToReg[code[1]]=reg2
                else:
                    reg2=varToReg[code[1]]
            f.write("blez " + "$"+str(reg1)+"," + code[3] +"\n" )

    if (code[0]=="goto"):
        reset()
        f.write("j " + code[1]+"\n")

    if(len(code)==4 and code[2]=="&"):
        reg1=getReg(0,code[0])
        regToVar[reg1]=code[0]
        varToReg[code[0]]=reg1
        if(varToReg.get(code[3])==None):
            reg2=getReg(0)
            if(code[3][0]=='t'):
                off=getOffset(code[3])
                f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
            else:
                off, control=getVarOffset(code[3])
                if(control==0):
                    f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
                else:
                    f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
            regToVar[reg2]=code[3]
            varToReg[code[3]]=reg2
        else:
            reg2=varToReg[code[3]]
        f.write("addi $"+str(reg1)+",$"+str(reg2)+",0\n")

    if(code[0]=="startf"):
        currentFunc=code[1]
        retSize=scopeTab[0].table[currentFunc]["#total_retSize"]
        f.write("addi $sp,$sp,"+str(-retSize)+"\n")

    if(code[0]=="param" and len(code)==2): # param reg
        if(code[1][0]!='t' and code[1][0]!='v'): #constant
            reg=getReg(0)
            f.write("addi "+ "$" +str(reg)+",$0," + code[1] +"\n")
            regToVar[reg]="free"
        else:
            if(varToReg.get(code[1])==None):
                reg=getReg(0)
                if(code[1][0]=='t'):
                    off=getOffset(code[1])
                    f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($fp)\n")
                else:
                    off, control=getVarOffset(code[1])
                    if(not getType(code[1])):
                        if(control==0):
                            f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($fp)\n")
                    else:
                        if(control==0):
                            f.write("addi " + "$"+ str(reg) + "," + "$gp," + str(-off)+"\n")
                        else:
                            f.write("addi " + "$"+ str(reg) + "," + "$fp," + str(-off)+"\n")
                regToVar[reg]=code[1]
                varToReg[code[1]]=reg
            else:
                reg=varToReg[code[1]]
        f.write("addi $sp,$sp,-4\nsw $"+str(reg)+",0($sp)\n")

    if(code[0]=="param" and len(code)==3): # param reg size
        size=int(code[2])
        if(code[1][0]!='t' and code[1][0]!='v'): #constant
            reg=getReg(0)
            f.write("addi "+ "$" +str(reg2)+",$0," + code[1] +"\n")
            regToVar[reg]="free"
        else:
            if(varToReg.get(code[1])==None):
                reg=getReg(0)
                if(code[1][0]=='t'):
                    off=getOffset(code[1])
                    f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($fp)\n")
                else:
                    off, control=getVarOffset(code[1])
                    if(not getType(code[1])):
                        if(control==0):
                            f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($fp)\n")
                    else:
                        if(control==0):
                            f.write("addi " + "$"+ str(reg) + "," + "$gp," + str(-off)+"\n")
                        else:
                            f.write("addi " + "$"+ str(reg) + "," + "$fp," + str(-off)+"\n")
                regToVar[reg]=code[1]
                varToReg[code[1]]=reg
            else:
                reg=varToReg[code[1]]
        regToCopy=getReg(0)
        off=0
        while size>0:
            f.write("addi $sp,$sp,-4\n")
            f.write("lw $"+str(regToCopy)+","+str(off)+"($"+str(reg)+")\n")
            f.write("sw $"+str(regToCopy)+",0($sp)\n")
            size=size-4
            off=off+4

    if(code[0]=="call"):
        ## Reset the reg-var maps
        for index in range(2, 26):
            if (regToVar[index]=="free"):
                continue
            if(regToVar[index][0]=='t'):
                off=getOffset(regToVar[index])
                f.write("sw " + "$"+ str(index) + "," + str(-off)+"($fp)\n")
            elif(not getType(regToVar[index])):
                off,control=getVarOffset(regToVar[index])
                if (not control):
                    f.write("sw " + "$"+ str(index) + "," + str(-off)+"($gp)\n")
                else:
                    f.write("sw " + "$"+ str(index) + "," + str(-off)+"($fp)\n")
            if(varToReg.get(regToVar[index])!=None):
                del varToReg[regToVar[index]]
            regToVar[index]="free"

        f.write("addi $sp,$sp,-4\n")
        f.write("sw $ra,0($sp)\n")
        f.write("addi $sp,$sp,-4\n")
        f.write("sw $fp,0($sp)\n")
        f.write("add $fp,$0,$sp\n")
        f.write("jal "+currentFunc+"\n")

    if(code[0]=="endf"):
        size=4+scopeTab[0].table[currentFunc]["#total_retSize"]+scopeTab[0].table[currentFunc]["#total_parSize"]
        f.write("lw $ra,0($sp)\n")
        f.write("addi $sp,$sp,"+str(size)+"\n")

    if(len(code)==3 and code[2][0:3]=="ret"):
        reg=getReg(0,code[0])
        regToVar[reg]=code[0]
        varToReg[code[0]]=reg
        retNumber=int(code[2][7:])
        off=4*retNumber
        if(varToReg.get(code[0])==None):
            reg=getReg(0)
            off=getOffset(code[0])
            f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($fp)\n")
            regToVar[reg]=code[0]
            varToReg[code[0]]=reg
        else:
            reg=varToReg[code[0]]
        f.write("lw $"+str(reg)+","+str(-off)+"($sp)\n")

    if(len(code)==1 and code[0]=="return"):
        ## Reset reg-var maps
        for index in range(2, 26):
            if (regToVar[index]=="free"):
                continue
            if(varToReg.get(regToVar[index])!=None):
                del varToReg[regToVar[index]]
            regToVar[index]="free"

        if(currentLabel=="main"):
            f.write("jr $ra\n")
            currentLabel=""
        else:
            f.write("add $sp,$fp,$0\n")
            f.write("lw $fp,0($sp)\n")
            f.write("addi $sp,$sp,4\n")
            f.write("jr $ra\n")

    if(len(code)==4 and code[1]=="return"):
        retNumber=int(code[3])
        func=code[0]
        retOff=scopeTab[0].table[func]["retSizeList"][retNumber]

        if(code[2][0]!='t' and code[2][0]!='v'): #constant
            reg=getReg(0)
            f.write("addi "+ "$" +str(reg)+",$0," + code[2] +"\n")
            f.write("sw $"+str(reg)+","+str(-retOff)+"($fp)\n")
            regToVar[reg]="free"
        else:
            if(varToReg.get(code[2])==None):
                reg=getReg(0)
                if(code[2][0]=='t'):
                    off=getOffset(code[2])
                    f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($fp)\n")
                else:
                    off, control=getVarOffset(code[2])
                    if(not getType(code[2])):
                        if(control==0):
                            f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($fp)\n")
                    else:
                        if(control==0):
                            f.write("addi " + "$"+ str(reg) + "," + "$gp," + str(-off)+"\n")
                        else:
                            f.write("addi " + "$"+ str(reg) + "," + "$fp," + str(-off)+"\n")
                regToVar[reg]=code[2]
                varToReg[code[2]]=reg
            else:
                reg=varToReg[code[2]]
            f.write("sw $"+str(reg)+","+str(-retOff)+"($fp)\n")

    if(code[0]=="print_int"):
        saveReg(2)
        f.write("addi "+ "$v0,$0,1\n" )  #print syscall is 1 , $v0 is $2
        saveReg(4)
        if(varToReg.get(code[1])==None):
            if(code[1][0]=='t'):
                off=getOffset(code[1])
                f.write("lw " + "$a0,"+ str(-off)+"($fp)\n")  #CHECK ABOVE
                varToReg[code[1]]=4
                regToVar[4]=code[1]
            elif(code[1][0]=='v'):
                off, control=getVarOffset(code[1])
                if(not getType(code[1])):  #if basic type // only basic types are allowed anyways
                    if(control==0):  # if global
                        f.write("lw " + "$a0," + str(-off)+"($gp)\n")
                    else:
                        f.write("lw " + "$a0," + ","+str(-off)+"($fp)\n")
                varToReg[code[1]]=4
                regToVar[4]=code[1]
            else:  #is a constant
                f.write("addi " + "$a0,$0,"+ code[1]+"\n")   #place constant integer into $4
        else:
            f.write("add " + "$a0,$0,$"+ str(varToReg[code[1]]) +"\n")  #put integer to be printed into $4
        f.write("syscall\n")


    if(code[0]=="vscan_int"):
        saveReg(2)
        f.write("addi "+ "$v0,$0,5\n" )  #scanint syscall is 5, $v0 is $2
        f.write("syscall\n")
        off, control=getVarOffset(code[1])
        if(not getType(code[1])):  #if basic type // only basic types are allowed anyways
            if(control==0):  # if global
                f.write("sw " + "$v0," + str(-off)+"($gp)\n")  #scanned int is present in $v0
            else:
                f.write("sw " + "$v0," +str(-off)+"($fp)\n")
        varToReg[code[1]]=2
        regToVar[2]=code[1]


    if(code[0]=="scan_int"):
        saveReg(2)
        f.write("addi "+ "$v0,$0,5\n" )  #scanint syscall is 5, $v0 is $2
        f.write("syscall\n")
        if(varToReg.get(code[1])!=None):
            f.write("sw " + "$v0," + "0($" +str(varToReg[code[1]])+")\n")
        else:
            off=getOffset(code[1])
            reg=getReg(0,code[1])
            f.write("lw $"+str(reg)+","+str(off)+"($fp)\n")
            regToVar[reg]=code[1]
            varToReg[code[1]]=reg
            f.write("sw " + "$v0," + "0($" +str(reg)+")\n")

    if(code[0]=="print_string"):
#        f.write("start string printing\n")
        saveReg(2)
        f.write("addi "+ "$v0,$0,4\n" )  #print_string syscall is 4, $v0 is $2
        saveReg(4)
        if(code[1][0]=="\""): #is a literal string
            msg=newMsg()
            st=""
            for i in range(1, len(code)):
                if(i==len(code)-1):
                    st=st+code[i]
                    break
                st=st+code[i]+" "
            f.write(msg +": "+".asciiz "+ st+ "\n" )
            f.write("la "+ "$a0," +msg+"\n")  #la might be a pseudo instruction so might have to change this #CHECK
            f.write("syscall\n")
        else:
            xxx=0

    # print (code)
    # print("-----------------------------------------------")
    # print (regToVar)
    # print("-----------------------------------------------")
    # print(varToReg)
    # f.write("###############################################\n")








f.close()
