"""
Configuration for Discord Webhooks used by the RSS Feed Aggregator.

This file contains sensitive information and should be excluded from version control
(e.g., added to .gitignore).

GLOBAL_DISCORD_WEBHOOK:
    The webhook URL for the global Discord channel where all feed entries will be posted.
    
FEED_DISCORD_WEBHOOKS:
    A dictionary mapping feed type identifiers (typically the class name of the feed module)
    to a list of Discord webhook URLs. This allows you to post the same entry to multiple channels.
    
    For example, if you want Cisco feed entries to appear in two separate channels, include both webhook
    URLs in the list for the "CiscoFeed" key.
    
Usage:
    In your aggregator code, import these variables:
        from config import GLOBAL_DISCORD_WEBHOOK, FEED_DISCORD_WEBHOOKS
"""

# Global Discord webhook URL for the global channel (e.g., "News").
GLOBAL_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"  # vendor-sec

# Feed-specific Discord webhooks.
# Each key corresponds to a feed type (e.g., "SophosFeed", "CiscoFeed").
# The associated value is a list of webhook URLs. Multiple webhooks allow posting the same entry
# to different Discord channels.
FEED_DISCORD_WEBHOOKS = {
    "SophosFeed": [
        "https://discord.com/api/webhooks/YOUR_SOPHOS_WEBHOOK_ID/YOUR_SOPHOS_WEBHOOK_TOKEN",  # sophos
        "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"  # global-news
    ],
    "CiscoFeed": [
        "https://discord.com/api/webhooks/YOUR_CISCO_WEBHOOK_ID/YOUR_CISCO_WEBHOOK_TOKEN",  # cisco
        "https://discord.com/api/webhooks/YOUR_THREAT_INTEL_WEBHOOK_ID/YOUR_THREAT_INTEL_WEBHOOK_TOKEN",  # threat-intel
        "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"  # global-news
    ],
    "ZDIFeed": [
        "https://discord.com/api/webhooks/YOUR_ZDI_WEBHOOK_ID/YOUR_ZDI_WEBHOOK_TOKEN",  # exploits
        "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"  # global-news
    ],
    "ProjectZeroFeed": [
        "https://discord.com/api/webhooks/YOUR_PROJECT_ZERO_WEBHOOK_ID/YOUR_PROJECT_ZERO_WEBHOOK_TOKEN"  # exploits
    ],
    "GithubFeed": [
        "https://discord.com/api/webhooks/YOUR_GITHUB_WEBHOOK_ID/YOUR_GITHUB_WEBHOOK_TOKEN"  # github-sec
    ],
    "CheckPointFeed": [
        "https://discord.com/api/webhooks/YOUR_CHECKPOINT_WEBHOOK_ID/YOUR_CHECKPOINT_WEBHOOK_TOKEN",  # exploits
        "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"  # global-news
    ],
    "HackerNewsFeed": [
        "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN",  # global-news
        "https://discord.com/api/webhooks/YOUR_THREAT_INTEL_WEBHOOK_ID/YOUR_THREAT_INTEL_WEBHOOK_TOKEN",  # threat-intel
        "https://discord.com/api/webhooks/YOUR_EXPLOITS_WEBHOOK_ID/YOUR_EXPLOITS_WEBHOOK_TOKEN"  # exploits
    ],
    "BleepingComputerFeed": [
        "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"  # global-news
    ],
    "MicrosoftFeed": [
        "https://discord.com/api/webhooks/YOUR_MICROSOFT_WEBHOOK_ID/YOUR_MICROSOFT_WEBHOOK_TOKEN",  # microsoft
        "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"  # global-news
    ],
    "SchneierFeed": [
        "https://discord.com/api/webhooks/YOUR_RESEARCH_WEBHOOK_ID/YOUR_RESEARCH_WEBHOOK_TOKEN",  # Research
        "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"  # global-news
    ],
    "CVEFeed": [
        "https://discord.com/api/webhooks/YOUR_RESEARCH_WEBHOOK_ID/YOUR_RESEARCH_WEBHOOK_TOKEN"  # Research
    ],
    # Add additional feed-specific webhooks as needed.
}
