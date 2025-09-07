from collections import Counter
from bs4 import BeautifulSoup

class StyleAnalyzer:
    """Extract simple stylistic patterns from HTML content."""

    def analyze(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        subheadings = soup.find_all(["h2", "h3"])
        paragraphs = [p.get_text().strip() for p in soup.find_all("p") if p.get_text().strip()]
        avg_par_len = (
            sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        )
        lists = soup.find_all(["ul", "ol"])
        list_frequency = len(lists) / max(len(paragraphs), 1)
        text = " ".join(paragraphs).lower()
        formal_markers = ["sir", "madam", "please", "regards", "dear"]
        informal_markers = ["hey", "hi", "folks", "guys", "cheers"]
        formal_count = sum(text.count(w) for w in formal_markers)
        informal_count = sum(text.count(w) for w in informal_markers)
        tone = "neutral"
        if formal_count > informal_count:
            tone = "formal"
        elif informal_count > formal_count:
            tone = "informal"
        return {
            "has_subheadings": len(subheadings) > 0,
            "avg_paragraph_length": avg_par_len,
            "list_frequency": list_frequency,
            "tone": tone,
        }

    def aggregate(self, analyses: list[dict]) -> dict:
        if not analyses:
            return {
                "has_subheadings": False,
                "avg_paragraph_length": 0,
                "list_frequency": 0,
                "tone": "neutral",
            }
        has_subheadings = any(a["has_subheadings"] for a in analyses)
        avg_paragraph_length = sum(a["avg_paragraph_length"] for a in analyses) / len(analyses)
        list_frequency = sum(a["list_frequency"] for a in analyses) / len(analyses)
        tone_counts = Counter(a["tone"] for a in analyses)
        tone = tone_counts.most_common(1)[0][0]
        return {
            "has_subheadings": has_subheadings,
            "avg_paragraph_length": avg_paragraph_length,
            "list_frequency": list_frequency,
            "tone": tone,
        }
