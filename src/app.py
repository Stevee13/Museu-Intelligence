from crawlers.oeco_news import OecoCrawler


def main():
    crawler = OecoCrawler()
    preview, content = crawler.run()

    print("=== PREVIEWS ===")
    for article in preview:
        print(f"Title: {article['title']}, URL: {article['url']}")

    print("\n=== CONTENT ===")
    for item in content:
        print(f"Paragraphs: {item['paragraph']}")


if __name__ == "__main__":
    main()


