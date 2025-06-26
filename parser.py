from lexer import lexer
from parser_lexical import parser, artigos
import gzip
import csv
import re

def parse_pubmed(file_path, output_path="resultado.csv"):
    artigos.clear()
    inside_article = False
    buffer = []

    if file_path.endswith('.gz'):
        f = gzip.open(file_path, 'rt', encoding='utf-8')
    else:
        f = open(file_path, 'r', encoding='utf-8')

    for line in f:
        if "<PubmedArticle>" in line:
            inside_article = True
            buffer = [line]
        elif "</PubmedArticle>" in line:
            buffer.append(line)
            article_str = ''.join(buffer)

            try:
                lexer.input(article_str)
                parser.parse(article_str, lexer=lexer)
            except Exception:
                continue  # ignora artigos problemáticos

            inside_article = False
            buffer = []
        elif inside_article:
            buffer.append(line)

    f.close()

    # Exportar para CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['titulo', 'autores', 'abstract', 'ano']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for artigo in artigos:
            writer.writerow(artigo)

    print(f"[✓] Processamento concluído. {len(artigos)} artigos salvos em {output_path}")
