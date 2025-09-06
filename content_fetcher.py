import requests
from bs4 import BeautifulSoup

class ContentFetcher:
    """Fetch HTML content by URL and return cleaned text free of navigation and noise."""

    def fetch(self, url: str) -> tuple[str, str]:
        """Return cleaned HTML and extracted text for the given URL."""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        for tag in ["script", "style", "nav", "header", "footer", "aside"]:
            for element in soup.find_all(tag):
                element.decompose()
        clean_html = str(soup)
        text = soup.get_text(separator=" ", strip=True)
        return clean_html, text
