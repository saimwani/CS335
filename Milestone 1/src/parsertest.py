import ply.yacc as yacc
import lexer
import sys

tokens=lexer.tokens
precedence = (
    ('left','ID'),
    ('left','DEFINE'),
    ('left','COMMA'),
    ('left','LBRACK'),
    ('left','RBRACK'),
    ('left','LBRACE'),
    ('left','RBRACE'),
    ('left','ELLIPSIS'),
    ('left','DOT'),
    ('left','SEMICOLON'),
    ('left','COLON'),
    ('left','INT'),
    ('left','FLOAT'),
    ('left','STRING'),
    ('left','BREAK'),
    ('left','CONTINUE'),
    ('left','RETURN'),
    ('left','LPAREN'),
    ('left','RPAREN'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'EQL', 'NEQ','LTN','LEQ','GTN','GEQ'),
    ('left', 'ADD', 'SUB','OR','XOR'),
    ('left', 'MUL', 'DIV','MOD','AND','AND_NOT','SHL','SHR'),
)

def p_SourceFile(p):
    """
    SourceFile : PackageClause SEMICOLON ImportDecl_curl TopLevelDecl_curl
    """
    p[0]=['SourceFile',p[1],p[3], p[4]]

def p_TopLevelDecl_curl(p):
    """
    TopLevelDecl_curl : TopLevelDecl_curl TopLevelDecl SEMICOLON
                      |
    """
    if (len(p)==1):
        p[0]=[]
    else:
        p[0]=['TopLevelDecl_curl', p[1], p[2]]

def p_ImportDecl_curl(p):
    """
    ImportDecl_curl : ImportDecl_curl ImportDecl SEMICOLON
                    |
    """
    p[0]=[]
    if(len(p)>1):
      p[0]=['ImportDecl_curl',p[1],p[2]]

def p_PackageClause(p):
    """
    PackageClause : PACKAGE ID
    """
    p[0]=[p[2]]

def p_ImportDecl(p):
    """
    ImportDecl : IMPORT ImportSpec
               | IMPORT LPAREN ImportSpec_curl RPAREN
    """
    if(len(p)==3):
      p[0]=p[2]
    else:
      p[0]=p[3]

def p_ImportSpec_curl(p):
    """
    ImportSpec_curl : ImportSpec_curl ImportSpec SEMICOLON
                    |
    """
    p[0]=[]
    if(len(p)>1):
      p[0]=['ImportSpec_curl',p[1],p[2]]

def p_ImportSpec(p):
    """
    ImportSpec : DOT ImportPath
               | ID ImportPath
               | ImportPath
    """
    if(len(p)==2):
      p[0]=p[1]                             # Removing ImportSpec if only string occurs
    else:
      p[0]=['ImportSpec',[p[1]],p[2]]

def p_ImportPath(p):
    """
    ImportPath : STRING
    """
    p[0]=[p[1]]

def p_TopLevelDecl(p):
    """
    TopLevelDecl : Declaration
                 | FunctionDecl
                 | MethodDecl
    """
    p[0]=p[1]

def p_Declaration(p):
    """
    Declaration : ConstDecl
                | TypeDecl
                | VarDecl
    """
    p[0]=p[1]

def p_ConstDecl(p):
    """
    ConstDecl : CONST ConstSpec
              | CONST LPAREN ConstSpec_curl RPAREN
    """
    if (len(p)==3):
        p[0]=p[2]
    else:
        p[0]=p[3]

def p_ConstSpec_curl(p):
    """
    ConstSpec_curl : ConstSpec_curl ConstSpec SEMICOLON
                   |
    """
    if(len(p)==1):
        p[0]=[]
    else:
        p[0]=['ConstSpec_curl', p[1], p[2]]

def p_ConstSpec(p):
    """
    ConstSpec : IdentifierList ID ASSIGN ExpressionList
              | IdentifierList ID DOT ID ASSIGN ExpressionList
              | IdentifierList Type ASSIGN ExpressionList
              | IdentifierList ASSIGN ExpressionList
              | IdentifierList
    """
    if (len(p)==2):
        p[0]=p[1]
    elif (len(p)==4):
        p[0]=['ConstSpec', p[1], [p[2]], p[3] ]
    elif (len(p)==7):
        p[0]=['ConstSpec', p[1], [p[2]], [p[3]], [p[4]], [p[5]], p[6] ]
    elif (isinstance(p[2], str)):
        p[0]=['ConstSpec', p[1], [p[2]], [p[3]], p[4] ]
    else:
        p[0]=['ConstSpec', p[1], p[2], [p[3]], p[4]]

def p_IdentifierList(p):
    """
    IdentifierList : ID
                   | ID COMMA IdentifierList
    """
    if (len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=['IdentifierList', [p[1]], p[3]]

def p_ExpressionList(p):
    """
    ExpressionList : Expression
                   | ExpressionList COMMA Expression
    """
    if (len(p)==2):
        p[0]=p[1]
    else:
        p[0]=['ExpressionList', p[1], p[3] ]

def p_TypeDecl(p):
    """
    TypeDecl : TYPE TypeSpec
             | TYPE LPAREN TypeSpec_curl RPAREN
    """
    if (len(p)==3):
        p[0]=['TypeDecl', [p[1]], p[2]]
    else:
        p[0]=['TypeDecl', [p[1]], p[3]]

def p_TypeSpec_curl(p):
    """
    TypeSpec_curl : TypeSpec_curl TypeSpec SEMICOLON
                  |
    """
    if (len(p)==1):
        p[0]=[]
    else:
        p[0]=['TypeSpec_curl', p[1], p[2]]

def p_TypeSpec(p):
    """
    TypeSpec : AliasDecl
             | TypeDef
    """
    p[0]=p[1]

def p_AliasDecl(p):
    """
    AliasDecl : ID ASSIGN Type
              | ID ASSIGN ID
              | ID ASSIGN ID DOT ID
    """
    if (len(p)==4 and isinstance(p[3], str) ):
        p[0]=['AliasDecl', [p[1]], [p[2]], [p[3]] ]
    elif (len(p)==4 ):
        p[0]=['AliasDecl', [p[1]], [p[2]], p[3] ]
    else:
        p[0]=['AliasDecl', [p[1]], [p[2]], [p[3]], [p[4]], [p[5]] ]


def p_TypeDef(p):
    """
    TypeDef : ID Type
            | ID ID
            | ID ID DOT ID
    """
    if (len(p)==5):
        p[0]=['TypeDef', [p[1]], [p[2]], [p[3]], [p[4]] ]
    elif (len(p)==3 and isinstance(p[2], str)):
        p[0]=['TypeDef', [p[1]], [p[2]] ]
    else:
        p[0]=['TypeDef', [p[1]], p[2]]

def p_VarDecl(p):
    """
    VarDecl : VAR VarSpec
            | VAR LPAREN VarSpec_curl RPAREN
    """
    if (len(p)==3):
        p[0]=['VarDecl', [p[1]], p[2] ]
    else:
        p[0]=['VarDecl', [p[1]], p[3] ]

def p_VarSpec_curl(p):
    """
    VarSpec_curl : VarSpec_curl VarSpec SEMICOLON
                 |
    """
    if (len(p)==1):
        p[0]=[]
    else:
        p[0]=['VarSpec_curl', p[1], p[2] ]

def p_VarSpec(p):
    """
    VarSpec : IdentifierList Type ASSIGN ExpressionList
            | IdentifierList ID ASSIGN ExpressionList
            | IdentifierList ID DOT ID ASSIGN ExpressionList
            | IdentifierList ASSIGN ExpressionList
            | IdentifierList ID
            | IdentifierList ID DOT ID
            | IdentifierList Type
    """
    p[0]=['VarSpec']
    for index in range(1,len(p)):
      if(isinstance(p[index],str)):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])

def p_FunctionDecl(p):
    """
    FunctionDecl : FUNC ID Signature Block
                 | FUNC ID Signature
    """
    if(len(p)==5):
      p[0]=['FunctionDecl',[p[2]],p[3],p[4]]
    else:
      p[0]=['FunctionDecl',[p[2]],p[3]]

def p_MethodDecl(p):
    """
    MethodDecl : FUNC Receiver ID Signature Block
               | FUNC Receiver ID Signature
    """
    p[0]=['MethodDecl']
    for index in range(1,len(p)):
      if(p[index]=='func'):
        continue
      if(isinstance(p[index],str)):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])

def p_Receiver(p):
    """
    Receiver : Parameters
    """
    p[0]=p[1]

def p_Type(p):
    """
    Type : LPAREN Type RPAREN
         | LPAREN ID RPAREN
         | LPAREN ID DOT ID RPAREN
         | TypeLit
    """
    if(len(p)==2):
      p[0]=p[1]
    elif(len(p)==4 and not isinstance(p[2],str)):
    	p[0]=p[2]
    elif(len(p)==4 and isinstance(p[2],str)):
    	p[0]=[p[2]]
    else:
      p[0]=['Type']
      for index in range(1,len(p)):
        if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=";"):
          p[0].append([p[index]])
        elif(p[index]!="(" and p[index]!=")" and p[index]!=";"):
          p[0].append(p[index])

def p_TypeLit(p):
    """
    TypeLit : ArrayType
            | StructType
            | PointerType
            | FunctionType
            | InterfaceType
            | SliceType
            | MapType
    """
    p[0]=p[1]

def p_ArrayType(p):
    """
    ArrayType : LBRACK Expression RBRACK Type
              | LBRACK Expression RBRACK ID
              | LBRACK Expression RBRACK ID DOT ID
    """
    p[0]=['ArrayType']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="[" and p[index]!="]" and p[index]!=";"):
        p[0].append([p[index]])
      elif(p[index]!="[" and p[index]!="]" and p[index]!=";"):
        p[0].append(p[index])

def p_SliceType(p):
    """
    SliceType : LBRACK RBRACK Type
    """
    p[0]=['SliceType',p[3]]

def p_StructType(p):
    """
    StructType : STRUCT LBRACE FieldDecl_curl RBRACE
    """
    p[0]=['StructType']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="{" and p[index]!="}" and p[index]!=";"):
        p[0].append([p[index]])
      elif(p[index]!="{" and p[index]!="}" and p[index]!=";"):
        p[0].append(p[index])

def p_FieldDecl_curl(p):
    """
    FieldDecl_curl : FieldDecl_curl FieldDecl SEMICOLON
                   |
    """
    if(len(p)==1):
        p[0]=[]
    else:
        p[0]=['FieldDecl_curl', p[1], p[2]]

def p_FieldDecl(p):
    """
    FieldDecl : ID COMMA IdentifierList Type
              | ID COMMA IdentifierList ID
              | ID COMMA IdentifierList ID DOT ID
              | ID Type
              | ID ID
              | ID ID DOT ID
              | EmbeddedField
              | ID COMMA IdentifierList Type Tag
              | ID Type Tag
              | ID COMMA IdentifierList ID Tag
              | ID ID Tag
              | ID COMMA IdentifierList ID DOT ID Tag
              | ID ID DOT ID Tag
              | EmbeddedField Tag
    """
    if (len(p)==2):
        p[0]=p[1]
    else:
        p[0]=['FieldDecl']
        for index in range(1,len(p)):
          if(isinstance(p[index],str) and p[index]!=","):
            p[0].append([p[index]])
          elif(p[index]!=','):
            p[0].append(p[index])

def p_EmbeddedField(p):
    """
    EmbeddedField : MUL ID
                  | MUL ID DOT ID
                  | ID
                  | ID DOT ID
    """
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=['EmbeddedField']
        for index in range(1,len(p)):
          if(isinstance(p[index],str)):
            p[0].append([p[index]])
          else:
            p[0].append(p[index])

def p_Tag(p):
    """
    Tag : STRING
    """
    p[0]=[p[1]]

def p_PointerType(p):
    """
    PointerType : MUL Type
                | MUL ID
                | MUL ID DOT ID
    """
    p[0]=['PointerType']
    for index in range(1,len(p)):
      if(isinstance(p[index],str)):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])

def p_FunctionType(p):
    """
    FunctionType : FUNC Signature
    """
    p[0]=['FunctionType', [p[0]], p[1]]

def p_Signature(p):
    """
    Signature : Parameters Result
    """
    p[0]=['Signature',p[1],p[2]]

#introduced CHAN
def p_Result(p):
    """
    Result : Parameters
           | Type
           | ID
           | ID DOT ID
           | CHAN
    """
    if(p[1]=='chan'):
      p[0]=[]
    elif(isinstance(p[1],str)):
      if(len(p)==2):
        p[0]=[p[1]]
      else:
        p[0]=['Result',[p[1]],[p[2]],[p[3]]]
    else:
      p[0]=p[1]

def p_Parameters(p):
    """
    Parameters : LPAREN RPAREN
               | LPAREN ParameterList RPAREN
               | LPAREN ParameterList COMMA RPAREN
    """
    if(len(p)==3):
      p[0]=['Parameters',[]]
    else:
      p[0]=['Parameters',p[2]]

#Introduced CHAN

def p_ParameterList(p):
    """
    ParameterList : ParameterDecl
                  | ID
                  | ID DOT ID
                  | CHAN Type
                  | ParameterList COMMA ID
                  | ParameterList COMMA ID DOT ID
                  | ParameterList COMMA CHAN Type
                  | ParameterList COMMA ParameterDecl
    """
    if(len(p)==2 and not isinstance(p[1],str)):
      p[0]=p[1]
    elif(len(p==2)):
      p[0]=[p[1]]
    elif(len(p)==3):
      p[0]=p[2]
    elif(len(p)==4 and isinstance(p[1],str)):
      p[0]=['ParameterList',[p[1]],[p[2]],[p[3]]]
    elif(len(p)==4 and isinstance(p[3],str)):
      p[0]=['ParameterList',p[1],[p[3]]]
    elif(len(p)==4):
      p[0]=['ParameterList',p[1],p[3]]
    elif(len(p)==5):
      p[0]=['ParameterList',p[1],p[4]]
    else:
      p[0]=['ParameterList',p[1],[p[3]],[p[4]],[p[5]]]

def p_ParaIdList(p):
    """
    ParaIdList : ID COMMA ID
               | ParaIdList COMMA ID
    """
    if(isinstance(p[1],str)):
      p[0]=['ParaIdList',[p[1]],[p[3]]]
    else:
      p[0]=['ParaIdList',p[1],[p[3]]]

def p_ParameterDecl(p):
    """
    ParameterDecl : ParaIdList ELLIPSIS Type
                  | ParaIdList Type
                  | ID ELLIPSIS Type
                  | ID Type
                  | ELLIPSIS Type
                  | ParaIdList ELLIPSIS ID
                  | ParaIdList ID
                  | ID ELLIPSIS ID
                  | ID ID
                  | ELLIPSIS ID
                  | ParaIdList ELLIPSIS ID DOT ID
                  | ParaIdList ID DOT ID
                  | ID ELLIPSIS ID DOT ID
                  | ID ID DOT ID
                  | ELLIPSIS ID DOT ID

    """
    p[0]=['ParameterDecl']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=";"):
        p[0].append([p[index]])
      elif(p[index]!="(" and p[index]!=")" and p[index]!=";"):
        p[0].append(p[index])

def p_InterfaceType(p):
    """
    InterfaceType : INTERFACE LBRACE MethodSpec_curl RBRACE
    """
    p[0]=['InterfaceType',[p[1]],p[3]]

def p_MethodSpec_curl(p):
    """
    MethodSpec_curl : MethodSpec_curl MethodSpec SEMICOLON
                    |
    """
    if(len(p)>1):
        p[0]=['MethodSpec_curl',p[1],p[2]]
    else:
        p[0]=[]

def p_MethodSpec(p):
    """
    MethodSpec : ID Signature
               | ID
               | ID DOT ID
    """
    if(len(p)==2):
      p[0]=[p[1]]
    elif(len(p)==3):
      p[0]=['MethodSpec',[p[1]],p[2]]
    else:
      p[0]=['MethodSpec',[p[1]],[p[2]],[p[3]]]

def p_MapType(p):
    """
    MapType : MAP LBRACK Type RBRACK Type
            | MAP LBRACK Type RBRACK ID
            | MAP LBRACK Type RBRACK ID DOT ID
            | MAP LBRACK ID RBRACK Type
            | MAP LBRACK ID RBRACK ID
            | MAP LBRACK ID RBRACK ID DOT ID
            | MAP LBRACK ID DOT ID RBRACK Type
            | MAP LBRACK ID DOT ID RBRACK ID
            | MAP LBRACK ID DOT ID RBRACK ID DOT ID
    """
    p[0]=['MapType']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="[" and p[index]!="]" and p[index]!="map"):
        p[0].append([p[index]])
      elif(p[index]!="[" and p[index]!="]" and p[index]!="map"):
        p[0].append(p[index])

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
    if(len(p)==1):
        p[0]=[]
    else:
        p[0]=['Statement_curl', p[1], p[2]]


def p_Expression(p):
    """
    Expression : UnaryExpr
               | Expression BinaryOp UnaryExpr
    """
    if (len(p)==2):
        p[0]=p[1]
    else:
        p[0]=[p[2], p[1], p[3]]

def p_UnaryExpr(p):
    """
    UnaryExpr : PrimaryExpr
              | UnaryOp PrimaryExpr
    """

    if (len(p)==2):
        p[0]=p[1]
    else:
        p[0]=['UnaryExpr', p[1], p[2]]

def p_BinaryOp(p):
    """
    BinaryOp : LOR
             | LAND
             | RelOp
             | AddOp
             | MulOp
    """
    if(isinstance(p[1],str)):
    	p[0]=p[1]
    else:
    	p[0]=p[1]

def p_RelOp(p):
    """
    RelOp : EQL
          | NEQ
          | LTN
          | LEQ
          | GTN
          | GEQ
    """
    p[0]=p[1]

def p_AddOp(p):
    """
    AddOp : ADD
          | SUB
          | OR
          | XOR
    """
    p[0]=p[1]

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
    p[0]=p[1]
def p_UnaryOp(p):
    """
    UnaryOp : ADD
            | SUB
            | NOT
            | XOR
            | MUL
            | AND
            | ARROW
    """
    p[0]=[p[1]]

def p_PrimaryExpr(p):
    """
    PrimaryExpr : Literal
                | ID
                | ID DOT ID
                | LPAREN Expression RPAREN
                | Conversion
                | MethodExpr
                | PrimaryExpr Selector
                | PrimaryExpr Index
                | PrimaryExpr Slice
                | PrimaryExpr TypeAssertion
                | PrimaryExpr Arguments
    """
    if (len(p)==3):
        p[0]=['PrimaryExpr', p[1], p[2]]
    elif(len(p)==4 and isinstance(p[2], str)):
        p[0]=['PrimaryExpr', [p[1]], [p[2]], [p[3]]]
    elif(len(p)==4 ):
        p[0]=p[2]
    elif(len(p)==2 and isinstance(p[1], str)):
        p[0]=[p[1]]
    elif (len(p)==2):
        p[0]=p[1]


def p_Selector(p):
    """
    Selector : DOT ID
    """
    p[0]=['Selector', [p[1]], [p[2]]]

def p_Index(p):
    """
    Index : LBRACK Expression RBRACK
    """
    p[0]=p[2]

def p_Slice(p):
    """
    Slice : LBRACK Expression COLON Expression RBRACK
          | LBRACK COLON Expression RBRACK
          | LBRACK Expression COLON RBRACK
          | LBRACK COLON RBRACK
          | LBRACK Expression COLON Expression COLON Expression RBRACK
          | LBRACK COLON Expression COLON Expression RBRACK
    """
    p[0]=['Slice']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="[" and p[index]!="]" and p[index]!=";"):
        p[0].append([p[index]])
      elif(p[index]!="[" and p[index]!="]" and p[index]!=";"):
        p[0].append(p[index])

def p_TypeAssertion(p):
    """
    TypeAssertion : DOT LPAREN Type RPAREN
                  | DOT LPAREN ID RPAREN
                  | DOT LPAREN ID DOT ID RPAREN
    """
    p[0]=['TypeAssertion']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=";"):
        p[0].append([p[index]])
      elif(p[index]!="(" and p[index]!=")" and p[index]!=";"):
        p[0].append(p[index])


def p_Arguments(p):
    """
    Arguments : LPAREN RPAREN
              | LPAREN ExpressionList RPAREN
              | LPAREN ExpressionList COMMA RPAREN
              | LPAREN ExpressionList ELLIPSIS RPAREN
              | LPAREN ExpressionList ELLIPSIS COMMA RPAREN
              | LPAREN Type RPAREN
              | LPAREN Type COMMA RPAREN
              | LPAREN Type ELLIPSIS RPAREN
              | LPAREN Type ELLIPSIS COMMA RPAREN
              | LPAREN Type COMMA ExpressionList RPAREN
              | LPAREN Type COMMA ExpressionList COMMA RPAREN
              | LPAREN Type COMMA ExpressionList ELLIPSIS RPAREN
              | LPAREN Type COMMA ExpressionList ELLIPSIS COMMA RPAREN
              | LPAREN ID RPAREN
              | LPAREN ID COMMA RPAREN
              | LPAREN ID ELLIPSIS RPAREN
              | LPAREN ID ELLIPSIS COMMA RPAREN
              | LPAREN ID COMMA ExpressionList RPAREN
              | LPAREN ID COMMA ExpressionList COMMA RPAREN
              | LPAREN ID COMMA ExpressionList ELLIPSIS RPAREN
              | LPAREN ID COMMA ExpressionList ELLIPSIS COMMA RPAREN
              | LPAREN ID DOT ID RPAREN
              | LPAREN ID DOT ID COMMA RPAREN
              | LPAREN ID DOT ID ELLIPSIS RPAREN
              | LPAREN ID DOT ID ELLIPSIS COMMA RPAREN
              | LPAREN ID DOT ID COMMA ExpressionList RPAREN
              | LPAREN ID DOT ID COMMA ExpressionList COMMA RPAREN
              | LPAREN ID DOT ID COMMA ExpressionList ELLIPSIS RPAREN
              | LPAREN ID DOT ID COMMA ExpressionList ELLIPSIS COMMA RPAREN
    """
    p[0]=['Arguments']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=","):
        p[0].append([p[index]])
      elif(p[index]!="(" and p[index]!=")" and p[index]!=","):
        p[0].append(p[index])

#introduced CHAN
def p_MethodExpr(p):
    """
    MethodExpr : CHAN Type DOT ID
               | CHAN ID DOT ID
               | CHAN ID DOT ID DOT ID
    """
    p[0]=['MethodExpr']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!="," and p[index]!="chan"):
        p[0].append([p[index]])
      elif (p[index]!="(" and p[index]!=")" and p[index]!="," and p[index]!="chan"):
        p[0].append(p[index])

def p_Conversion(p):
    """
    Conversion : Type LPAREN Expression COMMA RPAREN
               | Type LPAREN Expression RPAREN
               | ID LPAREN Expression COMMA RPAREN
               | ID LPAREN Expression RPAREN
    """
    p[0]=['Conversion']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=","):
        p[0].append([p[index]])
      elif(p[index]!="(" and p[index]!=")" and p[index]!=","):
        p[0].append(p[index])

def p_Literal(p):
    """
    Literal : BasicLit
            | CompositeLit
            | FunctionLit
    """
    p[0]=p[1]

def p_BasicLit(p):
    """
    BasicLit : INT
             | FLOAT
             | IMAG
             | RUNE
             | STRING
    """
    p[0]=[p[1]]

def p_CompositeLit(p):
    """
    CompositeLit : StructType LiteralValue
                 | ArrayType LiteralValue
                 | LBRACK ELLIPSIS RBRACK Type LiteralValue
                 | LBRACK ELLIPSIS RBRACK ID LiteralValue
                 | LBRACK ELLIPSIS RBRACK ID DOT ID LiteralValue
                 | SliceType  LiteralValue
                 | MapType LiteralValue
                 | ID LiteralValue
                 | ID DOT ID LiteralValue
    """
    p[0]=['CompositeLit']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="[" and p[index]!="]" and p[index]!=","):
        p[0].append([p[index]])
      elif(p[index]!="[" and p[index]!="]" and p[index]!=","):
        p[0].append(p[index])

def p_LiteralValue(p):
    """
    LiteralValue : LBRACE ElementList COMMA RBRACE
                 | LBRACE ElementList RBRACE
                 | LBRACE RBRACE
    """
    if (len(p)==3):
        p[0]=[]
    else:
        p[0]=p[2]


def p_ElementList(p):
    """
    ElementList : KeyedElement
                | ElementList COMMA KeyedElement
    """
    if (len(p)==2):
        p[0]=p[1]
    else:
        p[0]=['ElementList', p[1], p[3]]

def p_KeyedElement(p):
    """
    KeyedElement : ID COLON Element
                 | Expression COLON Element
                 | LiteralValue COLON Element
                 | Element
    """
    if (len(p)==2):
        p[0]=p[1]
    elif(isinstance(p[1], str)):
        p[0]=['KeyedElement', [p[1]], [p[2]], p[3]]
    else:
        p[0]=['KeyedElement', p[1], [p[2]], p[3]]



def p_Element(p):
    """
    Element : Expression
            | LiteralValue
    """
    p[0]=p[1]

def p_FunctionLit(p):
    """
    FunctionLit : FUNC Signature Block
    """
    p[0]=['FunctionLit', p[2], p[3]]

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
              | SelectStmt
              | ForStmt
              | DeferStmt
    """
    p[0]=p[1]

def p_SimpleStmt(p):
    """
    SimpleStmt : ExpressionStmt
               | SendStmt
               | IncDecStmt
               | Assignment
               | ShortVarDecl
               |
    """
    p[0]=p[1]

def p_ExpressionStmt(p):
    """
    ExpressionStmt : Expression
    """
    p[0]=p[1]

def p_SendStmt(p):
    """
    SendStmt : Expression ARROW Expression
    """
    p[0]=['SendStmt', p[1], [p[2]], p[3]]

def p_IncDecStmt(p):
    """
    IncDecStmt : Expression INC
               | Expression DEC
    """
    p[0]=['IncDecStmt', p[1], [p[2]]]

def p_Assignment(p):
    """
    Assignment : ExpressionList AssignOp ExpressionList
    """
    p[0]=[p[2], p[1], p[3]]

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
    p[0]=p[1]

def p_LabelledStmt(p):
    """
    LabelledStmt : ID COLON Statement
    """
    p[0]=['LabelledStmt', [p[1]], [p[2]], p[3]  ]

def p_GoStmt(p):
    """
    GoStmt : GO Expression
    """
    p[0]=['GoStmt', [p[1]], p[2]]


def p_ReturnStmt(p):
    """
    ReturnStmt : RETURN ExpressionList
               | RETURN
    """
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=['ReturnStmt', [p[1]], p[2]]

def p_BreakStmt(p):
    """
    BreakStmt : BREAK ID
              | BREAK
    """
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=['BreakStmt', [p[1]], [p[2]]]

def p_ContinueStmt(p):
    """
    ContinueStmt : CONTINUE ID
                 | CONTINUE
    """
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=['ContinueStmt', [p[1]], [p[2]]]

def p_GotoStmt(p):
    """
    GotoStmt : GOTO ID
    """
    p[0]=['GotoStmt', [p[1]], [p[2]]]

def p_FallthroughStmt(p):
    """
    FallthroughStmt : FALLTHROUGH
    """
    p[0]=[p[1]]

def p_DeferStmt(p):
    """
    DeferStmt : DEFER Expression
    """
    p[0]=['DeferStmt', [p[1]], p[2]]

def p_ShortVarDecl(p):
    """
    ShortVarDecl : IdentifierList DEFINE ExpressionList
    """
    p[0]=[p[2], p[1], p[3]]

def p_IfStmt(p):
    """
    IfStmt : IF Expression Block
           | IF SimpleStmt SEMICOLON Expression Block
           | IF Expression Block ELSE IfStmt
           | IF Expression Block ELSE Block
           | IF SimpleStmt SEMICOLON Expression Block ELSE Block
           | IF SimpleStmt SEMICOLON Expression Block ELSE IfStmt
    """
    p[0]=['IfStmt']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!=";" and p[index]!="]" and p[index]!=","):
        p[0].append([p[index]])
      elif(p[index]!=";" and p[index]!="]" and p[index]!=","):
        p[0].append(p[index])

def p_SwitchStmt(p):
    """
    SwitchStmt : ExprSwitchStmt
               | TypeSwitchStmt
    """
    p[0]=p[1]

# """
#    ExprSwitchStmt : SWITCH LBRACE ExprCaseClause_curl RBRACE
#                   | SWITCH SimpleStmt SEMICOLON LBRACE ExprCaseClause_curl RBRACE
#                   | SWITCH Expression LBRACE ExprCaseClause_curl RBRACE
#                   | SWITCH SimpleStmt SEMICOLON Expression LBRACE ExprCaseClause_curl RBRACE
# """

def p_ExprSwitchStmt(p):
    """
    ExprSwitchStmt : SWITCH LBRACE ExprCaseClause_curl RBRACE
                   | SWITCH SimpleStmt SEMICOLON LBRACE ExprCaseClause_curl RBRACE
                   | SWITCH SimpleStmt SEMICOLON Expression LBRACE ExprCaseClause_curl RBRACE
    """
    p[0]=['ExprSwitchStmt']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="{" and p[index]!="}" and p[index]!=";"):
        p[0].append([p[index]])
      elif(p[index]!="{" and p[index]!="}" and p[index]!=";"):
        p[0].append(p[index])

def p_ExprCaseClause_curl(p):
    """
    ExprCaseClause_curl : ExprCaseClause_curl ExprCaseClause
                        |
    """
    if(len(p)==1):
        p[0]=[]
    else:
        p[0]=['ExprCaseClause_curl', p[1], p[2]]

def p_ExprCaseClause(p):
    """
    ExprCaseClause : ExprSwitchCase COLON StatementList
    """
    p[0]=['ExprCaseClause', p[1], [p[2]], p[3]]

def p_ExprSwitchCase(p):
    """
    ExprSwitchCase : CASE ExpressionList
                   | DEFAULT
    """
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=['ExprSwitchCase', [p[1]], p[2]]


def p_TypeSwitchStmt(p):
    """
    TypeSwitchStmt : SWITCH SimpleStmt SEMICOLON TypeSwitchGuard LBRACE TypeCaseClause_curl RBRACE
                   | SWITCH TypeSwitchGuard LBRACE TypeCaseClause_curl RBRACE
    """
    p[0]=['TypeSwitchStmt']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="{" and p[index]!="}" and p[index]!=";"):
        p[0].append([p[index]])
      elif(p[index]!="{" and p[index]!="}" and p[index]!=";"):
        p[0].append(p[index])

def p_TypeCaseClause_curl(p):
    """
    TypeCaseClause_curl : TypeCaseClause_curl TypeCaseClause
                        |
    """
    if(len(p)==1):
        p[0]=[]
    else:
        p[0]=['TypeCaseClause_curl', p[1], p[2]]

def p_TypeCaseClause(p):
    """
    TypeCaseClause : TypeSwitchCase COLON StatementList
    """
    p[0]=['TypeCaseClause', p[1], [p[2]], p[3]]

def p_TypeSwitchGuard(p):
    """
    TypeSwitchGuard : ID DEFINE PrimaryExpr DOT LPAREN TYPE RPAREN
                    | PrimaryExpr DOT LPAREN TYPE RPAREN
    """
    p[0]=['TypeSwitchGuard']          ### CHECK CHECK CHECK
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=";"):
        p[0].append([p[index]])
      elif(p[index]!="(" and p[index]!=")" and p[index]!=";"):
        p[0].append(p[index])

def p_TypeSwitchCase(p):
    """
    TypeSwitchCase : CASE TypeList
                   | DEFAULT
    """
    if(len(p)==2):
        p[0]=['TypeSwitchCase', [p[1]]]
    else:
        p[0]=['TypeSwitchCase', [p[1]], p[2] ]

def p_TypeList(p):
    """
    TypeList : Type C_Type_curl
             | ID C_Type_curl
             | ID DOT ID C_Type_curl
    """
    p[0]=['TypeList']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=";"):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])

def p_C_Type_curl(p):
    """
    C_Type_curl : C_Type_curl COMMA Type
                | C_Type_curl COMMA ID
                | C_Type_curl COMMA ID DOT ID
                |
    """
    p[0]=['C_Type_curl']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=","):
        p[0].append([p[index]])
      elif(p[index]!="(" and p[index]!=")" and p[index]!=","):
        p[0].append(p[index])


def p_ForStmt(p):
    """
    ForStmt : FOR Expression Block
            | FOR ForClause Block
            | FOR RangeClause Block
            | FOR Block
    """
    p[0]=['ForStmt']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=","):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])

def p_ForClause(p):
    """
    ForClause : SimpleStmt SEMICOLON SEMICOLON SimpleStmt
              | SimpleStmt SEMICOLON Expression SEMICOLON SimpleStmt
    """
    p[0]=['ForClause']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")"):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])

def p_RangeClause(p):
    """
    RangeClause : IdentifierList DEFINE RANGE Expression
                | ExpressionList ASSIGN RANGE Expression
                | RANGE Expression
    """
    p[0]=['RangeClause']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="(" and p[index]!=")" and p[index]!=";"):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])

def p_SelectStmt(p):
    """
    SelectStmt : SELECT LBRACE CommClause_curl RBRACE
    """
    p[0]=['SelectStmt', p[3]]

def p_CommClause_curl(p):
    """
    CommClause_curl : CommClause_curl CommClause
                    |
    """
    if (len(p)==1):
        p[0]=[]
    else:
        p[0]=['CommClause_curl', p[1], p[2]]

def p_CommClause(p):
    """
    CommClause : CommCase COLON StatementList
    """
    p[0]=['CommClause', p[1], [p[2]], p[3]]

def p_CommCase(p):
    """
    CommCase : CASE SendStmt
             | CASE RecvStmt
             | DEFAULT
    """
    if (len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=['CommCase', [p[1]], p[2]]

def p_RecvStmt(p):
    """
    RecvStmt : IdentifierList DEFINE Expression
             | ExpressionList ASSIGN Expression
             | Expression
    """
    if (len(p)==2):
        p[0]=p[1]
    else:
        p[0]=['RecvStmt', p[1], [p[2]], p[3] ]


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


import os

with open(sys.argv[1],'r') as f:
    input_str = f.read()

out=parser.parse(input_str)
print out

outputDot=sys.argv[2][6:]

alist=out
file1 = open(outputDot,"w")#write mode
#file1 = open(outputHtml,"a")
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
outputTree=sys.argv[1][15:]+".ps"



os.system("dot -Tps "+ outputDot+ " -o " + outputTree)
