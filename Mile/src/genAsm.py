import pickle
import os
import sys
#import ascii
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
    for x in i.split(','):
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

regReplace=2
regReplaceFloat=0

currentFunc=""
currentLabel=""

msgCount=0
string_dict={}

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
            if(regReplace==26):
                regReplace=2
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
        if(b!=None):
            if(varToRegFloat.get(b)!=None):
                return varToRegFloat[b]
        for i in range(0, 32):
            if (regToVarFloat[i]=="free"):
                return i
        while(regToVarFloat[regReplaceFloat]=="const"):
            regReplaceFloat+=1
            if(regReplaceFloat==32):
                regReplaceFloat=0
        if(regToVarFloat[regReplaceFloat][0]=='t'):
            off=getOffset(regToVarFloat[regReplaceFloat])
            f.write("swc1 " + "$"+ str(regReplaceFloat) + "," + str(-off)+"($fp)\n")
        elif(not getType(varToRegFloat[regToVarFloat[regReplaceFloat]])):
            off, control=getVarOffset(regToVarFloat[regReplaceFloat])
            if(not control):
                f.write("swc1 " + "$"+ str(regReplaceFloat) + "," + str(-off)+"($gp)\n")
            else:
                f.write("swc1 " + "$"+ str(regReplaceFloat) + "," + str(-off)+"($fp)\n")
        del varToRegFloat[regToVarFloat[regReplaceFloat]]
        org=regReplaceFloat
        regReplaceFloat=(regReplaceFloat%32)
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



def writeInstrBinFloat(reg1, reg2, reg3, op):
    f.write("mtc1 $"+str(reg2)+",$f1\n")
    f.write("mtc1 $"+str(reg3)+",$f2\n")
    if(op=="+"):
        f.write("add.s $f0, $f1, $f2\n" + "mfc1 $"+str(reg1)+",$f0\n")
    elif(op=="-"):
        f.write("sub.s $f0, $f1, $f2\n" + "mfc1 $"+str(reg1)+",$f0\n")
    elif(op=="*"):
        f.write("mul.s $f0, $f1, $f2\n" + "mfc1 $"+str(reg1)+",$f0\n")
    elif(op=="/"):
        f.write("div.s $f0, $f1, $f2\n" + "mfc1 $"+str(reg1)+",$f0\n")
    elif(op=="<"):
        f.write("c.lt.s $f1, $f2\n" + "cfc1 $" + str(reg1)+",$25"+"\n")
    elif(op==">"):
        f.write("c.gt.s $f1, $f2\n" + "cfc1 $" + str(reg1)+",$25"+"\n")
    elif(op=="<="):
        f.write("c.le.s $f1, $f2\n" + "cfc1 $" + str(reg1)+",$25"+"\n")
    elif(op==">="):
        f.write("c.ge.s $f1, $f2\n" + "cfc1 $" + str(reg1)+",$25"+"\n")
    elif(op=="=="):
        f.write("c.eq.s $f1, $f2\n" + "cfc1 $" + str(reg1)+",$25"+"\n")
    elif(op=="!="):
        f.write("c.ne.s $f1, $f2\n" + "cfc1 $" + str(reg1)+",$25"+"\n")

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



def saveRegFloat(index):
    if(regToVarFloat[index]=="free"):
        return
    if(regToVarFloat[index][0]=='t'):
        off=getOffset(regToVarFloat[index])
        f.write("swc1 " + "$"+ str(index) + "," + str(-off)+"($fp)\n")
    elif(not getType(regToVarFloat[index])):
        off,control=getVarOffset(regToVar[index])
        if (not control):
            f.write("swc1 " + "$"+ str(index) + "," + str(-off)+"($gp)\n")
        else:
            f.write("swc1 " + "$"+ str(index) + "," + str(-off)+"($fp)\n")
    if(varToRegFloat.get(regToVarFloat[index])!=None):
        del varToRegFloat[regToVarFloat[index]]
    regToVarFloat[index]="free"

def reset(a=None):
    if(a==None):
        for i in range(2,26):
            if(regToVar[i]=="free"):
                continue
            elif(regToVar[i]=="const"):
                regToVar[i]="free"
                continue
            # print (regToVar[i],varToReg[regToVar[i]])
            saveReg(i)
    else:
        for i in range(0,32):
            if(regToVarFloat[i]=="free"):
                continue
            elif(regToVarFloat[i]=="const"):
                regToVarFloat[i]="free"
                continue
            saveRegFloat(i)

def resetVars(a=None):
    if(a==None):
        for i in range(2,26):
            if(regToVar[i]=='free' or regToVar[i][0]=='t' or regToVar[i][0]=='c'):
                continue
            saveReg(i)
    else:
        for i in range(0,32):
            if(regToVarFloat[i]=='free' or regToVarFloat[i][0]=='t' or regToVarFloat[i][0]=='c'):
                continue
            saveRegFloat(i)

def resetF(a=None):
    if(a==None):
        for i in range(2,26):
            if(regToVar[i]!="free"):
                del varToReg[regToVar[i]]
            regToVar[i]=="free"
    else:
        for i in range(0,32):
            if(regToVarFloat[i]!="free"):
                del varToRegFloat[regToVarFloat[i]]
            regToVarFloat[i]=="free"


def convertToAscii(code):
    asc_str=[]
    i=0
    while i < len(code):
        if(code[i]!="\\"):
            # print(code[3][i])
            asc_str.append(ord(code[i]))
            i+=1
        else:
            i+=1
            if(code[i]=="\'"):
                asc_str.append(ord("\'"))
            if(code[i]=="\""):
                asc_str.append(ord("\""))
            if(code[i]=="n"):
                asc_str.append(ord("\n"))
            if(code[i]=="t"):
                asc_str.append(ord("\t"))
            if(code[i]=="\\"):
                asc_str.append(ord("\\"))
            i+=1
    return asc_str

def allocateBytes(bytes):
    saveReg(2)
    saveReg(4)
    f.write("li $a0,"+str(bytes)+"\n")
    f.write("li $v0,9\nsyscall\n")

def writeConst(list,offset):
    for x in range(len(list)):
        f.write("li $a0,"+str(list[x])+"\n")
        f.write("sb $a0,"+str(offset)+"($v0)\n")
        offset=offset+1

def writeVar(reg,base,size):
    index=0
    while(index<size):
        off1=index
        off2=base+index
        f.write("lb $a0,"+str(off1)+"($"+str(reg)+")\n")
        f.write("sb $a0,"+str(off2)+"($v0)\n")
        index=index+1

f=open('mips.txt', 'wr')

f.write(".data\n .text\n.globl main\n")
count=0
for code in codeLines:
    count=count+1
    # f.write("+++++++++++++++++++++++++++++++ "+str(count)+"\n")
    #print (count,"\n",regToVar)
    #print ("++++++++++++++++++++++++++++++++")
    temp=""
    for x in code:
        temp=temp+x+" "
    # f.write(temp+"\n")
    # f.write("...........................\n")
    if (len(code) == 2 and code[1]==":"):
        reset()
	if(code[0]=="main"):
            currentLabel="main"
            f.write(code[0]+code[1]+"\n")
            f.write("addi "+ "$fp,$sp,0\n")
        else:
            f.write(code[0]+code[1]+"\n")
        if (scopeTab[0].table.get(code[0])!= None):
            scope=scopeTab[0].table[code[0]]["Scope"]
            f.write("addi "+"$sp,"+"$sp,"+"-"+str(scopeTab[scope].table["#total_size"]["type"])+"\n")

    if(len(code)==3 and code[1]=="malloc"):
        saveReg(2)
        saveReg(4)
        f.write("li $a0,"+str(code[2])+"\nli $v0,9\nsyscall\n")
        if(code[0][0]=='t'):
            if(varToReg.get(code[0])!=None):
                f.write("sw " + "$v0"+",0($"+str(varToReg[code[0]])+")\n")
                saveReg(varToReg[code[0]])
            else:
                off=getOffset(code[0])
                f.write("lw $a0,"+str(-off)+"($fp)\n")
                f.write("sw $v0,0($a0)\n")
        else:
            off, control=getVarOffset(code[0])
            if(control==0):
                f.write("sw " + "$v0" + "," +str(-off)+"($gp)\n")
            else:
                f.write("sw " + "$v0" + ","+str(-off)+"($fp)\n")
            if(varToReg.get(code[0])!=None):
                saveReg(varToReg[code[0]])

    if(code[0]=="string_assign"):
        if(len(code)==4):
            if(code[3][0]=="\""):
                code[3]=code[3][1:-1]
                asc_str=[]
                i=0
                while i < len(code[3]):
                    if(code[3][i]!="\\"):
                        # print(code[3][i])
                        asc_str.append(ord(code[3][i]))
                        i+=1
                    else:
                        i+=1
                        if(code[3][i]=="\'"):
                            asc_str.append(ord("\'"))
                        if(code[3][i]=="\""):
                            asc_str.append(ord("\""))
                        if(code[3][i]=="n"):
                            asc_str.append(ord("\n"))
                        if(code[3][i]=="t"):
                            asc_str.append(ord("\t"))
                        if(code[3][i]=="\\"):
                            asc_str.append(ord("\\"))
                        i+=1
                saveReg(2)
                saveReg(4)
                size=len(asc_str)+((4-len(asc_str)%4)%4)+4
                ## Replacing size by len(asc_str)
                string_dict[code[1]]=len(asc_str)
                f.write("li $a0,"+str(size)+"\n")
                f.write("li $v0,9\nsyscall\n")
                for i in range(0,len(asc_str)):
                    f.write("li $a0,"+str(asc_str[i])+"\n")
                    f.write("sb $a0,"+str(i)+"($v0)\n")
                f.write("li $a0,"+str(0)+"\n")
                f.write("sb $a0,"+str(len(asc_str))+"($v0)\n")
                if(code[1][0]=='v'):
                    off, control=getVarOffset(code[1])
                    if(control==0):
                        f.write("sw " + "$v0,"+str(-off)+"($gp)\n")
                    else:
                        f.write("sw " + "$v0,"+str(-off)+"($fp)\n")
                else:
                    off=getOffset(code[1])
                    f.write("sw " + "$v0,"+str(-off)+"($fp)\n")
            else:
                string_dict[code[1]]=string_dict[code[3]]
                reg1=getReg(0,code[1])
                regToVar[reg1]=code[1]
                varToReg[code[1]]=reg1

                if(varToReg.get(code[3])==None):
                    reg2=getReg(0)
                    if(code[3][0]=='t'):
                        off=getOffset(code[3])
                        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[3])
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                    regToVar[reg2]=code[3]
                    varToReg[code[3]]=reg2
                else:
                    reg2=varToReg[code[3]]
                f.write("addi $" +str(reg1)+",$"+str(reg2)+",0\n")

    if (len(code) == 5 and code[0][0]!='p'):

        if(code[3][-1]=='g'):
            if((code[2][0]!='t' and code[2][0]!='v') and (code[4][0]!='t' and code[4][0]!='v')): ## Both constants
                asc_str=convertToAscii(code[2][1:-1])+convertToAscii(code[4][1:-1])
                bytes=len(asc_str)-len(asc_str)%4+4
                string_dict[code[0]]=len(asc_str)
                allocateBytes(bytes) # $v0 has the address and $a0 is free
                writeConst(asc_str,0)
                f.write("li $a0,0\nsb $a0,"+str(len(asc_str))+"($v0)\n")
                reg=getReg(0,code[0])
                varToReg[code[0]]=reg
                regToVar[reg]=code[0]
                f.write("addi $"+str(reg)+",$v0,0\n")

            elif((code[2][0]!='t' and code[2][0]!='v')): ## first constant
                asc_str=convertToAscii(code[2][1:-1])
                length=len(asc_str)+string_dict[code[4]]
                string_dict[code[0]]=length
                bytes=length-length%4+4
                allocateBytes(bytes) # $v0 has the address and $a0 is free
                writeConst(asc_str,0)
                if(regReplace==2 or regReplace==4):
                    regReplace=3
                regToVar[2]="busy"
                regToVar[4]="busy"
                if(varToReg.get(code[4])==None):
                    reg2=getReg(0)
                    if(code[4][0]=='t'):
                        off=getOffset(code[4])
                        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[4])
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                    regToVar[reg2]=code[4]
                    varToReg[code[4]]=reg2
                else:
                    reg2=varToReg[code[4]]
                writeVar(reg2,len(asc_str),string_dict[code[4]])
                f.write("li $a0,0\nsb $a0,"+str(length)+"($v0)\n")
                reg=getReg(0,code[0])
                varToReg[code[0]]=reg
                regToVar[reg]=code[0]
                f.write("addi $"+str(reg)+",$v0,0\n")
                regToVar[2]="free"
                regToVar[4]="free"

            elif((code[4][0]!='t' and code[4][0]!='v')): ## second constant
                asc_str=convertToAscii(code[4][1:-1])
                length=len(asc_str)+string_dict[code[2]]
                string_dict[code[0]]=length
                bytes=length-length%4+4
                allocateBytes(bytes) # $v0 has the address and $a0 is free

                if(regReplace==2 or regReplace==4):
                    regReplace=3
                regToVar[2]="busy"
                regToVar[4]="busy"
                if(varToReg.get(code[2])==None):
                    reg2=getReg(0)
                    if(code[2][0]=='t'):
                        off=getOffset(code[2])
                        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[2])
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                    regToVar[reg2]=code[2]
                    varToReg[code[2]]=reg2
                else:
                    reg2=varToReg[code[2]]
                writeVar(reg2,0,string_dict[code[2]])
                writeConst(asc_str,string_dict[code[2]])

                f.write("li $a0,0\nsb $a0,"+str(length)+"($v0)\n")
                reg=getReg(0,code[0])
                varToReg[code[0]]=reg
                regToVar[reg]=code[0]
                f.write("addi $"+str(reg)+",$v0,0\n")
                regToVar[2]="free"
                regToVar[4]="free"

            else:  ## temps or vartemps
                length=string_dict[code[2]]+string_dict[code[4]]
                string_dict[code[0]]=length
                bytes=length-length%4+4
                allocateBytes(bytes) # $v0 has the address and $a0 is free

                if(regReplace==2 or regReplace==4):
                    regReplace=3
                regToVar[2]="busy"
                regToVar[4]="busy"
                if(varToReg.get(code[2])==None):
                    reg2=getReg(0)
                    if(code[2][0]=='t'):
                        off=getOffset(code[2])
                        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[2])
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                    regToVar[reg2]=code[2]
                    varToReg[code[2]]=reg2
                else:
                    reg2=varToReg[code[2]]
                writeVar(reg2,0,string_dict[code[2]])

                if(regReplace==2 or regReplace==4):
                    regReplace=3
                regToVar[2]="busy"
                regToVar[4]="busy"
                if(varToReg.get(code[4])==None):
                    reg2=getReg(0)
                    if(code[4][0]=='t'):
                        off=getOffset(code[4])
                        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[4])
                        if(control==0):
                            f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg2) + ","+str(-off)+"($fp)\n")
                    regToVar[reg2]=code[4]
                    varToReg[code[4]]=reg2
                else:
                    reg2=varToReg[code[4]]
                writeVar(reg2,string_dict[code[2]],string_dict[code[4]])

                f.write("li $a0,0\nsb $a0,"+str(length)+"($v0)\n")
                reg=getReg(0,code[0])
                varToReg[code[0]]=reg
                regToVar[reg]=code[0]
                f.write("addi $"+str(reg)+",$v0,0\n")
                regToVar[2]="free"
                regToVar[4]="free"


########################++++++++++++++++++++++++++++++++++++++++++++++++++++########################################GO

        elif(code[2][0]!='t' and code[2][0]!='v' and code[4][0]!='t' and code[4][0]!='v'):   #constant, constant
            if (code[3][-3]=="i" or code[3][-3]=='u' or code[3]=='bool'):  #integer op
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
                flag=0
                op=code[3][:-5]
                val=eval(code[2]+op+code[4])
                if (val=="True"):
                    val=1
                    flag=1
                elif(val=="False"):
                    val=0
                    flag=1
                reg=getReg(0,code[0])
                regToVar[reg]=code[0]
                varToReg[code[0]]=reg
                if(flag==1):
                    f.write("li $" + str(reg)+","+str(val)+"\n")
                else:
                    f.write("li.s $f0," + str(val)+ "\n" + "mfc1 $"+str(reg) +",$f0\n" )


        elif(code[2][0]!='t' and code[2][0]!='v' and (code[4][0]=='t' or code[4][0]=='v')):   # constant, temp or constant, vartemp
                if (code[3][-3]=="i" or code[3][-3]=='u' or code[3]=='bool'):  #integer op or rune op
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
                else:   ##Float
                    op=code[3][:-5]
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
                    f.write("li.s " + "$f1,"+ str(code[2])+"\n")
                    f.write("mfc1 " + "$"+ str(reg2) + ",$f1"+"\n")
                    regToVar[reg2]="const"
                    reg1=getReg(0,code[0])
                    regToVar[reg1]=code[0]
                    varToReg[code[0]]=reg1
                    writeInstrBinFloat(reg1, reg2, reg3, op)
                    regToVar[reg2]="free"

        elif(code[4][0]!='t' and code[4][0]!='v' and (code[2][0]=='t' or code[2][0]=='v')):   # temp, constant or vartemp, constant
                if (code[3][-3]=="i" or code[3][-3]=='u' or code[3]=='bool'):  #integer op or rune op
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
                    # print(regToVar)
                    # print(varToReg)
                    reg1=getReg(0,code[0])
                    regToVar[reg1]=code[0]
                    varToReg[code[0]]=reg1
                    # print("--",reg1,reg2,reg3)
                    writeInstrBin(reg1, reg2, reg3, op)
                    regToVar[reg3]="free"
                else:   #FLoat for t,c or v,c
                    op=code[3][:-5]
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
                    f.write("li.s " + "$f1,"+ str(code[4])+"\n")
                    f.write("mfc1 " + "$"+ str(reg3) + ",$f1"+"\n")
                    regToVar[reg3]="const"
                    reg1=getReg(0,code[0])
                    regToVar[reg1]=code[0]
                    varToReg[code[0]]=reg1
                    writeInstrBinFloat(reg1, reg2, reg3, op)
                    regToVar[reg3]="free"
        else:  # t,t or t,v, or v,t, or v,v
            if (code[3][-3]=="i" or code[3][-3]=='u' or code[3][-4]=='b' or code[3][-3]=='p'):  #integer or rune  op
                op=code[3][:-3] if (code[3][-3]=="i" or code[3][-3]=='p') else code[3][:-4]
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
            else:    #FLOAT for t,v or v,t etc.
                xxxyyy=0
                op=code[3][:-5]
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
                writeInstrBinFloat(reg1, reg2, reg3, op)

    ########################++++++++++++++++++++++++++++++++++++++++++++++++++++########################################GO

    if (len(code)==3 and code[1]!="malloc"  and (code[0][0]=='t' or code[0][0]=='v') and code[2][0]!="*" and code[2][0]!="r"):  #CHECK
        #reg1=getReg(0,code[0])
        #regToVar[reg1]=code[0]
        #varToReg[code[0]]=reg1
        if(code[2][0]!='t' and code[2][0]!='v'): #constant
            if(code[2].count(".")==0):
                reg2=getReg(0)
                f.write("addi "+ "$" +str(reg2)+",$0," + code[2] +"\n")
                regToVar[reg2]="free"
            else:
                f.write("li.s $f1," + str(code[2])+"\n")
                reg2=getReg(0)
                f.write("mfc1 $"+str(reg2)+ ",$f1\n")
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
        #f.write("addi "+"$"+str(reg1)+ ",$" + str(reg2) + ","+ "0\n")
        if(code[0][0]=='t' or not getType(code[0])):
            reg1=getReg(0,code[0])
            regToVar[reg1]=code[0]
            varToReg[code[0]]=reg1
            f.write("addi "+"$"+str(reg1)+ ",$" + str(reg2) + ","+ "0\n")
        else:
            off,control=getVarOffset(code[0])
            addReg=getReg(0)
            regToVar[addReg]="free"
            if(control==0):
                f.write("addi " + "$"+ str(addReg) + "," + "$gp," + str(-off)+"\n")
            else:
                f.write("addi " + "$"+ str(addReg) + "," + "$fp," + str(-off)+"\n")
            f.write("sw $"+str(reg2)+",0($"+str(addReg)+")\n")





    if(len(code)==4 and code[0]=="*"):
        resetVars()
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
            elif(code[1][0]=='v'):
                off, control=getVarOffset(code[1])
                if(control==0):
                    f.write("addi " + "$"+ str(reg1) + "," + "$gp," + str(-off)+"\n")
                else:
                    f.write("addi " + "$"+ str(reg1) + "," + "$fp," + str(-off)+"\n")
            regToVar[reg1]=code[1]
            varToReg[code[1]]=reg1
        else:
            reg1=varToReg[code[1]]
        # print(code[1],reg1)
        f.write("sw $"+str(reg2)+",0($"+str(reg1)+")\n")

    if(len(code)==4 and code[2]=="*"):
        resetVars()
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
            reset()
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
                    reg1=getReg(0)
                    if(code[1][0]=='t'):
                        off=getOffset(code[1])
                        f.write("lw " + "$"+ str(reg1) + "," + str(-off)+"($fp)\n")
                    else:
                        off, control=getVarOffset(code[1])
                        if(control==0):
                            f.write("lw " + "$"+ str(reg1) + "," + str(-off)+"($gp)\n")
                        else:
                            f.write("lw " + "$"+ str(reg1) + ","+str(-off)+"($fp)\n")
                    regToVar[reg2]=code[1]
                    varToReg[code[1]]=reg2
                else:
                    reg2=varToReg[code[1]]
            reset()
            f.write("blez " + "$"+str(reg1)+"," + code[3] +"\n" )

    if (code[0]=="goto"):
        reset()
        f.write("j " + code[1]+"\n")

    if(len(code)==4 and code[2]=="&"):
        reg1=getReg(0,code[0])
        regToVar[reg1]=code[0]
        varToReg[code[0]]=reg1
        if(code[3][0]=='t'):
            if(varToReg.get(code[3])==None):
                reg2=getReg(0)
                off=getOffset(code[3])
                f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
                regToVar[reg2]=code[3]
                varToReg[code[3]]=reg2
                f.write("addi $"+str(reg1)+",$"+str(reg2)+",0\n")
            else:
                reg2=varToReg[code[3]]
                f.write("addi $"+str(reg1)+",$"+str(reg2)+",0\n")
        else:
            reg2=getReg(0)
            off, control=getVarOffset(code[3])
            if(control==0):
                f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
            else:
                f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
            regToVar[reg2]="free"
            f.write("addi $"+str(reg1)+",$"+str(reg2)+",0\n")

        #if(varToReg.get(code[3])==None):
        #    reg2=getReg(0)
        #    if(code[3][0]=='t'):
        #        off=getOffset(code[3])
        #        f.write("lw " + "$"+ str(reg2) + "," + str(-off)+"($fp)\n")
        #        regToVar[reg2]=code[3]
        #        varToReg[code[3]]=reg2
        #    else:
        #        off, control=getVarOffset(code[3])
        #        if(control==0):
        #            f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
        #        else:
        #            f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
        #        regToVar[reg2]="free"
        #else:
        #    if(code[3][0]=='t'):
        #        reg2=varToReg[code[3]]
        #        f.write("addi $"+str(reg1)+",$"+str(reg2)+",0\n")
        #    else:
        #        reg2=getReg(0)
        #        off, control=getVarOffset(code[3])
        #        if(control==0):
        #            f.write("addi " + "$"+ str(reg2) + "," + "$gp," + str(-off)+"\n")
        #        else:
        #            f.write("addi " + "$"+ str(reg2) + "," + "$fp," + str(-off)+"\n")
        #        regToVar[reg2]="free"
        #        f.write("addi $"+str(reg1)+",$"+str(reg2)+",0\n")


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
        off=size-4
        while size>0:
            f.write("addi $sp,$sp,-4\n")
            f.write("lw $"+str(regToCopy)+","+str(off)+"($"+str(reg)+")\n")
            f.write("sw $"+str(regToCopy)+",0($sp)\n")
            size=size-4
            off=off-4

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
        retOff=scopeTab[0].table[func]["retSizeList"][len(scopeTab[0].table[func]["retSizeList"])-1-retNumber]

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

    if(code[0]=="print_int" or code[0]=="print_bool"):
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

    if(code[0]=="print_rune"):
        saveReg(2)
        f.write("addi "+ "$v0,$0,11\n" )  #print syscall is 1 , $v0 is $2
        saveReg(4)
        if(varToReg.get(code[1])==None):
            if(code[1][0]=='t'):
                off=getOffset(code[1])
                f.write("lb " + "$a0,"+ str(-off)+"($fp)\n")  #CHECK ABOVE
                varToReg[code[1]]=4
                regToVar[4]=code[1]
            elif(code[1][0]=='v'):
                off, control=getVarOffset(code[1])
                if(not getType(code[1])):  #if basic type // only basic types are allowed anyways
                    if(control==0):  # if global
                        f.write("lb " + "$a0," + str(-off)+"($gp)\n")
                    else:
                        f.write("lb " + "$a0," + ","+str(-off)+"($fp)\n")
                varToReg[code[1]]=4
                regToVar[4]=code[1]
            else:  #is a constant
                f.write("addi " + "$a0,$0,"+ code[1]+"\n")   #place constant integer into $4
        else:
            f.write("add " + "$a0,$0,$"+ str(varToReg[code[1]]) +"\n")  #put integer to be printed into $4
        f.write("syscall\n")

    if(code[0]=="print_float"):
        saveReg(2)
        f.write("addi "+ "$v0,$0,2\n" )  #print syscall is 1 , $v0 is $2
        #saveReg(4)  #$4 is a0
        if(varToReg.get(code[1])==None):
            if(code[1][0]=='t'):
                off=getOffset(code[1])
                f.write("lwc1 " + "$f12,"+ str(-off)+"($fp)\n")  #CHECK ABOVE
            elif(code[1][0]=='v'):
                off, control=getVarOffset(code[1])
                if(not getType(code[1])):  #if basic type // only basic types are allowed anyways
                    if(control==0):  # if global
                        f.write("lwc1 " + "$f12," + str(-off)+"($gp)\n")
                    else:
                        f.write("lwc1 " + "$f12," +str(-off)+"($fp)\n")
            else:  #is a constant
                f.write("li.s " + "$f12,"+ code[1]+"\n")   #place constant integer into $4
        else:
            f.write("mtc1 " + "$"+ str(varToReg[code[1]]) + ",$f12" +"\n")  #put integer to be printed into $4
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
        if(varToReg.get(code[1])!=None):
            regToVar[varToReg[code[1]]]="free"
            del varToReg[code[1]]


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
        if(varToReg.get(code[1])!=None):
            regToVar[varToReg[code[1]]]="free"
            del varToReg[code[1]]
    
    if(code[0]=="vscan_float"):
        saveReg(2)
        f.write("addi "+ "$v0,$0,6\n" )  #scanint syscall is 5, $v0 is $2
        f.write("syscall\n")
        off, control=getVarOffset(code[1])
        if(not getType(code[1])):  #if basic type // only basic types are allowed anyways
            if(control==0):  # if global
                f.write("swc1 " + "$f0," + str(-off)+"($gp)\n")  #scanned int is present in $v0
            else:
                f.write("swc1 " + "$f0," +str(-off)+"($fp)\n")
        if(varToReg.get(code[1])!=None):
            regToVar[varToReg[code[1]]]="free"
            del varToReg[code[1]]

    if(code[0]=="scan_float"):
        saveReg(2)
        f.write("addi "+ "$v0,$0,6\n" )  #scanint syscall is 5, $v0 is $2
        f.write("syscall\n")
        if(varToReg.get(code[1])!=None):
            f.write("swc1 " + "$f0," + "0($" +str(varToReg[code[1]])+")\n")
        else:
            off=getOffset(code[1])
            reg=getReg(0,code[1])
            f.write("lw $"+str(reg)+","+str(off)+"($fp)\n")
            regToVar[reg]=code[1]
            varToReg[code[1]]=reg
            f.write("swc1 " + "$f0," + "0($" +str(reg)+")\n")
        if(varToReg.get(code[1])!=None):
            regToVar[varToReg[code[1]]]="free"
            del varToReg[code[1]]

    if(code[0]=="print_string"):
        if(code[1][0]!='\"'):
            saveReg(2)
            saveReg(4)
            if(regReplace==2 or regReplace==4):
                regReplace=3
            regToVar[2]="busy"
            regToVar[4]="busy"

            if(varToReg.get(code[1])==None):
                reg=getReg(0)
                off, control=getVarOffset(code[1])
                if(control==0):
                    f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($gp)\n")
                else:
                    f.write("lw " + "$"+ str(reg) + ","+str(-off)+"($fp)\n")
                regToVar[reg]=code[1]
                varToReg[code[1]]=reg
            else:
                reg=varToReg[code[1]]
            f.write("add $a0,$"+str(reg)+",0\n")
            f.write("li $v0,4\nsyscall\n")
            regToVar[2]="free"
            regToVar[4]="free"
        else:
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

    # print (code)
    # print("-----------------------------------------------")
    # print (regToVar)
    # print("-----------------------------------------------")
    # print(varToReg)
    # f.write("###############################################\n")








f.close()
