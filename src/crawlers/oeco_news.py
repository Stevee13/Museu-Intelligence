from .base import BaseCrawler
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import date
import time

REQUEST_DELAY = 3

MONTHS = {
    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
    'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
    'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12,
}

class OecoCrawler(BaseCrawler):
    def __init__(self):
        super().__init__('https://oeco.org.br/')

    def extract_preview(self, soup: BeautifulSoup, base_url: str) -> list[dict]:
        preview = []

        elements = soup.select('h3.h6.mb-3')#Seleciona todos os elementos h3 com as classes h6 e mb-3

        for i in elements:#Itera sobre cada h3 encontrado, seleciona o <a>, armazena o texto como 'title' e o href como 'url', e adiciona um dicionário com essas informações à lista 'preview'
            a = i.find('a')
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

    def parse_date(self, text: str | None) -> date:
        modified = text.split("de")
        month = modified[1].strip()

        if month in MONTHS:
            for k, v in MONTHS.items():
                if month == k:
                    modified[1] = v
                    day = modified[0].strip()
                    month = modified[1]
                    year = modified[2].strip()
                                
        return date(
            day=int(day),
            month=int(month),
            year=int(year)
        )

    def extract_article(self, preview: list[dict]) -> list[dict]:
        articles = []

        for a in preview:
            page = self.search_page(a['url'])
            time.sleep(REQUEST_DELAY)

            if not page:
                continue

            paragraphs = []
            for p in page.select('p.wp-block-paragraph'):
                text = p.get_text(strip=True)
                if text:
                    paragraphs.append(text)

            date_element = page.select_one('span.text-muted')
            date_text = date_element.get_text(strip=True) if date_element else None

            articles.append({
                'title': a['title'],
                'url': a['url'],
                'paragraphs': paragraphs,
                'date': self.parse_date(date_text)
            })

        return articles

    def run(self) -> list[dict]:
        soup = self.search_page(self.base_url)
        if not soup:
            print("Erro na busca.")
            return []

        preview = self.extract_preview(soup, self.base_url)
        return self.extract_article(preview)