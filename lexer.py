import ply.lex as lex

# Tokens esperados
tokens = (
    'LTAG',     # <Tag>
    'RTAG',     # </Tag>
    'TEXT',     # conteúdo entre tags
)

# Ignora espaços, tabs e quebras de linha
t_ignore = ' \t\n'

# Tag de abertura: <Tag>
def t_LTAG(t):
    r'<[a-zA-Z0-9]+>'
    return t

# Tag de fechamento: </Tag>
def t_RTAG(t):
    r'</[a-zA-Z0-9]+>'
    return t

# Texto entre tags
def t_TEXT(t):
    r'[^<>]+'
    t.value = t.value.strip()
    return t

# Tratamento de erro
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Criar o lexer
lexer = lex.lex()
