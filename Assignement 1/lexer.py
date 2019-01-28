import ply.lex as lex

import sys


argumentList = sys.argv



cfg= sys.argv[1][6:]

inputProg=sys.argv[2]

outputHtml=sys.argv[3][9:]





reserved={
	'break' : 'BREAK',
	'case' : 'CASE',
	'chan' : 'CHAN',
	'const' : 'CONST',
	'continue' : 'CONTINUE',
	'default' : 'DEFAULT',
	'defer' : 'DEFER',
	'else' : 'ELSE',
	'fallthrough' : 'FALLTHROUGH',
	'for' : 'FOR',
	'func' : 'FUNC',
	'go' : 'GO',
	'goto' : 'GOTO',
	'if' : 'IF',
	'import' : 'IMPORT',
	'interface' : 'INTERFACE',
	'map' : 'MAP',
	'package' : 'PACKAGE',
	'range' : 'RANGE',
	'return' : 'RETURN',
	'select' : 'SELECT',
	'struct' : 'STRUCT',
	'switch' : 'SWITCH',
	'type' : 'TYPE',
	'var' : 'VAR'
}

tokens=['COMMENT','ID','INT','FLOAT','IMAG','STRING',
        'ADD','SUB','MUL','DIV','MOD',
        'AND','OR','XOR','SHL','SHR','AND_NOT',
        'ADD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN',
        'AND_ASSIGN','OR_ASSIGN','XOR_ASSIGN','SHL_ASSIGN','SHR_ASSIGN','AND_NOT_ASSIGN',
        'LAND','LOR','ARROW','INC','DEC',
	'EQL','LTN','GTN','ASSIGN','NOT',
        'NEQ','LEQ','GEQ','DEFINE','ELLIPSIS',
	'LPAREN','LBRACK','LBRACE','COMMA','DOT',
        'RPAREN','RBRACK','RBRACE','SEMICOLON','COLON', 'WHITESPACE', 'TABSPACE', 'NEWLINE'
]

tokens+=reserved.values()

jbjj="#FF0000"

t_ignore=''
t_WHITESPACE=r'\s'
t_TABSPACE=r'\t'
t_ADD=r'\+'
t_SUB=r'-'
t_MUL=r'\*'
t_DIV=r'/'
t_MOD=r'%'
t_AND=r'&'
t_OR=r'\|'
t_XOR=r'\^'
t_SHL=r'<<'
t_SHR=r'>>'
t_AND_NOT=r'&\^'
t_ADD_ASSIGN=r'\+='
t_SUB_ASSIGN=r'-='
t_MUL_ASSIGN=r'\*='
t_DIV_ASSIGN=r'/='
t_MOD_ASSIGN=r'%='
t_AND_ASSIGN=r'&='
t_OR_ASSIGN=r'\|='
t_XOR_ASSIGN=r'\^='
t_SHL_ASSIGN=r'<<='
t_SHR_ASSIGN=r'>>='
t_LAND=r'&&'
t_LOR=r'\|\|'
t_ARROW=r'<-'
t_INC=r'\+\+'
t_DEC=r'--'
t_EQL=r'=='
t_LTN=r'<'
t_GTN=r'>'
t_ASSIGN=r'='
t_NOT=r'!'
t_NEQ=r'!='
t_LEQ=r'<='
t_GEQ=r'>='
t_DEFINE=r':='
t_ELLIPSIS=r'\.\.\.'
t_LPAREN=r'\('
t_RPAREN=r'\)'
t_LBRACK=r'\['
t_RBRACK=r'\]'
t_LBRACE=r'\{'
t_RBRACE=r'\}'
t_SEMICOLON=r';'
t_COLON=r':'
t_COMMA=r','
t_DOT=r'\.'

def t_COMMENT(t):
	r'//.* | /\*(.|\n)*?\*/'
	return t


def t_IMAG(t):
	r'([0-9]+\.[0-9]*(e|E)(\+|-)[0-9]+ | [0-9]+\.[0-9]*(e|E)[0-9]+ | \.[0-9]+(e|E)(\+|-)[0-9]+ | \.[0-9]+(e|E)[0-9]+ | [0-9]+(e|E)(\+|-)[0-9]+ | [0-9]+(e|E)[0-9]+ | [0-9]+\.[0-9]* |   \.[0-9]+)i  '
	return t

def t_FLOAT(t):
	r'[0-9]+\.[0-9]*(e|E)(\+|-)[0-9]+ | [0-9]+\.[0-9]*(e|E)[0-9]+ | \.[0-9]+(e|E)(\+|-)[0-9]+ | \.[0-9]+(e|E)[0-9]+ | [0-9]+(e|E)(\+|-)[0-9]+ | [0-9]+(e|E)[0-9]+ | [0-9]+\.[0-9]* |   \.[0-9]+  '
	return t

def t_INT(t):
	r'0(x|X)[0-9A-Fa-f]+ | [1-9]\d* | 0[0-7]*'
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved:
		t.type = reserved[t.value]
	return t

def t_STRING(t):
	r'(\"(. | \n )*?[^\\]\") | (\`(. | \n)*?\`)'
	return t

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()


with open(inputProg, 'r') as myfile:
  data = myfile.read()




# Give the lexer OBsome input
lexer.input(data)

# Python program to illustrate


# Write-Overwrites
file1 = open(outputHtml,"w")#write mode
#file1 = open(outputHtml,"a")
file1.write("<html><body bgcolor= \"#D3D3D3\"><div><pre>")
file1.write("\n")

colorDic = {}

with open(cfg) as f:
    for line in f:
       (key, val) = line.split()
       colorDic[key] = val
colorDic["WHITESPACE"]="#FFE6E6"
colorDic["TABSPACE"]="#FFE6E6"
colorDic["NEWLINE"]="#FFE6E6"

while True:
	tok = lexer.token()
	if not tok:
	    break
	file1.write("<span style=\"color: "+colorDic[tok.type]+"\">"+tok.value+"</span>")

file1.write("</pre></div></body></html>")
file1.close()
