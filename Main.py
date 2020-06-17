import json

import requests
import urllib
from bs4 import BeautifulSoup
import unicodedata
from Arquivo import InserirArquivo

result = []
dados_recebidos=0
index_request = 1
total_percorrido = 0

def tansformaString(result):
    return result.unicode('ascii', 'ignore')

r = requests.get("http://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados?d={}&s={}&l=10&o%5B0%5D%5BdataEntrega%5D=desc&tipoFundo=1&idCategoriaDocumento=6&idTipoDocumento=45&idEspecieDocumento=0&_=1592263465886".format(str(index_request),str(dados_recebidos)))
print(r.encoding)
#quantidade_paginas = 10*pagina['recordsTotal']
#Se quiser o limite total de empresas, descomente a linha acima
quantidade_paginas = 40 #Aqui coloca um limite para a quantidade de empresas

while total_percorrido <quantidade_paginas:
    if total_percorrido!=0 and total_percorrido%10 == 0:
        dados_recebidos += 10
        index_request += 1
    r = requests.get("http://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados?d={}&s={}&l=10&o%5B0%5D%5BdataEntrega%5D=desc&tipoFundo=1&idCategoriaDocumento=6&idTipoDocumento=45&idEspecieDocumento=0&_=1592263465886".format(str(index_request),str(dados_recebidos)))
    pagina = r.json()
    for dados in pagina['data']:
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': 'S01d1c2dd=011d592ce17b2c69f24ccef9694642df9126122f8285f1428997b42dc2bead643042e1cc0857419ed29c082c97535b658371e06ea236868c3de2107f804672c7787e720f3f; TS01871345=011d592ce163adb39d2aab1579ffa7a83585edaed6542a6cbb599c3c094c4f7d5a4f4e3f3d79906a7469c663ab4ef0addeebb3e47b',
            'Host': 'fnet.bmfbovespa.com.br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }

        url_documento = "http://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id={}&cvm=true".format(dados['id'])
        documento_empresa = requests.get(url_documento, headers=headers)
        bf = BeautifulSoup(documento_empresa.text, 'html.parser')
        conteudos_requeridos = bf.find_all('span', {'class': 'dado-cabecalho'})

        dados_pagina = {
            'Nome-do-fundo': dados['descricaoFundo'],
            'CNPJ': conteudos_requeridos[1].text,
            'Data-de-funcionamento': conteudos_requeridos[2].text,
            'Publico-alvo': conteudos_requeridos[3].text,
            'Quantidade-de-cotas-emitidas': conteudos_requeridos[5].text,
            'Prazo-de-duracao': conteudos_requeridos[11].text,
        }
        result_dados = json.dumps(dados_pagina, ensure_ascii=False)
        result.append(result_dados)
        print("Total de paginas percorridas: "+str(total_percorrido))
        total_percorrido += 1

print("\n")
InserirArquivo(result)
for r in result:
    print(str(r))

