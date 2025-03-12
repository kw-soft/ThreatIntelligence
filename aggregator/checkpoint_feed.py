import feedparser
from bs4 import BeautifulSoup
import html
from aggregator.base_feed import BaseFeed

class CheckPointFeed(BaseFeed):
    """
    CheckPoint_Feed parses the Checkpoint RSS feed.

    It extracts:
      - Title
      - Publication date
      - Link
      - Author (always "Zero Day Initiative")
      - Overview text, cleaned of HTML and truncated to the first 40 words.
    """

    def load(self):
        """
        Load the RSS feed from the specified URL using feedparser.
        """
        self.feed = feedparser.parse(self.url)

    def get_entries(self):
        """
        Process each entry in the ZDI RSS feed and extract the required fields.

        :return: A list of dictionaries representing the feed entries.
        """
        entries = []
        for entry in self.feed.entries:
            title = entry.get("title", "No Title")
            pub_date = entry.get("published", "No Date")
            link = entry.get("link", "No Link")
            author = "Checkpoint Research"

            # Retrieve and clean the description field
            description_html = entry.get("description", "")
            description_html_unescaped = html.unescape(description_html)
            soup = BeautifulSoup(description_html_unescaped, "html.parser")
            overview_text = soup.get_text(separator=" ").strip()

            # Remove CDATA markers (if any)
            overview_text = overview_text.replace("<![CDATA[", "").replace("]]>", "")

            # Limit the overview text to the first 40 words.
            words = overview_text.split()
            overview_limited = " ".join(words[:40])

            entries.append({
                "title": title,
                "pub_date": pub_date,
                "link": link,
                "author": author,
                "overview": overview_limited
            })

        return entries
