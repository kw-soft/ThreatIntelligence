import feedparser
from bs4 import BeautifulSoup
import html
import logging
from aggregator.base_feed import BaseFeed

class GithubFeed(BaseFeed):
    """
    GithubFeed parses the GitHub Security Advisory RSS feed.

    It extracts:
      - Title
      - Publication date
      - Link (converted if needed)
      - Author (always "GitHub Security")
      - Overview text, cleaned of HTML and truncated to the first 40 words.
    """

    def load(self):
        """
        Load the RSS feed from the specified URL using feedparser.
        """
        self.feed = feedparser.parse(self.url)

    def extract_github_advisory_url(self, tag_uri):
        """
        Converts a GitHub tag URI into a valid GitHub Security Advisory URL.

        Example:
            Input: 'tag:github.com,2008:GHSA-3rmv-2pg5-xvqj'
            Output: 'https://github.com/advisories/GHSA-3rmv-2pg5-xvqj'

        :param tag_uri: The original tag string.
        :return: The corrected GitHub Advisory URL or None if invalid.
        """
        if tag_uri.startswith("tag:github.com") and "GHSA-" in tag_uri:
            ghsa_id = tag_uri.split(":")[-1]  # Extract 'GHSA-3rmv-2pg5-xvqj'
            return f"https://github.com/advisories/{ghsa_id}"
        return tag_uri  # Return original if it's already a valid URL

    def get_entries(self):
        """
        Process each entry in the GitHub Security RSS feed and extract the required fields.

        :return: A list of dictionaries representing the feed entries.
        """
        entries = []
        for entry in self.feed.entries:
            title = entry.get("title", "No Title")
            pub_date = entry.get("published", "No Date")
            link = entry.get("link", "No Link")
            author = "GitHub Security"  # Fixed typo

            # Convert tag URI to actual GitHub Advisory URL
            link = self.extract_github_advisory_url(link)

            # Retrieve and clean the description field
            description_html = entry.get("description", "No description available")
            description_html_unescaped = html.unescape(description_html)
            soup = BeautifulSoup(description_html_unescaped, "html.parser")
            overview_text = soup.get_text(separator=" ").strip()

            # Limit the overview text to the first 40 words (without cutting words in half)
            words = overview_text.split()
            overview_limited = " ".join(words[:40])

            entry_data = {
                "title": title,
                "pub_date": pub_date,
                "link": link,
                "author": author,
                "overview": overview_limited
            }

            
            entries.append(entry_data)

        return entries
