from .base import BaseCrawler
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

class OecoCrawler(BaseCrawler):
    def __init__(self):
        super().__init__('https://oeco.org.br/')

    def extract_preview(self, soup: BeautifulSoup, base_url: str) -> list[dict]:
        preview = []

        elements = soup.select('h3.h6.mb-3')#Seleciona todos os elementos h3 com as classes h6 e mb-3

        for h3 in elements:#Itera sobre cada h3 encontrado, seleciona o <a>, armazena o texto como 'title' e o href como 'url', e adiciona um dicionário com essas informações à lista 'preview'
            a = h3.find('a')
            if not a:
                continue
            title = a.get_text(strip=True)
            href = a.get('href')
            url = urljoin(base_url, href)

            preview.append({
                'title': title,
                'url': url
            })

        return preview
    
    def extract_article(self, preview) -> list:
        all_content = []

        #Recebe a variavel preview da função extract_preview() e utiliza a url de cada artigo.
        for a in preview:
            url = a['url']
            soup = self.search_page(url)

            if soup:
                content = soup.select('p.wp-block-paragraph')
                paragraph = [p.get_text(strip=True) for p in content if p.get_text(strip=True)]#list comprehension que armazena o texto de cada parágrafo não vazio numa lista
                all_content.append({
                    'paragraph': paragraph
                })

        return all_content

    #def catch_date(self, soup: BeautifulSoup) -> datetime:
        
    def run(self):
        soup = self.search_page(self.base_url)
        if soup:
            preview = self.extract_preview(soup, self.base_url)
            content = self.extract_article(preview)
            return preview, content
        else:
            print("Erro na busca.")
            return []

