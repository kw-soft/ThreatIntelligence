import feedparser
from bs4 import BeautifulSoup
import html
from aggregator.base_feed import BaseFeed

class MicrosoftFeed(BaseFeed):
    """
    MicrosoftFeed parses the Microsoft Security Response Center RSS feed.

    It extracts:
      - Title
      - Publication date
      - Link
      - Author (always "Microsoft")
      - Overview text, cleaned of HTML (if present) and truncated to the first 40 words.
    """

    def load(self):
        """
        Load the RSS feed from the specified URL using feedparser.
        """
        self.feed = feedparser.parse(self.url)

    def get_entries(self):
        """
        Process each entry in the Microsoft Security RSS feed and extract the required fields.

        :return: A list of dictionaries representing the feed entries.
        """
        entries = []
        for entry in self.feed.entries:
            title = entry.get("title", "No Title")
            pub_date = entry.get("published", "No Date")
            link = entry.get("link", "No Link")
            author = "Microsoft"

            # Retrieve and unescape the description field
            description_html = entry.get("description", "")
            description_html_unescaped = html.unescape(description_html).strip()

            
            description_html_unescaped = description_html_unescaped.replace("<![CDATA[", "").replace("]]>", "")

            
            stripped = description_html_unescaped.strip()
            if stripped.startswith("<") and stripped.endswith(">"):
                
                soup = BeautifulSoup(description_html_unescaped, "html.parser")
                overview_text = soup.get_text(separator=" ").strip()
            else:
                
                overview_text = description_html_unescaped

            
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
