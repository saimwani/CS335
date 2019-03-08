import ply.yacc as yacc
import os
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

scopeTab={}
scopeNum=0
scopeList=[0]
scopeTab[0]=symbolTable
currentScope=0

def checkUse(ident,checkWhat):
    if(checkWhat=='redeclaration'):
        if(scopeTab[currentScope].search(ident) is not None):
            return True
        else:
            return False
    if(checkWhat=='anywhere'):
        for x in scopeList[::-1]:
            if(scopeTab[x].search(ident) is not None)
                return x
        return False

def p_SourceFile(p):
    """
    SourceFile : PackageClause SEMICOLON ImportDecl_curl TopLevelDecl_curl
    """

def p_OpenS(p):
    "OpenS : "
    p[0]=[]

def p_CloseS(p):
    "CloseS : "
    p[0]=[]

def p_OpenStructS(p):
    "OpenStructS : "
    p[0]=[]

def p_CloseStructS(p):
    "CloseStructS : "
    p[0]=[]

def p_TopLevelDecl_curl(p):
    """
    TopLevelDecl_curl : TopLevelDecl_curl TopLevelDecl SEMICOLON
                    |
    """

def p_ImportDecl_curl(p):
    """
    ImportDecl_curl : ImportDecl_curl ImportDecl SEMICOLON
                  |
    """

def p_PackageClause(p):
    """
    PackageClause : PACKAGE ID
    """
    if(checkUse(p[2],'redeclaration')==True):
        raise NameError("Redeclaration of variable:"+p[2])
    else:
        scopeTab[currentScope].insert(p[2],['package'])

def p_ImportDecl(p):
    """
    ImportDecl : IMPORT ImportSpec
               | IMPORT LPAREN ImportSpec_curl RPAREN
    """

def p_ImportSpec_curl(p):
    """
    ImportSpec_curl : ImportSpec_curl ImportSpec SEMICOLON
                    |
    """

def p_ImportSpec(p):
    """
    ImportSpec : DOT ImportPath
               | ID ImportPath
               | ImportPath
    """


def p_ImportPath(p):
    """
    ImportPath : STRING
    """

def p_TopLevelDecl(p):
    """
    TopLevelDecl : Declaration
                 | FunctionDecl
    """

def p_Declaration(p):
    """
    Declaration : ConstDecl
                | TypeDecl
                | VarDecl
    """

def p_ConstDecl(p):
    """
    ConstDecl : CONST ConstSpec
              | CONST LPAREN ConstSpec_curl RPAREN
    """

def p_ConstSpec_curl(p):
    """
    ConstSpec_curl : ConstSpec_curl ConstSpec SEMICOLON
                   |
    """

def p_ConstSpec(p):
    """
    ConstSpec : IdentifierList ID ASSIGN ExpressionList
              | IdentifierList Type ASSIGN ExpressionList
    """
    if(isinstance(p[2],str) and not p[2] in scopeTab[currentScope].typeList):
        raise NameError("Invalid type of identifier "+p[2])
    
    for x in p[1].idList:
        if(checkUse(x,'redeclaration')==True):
            raise NameError('Redeclaration of identifier:'+x)
        else:
            if(isinstance(p[2],str)):
                scopeTab[currentScope].insert(x,p[2])
            else:
                scopeTab[currentScope].insert(x,p[2].type)
            scopeTab[currentScope].updateList(x,'constant',True)
    
    if(len(p[1].idList) != len(p[4].expTList)):
        raise NameError("Imbalanced assignment")
    
    for i in range(0,len(p[1].idList)):
        if(p[4].expTList[i] != scopeTab[currentScope][p[1].idList[i]]["type"]):
            raise ("Mismatch of type for "+p[1].idList[i])

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
        p[0]=p[0]+p[3].idList

def p_ExpressionList(p):
    """
    ExpressionList : Expression
                   | ExpressionList COMMA Expression
    """
    p[0]=node()
    if(len(p)==2):
        p[0].expTList+=p[1].expTList
    else:
        p[0].expTList+=p[1].expTList
        p[0].expTList+=p[3].expTList

def p_TypeDecl(p):
    """
    TypeDecl : TYPE TypeSpec
             | TYPE LPAREN TypeSpec_curl RPAREN
    """

def p_TypeSpec_curl(p):
    """
    TypeSpec_curl : TypeSpec_curl TypeSpec SEMICOLON
                  |
    """

def p_TypeSpec(p):
    """
    TypeSpec : TypeDef
    """

def p_TypeDef(p):
    """
    TypeDef : ID Type
            | ID ID
            | ID ID DOT ID
    """

def p_VarDecl(p):
    """
    VarDecl : VAR VarSpec
            | VAR LPAREN VarSpec_curl RPAREN
    """

def p_VarSpec_curl(p):
    """
    VarSpec_curl : VarSpec_curl VarSpec SEMICOLON
                 |
    """

def p_VarSpec(p):
    """
    VarSpec : IdentifierList Type ASSIGN ExpressionList
            | IdentifierList ID ASSIGN ExpressionList
            | IdentifierList ASSIGN ExpressionList
            | IdentifierList ID
            | IdentifierList Type
    """
    if(isinstance(p[2],str) and p[2]!="=" and not p[2] in scopeTab[currentScope].typeList):
        raise NameError("Invalid type of identifier "+p[2])
    
    if(len(p)==5 or len(p)==3):
        for x in p[1].idList:
            if(checkUse(x,'redeclaration')==True):
                raise NameError('Redeclaration of identifier:'+x)
            else:
                if(isinstance(p[2],str)):
                    scopeTab[currentScope].insert(x,p[2])
                else:
                    scopeTab[currentScope].insert(x,p[2].type)
    
    if(len(p)==5):
        if(len(p[1].idList) != len(p[4].idList)):
            raise NameError("Imbalanced assignment")
        for i in range(0,len(p[1].idList)):
            if(p[4].expTList[i] != scopeTab[currentScope][p[1].idList[i]]["type"]):
                raise ("Mismatch of type for "+p[1].idList[i])
    
    if(len(p)==4):
        if(len(p[1].idList) != len(p[3].expTList)):
            raise NameError("Imbalanced assignment")
        for i in range(0,p[1].idList):
            if(checkUse(p[1].idList[i],'redeclaration')==True):
                raise NameError('Redeclaration of identifier:'+p[1].idList[i])
            scopeTab[currentScope].insert(p[1].idList[i],p[3].expTList[i])

def p_FunctionDecl(p):
    """
    FunctionDecl : FUNC ID Signature Block
    """

def p_Type(p):
    """
    Type : LPAREN Type RPAREN
         | LPAREN ID RPAREN
         | TypeLit
    """
    if(len(p)==2):
        p[0]=p[1]
    else:
        if(isinstance(p[2],str) and not p[2] in scopeTab[currentScope].typeList):
            raise NameError("Invalid type of identifier "+p[2])
        if(isinstance(p[2],str)):
            p[0]=node()
            p[0].type.append(p[2])
        else:
            p[0]=p[2]

def p_TypeLit(p):
    """
    TypeLit : ArrayType
            | StructType
            | PointerType
            | SliceType
    """
    p[0]=p[1]

def p_ArrayType(p):
    """
    ArrayType : LBRACK Expression RBRACK Type
              | LBRACK Expression RBRACK ID
    """
    if(p[2].expTList[0]!=["int"]):
        raise NameError("Array index must be integer")
    if(isinstance(p[4],str) and not p[4] in scopeTab[currentScope].typeList):
        raise NameError("Invalid type of identifier "+p[4])
    if(isinstance(p[4],str)):
        p[0]=node()
        p[0].type.append("arr")
        p[0].type.append(p[4])
    else:
        p[0]=node()
        p[0].type.append("arr")
        p[0].type+=p[4].type

def p_SliceType(p):
    """
    SliceType : LBRACK RBRACK Type
              | LBRACK RBRACK ID
    """
    if(isinstance(p[3],str) and not p[3] in scopeTab[currentScope].typeList):
        raise NameError("Invalid type of identifier "+p[3])
    if(isinstance(p[4],str)):
        p[0]=node()
        p[0].type.append("slice")
        p[0].type.append(p[3])
    else:
        p[0]=node()
        p[0].type.append("slice")
        p[0].type+=p[3].type

def p_StructType(p):
    """
    StructType : STRUCT OpenStructS LBRACE FieldDecl_curl RBRACE CloseStructS
    """
    #p[0]=node()
    #p[0].type.append("struct")

def p_FieldDecl_curl(p):
    """
    FieldDecl_curl : FieldDecl_curl FieldDecl SEMICOLON
                   |
    """

def p_FieldDecl(p):
    """
    FieldDecl : ID COMMA IdentifierList Type
              | ID COMMA IdentifierList ID
              | ID Type
              | ID ID
    """
    #if(len(p)==3):
    #    if(checkUse(p[1],'redeclaration')==True)
    #        raise NameError("Redeclaration of variable in struct")\
    #    if(isinstance(p[2],str) and p[2] not in scopeTab[currentScope].typeList):
    #        raise NameError("Type undefined "+p[2])
    #    if(isinstance(p[2],str)):


def p_PointerType(p):
    """
    PointerType : MUL Type
                | MUL ID
    """
    if(isinstance(p[2],str) and not p[2] in scopeTab[currentScope].typeList):
        raise NameError("Invalid type of identifier "+p[2])
    if(isinstance(p[2],str)):
        p[0]=node()
        p[0].type.append("pointer")
        p[0].type.append(p[2])
    else:
        p[0]=node()
        p[0].type.append("pointer")
        p[0].type+=p[2].type

def p_Signature(p):
    """
    Signature : Parameters Result
    """

#introduced CHAN
def p_Result(p):
    """
    Result : Parameters
           | Type
           | ID
           | ID DOT ID
           | CHAN
    """

def p_Parameters(p):
    """
    Parameters : LPAREN RPAREN
               | LPAREN ParameterList RPAREN
               | LPAREN ParameterList COMMA RPAREN
    """

#Introduced CHAN

def p_ParameterList(p):
    """
    ParameterList : ParameterDecl
                  | CHAN ID
                  | CHAN ID DOT ID
                  | CHAN Type
                  | ParameterList COMMA CHAN ID
                  | ParameterList COMMA CHAN ID DOT ID
                  | ParameterList COMMA CHAN Type
                  | ParameterList COMMA ParameterDecl
    """

def p_ParaIdList(p):
    """
    ParaIdList : ID COMMA ID
               | ParaIdList COMMA ID
    """

def p_ParameterDecl(p):
    """
    ParameterDecl : ParaIdList Type
                  | ID Type
                  | ParaIdList ID
                  | ID ID
                  | ParaIdList ID DOT ID
                  | ID ID DOT ID

    """

def p_Block(p):
    """
    Block : OpenS LBRACE StatementList RBRACE CloseS
    """

def p_StatementList(p):
    """
    StatementList : Statement_curl
    """

def p_Statement_curl(p):
    """
    Statement_curl : Statement_curl Statement SEMICOLON
                   |
    """

def p_Expression(p):
    """
    Expression : UnaryExpr
               | Expression BinaryOp UnaryExpr
    """
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=node()
        #p[0].expList.append(p[1].expList[0]+p[2].expList[0]+p[3].expList[0])
        if(checkOprn(p[1].expTList[0] , p[2].expTList[0], p[3].expTList[0] )==None):
            raise NameError("Invalid types for operator ",p[2].expTList[0])
        p[0].expTList.append(checkOprn(p[1].expTList[0] , p[2].expTList[0], p[3].expTList[0] ))

def p_UnaryExpr(p):
    """
    UnaryExpr : PrimaryExpr
              | UnaryOp UnaryExpr
    """
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=node()
        #p[0].expList.append(p[1].expList[0]+p[2].expList[0])
        if(checkUnOprn(p[1].expTList[0], p[2].expTList[0])==None):
            raise NameError("Invalid types for operator ",p[2].expTList[0])
        p[0].expTList.append(checkUnOprn(p[1].expTList[0], p[2].expTList[0]))

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

def p_PrimaryExpr(p):
    """
    PrimaryExpr : Literal
                | ID
                | ID DOT ID
                | LPAREN Expression RPAREN
                | Conversion
                | PrimaryExpr Index
                | PrimaryExpr Slice
                | PrimaryExpr Arguments
    """
    #Slices isn't implememted indefinitely
    if(len(p)==2 and not isinstance(p[1],str)):
        p[0]=p[1]
    elif(len(p)==2):
        if(scopeTab[currentScope].search(p[1])==None):
            raise NameError("Undeclared identifier "+p[1])
        p[0]=node()
        p[0].expTList.append(scopeTab[currentScope][p[1]]["type"])
    elif(isinstance(p[1],str) and p[1]!='('):
        a=0
        #Not to be done before declaring structs
    elif(len(p)==4):
        p[0]=p[2]
    elif(p[2].info.get("index")!=None):
        if(p[1].expTList[0][0]!="arr"):
            raise NameError("The type of this expression is not an array ")
        p[0]=p[1]
        p[0].expTList[0]=p[0].expTList[0][1:]
    elif(p[2].info.get("arguments")!=None):
        #TO de done after doinf functions
        if(p[1].expTList[0][0]!="func"):
            raise NameError("The primary expression is not a function")
        signature=scopeTab[0][p[1]]

def p_Index(p):
    """
    Index : LBRACK Expression RBRACK
    """
    if(p[2].expTList[0]!="int"):
        raise NameError("Only integer indices are allowed")
    p[0]=p[2]
    p[0].info["index"]=1

def p_Slice(p):
    """
    Slice : LBRACK Expression COLON Expression RBRACK
          | LBRACK COLON Expression RBRACK
          | LBRACK Expression COLON RBRACK
          | LBRACK COLON RBRACK
          | LBRACK Expression COLON Expression COLON Expression RBRACK
          | LBRACK COLON Expression COLON Expression RBRACK
    """
    #to be done later

def p_Arguments(p):
    """
    Arguments : LPAREN RPAREN
              | LPAREN ExpressionList RPAREN
              | LPAREN ExpressionList COMMA RPAREN
    """
    if(len(p)==3):
        p[0]=node()
        p[0].info["arguments"]=1
    else:
        p[0]=p[2]
        p[0].info["arguments"]=1

def p_Conversion(p):
    """
    Conversion : TYPECAST Type LPAREN Expression COMMA RPAREN
               | TYPECAST Type LPAREN Expression RPAREN
               | TYPECAST ID LPAREN Expression COMMA RPAREN
               | TYPECAST ID LPAREN Expression RPAREN
    """

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
    """
    p[0]=p[1]

def p_IntLit(p):
    """
    IntLit : INT
    """
    p[0]=node()
    p[0].expTList.append("int")

def p_FloatLit(p):
    """
    FloatLit : FLOAT
    """
    p[0]=node()
    p[0].expTList.append("float")

def p_RuneLit(p):
    """
    RuneLit : RUNE
    """
    p[0]=node()
    p[0].expTList.append("rune")

def p_StringLit(p):
    """
    StringLit : STRING
    """
    p[0]=node()
    p[0].expTList.append("string")

#Removed struct assignments in compositelit

#"""
#CompositeLit : ArrayType LiteralValue
#             | SliceType  LiteralValue
#             | MapType LiteralValue
#"""

#def p_CompositeLit(p):
#    """
#    CompositeLit : ArrayType LiteralValue
#                 | SliceType LiteralValue
#    """
#
#def p_LiteralValue(p):
#    """
#    LiteralValue : LBRACE ElementList COMMA RBRACE
#                 | LBRACE ElementList RBRACE
#                 | LBRACE RBRACE
#    """
#
#def p_ElementList(p):
#    """
#    ElementList : KeyedElement
#                | ElementList COMMA KeyedElement
#    """
#
#def p_KeyedElement(p):
#    """
#    KeyedElement : Expression COLON Expression
#                 | Expression
#    """

def p_Statement(p):
    """
    Statement : Declaration
              | LabelledStmt
              | SimpleStmt
              | GoStmt
              | ReturnStmt
              | BreakStmt
              | ContinueStmt
              | GotoStmt
              | FallthroughStmt
              | IfStmt
              | Block
              | SwitchStmt
              | ForStmt
              | DeferStmt
    """

def p_SimpleStmt(p):
    """
    SimpleStmt : Expression
               | IncDecStmt
               | Assignment
               | ShortVarDecl
               |
    """

def p_IncDecStmt(p):
    """
    IncDecStmt : Expression INC
               | Expression DEC
    """

def p_Assignment(p):
    """
    Assignment : ExpressionList AssignOp ExpressionList
    """

def p_AssignOp(p):
    """
    AssignOp : ADD_ASSIGN
             | SUB_ASSIGN
             | MUL_ASSIGN
             | DIV_ASSIGN
             | MOD_ASSIGN
             | AND_ASSIGN
             | AND_NOT_ASSIGN
             | OR_ASSIGN
             | XOR_ASSIGN
             | SHL_ASSIGN
             | SHR_ASSIGN
             | ASSIGN
    """

def p_LabelledStmt(p):
    """
    LabelledStmt : ID COLON Statement
    """

def p_GoStmt(p):
    """
    GoStmt : GO Expression
    """

def p_ReturnStmt(p):
    """
    ReturnStmt : RETURN ExpressionList
               | RETURN
    """

def p_BreakStmt(p):
    """
    BreakStmt : BREAK ID
              | BREAK
    """

def p_ContinueStmt(p):
    """
    ContinueStmt : CONTINUE ID
                 | CONTINUE
    """

def p_GotoStmt(p):
    """
    GotoStmt : GOTO ID
    """

def p_FallthroughStmt(p):
    """
    FallthroughStmt : FALLTHROUGH
    """

def p_DeferStmt(p):
    """
    DeferStmt : DEFER Expression
    """

def p_ShortVarDecl(p):
    """
    ShortVarDecl : IdentifierList DEFINE ExpressionList
    """
    if(len(p[1].idList) != len(p[3].expTList)):
        raise NameError("Imbalanced assignment")
    
    for i in range(0,p[1].idList):
        if(checkUse(p[1].idList[i],'redeclaration')==True):
            raise NameError('Redeclaration of identifier:'+p[1].idList[i])
        scopeTab[currentScope].insert(p[1].idList[i],p[3].expTList[i])

def p_IfStmt(p):
    """
    IfStmt : IF Expression Block
           | IF SimpleStmt SEMICOLON Expression Block
           | IF Expression Block ELSE IfStmt
           | IF Expression Block ELSE Block
           | IF SimpleStmt SEMICOLON Expression Block ELSE Block
           | IF SimpleStmt SEMICOLON Expression Block ELSE IfStmt
    """

def p_SwitchStmt(p):
    """
    SwitchStmt : ExprSwitchStmt
    """

def p_ExprSwitchStmt(p):
    """
        ExprSwitchStmt : SWITCH OpenS LBRACE ExprCaseClause_curl RBRACE CloseS
                       | SWITCH SimpleStmt SEMICOLON OpenS LBRACE ExprCaseClause_curl RBRACE CloseS
                       | SWITCH Expression OpenS LBRACE ExprCaseClause_curl RBRACE CloseS
                       | SWITCH SimpleStmt SEMICOLON Expression OpenS LBRACE ExprCaseClause_curl RBRACE CloseS
    """

def p_ExprCaseClause_curl(p):
    """
    ExprCaseClause_curl : ExprCaseClause_curl ExprCaseClause
                        |
    """

def p_ExprCaseClause(p):
    """
    ExprCaseClause : ExprSwitchCase COLON StatementList
    """

def p_ExprSwitchCase(p):
    """
    ExprSwitchCase : CASE ExpressionList
                   | DEFAULT
    """

def p_ForStmt(p):
    """
    ForStmt : FOR Expression Block
            | FOR ForClause Block
            | FOR RangeClause Block
            | FOR Block
    """

def p_ForClause(p):
    """
    ForClause : SimpleStmt SEMICOLON SEMICOLON SimpleStmt
              | SimpleStmt SEMICOLON Expression SEMICOLON SimpleStmt
    """

def p_RangeClause(p):
    """
    RangeClause : IdentifierList DEFINE RANGE Expression
                | ExpressionList ASSIGN RANGE Expression
                | RANGE Expression
    """

#def p_error(p):
#    print("Syntax Error at Line No:", p.lineno, "at position", p.lexpos, p.value)

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

out=parser.parse(input_str)

outputDot="../"+sys.argv[2][6:]

alist=out
file1 = open(outputDot,"w")#write mode
file1.write("digraph graphname {")
file1.write("\n")
counter=0
def writeGraph(someList):
    global counter
    local=counter
    counter+=1
    name=someList[0]
    if(len(someList) > 1):
        for innerList in someList[1:]:
            if(len(innerList) >0):
                file1.write(str(local))
                file1.write ("[label=\"")
                file1.write (name)
                file1.write ("\" ] ;")
                file1.write(str(counter))
                file1.write ("[label=\"")
                if ((innerList[0][0])=="\""):
                    innerList[0]=innerList[0][1:-1]
                file1.write (innerList[0])
                file1.write ("\" ] ;")
                file1.write(str(local) + "->" + str(counter) + ";")
                file1.write("\n")
                writeGraph(innerList)
writeGraph(alist)
file1.write("}")
file1.close()
outputTree="../"+sys.argv[1][15:]+".ps"



os.system("dot -Tps "+ outputDot+" -o "+outputTree)
