from base import BaseCrawler
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class OecoCrawler(BaseCrawler):
    def __init__(self):
        super().__init__('https://oeco.org.br/')

    def extract_preview(self, soup: BeautifulSoup, base_url: str) -> list[dict]:
        articles = []

        elements = soup.select('h3.h6.mb-3')#Seleciona todos os elementos h3 com as classes h6 e mb-3

        for h3 in elements:#Itera sobre cada h3 encontrado, seleciona o <a>, armazena o texto como 'title' e o href como 'url', e adiciona um dicionário com essas informações à lista 'articles'
            a = h3.find('a')
            if not a:
                continue
            title = a.get_text(strip=True)
            href = a.get('href')
            url = urljoin(base_url, href)

            articles.append({
                'title': title,
                'url': url
            })

        return articles

    def run(self):
        soup = self.search_page(self.base_url)
        if soup:
            articles = self.extract_preview(soup, self.base_url)
            return articles
        else:
            print("Erro na busca.")
            return []

if __name__ == "__main__":
    crawler = OecoCrawler()
    articles = crawler.run()
    for i in articles:
        print(f"Title: {i['title']}, URL: {i['url']}")