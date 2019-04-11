import csv
import ply.yacc as yacc
import os
import pprint
import lexer
import sys
from symTab import symbolTable
from symTab import node

tokens=lexer.tokens
precedence = (
    ('left','LPAREN'),
    ('left','LBRACE'),
    ('left','ID'),
    ('left','DEFINE'),
    ('left','COMMA'),
    ('left','LBRACK'),
    ('left','RBRACK'),
    ('left','DOT'),
    ('left','SEMICOLON'),
    ('left','COLON'),
    ('left','INT'),
    ('left','FLOAT'),
    ('left','STRING'),
    ('left','BREAK'),
    ('left','CONTINUE'),
    ('left','RETURN'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'EQL', 'NEQ','LTN','LEQ','GTN','GEQ'),
    ('left', 'ADD', 'SUB','OR','XOR'),
    ('left', 'MUL', 'DIV','MOD','AND','AND_NOT','SHL','SHR'),
)

basicTypes=["int","float","rune","string","bool"]
scopeTab={}
scopeList=[0]
offsetList=[0]
scopeTab[0]=symbolTable()
currentScope=0
scopeNum=0
currentFunc=0
currentStruct=0
structOff=0
openF=0
openW=0
currentSwitch=0
tempCount=1
labelCount=1
structSymbolList=[]
startFor=[]
endFor=[]
currentFScope=0
switchExp=""
baseOffset=0

def checkUse(ident,checkWhat):
    if(checkWhat=='redeclaration'):
        if(scopeTab[currentScope].search(ident)!=None):
            return True
        else:
            return False
    if(checkWhat=='anywhere'):
        for x in scopeList[::-1]:
            if(scopeTab[x].search(ident)!=None):
                return x+1
        return False

def openS():
    global currentScope
    global scopeList
    global scopeNum
    prevScope=currentScope
    scopeNum+=1
    currentScope=scopeNum
    scopeList.append(currentScope)
    offsetList.append(0)
    scopeTab[currentScope]=symbolTable()
    scopeTab[currentScope].assignParent(prevScope)
    scopeTab[currentScope].typeList=scopeTab[prevScope].typeList
    scopeTab[currentScope].typeSList=scopeTab[prevScope].typeSList
    for x in scopeTab[0].table:
        if(scopeTab[0].table[x]["type"]==["func"]):
            scopeTab[currentScope].insert(x,["func"])
    for x in scopeTab[prevScope].table:
        if(scopeTab[prevScope].table[x]["type"]==["struct"]):
            scopeTab[currentScope].table[x]=scopeTab[prevScope].table[x]

def closeS():
    global currentScope
    global scopeList
    currentScope=scopeList[-2]
    scopeList=scopeList[0:-1]

def checkOprn(exp1,binop,exp2):
    if(exp1!=exp2):
        return None
    if(len(exp1)>1 or len(exp2)>1):
        if(exp1[0]==exp2[0] and exp1[0]=="pointer" and (binop[0]=="==" or binop[0]=="!=")):
            return ["bool"]
        return None
    binop=binop[0]
    exp1=exp1[0]
    exp2=exp2[0]
    if(binop=="||" or binop=="&&"):
        if(exp1=="bool"):
            return [exp1]
        else:
            return None
    if(exp1=="int" or exp1=="rune"):
        if(binop == ">" or binop =="<" or binop=="==" or binop==">=" or binop=="<="or binop=="!="):
            return ["bool"]
        return [exp1]
    if(exp1=="float"):
        if(binop == ">" or binop =="<" or binop=="==" or binop==">=" or binop=="<=" or binop=="==" or binop=="!="):
            return ["bool"]
        if(binop=="|" or binop=="^" or binop=="<<" or binop==">>" or binop=="%" or binop=="&" or binop=="&^"):
            return None
        else:
            return [exp1]
    if(exp1=="string"):
        if(binop=="+"):
            return [exp1]
        else:
            return None

def checkUnOprn(unop,exp1):
    unop=unop[0]
    if(unop=="+" or unop=="-"):
        if(len(exp1)>1):
            return None
        exp1=exp1[0]
        if(exp1=="int" or exp1=="float" or exp1=="rune"):
            return [exp1]
        else:
            return None
    if(unop == "!"):
        if(len(exp1)>1):
            return None
        if(exp1==["bool"]):
            return exp1
        else:
            return None
    if(unop=="^"):
        if(len(exp) >1 or exp1[0]!="int"):
            return None
        else:
            return exp1
    if(unop=="*"):
        if(exp1[0]!="pointer"):
            return None
        exp1=exp1[1:]
        return exp1
    if(unop=="&"):
        exp2=["pointer"]
        exp1= exp2+exp1
        return exp1

def newTemp(a=None):
    global tempCount
    if(a==None):
        newt="temp#"+str(tempCount)
        tempCount+=1
        scopeTab[currentScope].insert(newt,"Temporary")
        offsetList[currentFScope]+=4
        scopeTab[currentScope].updateList(newt,"offset",offsetList[currentFScope])
    else:
        newt="vartemp#"+str(tempCount)
        tempCount+=1
    return newt




def newLabel(a=None):
    global labelCount
    newl="label_"+str(labelCount)
    labelCount+=1
    if(a!=None and a==1):
        startFor.append(newl)
    if(a!=None and a==2):
        endFor.append(newl)
    return newl

def p_SourceFile(p):
    """
    SourceFile : PackageClause SEMICOLON ImportDecl_curl TopLevelDecl_curl
    """
    p[0]=node()
    p[0].code+=p[1].code
    p[0].code+=p[3].code
    p[0].code+=p[4].code
    csv_file = "symTab.csv"
#   print("-----------------------------------------------------------------------")
    with open(csv_file, 'w+') as csvfile:
        for x in range(0,scopeNum+1):
#           print("Table number",x)
            writer=csv.writer(csvfile)
            writer.writerow([])
            writer.writerow(["Table Number",x])
            writer.writerow([])
            writer.writerow(["Parent",x,"=",scopeTab[x].parent])
            writer.writerow([])
            for key,value in scopeTab[x].table.items():
                writer.writerow([key,value])
#           pprint.pprint(scopeTab[x].table)
#           print("-----------------------------------------------------------------------")
#   print("#############################################################################")
    f=open('code.txt',"w")
    for i in range(0,len(p[0].code)):
        y=""
        for x in p[0].code[i]:
            y=y+" "+str(x)
        f.write(y+'\n')

def p_OpenS(p):
    "OpenS : "
    openS()

def p_CloseS(p):
    "CloseS : "
    closeS()

def p_OpenStructS(p):
    "OpenStructS : "
    structSymbolList=[]

def p_CloseStructS(p):
    "CloseStructS : "

def p_TopLevelDecl_curl(p):
    """
    TopLevelDecl_curl : TopLevelDecl_curl TopLevelDecl SEMICOLON
                      |
    """
    p[0]=node()
    if(len(p)>1):
        p[0].code+=p[1].code
        p[0].code+=p[2].code

def p_ImportDecl_curl(p):
    """
    ImportDecl_curl : ImportDecl_curl ImportDecl SEMICOLON
                    |
    """
    p[0]=node()
    if(len(p)>1):
        p[0].code+=p[1].code
        p[0].code+=p[2].code

def p_PackageClause(p):
    """
    PackageClause : PACKAGE ID
    """
    p[0]=node()

def p_ImportDecl(p):
    """
    ImportDecl : IMPORT ImportSpec
               | IMPORT LPAREN ImportSpec_curl RPAREN
    """
    p[0]=node()

def p_ImportSpec_curl(p):
    """
    ImportSpec_curl : ImportSpec_curl ImportSpec SEMICOLON
                    |
    """
    p[0]=node()

def p_ImportSpec(p):
    """
    ImportSpec : ID ImportPath
               | ImportPath
    """
    p[0]=node()


def p_ImportPath(p):
    """
    ImportPath : STRING
    """
    p[0]=node()

def p_TopLevelDecl(p):
    """
    TopLevelDecl : Declaration
                 | FunctionDecl
    """
    p[0]=p[1]

def p_Declaration(p):
    """
    Declaration : ConstDecl
                | StructDecl
                | VarDecl
    """
    p[0]=p[1]

def p_ConstDecl(p):
    """
    ConstDecl : CONST ConstSpec
              | CONST LPAREN ConstSpec_curl RPAREN
    """
    if(len(p)==3):
        p[0]=p[2]
    else:
        p[0]=p[3]

def p_ConstSpec_curl(p):
    """
    ConstSpec_curl : ConstSpec_curl ConstSpec SEMICOLON
                   |
    """
    p[0]=node()
    if(len(p)>1):
        p[0].code+=p[2].code

def p_ConstSpec(p):
    """
    ConstSpec : IdentifierList ID ASSIGN ExpressionList
    """
    p[0]=node()
    p[0].code+=p[1].code
    p[0].code+=p[4].code
    if(isinstance(p[2],str) and not p[2] in basicTypes):
        raise NameError("Invalid type for constant declaration "+p[2], p.lienno(1))

    for x in p[1].idList:
        if(checkUse(x,'redeclaration')==True):
            raise NameError('Redeclaration of identifier:'+x, p.lineno(1))
        else:
            if(isinstance(p[2],str)):
                var1=newTemp(1)
                scopeTab[currentScope].insert(x,[p[2]])
                scopeTab[currentScope].insert(var1,x)
                scopeTab[currentScope].updateList(x,"tmp",var1)
                offsetList[currentFScope]+=scopeTab[currentScope].typeSList[p[2]]
                scopeTab[currentScope].updateList(x,"offset",offsetList[currentFScope])

            scopeTab[currentScope].updateList(x,'constant',True)

    if(len(p[1].idList) != len(p[4].expTList)):
        raise NameError("Imbalanced assignment", p.lineno(1))

    for i in range(0,len(p[1].idList)):
        if(p[4].expTList[i] != scopeTab[currentScope][p[1].idList[i]]["type"]):
            raise ("Mismatch of type for "+p[1].idList[i])

    for i in range(0,len(p[1].idList)):
        temp=[scopeTab[currentScope].table[p[1].idList[i]]["tmp"],"="]
        if(p[4].info["dereflist"][i]==1):
            temp.append("*")
        temp.append(p[4].expList[i])
        p[0].code.append(temp)


def p_IdentifierList(p):
    """
    IdentifierList : ID
                   | ID COMMA IdentifierList
    """
    p[0]=node()
    if(len(p)==2):
        p[0].idList.append(p[1])
    else:
        p[0].idList.append(p[1])
        p[0].idList=p[0].idList+p[3].idList

def p_ExpressionList(p):
    """
    ExpressionList : Expression
                   | ExpressionList COMMA Expression
    """
    p[0]=node()
    if(len(p)==2):
        p[0].expTList+=p[1].expTList
        p[0].code=p[1].code
        p[0].info["dereflist"]=[]
        if(p[1].info.get("deref")==None):
            p[0].expList+=p[1].expList
            for i in range(0,len(p[1].expList)):
                p[0].info["dereflist"].append(0)
        else:
            p[0].expList+=p[1].expList
            p[0].info["dereflist"]=[1]
        if(p[1].info.get("memory")):
            p[0].info["memory"]=1
        else:
            p[0].info["memory"]=0
    else:
        p[0].expTList+=p[1].expTList
        p[0].expTList+=p[3].expTList
        p[0].expList+=p[1].expList
        p[0].info["dereflist"]=p[1].info["dereflist"]
        if(p[3].info.get("deref")==None):
            p[0].expList+=p[3].expList
            for i in range(0,len(p[3].expList)):
                p[0].info["dereflist"].append(0)
        else:
            p[0].expList+=p[3].expList
            p[0].info["dereflist"].append(1)
        p[0].code=p[1].code+p[3].code
        if(p[1].info["memory"]==1 and p[3].info["memory"]==1):
            p[0].info["memory"]=1
        else:
            p[0].info["memory"]=0

def p_StructDecl(p):
    """
    StructDecl : TYPE StructName StructType
    """
    p[0]=node()
    scopeTab[currentScope].typeList.append(currentStruct)
    scopeTab[currentScope].typeSList[currentStruct]=structOff

def p_StructName(p):
    """
    StructName : ID
    """
    p[0]=node()
    global currentStruct,structOff
    currentStruct=p[1]
    structOff=0
    if(p[1] in scopeTab[currentScope].typeList):
        raise NameError("StructName has been already used", p.lineno(1))
    if(p[1] in scopeTab[currentScope].table):
        raise NameError("This name has been already assigned", p.lineno(1))
    scopeTab[currentScope].insert(p[1],["struct"])

def p_VarDecl(p):
    """
    VarDecl : VAR VarSpec
            | VAR LPAREN VarSpec_curl RPAREN
    """
    if(len(p)==3):
        p[0]=p[2]
    else:
        p[0]=p[3]

def p_VarSpec_curl(p):
    """
    VarSpec_curl : VarSpec_curl VarSpec SEMICOLON
                 |
    """
    p[0]=node()
    if(len(p)>1):
        p[0].code+=p[2].code

def p_VarSpec(p):
    """
    VarSpec : IdentifierList Type ASSIGN ExpressionList
            | IdentifierList ID ASSIGN ExpressionList
            | IdentifierList ASSIGN ExpressionList
            | IdentifierList ID
            | IdentifierList Type
    """
    p[0]=node()
    if (len(p)==5):
        for i in range(0,len(p[4].expTList)):
            if(not (p[4].expTList[i][0] in basicTypes or p[4].expTList[i][0]=="pointer")):
                raise NameError ("Invalid Assignment",p.lineno(1))

    if(isinstance(p[2],str) and p[2]!="=" and not p[2] in scopeTab[currentScope].typeList):
        raise NameError("Invalid type of identifier "+p[2], p.lineno(1))

    if(len(p)==5 or len(p)==3):
        for x in p[1].idList:
            if(checkUse(x,'redeclaration')==True):
                raise NameError('Redeclaration of identifier:'+x, p.lineno(1))
            else:
                if(isinstance(p[2],str)):
                    var1=newTemp(1)
                    scopeTab[currentScope].insert(x,[p[2]])
                    scopeTab[currentScope].insert(var1,x)
                    scopeTab[currentScope].updateList(x,"tmp",var1)
                    offsetList[currentFScope]+=scopeTab[currentScope].typeSList[p[2]]
                    scopeTab[currentScope].updateList(x,"offset",offsetList[currentFScope])

                else:
                    var1=newTemp(1)
                    scopeTab[currentScope].insert(x,p[2].type)
                    scopeTab[currentScope].insert(var1,x)
                    scopeTab[currentScope].updateList(x,"tmp",var1)
                    offsetList[currentFScope]+=p[2].info["typesize"]
                    scopeTab[currentScope].updateList(x,"offset",offsetList[currentFScope])


    if(len(p)==5):
        if(len(p[1].idList) != len(p[4].expTList)):
            raise NameError("Imbalanced assignment", p.lineno(1))
        for i in range(0,len(p[1].idList)):
            if(p[4].expTList[i] != scopeTab[currentScope].table[p[1].idList[i]]["type"]):
                raise NameError("Mismatch of type for "+p[1].idList[i],p.lineno(1))
        p[0]=node()
        p[0].code=p[1].code+p[4].code
        for i in range(0,len(p[1].idList)):
            temp=[scopeTab[currentScope].table[p[1].idList[i]]["tmp"],"="]
            if(p[4].info["dereflist"][i]==1):
                temp.append("*")
            temp.append(p[4].expList[i])
            p[0].code.append(temp)

    if(len(p)==4):
        if(len(p[1].idList) != len(p[3].expTList)):
            raise NameError("Imbalanced assignment", p.lineno(1))
        for i in range(0,len(p[1].idList)):
            if(len(p[3].expTList[i])>1):
                raise NameError("Auto assignment of complex expressions not allowed",p.lineno(1))
            if(not p[3].expTList[i][0] in basicTypes):
                raise NameError("Auto assignment of only basic types allowed",p.lineno(1))
            if(checkUse(p[1].idList[i],'redeclaration')==True):
                raise NameError('Redeclaration of identifier:'+p[1].idList[i], p.lineno(1))
            var1=newTemp(1)
            scopeTab[currentScope].insert(p[1].idList[i],p[3].expTList[i])
            scopeTab[currentScope].insert(var1,p[1].idList[i])
            scopeTab[currentScope].updateList(p[1].idList[i],"tmp",var1)
            offsetList[currentFScope]+=scopeTab[currentScope].typeSList[p[3].expTList[i][0]]
            scopeTab[currentScope].updateList(p[1].idList[i],"offset",offsetList[currentFScope])

            p[0]=node()
            p[0].code=p[1].code+p[3].code
            for i in range(0,len(p[1].idList)):
                temp=[scopeTab[currentScope].table[p[1].idList[i]]["tmp"],"="]
                if(p[3].info["dereflist"][i]==1):
                    temp.append("*")
                temp.append(p[3].expList[i])
                p[0].code.append(temp)

def p_FunctionDecl(p):
    """
    FunctionDecl : FUNC SetBase FuncName OpenS Signature Block CloseBase CloseS
    """
    p[0]=node()
    p[0].code=p[3].code+p[5].code
    p[0].code+=p[6].code
    p[0].code.append(["return"])

def p_SetBase(p):
    "SetBase : "
    global currentFScope
    global scopeNum
    currentFScope=scopeNum+1

def p_CloseBase(p):
    "CloseBase : "
    scopeTab[currentScope].insert("#total_size",offsetList[currentFScope])

def p_FuncName(p):
    """
    FuncName : ID
    """
    p[0]=node()
    global currentFunc
    if(checkUse(p[1],'redeclaration')==True):
        raise NameError('The name of function has been used elsewhere :'+p[1], p.lineno(1))
    scopeTab[0].insert(p[1],["func"])
    scopeTab[0].updateList(p[1],"Scope",currentFScope)
    currentFunc=p[1]
    p[0].code.append([p[1],":"])

def p_Type(p):
    """
    Type : LPAREN Type RPAREN
         | LPAREN ID RPAREN
         | TypeLit
    """
    p[0]=node()
    if(len(p)==2):
        p[0]=p[1]
    else:
        if(isinstance(p[2],str) and not p[2] in scopeTab[currentScope].typeList):
            raise NameError("Invalid type of identifier "+p[2], p.lineno(1))
        if(isinstance(p[2],str)):
            p[0]=node()
            p[0].type.append(p[2])
            p[0].info["typesize"]=scopeTab[currentScope].typeSList[p[2]]
        else:
            p[0]=p[2]

def p_TypeLit(p):
    """
    TypeLit : ArrayType
            | PointerType
    """
    p[0]=p[1]

def p_ArrayType(p):
    """
    ArrayType : LBRACK INT RBRACK Type
              | LBRACK INT RBRACK ID
    """
    if(isinstance(p[4],str) and not p[4] in scopeTab[currentScope].typeList):
        raise NameError("This type hasn't been declared yet "+p[4], p.lineno(1))
    temp=int(p[2])
    if(isinstance(p[4],str)):
        p[0]=node()
        p[0].type.append("arr"+p[2])
        p[0].type.append(p[4])
        p[0].info["typesize"]=temp*scopeTab[currentScope].typeSList[p[4]]
    else:
        p[0]=node()
        p[0].type.append("arr"+p[2])
        p[0].type+=p[4].type
        p[0].info["typesize"]=temp*p[4].info["typesize"]

def p_StructType(p):
    """
    StructType : STRUCT OpenStructS LBRACE FieldDecl_curl RBRACE CloseStructS
    """
    p[0]=node()

def p_FieldDecl_curl(p):
    """
    FieldDecl_curl : FieldDecl_curl FieldDecl SEMICOLON
                   |
    """
    p[0]=node()

def p_FieldDecl(p):
    """
    FieldDecl : ID COMMA IdentifierList Type
              | ID COMMA IdentifierList ID
              | ID Type
              | ID ID
              | ID STRUCT MUL ID
              | ID COMMA IdentifierList STRUCT MUL ID
    """
    p[0]=node()
    global structOff
    if(len(p)==3):
        if(isinstance(p[2],str)):
            if(p[1] in structSymbolList):
                raise NameError("This identifier is already declared in this list", p.lineno(1))
            structSymbolList.append(p[1])
            scopeTab[currentScope].updateList(currentStruct,p[1],[p[2]])
            scopeTab[currentScope].updateList(currentStruct,"offset "+p[1],structOff)
            structOff+=scopeTab[currentScope].typeSList[p[2]]
        else:
            if(p[1] in structSymbolList):
                raise NameError("This identifier is already declared in this list", p.lineno(1))
            structSymbolList.append(p[1])
            scopeTab[currentScope].updateList(currentStruct,p[1],p[2].type)
            scopeTab[currentScope].updateList(currentStruct,"offset "+p[1],structOff)
            structOff+=p[2].info["typesize"]
    elif(len(p)==5 and not isinstance(p[3],str)):
        if(isinstance(p[4],str)):
            if(p[1] in structSymbolList):
                raise NameError("This identifier is already declared in this list", p.lineno(1))
            structSymbolList.append(p[1])
            scopeTab[currentScope].updateList(currentStruct,p[1],[p[4]])
            scopeTab[currentScope].updateList(currentStruct,"offset "+p[1],structOff)
            structOff+=scopeTab[currentScope].typeSList[p[4]]
            for x in p[3].idList:
                if(x in structSymbolList):
                    raise NameError("This identifier is already declared in this list", p.lineno(1))
                structSymbolList.append(x)
                scopeTab[currentScope].updateList(currentStruct,x,[p[4]])
                scopeTab[currentScope].updateList(currentStruct,"offset "+x,structOff)
                structOff+=scopeTab[currentScope].typeSList[p[4]]
        else:
            if(p[1] in structSymbolList):
                raise NameError("This identifier is already declared in this list", p.lineno(1))
            structSymbolList.append(p[1])
            scopeTab[currentScope].updateList(currentStruct,p[1],p[4].type)
            scopeTab[currentScope].updateList(currentStruct,"offset "+p[1],structOff)
            structOff+=p[4].info["typesize"]
            for x in p[3].idList:
                if(x in structSymbolList):
                    raise NameError("This identifier is already declared in this list", p.lineno(1))
                structSymbolList.append(x)
                scopeTab[currentScope].updateList(currentStruct,x,p[4].type)
                scopeTab[currentScope].updateList(currentStruct,"offset "+x,structOff)
                structOff+=p[4].info["typesize"]
    elif(len(p)==5):
        if(p[4]!=currentStruct):
            raise NameError("The identifier should be the current struct", p.lineno(1))
        structSymbolList.append(p[1])
        scopeTab[currentScope].updateList(currentStruct, p[1], ["pointer",currentStruct])
        scopeTab[currentScope].updateList(currentStruct,"offset "+p[1],structOff)
        structOff+=4
    else:
        if(p[6]!=currentStruct):
            raise NameError("The identifier should be the current struct", p.lineno(1))
        structSymbolList.append(p[1])
        scopeTab[currentScope].updateList(currentStruct, p[1], ["pointer",currentStruct])
        for x in p[3].idList:
            if(x in structSymbolList):
                raise NameError("This identifier is already declared in this list", p.lineno(1))
            structSymbolList.append(x)
            scopeTab[currentScope].updateList(currentStruct,x,["pointer",currentStruct])
            scopeTab[currentScope].updateList(currentStruct,"offset "+x,structOff)
            structOff+=4

def p_PointerType(p):
    """
    PointerType : MUL Type
                | MUL ID
    """
    if(isinstance(p[2],str) and not p[2] in scopeTab[currentScope].typeList):
        raise NameError("Invalid type of identifier "+p[2], p.lineno(1))
    if(isinstance(p[2],str)):
        p[0]=node()
        p[0].type.append("pointer")
        p[0].type.append(p[2])
        p[0].info["typesize"]=4
    else:
        p[0]=node()
        p[0].type.append("pointer")
        p[0].type+=p[2].type
        p[0].info["typesize"]=4

def p_Signature(p):
    """
    Signature : Parameters Result
    """
    p[0]=node()

def p_Result(p):
    """
    Result : LPAREN TypeList RPAREN
           |
    """
    p[0]=node()
    if(len(p)==1):
        scopeTab[0].updateList(currentFunc,"returns",[["void"]])
        scopeTab[0].updateList(currentFunc,"#total_retSize",0)
        scopeTab[0].updateList(currentFunc,"retSizeList",[])
    else:
        scopeTab[0].updateList(currentFunc,"returns",p[2].idList)
        total_sum=-8- scopeTab[0].table[currentFunc]["#total_parSize"]
        retList=[]
        re_sum=0
        for i in range(0,len(p[2].idList)):
            retList.append(total_sum)
            total_sum-=p[2].expList[i]
            re_sum+=p[2].expList[i]
        scopeTab[0].updateList(currentFunc,"#total_retSize",re_sum)
        scopeTab[0].updateList(currentFunc,"retSizeList",retList)

def p_TypeList(p):
    """
    TypeList : ID
             | Type
             | TypeList COMMA ID
             | TypeList COMMA Type
    """
    if(isinstance(p[1],str) and not p[1] in scopeTab[currentScope].typeList):
        raise NameError("Invalid return type "+p[1], p.lineno(1))
    if(len(p)==4 and isinstance(p[3],str) and not p[3] in scopeTab[currentScope].typeList):
        raise NameError("Invalid return type "+p[3], p.lineno(1))
    p[0]=node()
    if(len(p)==2):
        if(isinstance(p[1],str)):
            p[0].idList.append([p[1]])
            p[0].expList.append(scopeTab[currentScope].typeSList[p[1]])  #mag
        else:
            p[0].idList.append(p[1].type)
            p[0].expList.append(p[1].info["typesize"])
    else:
        if(isinstance(p[3],str)):
            p[0].idList=p[1].idList
            p[0].expList=p[1].expList
            p[0].idList.append([p[3]])
            p[0].expList.append(scopeTab[currentScope].typeSList[p[3]])
        else:
            p[0].idList=p[1].idList
            p[0].expList=p[1].expList
            p[0].idList.append(p[3].type)
            p[0].expList.append(p[3].info["typesize"])

def p_Parameters(p):
    """
    Parameters : LPAREN RPAREN
               | LPAREN ParameterList RPAREN
               | LPAREN ParameterList COMMA RPAREN
    """
    p[0]=node()
    if(len(p)==3):
        scopeTab[0].updateList(currentFunc,"takes",[["void"]])
        scopeTab[0].updateList(currentFunc,"#total_parSize",0)
    else:
        scopeTab[0].updateList(currentFunc,"takes",p[2].expTList)
        argOffset=-8
        parSum=0
        parList=[]
        n=len(p[2].idList)
        for i in range(0,len(p[2].idList)):
            scopeTab[currentScope].updateList(p[2].idList[n-i-1],"offset",argOffset)
            parList.append(p[2].expList[i])
            argOffset-=p[2].expList[n-i-1]
            parSum+=p[2].expList[i]
        scopeTab[0].updateList(currentFunc,"#total_parSize",parSum)
        scopeTab[0].updateList(currentFunc,"parSizeList",parList)

def p_ParameterList(p):
    """
    ParameterList : ParameterDecl
                  | ParameterList COMMA ParameterDecl
    """
    p[0]=node()
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0].idList=p[1].idList
        p[0].idList+=(p[3].idList)
        p[0].expTList=p[1].expTList
        p[0].expTList+=(p[3].expTList)
        p[0].expList=p[1].expList
        p[0].expList+=(p[3].expList)

def p_ParameterDecl(p):
    """
    ParameterDecl : ParaIdList Type
                  | ID Type
                  | ParaIdList ID
                  | ID ID
    """
    if(isinstance(p[2],str) and not p[2] in scopeTab[currentScope].typeList):
        raise NameError("Invalid type of identifier "+p[2], p.lineno(1))

    p[0]=node()
    if(not isinstance(p[1],str)):
        p[0].idList=p[1].idList
        for x in p[1].idList:
            if(checkUse(x,'redeclaration')==True):
                    raise NameError('Redeclaration of identifier:'+x, p.lineno(1))
            else:
                if(isinstance(p[2],str)):
                    var1=newTemp(1)
                    scopeTab[currentScope].insert(x,[p[2]])
                    scopeTab[currentScope].insert(var1,x)
                    scopeTab[currentScope].updateList(x,"tmp",var1)
                    p[0].expTList.append([p[2]])
                    p[0].expList.append(scopeTab[currentScope].typeSList[p[2]])
                else:
                    var1=newTemp(1)
                    scopeTab[currentScope].insert(x,p[2].type)
                    scopeTab[currentScope].insert(var1,x)
                    scopeTab[currentScope].updateList(x,"tmp",var1)
                    p[0].expTList.append(p[2].type)
                    p[0].expList.append(p[2].info["typesize"])
    else:
        if(checkUse(p[1],'redeclaration')==True):
            raise NameError('Redeclaration of identifier:'+x, p.lineno(1))
        else:
            p[0].idList=[p[1]]
            if(isinstance(p[2],str)):
                var1=newTemp(1)
                scopeTab[currentScope].insert(p[1], [p[2]])
                scopeTab[currentScope].insert(var1,p[1])
                scopeTab[currentScope].updateList(p[1],"tmp",var1)
                p[0].expTList.append([p[2]])
                p[0].expList.append(scopeTab[currentScope].typeSList[p[2]])
            else:
                var1=newTemp(1)
                scopeTab[currentScope].insert(p[1], p[2].type)
                scopeTab[currentScope].insert(var1,p[1])
                scopeTab[currentScope].updateList(p[1],"tmp",var1)
                p[0].expTList.append(p[2].type)
                p[0].expList.append(p[2].info["typesize"])


def p_ParaIdList(p):
    """
    ParaIdList : ID COMMA ID
               | ParaIdList COMMA ID
    """
    p[0]=node()
    if(isinstance(p[1],str)):
        p[0].idList.append(p[1])
        p[0].idList.append(p[3])
    else:
        p[0].idList=p[1].idList
        p[0].idList.append(p[3])

def p_Block(p):
    """
    Block : LBRACE StatementList RBRACE
    """
    p[0]=p[2]

def p_StatementList(p):
    """
    StatementList : Statement_curl
    """
    p[0]=p[1]

def p_Statement_curl(p):
    """
    Statement_curl : Statement_curl Statement SEMICOLON
                   |
    """
    p[0]=node()
    if(len(p)>1):
        p[0].code=p[1].code+p[2].code
        if(p[1].info.get("hasRStmt")!= None or p[2].info.get("hasRStmt")!=None):
            p[0].info["hasRStmt"]=1
def p_Expression(p):
    """
    Expression : UnaryExpr
               | Expression BinaryOp UnaryExpr
    """
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=node()
        if(len(p[1].expTList)>1 or len(p[3].expTList)>1):
            raise NameError("Can't apply binary operators to multiple values", p.lineno(1))
        if(checkOprn(p[1].expTList[0] , p[2].expTList[0], p[3].expTList[0] )==None):
            raise NameError("Invalid types for operator ",p[2].expTList[0],p.lineno(1))

        p[0].code=p[1].code+p[3].code
        if (p[1].info.get("deref")!=None):
            var1=newTemp()
            p[0].code.append([var1,"=","*",p[1].expList[0]])
        else:
            var1=p[1].expList[0]
        if (p[3].info.get("deref")!=None):
            var2=newTemp()
            p[0].code.append([var2,"=","*",p[3].expList[0]])
        else:
            var2=p[3].expList[0]
        p[0].expTList.append(checkOprn(p[1].expTList[0] , p[2].expTList[0], p[3].expTList[0] ))
        p[0].info["memory"]=0
        var3=newTemp()
        p[0].expList=[var3]
        if(p[3].expTList[0][0]=="pointer"):
            p[3].expTList[0][0]="ptr"
        p[0].code.append([var3,"=",var1,p[2].expTList[0][0]+p[3].expTList[0][0],var2])

def p_UnaryExpr(p):
    """
    UnaryExpr : PrimaryExpr
              | UnaryOp UnaryExpr
    """
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=node()
        if(len(p[1].expTList)>1):
            raise NameError("Can't apply unary operators to multiple values", p.lineno(1))
        if(checkUnOprn(p[1].expTList[0], p[2].expTList[0])==None):
            raise NameError("Invalid types for operator ",p[2].expTList[0], p.lineno(1))
        p[0].expTList.append(checkUnOprn(p[1].expTList[0], p[2].expTList[0]))
        p[0].code=p[2].code
        if(p[1].expTList[0][0]=="*"):
            p[0].info["memory"]=1
            p[0].info["deref"]=1
            var1=newTemp()
            p[0].code.append([var1,"=","*",p[2].expList[0]])
            p[0].expList=[var1]
        elif(p[1].expTList[0][0]=="&"):
            p[0].info["memory"]=0
            if(p[2].info.get("deref")==None):
                if(p[2].info["memory"]==0):
                    raise NameError("Can't get address",p.lineno(1))
                var1=newTemp()
                p[0].code.append([var1,"=","&",p[2].expList[0]])
                p[0].expList=[var1]
            else:
                p[0].expList=p[2].expList
        else:
            p[0].info["memory"]=0
            var1=newTemp()
            p[0].expList=[var1]
            if(p[1].expTList[0][0]=='+' or p[1].expTList[0][0]=='-'):
                p[0].code.append([var1,"=",0,p[1].expTList[0][0]+p[2].expTList[0][0],p[2].expList[0]])
            if(p[1].expTList[0][0]=='!'):
                p[0].code.append([var1,"=",1,'^'+p[2].expTList[0][0],p[2].expList[0]])
            if(p[1].expTList[0][0]=='^'):
                p[0].code.append([var1,"=",1,'+'+p[2].expTList[0][0],p[2].expList[0]])
                p[0].code.append([var1,"=",0,'-'+p[2].expTList[0][0],var1])

def p_BinaryOp(p):
    """
    BinaryOp : LOR
             | LAND
             | RelOp
             | AddOp
             | MulOp
    """
    if(not isinstance(p[1],str)):
        p[0]=p[1]
    else:
        p[0]=node()
        p[0].expTList.append([p[1]])

def p_RelOp(p):
    """
    RelOp : EQL
          | NEQ
          | LTN
          | LEQ
          | GTN
          | GEQ
    """
    p[0]=node()
    p[0].expTList.append([p[1]])


def p_AddOp(p):
    """
    AddOp : ADD
          | SUB
          | OR
          | XOR
    """
    p[0]=node()
    p[0].expTList.append([p[1]])

def p_MulOp(p):
    """
    MulOp : MUL
          | DIV
          | MOD
          | SHL
          | SHR
          | AND
          | AND_NOT
    """
    p[0]=node()
    p[0].expTList.append([p[1]])

def p_UnaryOp(p):
    """
    UnaryOp : ADD
            | SUB
            | NOT
            | XOR
            | MUL
            | AND
    """
    p[0]=node()
    p[0].expTList.append([p[1]])

#Removed Conversion
def p_PrimaryExpr(p):
    """
    PrimaryExpr : Literal
                | ID
                | PrimaryExpr DOT ID
                | LPAREN Expression RPAREN
                | PrimaryExpr Index
                | PrimaryExpr Arguments
    """
    if(len(p)==2 and not isinstance(p[1],str)):
        p[0]=p[1]
        p[0].info["memory"]=0
        p[0].expList=p[1].expList
    elif(len(p)==2):
        if(checkUse(p[1],"anywhere")==False):
            raise NameError("Undeclared identifier "+p[1], p.lineno(1))
        p[0]=node()
        p[0].expTList.append(scopeTab[checkUse(p[1],"anywhere")-1].table[p[1]]["type"])
        p[0].info["memory"]=1
        p[0].info["isID"]=p[1]
        x=checkUse(p[1],'anywhere')-1
        temp1=scopeTab[x].table[p[1]]["type"]
        if(temp1!=["func"]):
            p[0].expList=[scopeTab[checkUse(p[1],'anywhere')-1].table[p[1]]["tmp"]]
        else:
            p[0].expList=["func"]
        if(scopeTab[x].table.get(temp1[0])!=None):
            if(scopeTab[x].table[temp1[0]]["type"]==["struct"]):
                var1=newTemp()
                p[0].code.append([var1,"=", "&",scopeTab[checkUse(p[1],'anywhere')-1].table[p[1]]["tmp"]])
                p[0].info["deref"]=1
                p[0].expList=[var1]
        elif(temp1[0][0:3]=="arr" or temp1[0]=="pointer"):
            p[0].info["deref"]=1

    elif(len(p)==4 and p[2]=='.'):
        temp=p[1].expTList[0][0]
        if(scopeTab[currentScope].table.get(temp)!=None and scopeTab[currentScope].table[temp]["type"]==["struct"]):
            if(scopeTab[currentScope].table[temp].get(p[3])==None):
                raise NameError("No such attribute of given struct",p.lineno(1))
            p[0]=node()
            p[0].expTList.append(scopeTab[currentScope].table[temp][p[3]])
            p[0].info["memory"]=1
            p[0].code=p[1].code
            var1=newTemp()
            off=scopeTab[currentScope].table[p[1].expTList[0][0]]["offset "+p[3]]
            p[0].code.append([var1, "=", p[1].expList[0], '+int', off])
            p[0].info["deref"]=1
            p[0].expList.append(var1)
        else:
            raise NameError("The identifier is not declared or isn't a struct", p.lineno(1))

    elif(len(p)==4):
        p[0]=p[2]

    elif(p[2].info.get("index")!=None):
        if(p[1].expTList[0][0][0:3]!="arr"):
            raise NameError("The type of this expression is not an array ", p.lineno(1))
        p[0]=p[1]
        p[0].code+=p[2].code
        p[0].expTList[0]=p[0].expTList[0][1:]
        p[0].info["memory"]=1
        p[0].info["deref"]=1
        var1=newTemp()
        p[0].code.append([var1,"=",p[2].expList[0]])
        for i in range(0,len(p[0].expTList[0])):
            if(p[0].expTList[0][i][0:3]=="arr"):
                temp1=int(p[0].expTList[0][i][3:])
                p[0].code.append([var1,"=",var1,"*int",temp1])
            else:
                width=0
                if(p[0].expTList[0][i]=="pointer"):
                    width=4
                else:
                    width=scopeTab[currentScope].typeSList[p[0].expTList[0][i]]
                p[0].code.append([var1,"=",var1,"*int",width])
                p[0].code.append([var1,"=",var1,'+int',p[0].expList[0]])
                break
        p[0].expList=[var1]

    elif(p[2].info.get("arguments")!=None):
        if(p[1].expTList[0][0]!="func" or p[1].info.get("isID")==None):
            raise NameError("The primary expression is not a function", p.lineno(1))
        if(p[2].expTList != scopeTab[0].table[p[1].info["isID"]]["takes"]):
            raise NameError("Signature mismatch for function", p.lineno(1))
        p[0]=node()
        p[0].expTList=scopeTab[0].table[p[1].info["isID"]]["returns"]
        if(p[0].expTList[0][0]=="void"):
            p[0].expList=[]
        else:
            for i in range(0,len(p[0].expTList)):
                var1=newTemp()
                p[0].expList.append(var1)
        p[0].info["multi_return"]=1
        p[0].info["memory"]=0
        p[0].code=p[2].code
        p[0].code.append(["startf",p[1].info["isID"]])
        for i in range(0,len(p[2].expList)):
            if(p[2].info["dereflist"][i]==1):
                # var1=newTemp()
                # p[0].code.append([var1,"=","*",p[2].expList[i]])
                # p[0].code.append(["param",var1])
                p[0].code.append(["param",p[2].expList[i],scopeTab[0].table[p[1].info["isID"]]["parSizeList"][i]  ])
            else:
                p[0].code.append(["param",p[2].expList[i]])
        p[0].code.append(["call",p[1].info["isID"]])
        p[0].code.append(["endf",p[1].info["isID"]])
        for i in range(0,len(p[0].expList)):
            p[0].code.append([p[0].expList[i],"=","retval_"+str(i+1)])

def p_Index(p):
    """
    Index : LBRACK Expression RBRACK
    """
    if(p[2].expTList!=[["int"]]):
        raise NameError("Only integer indices are allowed", p.lineno(1))
    p[0]=p[2]
    p[0].info["index"]=1

def p_Arguments(p):
    """
    Arguments : LPAREN RPAREN
              | LPAREN ExpressionList RPAREN
              | LPAREN ExpressionList COMMA RPAREN
    """
    if(len(p)==3):
        p[0]=node()
        p[0].info["arguments"]=1
        p[0].expTList.append(["void"])
    else:
        p[0]=p[2]
        p[0].info["arguments"]=1
        p[0].expTList=p[2].expTList

def p_Literal(p):
    """
    Literal : BasicLit
    """
    p[0]=p[1]

def p_BasicLit(p):
    """
    BasicLit : IntLit
             | FloatLit
             | RuneLit
             | StringLit
             | TrueLit
             | FalseLit
    """
    p[0]=p[1]

def p_TrueLit(p):
    """
    TrueLit : TRUE
    """
    p[0]=node()
    p[0].expTList.append(["bool"])
    p[0].expList.append(1)

def p_FalseLit(p):
    """
    FalseLit : FALSE
    """
    p[0]=node()
    p[0].expTList.append(["bool"])
    p[0].expList.append(0)

def p_IntLit(p):
    """
    IntLit : INT
    """
    p[0]=node()
    p[0].expTList.append(["int"])
    p[0].expList.append(p[1])

def p_FloatLit(p):
    """
    FloatLit : FLOAT
    """
    p[0]=node()
    p[0].expTList.append(["float"])
    p[0].expList.append(p[1])

def p_RuneLit(p):
    """
    RuneLit : RUNE
    """
    p[0]=node()
    p[0].expTList.append(["rune"])
    p[0].expList.append(p[1])

def p_StringLit(p):
    """
    StringLit : STRING
    """
    p[0]=node()
    p[0].expTList.append(["string"])
    p[0].expList.append(p[1])

def p_Statement(p):
    """
    Statement : Declaration
              | SimpleStmt
              | ReturnStmt
              | BreakStmt
              | ContinueStmt
              | IfStmt
              | OpenS Block CloseS
              | SwitchStmt
              | ForStmt
              | PrintStmt
              | ScanStmt
    """
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[2]

def p_PrintStmt(p):
    """
    PrintStmt : PRINT ExpressionList
    """
    p[0]=node()
    p[0].code=p[2].code
    for i in range(0,len(p[2].expTList)):
        if( not (p[2].expTList[i][0] in basicTypes)):
            raise NameError ("We can only print the basic types",p.lineno(1))

        if(p[2].info["dereflist"][i]==1):
            var1=newTemp()
            p[0].code.append([var1,"=","*",p[2].expList[i]])
            p[0].code.append(['print_'+p[2].expTList[i][0],var1])
        else:
            p[0].code.append(['print_'+p[2].expTList[i][0],p[2].expList[i]])

def p_ScanStmt(p):
    """
    ScanStmt : SCAN ExpressionList
    """
    p[0]=node()
    p[0].code=p[2].code
    for i in range(0,len(p[2].expTList)):
        if( not (p[2].expTList[i][0] in basicTypes)):
            raise NameError ("We can only scan the basic types",p.lineno(1))

        if(p[2].info["dereflist"][i]==1):
            var1=newTemp()
            p[0].code.append(['scan_'+p[2].expTList[i][0],p[2].expList[i]])
        elif(p[2].expList[i][0:2]=="va"):
            p[0].code.append(['vscan_'+p[2].expTList[i][0],p[2].expList[i]])
        else:
            raise NameError("We can only scan to memory location",p.lineno(1))


def p_SimpleStmt(p):
    """
    SimpleStmt : Expression
               | IncDecStmt
               | Assignment
               | ShortVarDecl
               |
    """
    if(len(p)>1):
        p[0]=p[1]
    else:
        p[0]=node()
    b=node()
    if(p[1].expTList!=[]):
        if(p[1].expTList==[["void"]]):
            a=0
        else:
            raise NameError("Statement must have void return type", p.lineno(1))

def p_IncDecStmt(p):
    """
    IncDecStmt : Expression INC
               | Expression DEC
    """
    p[0]=p[1]
    if(p[0].expTList!=[["int"]]):
        raise NameError("This operation can only be done on integers", p.lineno(1))
    if(p[1].info["memory"]==0):
        raise NameError("This expression isn't a memory location",p.lineno(1))
    if(p[1].info.get("deref")==None):
        if(p[2]=="++"):
            p[0].code.append([p[1].expList[0],"=",p[1].expList[0],'+int',1])
        if(p[2]=="--"):
            p[0].code.append([p[1].expList[0],"=",p[1].expList[0],'-int',1])
    else:
        if(p[2]=="++"):
            var1=newTemp()
            p[0].code.append([var1,"=","*",p[1].expList[0]])
            p[0].code.append([var1,"=",var1,'+int',1])
            p[0].code.append(["*",p[1].expList[0],"=",var1])
        if(p[2]=="--"):
            var1=newTemp()
            p[0].code.append([var1,"=","*",p[1].expList[0]])
            p[0].code.append([var1,"=",var1,'-int',1])
            p[0].code.append(["*",p[1].expList[0],"=",var1])
    p[0].expTList=[]

def p_Assignment(p):
    """
    Assignment : ExpressionList AssignOp ExpressionList
    """
    p[0]=node()
    for i in range(0,len(p[3].expTList)):
        if(p[2].info["op"]=="="):
            if( not (p[1].expTList[i][0] in basicTypes or p[1].expTList[i][0]=="pointer")):
                raise NameError ("Invalid Assignment",p.lineno(1))
        else:
            if(p[1].expTList[i][0] not in basicTypes):
                raise NameError ("Invalid Assignment",p.lineno(1))
    if(p[1].info["memory"]==0):
        raise NameError("Assignment not allowed for this expression list", p.lineno(1))
    if(len(p[1].expTList) != len(p[3].expTList)):
        raise NameError("Imbalanced assignment", p.lineno(1))

    for i in range(0,len(p[1].expTList)):
        if(p[1].expTList[i] != p[3].expTList[i]):
            raise NameError("Mismatch of type for ",p[1].expTList[i], p.lineno(1))
    p[0].code+=p[1].code+p[3].code
    for i in range (0,len(p[1].expTList)):
        temp=None
        if(p[2].expTList[0][0]!="="):
            temp=checkOprn(p[1].expTList[i],[p[2].expTList[0][0][0:-1]],p[3].expTList[i])
            if(temp==None):
                raise NameError("Invalid operation for this type",p.lineno(1))
        # if(temp!=None):
        #     p[2].expTList[0]=[p[2].expTList[0][0]+temp[0]]
        if(p[1].info["dereflist"][i]==1):
            if(p[3].info["dereflist"][i]==1):
                var1=newTemp()
                p[0].code.append([var1,"=","*",p[3].expList[i]])
                if(p[2].expTList[0][0]=="="):
                    p[0].code.append(["*",p[1].expList[i],p[2].expTList[0][0],var1])
                else:
                    ops=p[2].expTList[0][0][:-1]
                    var2=newTemp()
                    p[0].code.append([var2,"=","*",p[1].expList[i]])
                    p[0].code.append([var2,"=",var2,ops+temp[0],var1])
                    p[0].code.append(["*",p[1].expList[i],"=",var2])
            else:
                if(p[2].expTList[0][0]=="="):
                    p[0].code.append(["*",p[1].expList[i],p[2].expTList[0][0],p[3].expList[i]])
                else:
                    ops=p[2].expTList[0][0][:-1]
                    var2=newTemp()
                    p[0].code.append([var2,"=","*",p[1].expList[i]])
                    p[0].code.append([var2,"=",var2,ops+temp[0],p[3].expList[i]])
                    p[0].code.append(["*",p[1].expList[i],"=",var2])
        else:
            if(p[3].info["dereflist"][i]==1):
                var1=newTemp()
                p[0].code.append([var1,"=","*",p[3].expList[i]])
                if(p[2].expTList[0][0]=="="):
                    p[0].code.append([p[1].expList[i],p[2].expTList[0][0],var1])
                else:
                    ops=p[2].expTList[0][0][:-1]
                    p[0].code.append([p[1].expList[i],"=",p[1].expList[i],ops+temp[0],var1])
            else:
                if(p[2].expTList[0][0]=="="):
                    p[0].code.append([p[1].expList[i],p[2].expTList[0][0],p[3].expList[i]])
                else:
                    ops=p[2].expTList[0][0][:-1]
                    p[0].code.append([p[1].expList[i],"=",p[1].expList[i],ops+temp[0],p[3].expList[i]])
    p[0].expTList=[]

def p_AssignOp(p):
    """
    AssignOp : ADD_ASSIGN
             | SUB_ASSIGN
             | MUL_ASSIGN
             | DIV_ASSIGN
             | MOD_ASSIGN
             | OR_ASSIGN
             | XOR_ASSIGN
             | SHL_ASSIGN
             | SHR_ASSIGN
             | ASSIGN
    """
    p[0]=node()
    p[0].expTList.append([p[1]])
    p[0].info["op"]=p[1]

def p_ReturnStmt(p):
    """
    ReturnStmt : RETURN ExpressionList
               | RETURN
    """
    if(len(p)==2 and not scopeTab[0].table[currentFunc]["returns"]==[["void"]]):
        raise NameError("The return type for this function is not void",p.lineno(1))
    if(len(p)==3 and not scopeTab[0].table[currentFunc]["returns"]==p[2].expTList):
        raise NameError("The return type for this function doesn't match",p.lineno(1))
    p[0]=node()
    if(len(p)==2):
        p[0].code=[ ["return"] ]
        p[0].info["hasRStmt"]=1
    if(len(p)==3):
        p[0].info["hasRStmt"]=1
        p[0].code=p[2].code
        for i in range(0,len(p[2].expList)):
            if(p[2].info["dereflist"][i]==1):
                var1=newTemp()
                p[0].code.append([var1,"=","*",p[2].expList[i]])
                p[0].code.append([currentFunc,"return",var1,str(i)])
            else:
                p[0].code.append([currentFunc,"return",p[2].expList[i],str(i)])
        p[0].code.append(["return"])

def p_BreakStmt(p):
    """
    BreakStmt : BREAK ID
              | BREAK
    """
    if(openF==0 and openW==0):
        raise NameError("Break can be only done inside loops and switches",p.lineno(1))
    p[0]=node()
    p[0].code.append(["goto",endFor[-1]])

def p_ContinueStmt(p):
    """
    ContinueStmt : CONTINUE ID
                 | CONTINUE
    """
    if(openF==0):
        raise NameError("Continue can be only done inside loops",p.lineno(1))
    p[0]=node()
    p[0].code.append(["goto",startFor[-1]])

def p_ShortVarDecl(p):
    """
    ShortVarDecl : IdentifierList DEFINE ExpressionList
    """
    if(len(p[1].idList) != len(p[3].expTList)):
        raise NameError("Imbalanced assignment", p.lineno(1))

    for i in range(0,len(p[1].idList)):
        if(len(p[3].expTList[i])>1):
            raise NameError("Auto assignment of complex expressions not allowed",p.lineno(1))
        if(not p[3].expTList[i][0] in basicTypes):
            raise NameError("Auto assignment of only basic types allowed",p.lineno(1))
        if(checkUse(p[1].idList[i],'redeclaration')==True):
            raise NameError('Redeclaration of identifier:'+p[1].idList[i], p.lineno(1))
        var1=newTemp(1)
        scopeTab[currentScope].insert(p[1].idList[i],p[3].expTList[i])
        scopeTab[currentScope].insert(var1,p[1].idList[i])
        scopeTab[currentScope].updateList(p[1].idList[i],"tmp",var1)
        offsetList[currentFScope]+=scopeTab[currentScope].typeSList[p[3].expTList[i][0]]
        scopeTab[currentScope].updateList(p[1].idList[i],"offset",offsetList[currentFScope])

    p[0]=node()
    p[0].code=p[3].code
    for i in range(0,len(p[1].idList)):
        temp=[scopeTab[currentScope].table[p[1].idList[i]]["tmp"],"="]
        if(p[3].info["dereflist"][i]==1):
            temp.append("*")
        temp.append(p[3].expList[i])
        p[0].code.append(temp)
    p[0].expTList=[]

def p_IfStmt(p):
    """
    IfStmt : IF OpenS Expression Block CloseS
           | IF OpenS Expression Block CloseS ELSE IfStmt
           | IF OpenS Expression Block CloseS ELSE OpenS Block CloseS
    """
    if(not p[3].expTList[0]==["bool"] or len(p[3].expTList)>1):
        raise NameError("The type of expression in if must be boolean", p.lineno(1))
    p[0]=node()
    p[0].code+=p[3].code
    if(len(p)==6):
        label1=newLabel()
        p[0].code.append(["ifnot",p[3].expList[0],"goto",label1])
        p[0].code+=p[4].code
        p[0].code.append([label1,":"])

    elif(len(p)==8):
        label1=newLabel()
        label2=newLabel()
        p[0].code.append(["ifnot",p[3].expList[0],"goto",label1])
        p[0].code+=p[4].code
        p[0].code.append(["goto",label2])
        p[0].code.append([label1,":"])
        p[0].code+=p[7].code
        p[0].code.append([label2,":"])

    else:
        label1=newLabel()
        label2=newLabel()
        p[0].code.append(["ifnot",p[3].expList[0],"goto",label1])
        p[0].code+=p[4].code
        p[0].code.append(["goto",label2])
        p[0].code.append([label1,":"])
        p[0].code+=p[8].code
        p[0].code.append([label2,":"])


def p_SwitchStmt(p):
    """
    SwitchStmt : SWITCH ExpressionName LBRACE OpenW ExprCaseClause_curl CloseW RBRACE
    """
    global endFor
    p[0]=node()
    p[0].code=p[2].code+p[5].code
    p[0].code.append([endFor[-1],":"])
    endFor=endFor[0:-1]
    if(p[5].info.get("hasRStmt") != None):
        p[0].info["hasRStmt"]=1


def p_ExpressionName(p):
    """
    ExpressionName : Expression
    """
    p[0]=p[1]
    global switchExp
    global currentSwitch
    if(len(p[1].expTList)>1):
        raise NameError("Complex types not allowed in switch", p.lineno(1))
    if(p[1].expTList[0][0]!="int" and p[1].expTList[0][0]!="rune" and p[1].expTList[0][0]!="bool"):
        raise NameError("Only int,bool and runes are allowed in switch")
    currentSwitch=p[1].expTList[0][0]
    switchExp=p[0].expList[0]
    label1=newLabel(2)


def p_ExprCaseClause_curl(p):
    """
    ExprCaseClause_curl : ExprCaseClause ExprCaseClause_curl
                        | DefCaseClause
                        | ExprCaseClause
    """
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]
        p[0].code+=p[2].code



def p_ExprCaseClause(p):
    """
    ExprCaseClause : OpenS CASE Expression COLON StatementList CloseS
    """
    global switchExp
    p[0]=node()
    if(len(p[3].expTList)>1):
        raise NameError("Complex types not allowed in switch", p.lineno(1))
    if(p[3].expTList[0][0]!="int" and p[3].expTList[0][0]!="rune"):
        raise NameError("Only int and runes are allowed in switch")
    if(currentSwitch!=p[3].expTList[0][0]):
        print(currentSwitch)
        raise NameError("type mismatch in case and switch",p.lineno(1))
    var1=newTemp()
    label1=newLabel()
    p[0].code=p[3].code
    p[0].code.append([var1, "=", switchExp, '-'+p[3].expTList[0][0], p[3].expList[0]])
    p[0].code.append([var1,"=",var1,"=="+p[3].expTList[0][0],'0'])
    p[0].code.append(["ifnot", var1, "goto", label1 ])
    p[0].code+=p[5].code
    p[0].code.append(["goto", endFor[-1]])
    p[0].code.append([label1, ":"])


def p_DefCaseClause(p):
    """
    DefCaseClause : DEFAULT COLON OpenS StatementList CloseS
    """
    p[0]=node()
    p[0].code=p[4].code



def p_ForStmt(p):
    """
    ForStmt : FOR OpenS OpenF Expression Block CloseF CloseS
            | FOR OpenS OpenF ForClause Block CloseF CloseS
            | FOR OpenS OpenF Block CloseF CloseS
    """
    global startFor,endFor
    p[0]=node()
    if(len(p)==8 and p[4].info.get("forclause")!=None):
        p[0].code=p[4].code
        p[0].code+=p[5].code
        p[0].code+=p[4].info["forLabelPass"]

    elif(len(p)==8):
        if(len(p[4].expTList)>1 or p[4].expTList[0][0]!="bool"):
            raise NameError("Only boolean value is allowed in this kind of for loop",p.lineno(1))
        label1=newLabel()
        p[0].code.append(["reset"])
        p[0].code.append([startFor[-1],":"])
        p[0].code+=p[4].code
        p[0].code.append(["ifnot",p[4].expList[0],"goto",label1])
        p[0].code+=p[5].code
        p[0].code.append(["goto",startFor[-1]])
        p[0].code.append([label1,":"])
    else:
        p[0].code.append(["reset"])
        p[0].code.append([startFor[-1],":"])
        p[0].code+=p[4].code
        p[0].code.append(["goto",startFor[-1]])
        # if(p[4].info.get("hasRStmt") != None):
        #     p[0].info["hasRStmt"]=1
    p[0].code.append([endFor[-1],":"])
    startFor=startFor[0:-1]
    endFor=endFor[0:-1]

def p_OpenF(p):
    """
    OpenF :
    """
    global openF
    openF+=1
    newLabel(1)
    newLabel(2)

def p_CloseF(p):
    """
    CloseF :
    """
    global openF
    openF-=1

def p_OpenW(p):
    """
    OpenW :
    """
    global openW
    openW+=1

def p_CloseW(p):
    """
    CloseW :
    """
    global openW
    openW-=1

def p_ForClause(p):
    """
    ForClause : SimpleStmt SEMICOLON SEMICOLON SimpleStmt
              | SimpleStmt SEMICOLON Expression SEMICOLON SimpleStmt
    """
    p[0]=node()
    p[0].info["forclause"]=1
    if(len(p)==6 and (len(p[3].expTList)>1 or p[3].expTList[0][0]!="bool")):
        raise NameError("Only boolean value is allowed in expression in for loop",p.lineno(1))
    p[0].code=p[1].code
    p[0].code.append(["reset"])
    p[0].code.append([startFor[-1],":"])
    if(len(p)==6):
        label2=newLabel()
        p[0].code+=p[3].code
        p[0].code.append(["ifnot",p[3].expList[0],"goto",label2])
        p[0].info["forLabelPass"]=[]
        p[0].info["forLabelPass"]+=p[5].code
        p[0].info["forLabelPass"].append(["goto",startFor[-1]])
        p[0].info["forLabelPass"].append([label2,":"])
    else:
        p[0].info["forLabelPass"]=[]
        p[0].info["forLabelPass"]+=p[4].code
        p[0].info["forLabelPass"].append(["goto",startFor[-1]])

def p_error(p):
    if p:
      print("Syntax error at line no:", p.lineno, "at position", p.lexpos, "in the code.   " "TOKEN VALUE=", p.value,  "TOKEN TYPE=" ,p.type)
      print("\n")
      parser.errok()
    else:
      print("Syntax error at EOF")

parser=yacc.yacc()

with open(sys.argv[1],'r') as f:
    input_str = f.read()
out=parser.parse(input_str,tracking=True)



import pickle
with open('scopeTabDump', 'wb') as handle:
    pickle.dump(scopeTab, handle, protocol=pickle.HIGHEST_PROTOCOL)
