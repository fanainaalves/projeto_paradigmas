from lexer import lexer
from parser_lexical import parser, artigos
import gzip
import csv

def parse_pubmed(file_path, output_path="resultado.csv"):
    # Ler o conteúdo do arquivo (GZ ou XML puro)
    if file_path.endswith('.gz'):
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            xml_content = f.read()
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()

    # Reiniciar os dados
    artigos.clear()

    # Analisar com lexer + parser
    lexer.input(xml_content)
    parser.parse(xml_content, lexer=lexer)

    # Escrever resultado em CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['titulo', 'autores', 'abstract', 'ano']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for artigo in artigos:
            writer.writerow(artigo)

    print(f"Arquivo CSV salvo em: {output_path}")
    return artigos
