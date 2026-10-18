import requests
from bs4 import BeautifulSoup

class BaseCrawler:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        self.TIMEOUT = 10

    def search_page(self, url: str) -> BeautifulSoup:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}#Define o User-Agent para evitar bloqueios por parte do site
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            return soup
        except requests.RequestException as e:
            print(f"Erro ao buscar {url}: {str(e)}")

            return None