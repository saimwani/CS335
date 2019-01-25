import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'COMMENT',
   'OCTAL',
   'HEXADECIMAL'
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMENT = r'//.*'
# A regular expression rule with some action code

def t_NUMBER(t):
    r'[1-9]\d*'
    t.value = int(t.value)
    return t

def t_HEXADECIMAL(t):
	r'0[xX][0-9A-Fa-f]+'
	t.value=int(t.value,16)
	return t

def t_OCTAL(t):
	r'0[0-7]+'
	t.value=int(t.value,8)
	return t




# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)





# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
# Test it out
data = '''
//ssss   ss     s
5 = 4 * 10
0x56
//ff
3 + 4// * 10
  + -20 *2
'''

# Give the lexer OBsome input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
