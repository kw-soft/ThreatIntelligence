import feedparser
from bs4 import BeautifulSoup
import html
import re
from aggregator.base_feed import BaseFeed

class CVEFeed(BaseFeed):
    """
    CVEFeed parses the CVE feed from cvefeed.io.

    It extracts:
      - Title
      - Publication date
      - Link
      - Author (always "CVEfeed.io")
      - Overview text, cleaned of HTML and truncated to the first 40 words.
      - Severity (extracted from the description, e.g. "3.1 | LOW")
    """

    def load(self):
        self.feed = feedparser.parse(self.url)

    def get_entries(self):
        entries = []
        for entry in self.feed.entries:
            title = entry.get("title", "No Title")
            pub_date = entry.get("published", "No Date")
            link = entry.get("link", "No Link")
            author = "CVEfeed.io"

            # Retrieve and unescape the description field
            description_html = entry.get("description", "")
            description_html_unescaped = html.unescape(description_html).strip()

            # Use BeautifulSoup to remove HTML tags
            soup = BeautifulSoup(description_html_unescaped, "html.parser")
            # Get the plain text from the description
            description_text = soup.get_text(separator=" ", strip=True)
            
            # Use regex to extract severity, e.g. "3.1 | LOW"
            severity_match = re.search(r"Severity:\s*([\d.]+\s*\|\s*\w+)", description_text)
            if severity_match:
                severity_value = severity_match.group(1)
                # Remove the severity text from the description_text so it doesn't appear in the overview
                description_text = re.sub(r"Severity:\s*[\d.]+\s*\|\s*\w+", "", description_text)
            else:
                severity_value = "N/A"

            # Limit the overview text to the first 40 words
            words = description_text.split()
            overview_limited = " ".join(words[:40])

            entries.append({
                "title": title,
                "pub_date": pub_date,
                "link": link,
                "author": author,
                "overview": overview_limited,
                "severity": severity_value
            })

        return entries
