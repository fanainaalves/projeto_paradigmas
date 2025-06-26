import ply.yacc as yacc
from lexer import tokens

# Lista de artigos extraídos
artigos = []

# Dicionário temporário para montar um artigo
artigo = {
    'titulo': '',
    'abstract': '',
    'ano': '',
    'autores': []
}

# Flags de controle de contexto
current_tag = ''
autor_temp = {'ForeName': '', 'LastName': ''}

def p_document(p):
    '''document : elementos'''
    pass

def p_elementos(p):
    '''elementos : elemento elementos
                 | elemento'''
    pass

def p_elemento(p):
    '''elemento : LTAG TEXT RTAG
                | LTAG elementos RTAG'''
    global current_tag, artigo, autor_temp

    tag_name = p[1].strip('<>').lower()
    closing_tag = p[len(p) - 1].strip('</>').lower()

    if tag_name != closing_tag:
        return  # ignora inconsistência

    # Conteúdo direto entre tags (caso base)
    if len(p) == 4 and isinstance(p[2], str):
        content = p[2].strip()

        if tag_name == 'articletitle':
            artigo['titulo'] = content

        elif tag_name == 'abstracttext':
            if artigo['abstract']:
                artigo['abstract'] += ' ' + content
            else:
                artigo['abstract'] = content

        elif tag_name == 'year' and not artigo['ano']:
            artigo['ano'] = content

        elif tag_name == 'forename':
            autor_temp['ForeName'] = content

        elif tag_name == 'lastname':
            autor_temp['LastName'] = content

    # Quando fecha Author, monta nome completo
    if tag_name == 'author':
        nome = autor_temp.get('ForeName', '')
        sobrenome = autor_temp.get('LastName', '')
        completo = f"{nome} {sobrenome}".strip()
        if completo:
            artigo['autores'].append(completo)
        autor_temp = {'ForeName': '', 'LastName': ''}

    # Quando fecha um PubmedArticle, salva e reinicia
    if tag_name == 'pubmedarticle':
        artigos.append({
            'titulo': artigo.get('titulo', '').strip(),
            'abstract': artigo.get('abstract', '').strip(),
            'ano': artigo.get('ano', '').strip(),
            'autores': '; '.join(artigo.get('autores', [])),
        })
        artigo = {'titulo': '', 'abstract': '', 'ano': '', 'autores': []}
        autor_temp = {'ForeName': '', 'LastName': ''}


def p_error(p):
    if p:
        print(f"[Aviso] Erro de sintaxe em token: {p.type} (valor: {p.value})")

parser = yacc.yacc()
