import json

import requests

def InserirArquivo(result):
    try:
        arquivo = open("dados.json", "w")
        json.dump(result, arquivo,ensure_ascii=False)
        arquivo.close()
    except Exception as error:
        print(error)

def LerArquivo():
    try:
        arquivo = open("dados.json", "r")
        result = json.load(arquivo)
        return result
        arquivo.close()
    except Exception as error:
        print(error)
