import ply.lex as lex
reserved={
	'break' : 'BREAK',
	'case' : 'CASE',
#        'chan' : 'CHAN',
	'const' : 'CONST',
	'continue' : 'CONTINUE',
	'default' : 'DEFAULT',
#	'defer' : 'DEFER',
	'else' : 'ELSE',
	'fallthrough' : 'FALLTHROUGH',
	'for' : 'FOR',
	'func' : 'FUNC',
#	'go' : 'GO',
	'goto' : 'GOTO',
	'if' : 'IF',
	'import' : 'IMPORT',
#	'interface' : 'INTERFACE',
#	'map' : 'MAP',
	'package' : 'PACKAGE',
#	'range' : 'RANGE',
	'return' : 'RETURN',
#	'select' : 'SELECT',
	'struct' : 'STRUCT',
	'switch' : 'SWITCH',
	'type' : 'TYPE',
	'var' : 'VAR',
        'True' : 'TRUE',
        'False' : 'FALSE',
}

tokens=['ID','INT','FLOAT','STRING',
        'ADD','SUB','MUL','DIV','MOD',
        'AND','OR','XOR','SHL','SHR','AND_NOT',
        'ADD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN',
        'OR_ASSIGN','XOR_ASSIGN','SHL_ASSIGN','SHR_ASSIGN',
        'LAND','LOR','INC','DEC',
	'EQL','LTN','GTN','ASSIGN','NOT',
        'NEQ','LEQ','GEQ','DEFINE',
	'LPAREN','LBRACK','LBRACE','COMMA','DOT',
        'RPAREN','RBRACK','RBRACE','SEMICOLON','COLON', 'RUNE'
]

tokens+=reserved.values()

prev_token=""

t_ignore=' \t'
def t_COMMENT(t):
    r'//.* | /\*(.|\n)*?\*/'
    global prev_token
    prev_token=t.type
    t.lexer.lineno += t.value.count('\n')

def t_FLOAT(t):
    r'[0-9]+\.[0-9]*(e|E)(\+|-)[0-9]+ | [0-9]+\.[0-9]*(e|E)[0-9]+ | \.[0-9]+(e|E)(\+|-)[0-9]+ | \.[0-9]+(e|E)[0-9]+ | [0-9]+(e|E)(\+|-)[0-9]+ | [0-9]+(e|E)[0-9]+ | [0-9]+\.[0-9]* |   \.[0-9]+  '
    global prev_token
    prev_token=t.type
    return t

def t_INT(t):
    r'0(x|X)[0-9A-Fa-f]+ | [1-9]\d* | 0[0-7]*'
    global prev_token
    prev_token=t.type
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    global prev_token
    prev_token=t.type
    if t.value in reserved:
	t.type = reserved[t.value]
        if(not (t.value=="break" or t.value=="return" or t.value=="continue" or t.value=="fallthrough")):
            prev_token="Not newline here"
    return t

def t_STRING(t):
    r'(\".*?[^\\\n]\") | \"\" | (`(. | \n)*?`)'
    global prev_token
    prev_token=t.type
    t.lexer.lineno += t.value.count('\n')
    return t

def t_INC(t):
    r'\+\+'
    global prev_token
    prev_token=t.type
    return t

def t_DEC(t):
    r'--'
    global prev_token
    prev_token=t.type
    return t

def t_SHL(t):
    r'<<'
    global prev_token
    prev_token=t.type
    return t

def t_SHR(t):
    r'>>'
    global prev_token
    prev_token=t.type
    return t

def t_AND_NOT(t):
    r'&\^'
    global prev_token
    prev_token=t.type
    return t

def t_ADD_ASSIGN(t):
    r'\+='
    global prev_token
    prev_token=t.type
    return t

def t_SUB_ASSIGN(t):
    r'-='
    global prev_token
    prev_token=t.type
    return t

def t_MUL_ASSIGN(t):
    r'\*='
    global prev_token
    prev_token=t.type
    return t

def t_DIV_ASSIGN(t):
    r'/='
    global prev_token
    prev_token=t.type
    return t

def t_MOD_ASSIGN(t):
    r'%='
    global prev_token
    prev_token=t.type
    return t

def t_OR_ASSIGN(t):
    r'\|='
    global prev_token
    prev_token=t.type
    return t

def t_XOR_ASSIGN(t):
    r'\^='
    global prev_token
    prev_token=t.type
    return t

def t_SHL_ASSIGN(t):
    r'<<='
    global prev_token
    prev_token=t.type
    return t

def t_SHR_ASSIGN(t):
    r'>>='
    global prev_token
    prev_token=t.type
    return t

def t_LAND(t):
    r'&&'
    global prev_token
    prev_token=t.type
    return t

def t_LOR(t):
    r'\|\|'
    global prev_token
    prev_token=t.type
    return t

def t_EQL(t):
    r'=='
    global prev_token
    prev_token=t.type
    return t

def t_NEQ(t):
    r'!='
    global prev_token
    prev_token=t.type
    return t

def t_LEQ(t):
    r'<='
    global prev_token
    prev_token=t.type
    return t

def t_GEQ(t):
    r'>='
    global prev_token
    prev_token=t.type
    return t

def t_ADD(t):
    r'\+'
    global prev_token
    prev_token=t.type
    return t

def t_SUB(t):
    r'-'
    global prev_token
    prev_token=t.type
    return t

def t_MUL(t):
    r'\*'
    global prev_token
    prev_token=t.type
    return t

def t_DIV(t):
    r'/'
    global prev_token
    prev_token=t.type
    return t

def t_MOD(t):
    r'%'
    global prev_token
    prev_token=t.type
    return t

def t_AND(t):
    r'&'
    global prev_token
    prev_token=t.type
    return t

def t_OR(t):
    r'\|'
    global prev_token
    prev_token=t.type
    return t

def t_XOR(t):
    r'\^'
    global prev_token
    prev_token=t.type
    return t


def t_LTN(t):
    r'<'
    global prev_token
    prev_token=t.type
    return t

def t_GTN(t):
    r'>'
    global prev_token
    prev_token=t.type
    return t

def t_ASSIGN(t):
    r'='
    global prev_token
    prev_token=t.type
    return t

def t_NOT(t):
    r'!'
    global prev_token
    prev_token=t.type
    return t

def t_DEFINE(t):
    r':='
    global prev_token
    prev_token=t.type
    return t

def t_LPAREN(t):
    r'\('
    global prev_token
    prev_token=t.type
    return t

def t_RPAREN(t):
    r'\)'
    global prev_token
    prev_token=t.type
    return t

def t_LBRACK(t):
    r'\['
    global prev_token
    prev_token=t.type
    return t

def t_RBRACK(t):
    r'\]'
    global prev_token
    prev_token=t.type
    return t

def t_LBRACE(t):
    r'\{'
    global prev_token
    prev_token=t.type
    return t

def t_RBRACE(t):
    r'\}'
    global prev_token
    prev_token=t.type
    return t

def t_SEMICOLON(t):
    r';'
    global prev_token
    prev_token=t.type
    return t

def t_COLON(t):
    r':'
    global prev_token
    prev_token=t.type
    return t

def t_COMMA(t):
    r','
    global prev_token
    prev_token=t.type
    return t

def t_DOT(t):
    r'\.'
    global prev_token
    prev_token=t.type
    return t

def t_RUNE(t):
    r'\'([^\\\n]|(\\(a|f|n|b|r|t|v|\\|\'|\")))\''
    global prev_token
    prev_token=t.type
    return t

def t_NEWLINE(t):
    r'\n+'
    global prev_token
    if(prev_token=="ID" or prev_token=="INT" or prev_token=="FLOAT" or prev_token=="IMAG" or prev_token=="RUNE" or prev_token=="STRING" or prev_token=="INC" or prev_token=="DEC" or prev_token=="RBRACE" or prev_token=="RBRACK" or prev_token=="RPAREN"):
        t.type="SEMICOLON"
        t.value=";"
        prev_token=t.type
        t.lexer.lineno += len(t.value)
        return t
    prev_token=t.type
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
