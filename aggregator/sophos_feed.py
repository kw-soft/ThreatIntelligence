# aggregator/sophos_feed.py

import feedparser
from bs4 import BeautifulSoup
import html
from aggregator.base_feed import BaseFeed

class SophosFeed(BaseFeed):
    """
    SophosFeed parses the Sophos Security Advisory RSS feed.
    
    It extracts relevant details such as title, publication date, link, and an
    "overview" section extracted from the advisory summary. The overview is truncated
    to the first 40 words.
    """

    def load(self):
        """
        Load the RSS feed from the specified URL using feedparser.
        """
        self.feed = feedparser.parse(self.url)

    def get_entries(self):
        """
        Process each entry in the RSS feed and extract the required fields.
        
        Extraction details:
          - Title
          - Publication date
          - Link
          - 'Overview' text: extracted from the advisory summary container.
            The overview is truncated to the first 40 words.
        
        :return: A list of dictionaries representing the feed entries.
        """
        entries = []
        for entry in self.feed.entries:
            title = entry.get("title", "No Title")
            pub_date = entry.get("published", "No Date")
            link = entry.get("link", "No Link")
            author = entry.get("author", "Sophos")
            
            # Retrieve the raw HTML content from the <description> tag and unescape HTML entities.
            description_html = entry.get("description", "")
            description_html_unescaped = html.unescape(description_html)
            
            # Parse the unescaped HTML using BeautifulSoup.
            soup = BeautifulSoup(description_html_unescaped, "html.parser")
            
            # Attempt to extract the advisory summary container that holds the "Overview" section.
            summary_div = soup.select_one("div.field--name-field-advisory-summary div.field__item")
            overview_text = ""
            if summary_div:
                # Find the <h2> element containing the word "Overview".
                overview_header = summary_div.find("h2", string=lambda t: t and "Overview" in t)
                if overview_header:
                    overview_parts = []
                    # Collect all sibling elements following the "Overview" header until a new <h2> is encountered.
                    for sibling in overview_header.find_next_siblings():
                        if sibling.name == "h2":
                            break
                        overview_parts.append(sibling.get_text(" ", strip=True))
                    overview_text = "\n".join(overview_parts).strip()
                else:
                    # Fallback: Use the entire text content of the summary container.
                    overview_text = summary_div.get_text(separator="\n").strip()
            else:
                # Fallback: Use the full text content of the description.
                overview_text = soup.get_text(separator="\n").strip()
            
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
