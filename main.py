"""
Main Entry Point for the RSS Feed Aggregator

This script aggregates multiple RSS feeds using modules from the aggregator package.
It prints out standardized feed entries and ensures that each entry is processed only once
by maintaining a persistent record of processed entries in a JSON file.
It polls all feeds, aggregates new entries, sorts them by publication date, and posts them 
in chronological order while respecting Discord’s rate limit.
"""

import os
import json
import time
import logging
import requests
from dateutil.parser import parse as parse_date  
from config import GLOBAL_DISCORD_WEBHOOK, FEED_DISCORD_WEBHOOKS

from aggregator.sophos_feed import SophosFeed
from aggregator.cisco_feed import CiscoFeed
from aggregator.zdi_feed import ZDIFeed
from aggregator.projectzero_feed import ProjectZeroFeed
from aggregator.githubsec_feed import GithubFeed
from aggregator.checkpoint_feed import CheckPointFeed
from aggregator.hackernews_feed import HackerNewsFeed
from aggregator.bleepingcomputer_feed import BleepingComputerFeed
from aggregator.microsoft_feed import MicrosoftFeed
from aggregator.schneier_feed import SchneierFeed 
from aggregator.cve_feed import CVEFeed
from aggregator.infostealer_feed import InfostealerFeed

# File used to persist processed entry identifiers (e.g., URLs)
POSTED_FILE = "posted_entries.json"
# Global polling interval for the overall loop (in seconds)
GLOBAL_SLEEP_INTERVAL = 30  # For example, 5 minutes
# Delay between processing individual feeds (in seconds)
DELAY_BETWEEN_FEEDS = 1

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("aggregator.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def load_posted_entries():
    """Loads the set of already processed entry IDs from a JSON file."""
    if os.path.exists(POSTED_FILE):
        try:
            with open(POSTED_FILE, "r", encoding="utf-8") as f:
                posted = json.load(f)
                logging.info(f"Loaded {len(posted)} posted entries.")
                return set(posted)
        except json.JSONDecodeError as e:
            logging.error("Error decoding JSON from posted entries file: %s", e)
            return set()
    logging.info("No posted entries file found. Starting fresh.")
    return set()


def save_posted_entries(posted_entries):
    """Saves the set of processed entry IDs to a JSON file."""
    try:
        with open(POSTED_FILE, "w", encoding="utf-8") as f:
            json.dump(list(posted_entries), f, indent=2)
        logging.info("Successfully saved %d posted entries.", len(posted_entries))
    except Exception as e:
        logging.error("Failed to save posted entries: %s", e)


def post_to_discord(entry, webhook_urls):
    """
    Sends a structured message to Discord using embeds while respecting rate limits.
    If the entry is from the CVEFeed, an additional severity line is included in the embed.

    :param entry: Dictionary containing feed entry data.
    :param webhook_urls: List (or single string) of Discord webhook URLs to send the message to.
    """
    # Check if the entry is from CVEFeed
    if entry.get("feed_type") == "CVEFeed":
        
        embed = {
            "title": entry["title"],
            "url": entry["link"],
            "description": (
                f"**Published on:** {entry['pub_date']}\n"
                f"**Author:** {entry['author']}\n\n"
                f"**Severity:** {entry['severity']}\n\n"
                f"**Overview:** {entry['overview']}..."
            ),
            "color": 0xff0000  # Red color for CVE alerts
        }
    else:
        embed = {
            "title": entry["title"],
            "url": entry["link"],
            "description": (
                f"**Published on:** {entry['pub_date']}\n"
                f"**Author:** {entry['author']}\n\n"
                f"**Overview:** {entry['overview']}..."
            ),
            "color": 0x007bff  # Blue color for regular feeds
        }

    payload = {
        "username": "ThreatFeed HQ",
        "embeds": [embed]
    }

    # Ensure webhook_urls is a list
    if not isinstance(webhook_urls, list):
        webhook_urls = [webhook_urls]

    for url in webhook_urls:
        while True:  # retry if rate limit is reached
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 204:
                    logging.info("Successfully posted to Discord via webhook: %s", url)
                    break  
                elif response.status_code == 429:  # Rate Limit Error
                    retry_after = response.json().get("retry_after", 1)  # wait 1 second
                    logging.warning(f"Rate limit hit! Waiting {retry_after} seconds...")
                    time.sleep(retry_after)  # wait for next try
                else:
                    logging.error("Discord webhook returned status %s: %s", response.status_code, response.text)
                    break  

            except Exception as e:
                logging.error("Error posting to Discord: %s", e)
                break  


def aggregate_new_entries(posted_entries):
    """
    Aggregates new entries from all configured feeds into a single list.
    Each new entry is augmented with its feed type for later channel-specific posting.

    :param posted_entries: A set of already processed entry IDs.
    :return: A list of new entry dictionaries.
    """
    new_entries = []
    # List of feed instances to process.
    feeds = [
        SophosFeed("https://www.sophos.com/de-de/security-advisories/feed"),
        CiscoFeed("https://newsroom.cisco.com/c/services/i/servlets/newsroom/rssfeed.json?feed=security"),
        ZDIFeed("https://www.zerodayinitiative.com/rss/published/"),
        ProjectZeroFeed("https://googleprojectzero.blogspot.com/feeds/posts/default"),
        GithubFeed("https://github.com/security-advisories"),
        CheckPointFeed("https://research.checkpoint.com/feed/"),
        HackerNewsFeed("https://feeds.feedburner.com/TheHackersNews/"),
        BleepingComputerFeed("https://www.bleepingcomputer.com/feed/"),
        MicrosoftFeed("https://msrc.microsoft.com/blog/feed/"),
        SchneierFeed("https://www.schneier.com/feed/atom/"),
        CVEFeed("https://cvefeed.io/rssfeed/latest.xml"),
        InfostealerFeed("https://www.infostealers.com/learn-info-stealers/feed/")
        
    ]

    for feed_instance in feeds:
        try:
            feed_instance.load()
            logging.info("Loaded feed from URL: %s", feed_instance.url)
        except Exception as e:
            logging.error("Error loading feed from URL %s: %s", feed_instance.url, e)
            continue

        try:
            entries = feed_instance.get_entries()
        except Exception as e:
            logging.error("Error processing entries for feed %s: %s", feed_instance.url, e)
            continue

        for entry in entries:
            entry_id = entry.get("link", "")
            if entry_id and entry_id not in posted_entries:
                entry["feed_type"] = feed_instance.__class__.__name__
                new_entries.append(entry)

        logging.info("Waiting %d seconds before processing the next feed...", DELAY_BETWEEN_FEEDS)
        time.sleep(DELAY_BETWEEN_FEEDS)

    return new_entries


def main():
    """
    Main function that aggregates new entries from all feeds, sorts them by publication date,
    and pushes them to Discord in chronological order while respecting rate limits.
    """
    logging.info("RSS Feed Aggregator started.")
    while True:
        logging.info("Starting feed polling cycle")
        posted_entries = load_posted_entries()

        # Aggregate new entries from all feeds.
        new_entries = aggregate_new_entries(posted_entries)
        logging.info("Aggregated %d new entries from all feeds.", len(new_entries))

        # Sort new entries by publication date (oldest first)
        try:
            new_entries.sort(key=lambda e: parse_date(e.get("pub_date", "")))
        except Exception as e:
            logging.error("Error sorting entries by publication date: %s", e)

        # Process sorted new entries.
        for entry in new_entries:
            
            

            # Post to feed-specific Discord channels
            feed_type = entry.get("feed_type", "")
            if feed_type in FEED_DISCORD_WEBHOOKS:
                post_to_discord(entry, FEED_DISCORD_WEBHOOKS[feed_type])
                
            # Mark this entry as processed.
            posted_entries.add(entry.get("link", ""))

        # Save the updated processed entries.
        save_posted_entries(posted_entries)
        logging.info("Global cycle completed. Sleeping for %d seconds...", GLOBAL_SLEEP_INTERVAL)
        time.sleep(GLOBAL_SLEEP_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Aggregator stopped by user.")
