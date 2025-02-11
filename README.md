# ThreatFeed HQ - RSS Feed Aggregator for Discord

## 🚀 Join Our Discord Server!

Stay updated with the latest security advisories and news from multiple trusted sources. Our Discord server aggregates real-time threat intelligence from vendors like Sophos, Cisco, and many more.

[**Join ThreatFeed HQ on Discord**](https://discord.gg/BgUCmYP3px)

[<img src="https://discord.com/api/guilds/1337808478613278742/widget.png?style=banner4">](https://discord.gg/BgUCmYP3px)

---

## 📌 About This Project

ThreatFeed HQ is an RSS feed aggregator that collects security-related news and advisories from multiple sources and posts them to designated Discord channels via webhooks. The script ensures:

- Automated retrieval of RSS feeds at a defined interval.
- Chronological sorting of news entries before posting.
- Posting to a global Discord channel and specific vendor-based channels.
- Prevention of duplicate postings via persistent tracking.

## 🛠️ Features

- Support for multiple RSS feeds (e.g., Sophos, Cisco, etc.)
- Posting to Discord webhooks in structured format
- Duplicate detection using persistent JSON storage
- Configurable polling intervals and webhook endpoints
- Logging for debugging and monitoring

## 📥 Installation

### Prerequisites

Ensure you have Python installed (version 3.7+ recommended). You also need:

- `pip install -r requirements.txt` to install dependencies.
- Webhooks set up in your Discord server.

### Clone the Repository

```sh
git clone https://github.com/KW-Soft/ThreatIntelligence.git
cd ThreatIntelligence
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Set Up Webhooks

Obtain your Discord webhooks from server settings and update the `config.py` file.

```python
GLOBAL_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_GLOBAL_WEBHOOK_ID/YOUR_GLOBAL_WEBHOOK_TOKEN"
FEED_DISCORD_WEBHOOKS = {
    "SophosFeed": ["https://discord.com/api/webhooks/YOUR_SOPHOS_WEBHOOK_ID/YOUR_SOPHOS_WEBHOOK_TOKEN"],
    "CiscoFeed": [
        "https://discord.com/api/webhooks/YOUR_CISCO_WEBHOOK_ID/YOUR_CISCO_WEBHOOK_TOKEN",
        "https://discord.com/api/webhooks/ANOTHER_CISCO_WEBHOOK_ID/ANOTHER_CISCO_WEBHOOK_TOKEN"
    ],
}
```

### 2. Run the Aggregator

```sh
python main.py
```

## 📌 Supported Feeds

Currently, the following RSS feeds are integrated:

- **Sophos Security Advisories**
- **Cisco Security News**

More sources can be added easily by creating new feed classes in the `aggregator` module.

## 🤝 Contributing

Want to add more sources or improve the project? Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For any issues or suggestions, feel free to open an issue or join our [**Discord Server**](https://discord.gg/BgUCmYP3px).

