import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import datetime
import sqlite3

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0, Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
}

baseURL = 'https://www.adorocinema.com/filmes/melhores/'
filmes = []
data_hoje = datetime.date.today().strftime('%d-%m-%Y')
agora = datetime.datetime.now()
paginaLimite = 2
card_temp_min = 1
card_temp_max = 3
pg_temp_min = 2
pg_temp_max = 4
pasta = 'C:/Users/sabado/Desktop/Python AD Janna Lima/'
bancoDados = 'banco_filmes.db'
saidaCSV = f'filmes_adoro_cinema_{data_hoje}.csv'

for pagina in range(1, paginaLimite + 1):
    url = f'{baseURL}?page={pagina}'
    print(f"Coletando dados da pagina: {pagina}\n Endereço: {url}\n")
    resposta = requests.get(url, headers=headers)
    

    if resposta.status_code != 200:
        print(f'Erro ao carregar a página {pagina}. \n Código do erro: {resposta.status_code}')
        continue

    soup = BeautifulSoup(resposta.text, "html.parser")
    cards = soup.find_all('div', class_="card entity-card entity-card-list cf")
    for card in cards:
        try: 
            titulo = "N/A"
            #capturar o titulo e o link da pagina do filme
            titulo_tag = card.find('a', class_= 'meta-title-link')
            titulo  = titulo_tag.text.strip() if titulo_tag else "N/A"
            link = 'https://www.adorocinema.com' + titulo_tag['href'] if titulo_tag else None

            #Capturar a nota do filme
            nota_tag = card.find('span', class_='stareval_note')
            nota = nota_tag.text.strip().replace(',','.') if nota_tag else "N/A"

            diretor = "N/A"
            categoria = "N/A"
            ano = "N/A"

            if link: 
                filme_resposta = requests.get(link, headers=headers)
                if filme_resposta.status_code != 200:
                    print(f"Falha ao abrir página do filme: {link} (HTTP {filme_resposta.status_code})")
                    continue

                filme_soup = BeautifulSoup(filme_resposta.text, 'html.parser')

                #capturar o diretor

                diretor_tag = filme_soup.find('div', class_= 'meta-body-item meta-body-direction meta-body-oneline')

                if diretor_tag: 
                    diretor = (
                        diretor_tag.text
                        .strip()
                        .replace('Direção: ','')
                        .replace(',','')
                        .replace('\n','')
                        .replace('\r','')
                        .strip()
                    )if diretor_tag else 'N/A'

                diretor = diretor.replace('\n',' ').replace('\r','').strip()

            #capturar os generos 
            genero_blocks = filme_soup.find('div', class_= 'meta-body-info')
            if genero_blocks:
                genero_links = genero_blocks.find_all('a')
                generos = [g.text.strip() for g in genero_links]
                categoria = ', '.join(generos[:3]) if generos else 'N/A'

            else: 
                categoria = 'N/A'

            #capturar o ano de lançamento filme
            ano_tag = genero_blocks.find('span', class_='date') if genero_blocks else None
            ano = ano_tag.text.strip() if ano_tag else 'N/A'

            if titulo != 'N/A' and link != 'N/A' and nota != 'N/A':
                filmes.append({
                    'Título': titulo,
                    'Direção': diretor,
                    'Nota': nota,
                    'Link': link,
                    'Ano': ano,
                    'Categoria': categoria
                })
            else:
                print(f'Filme incompleto ou erro na coleta de dados do filme {titulo}')
                
            tempo = random.uniform(card_temp_min, card_temp_max)
            print(f"Filme carregado: {titulo}")
            print(f'Tempo de espera entre filmes: {tempo: .1f}')
            time.sleep(tempo)

        except Exception as erro:  
            print(f'Erro ao processar o filme {titulo}\n Erro: {erro}')
    
    #esperar um tempo entre uma página e outra 
    tempo = random.uniform(pg_temp_min, pg_temp_max)
    print(f"Tempo de espera entre páginas: {tempo:.1f}")
    time.sleep(tempo)

df = pd.DataFrame(filmes)
print(df.head())

