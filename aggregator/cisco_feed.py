import feedparser
from bs4 import BeautifulSoup
import html
from aggregator.base_feed import BaseFeed

class CiscoFeed(BaseFeed):
    """
    CiscoFeed parses the Cisco Newsroom Security RSS feed.
    
    It extracts relevant details such as the title, publication date, link, author, and an
    "overview" section from the feed's description. The description text is cleaned of
    HTML tags and then truncated to the first 40 words. Additionally, any text starting with 
    "More RSS Feeds:" is removed.
    """

    def load(self):
        """
        Load the RSS feed from the specified URL using feedparser.
        """
        self.feed = feedparser.parse(self.url)

    def get_entries(self):
        """
        Process each entry in the Cisco RSS feed and extract the required fields.
        
        Extraction details:
          - Title
          - Publication date
          - Link
          - Author (defaults to 'Cisco' if not provided by the feed)
          - 'Overview' text: text content from the description field with HTML tags removed.
            The text is truncated to the first 40 words.
          - Any text starting with "More RSS Feeds:" is removed.
        
        :return: A list of dictionaries representing the feed entries.
        """
        entries = []
        for entry in self.feed.entries:
            title = entry.get("title", "No Title")
            pub_date = entry.get("published", "No Date")
            link = entry.get("link", "No Link")
            
            # Set author field. If the feed provides an author, use it; otherwise default to "Cisco"
            author = entry.get("author", "Cisco")
            
            # Retrieve the raw HTML content from the <description> tag.
            description_html = entry.get("description", "")
            # Unescape HTML entities (e.g., &lt; becomes <)
            description_html_unescaped = html.unescape(description_html)
            
            # Parse the HTML using BeautifulSoup to remove HTML tags.
            soup = BeautifulSoup(description_html_unescaped, "html.parser")
            
            # Extract all text from the description.
            overview_text = soup.get_text(separator=" ").strip()
            
            # Remove the unwanted "More RSS Feeds:" section if present.
            if "More RSS Feeds:" in overview_text:
                overview_text = overview_text.split("More RSS Feeds:")[0].strip()
            
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
