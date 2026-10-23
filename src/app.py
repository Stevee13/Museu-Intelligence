from crawlers.oeco_news import OecoCrawler
import os


def main():
    crawler = OecoCrawler()
    articles = crawler.run()

    for article in articles:
        print(article['title'])
        print(f"URL: {article['url']}")
        print(f"Data: {article['date']}")
        print(f"Parágrafos: {len(article['paragraphs'])}")
        print("-" * 40)

if __name__ == "__main__":
    os.system("clear")
    main()
