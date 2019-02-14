import ply.yacc as yacc
import lexer

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
                 | MethodDecl
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
              | IdentifierList ID DOT ID ASSIGN ExpressionList
              | IdentifierList Type ASSIGN ExpressionList
              | IdentifierList ASSIGN ExpressionList
              | IdentifierList 
    """

def p_IdentifierList(p):
    """
    IdentifierList : ID 
                   | ID COMMA IdentifierList
    """

def p_ExpressionList(p):
    """
    ExpressionList : Expression 
                   | ExpressionList COMMA Expression
    """

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
    TypeSpec : AliasDecl 
             | TypeDef
    """

def p_AliasDecl(p):
    """
    AliasDecl : ID ASSIGN Type
              | ID ASSIGN ID
              | ID ASSIGN ID DOT ID
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
            | IdentifierList ID DOT ID ASSIGN ExpressionList
            | IdentifierList ASSIGN ExpressionList
            | IdentifierList ID
            | IdentifierList ID DOT ID
            | IdentifierList Type 
    """

def p_FunctionDecl(p):
    """
    FunctionDecl : FUNC ID Signature Block 
                 | FUNC ID Signature
    """

def p_MethodDecl(p):
    """
    MethodDecl : FUNC Receiver ID Signature Block 
               | FUNC Receiver ID Signature
    """

def p_Receiver(p):
    """
    Receiver : Parameters
    """

def p_Type(p):
    """
    Type : LPAREN Type RPAREN
         | LPAREN ID RPAREN
         | LPAREN ID DOT ID RPAREN
         | TypeLit
    """

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

def p_ArrayType(p):
    """
    ArrayType : LBRACK Expression RBRACK Type
              | LBRACK Expression RBRACK ID
              | LBRACK Expression RBRACK ID DOT ID
    """

def p_SliceType(p):
    """
    SliceType : LBRACK RBRACK Type
    """

def p_StructType(p):
    """
    StructType : STRUCT LBRACE FieldDecl_curl RBRACE
    """

def p_FieldDecl_curl(p):
    """
    FieldDecl_curl : FieldDecl_curl FieldDecl SEMICOLON
                   |
    """
                
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

def p_EmbeddedField(p):
    """
    EmbeddedField : MUL ID
                  | MUL ID DOT ID
                  | ID
                  | ID DOT ID
    """

def p_Tag(p):
    """
    Tag : STRING
    """

def p_PointerType(p):
    """
    PointerType : MUL Type
                | MUL ID
                | MUL ID DOT ID
    """

def p_FunctionType(p):
    """
    FunctionType : FUNC Signature
    """

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
                  | ID
                  | ID DOT ID
                  | CHAN Type
                  | ParameterList COMMA ID 
                  | ParameterList COMMA ID DOT ID 
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

def p_InterfaceType(p):
    """
    InterfaceType : INTERFACE LBRACE MethodSpec_curl RBRACE
    """

def p_MethodSpec_curl(p):
    """
    MethodSpec_curl : MethodSpec_curl MethodSpec SEMICOLON
                    |
    """

def p_MethodSpec(p):
    """
    MethodSpec : ID Signature 
               | ID
               | ID DOT ID 
    """

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

def p_Block(p):
    """
    Block : LBRACE StatementList RBRACE
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

def p_UnaryExpr(p):
    """
    UnaryExpr : PrimaryExpr
              | UnaryOp PrimaryExpr
    """

def p_BinaryOp(p):
    """
    BinaryOp : LOR
             | LAND
             | RelOp
             | AddOp
             | MulOp
    """

def p_RelOp(P):
    """
    RelOp : EQL 
          | NEQ 
          | LTN 
          | LEQ 
          | GTN 
          | GEQ 
    """

def p_AddOp(p):
    """
    AddOp : ADD 
          | SUB 
          | OR 
          | XOR 
    """

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

def p_Selector(p):
    """
    Selector : DOT ID
    """

def p_Index(p):
    """
    Index : LBRACK Expression RBRACK
    """

def p_Slice(p):
    """
    Slice : LBRACK Expression COLON Expression RBRACK
          | LBRACK COLON Expression RBRACK
          | LBRACK Expression COLON RBRACK
          | LBRACK COLON RBRACK
          | LBRACK Expression COLON Expression COLON Expression RBRACK
          | LBRACK COLON Expression COLON Expression RBRACK
    """

def p_TypeAssertion(p):
    """
    TypeAssertion : DOT LPAREN Type RPAREN
                  | DOT LPAREN ID RPAREN
                  | DOT LPAREN ID DOT ID RPAREN
    """

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

#introduced CHAN
def p_MethodExpr(p):
    """
    MethodExpr : CHAN Type DOT ID
               | CHAN ID DOT ID
               | CHAN ID DOT ID DOT ID
    """

def p_Conversion(p):
    """
    Conversion : Type LPAREN Expression COMMA RPAREN 
               | Type LPAREN Expression RPAREN 
               | ID LPAREN Expression COMMA RPAREN 
               | ID LPAREN Expression RPAREN 
               | ID DOT ID LPAREN Expression COMMA RPAREN 
               | ID DOT ID LPAREN Expression RPAREN 
    """

def p_Literal(p):
    """
    Literal : BasicLit
            | CompositeLit
            | FunctionLit
    """

def p_BasicLit(p):
    """
    BasicLit : INT
             | FLOAT
             | IMAG
             | RUNE
             | STRING
    """

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

def p_LiteralValue(p):
    """
    LiteralValue : LBRACE ElementList COMMA RBRACE 
                 | LBRACE ElementList RBRACE
                 | LBRACE RBRACE
    """

def p_ElementList(p):
    """
    ElementList : KeyedElement
                | ElementList COMMA KeyedElement 
    """

def p_KeyedElement(p):
    """
    KeyedElement : ID COLON Element
                 | Expression COLON Element
                 | LiteralValue COLON Element
                 | Element
    """

def p_Element(p):
    """
    Element : Expression 
            | LiteralValue
    """

def p_FunctionLit(p):
    """
    FunctionLit : FUNC Signature Block
    """

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

def p_SimpleStmt(p):
    """
    SimpleStmt : ExpressionStmt
               | SendStmt
               | IncDecStmt
               | Assignment
               | ShortVarDecl
               |
    """

def p_expressionStmt(p):
    """
    ExpressionStmt : Expression 
    """

def p_SendStmt(p):
    """
    SendStmt : Expression ARROW Expression
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
               | TypeSwitchStmt
    """

def p_ExprSwitchStmt(p):
    """
    ExprSwitchStmt : SWITCH LBRACE ExprCaseClause_curl RBRACE
                   | SWITCH SimpleStmt SEMICOLON LBRACE ExprCaseClause_curl RBRACE
                   | SWITCH Expression LBRACE ExprCaseClause_curl RBRACE
                   | SWITCH SimpleStmt SEMICOLON Expression LBRACE ExprCaseClause_curl RBRACE
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

def p_TypeSwitchStmt(p):
    """
    TypeSwitchStmt : SWITCH SimpleStmt SEMICOLON TypeSwitchGuard LBRACE TypeCaseClause_curl RBRACE 
                   | SWITCH TypeSwitchGuard LBRACE TypeCaseClause_curl RBRACE 
    """

def p_TypeCaseClause_curl(p):
    """
    TypeCaseClause_curl : TypeCaseClause_curl TypeCaseClause 
                        |
    """

def p_TypeCaseClause(p):
    """
    TypeCaseClause : TypeSwitchCase COLON StatementList
    """

def p_TypeSwitchGuard(p):
    """
    TypeSwitchGuard : ID DEFINE PrimaryExpr DOT LPAREN TYPE RPAREN 
                    | PrimaryExpr DOT LPAREN TYPE RPAREN
    """

def p_TypeSwitchCase(p):
    """
    TypeSwitchCase : CASE TypeList 
                   | DEFAULT
    """

def p_TypeList(p):
    """
    TypeList : Type C_Type_curl
             | ID C_Type_curl 
             | ID DOT ID C_Type_curl 
    """

def p_C_Type_curl(p):
    """
    C_Type_curl : C_Type_curl COMMA Type 
                | C_Type_curl COMMA ID
                | C_Type_curl COMMA ID DOT ID
                | 
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

def p_SelectStmt(p):
    """
    SelectStmt : SELECT LBRACE CommClause_curl RBRACE
    """

def p_CommClause_curl(p):
    """
    CommClause_curl : CommClause_curl CommClause
                    |
    """

def p_CommClause(p):
    """
    CommClause : CommCase COLON StatementList
    """

def p_CommCase(p):
    """
    CommCase : CASE SendStmt 
             | CASE RecvStmt
             | DEFAULT
    """

def p_RecvStmt(p):
    """
    RecvStmt : IdentifierList DEFINE Expression 
             | ExpressionList ASSIGN Expression
             | Expression
    """

def p_error(p):
    print("Print Syntax Error", p)

parser=yacc.yacc()
