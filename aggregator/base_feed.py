# aggregator/base_feed.py

class BaseFeed:
    """
    BaseFeed is an abstract class that defines a common interface for RSS feed parsers.
    All subclasses must implement the load() and get_entries() methods.
    """

    def __init__(self, url):
        """
        Initialize the BaseFeed instance with the given URL.
        
        :param url: The URL of the RSS feed to be parsed.
        """
        self.url = url
        self.feed = None

    def load(self):
        """
        Load the RSS feed from the specified URL.
        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the load() method.")

    def get_entries(self):
        """
        Retrieve a list of entries from the RSS feed in a standardized format.
        Each entry should be a dictionary with keys such as 'title', 'pub_date',
        'link', and 'overview'.
        
        This method must be implemented by subclasses.
        
        :return: A list of dictionaries representing feed entries.
        """
        raise NotImplementedError("Subclasses must implement the get_entries() method.")
