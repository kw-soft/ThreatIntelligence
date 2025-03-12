# Changelog

All significant changes to this project will be documented in this file.

## [v1.1] - 2025-03-12

### Added
- **New Feed Integrations:**  
  Added the following feed modules:
  - `ZDIFeed`
  - `ProjectZeroFeed`
  - `GithubFeed`
  - `CheckPointFeed`
  - `HackerNewsFeed`
  - `BleepingComputerFeed`
  - `MicrosoftFeed`
  - `SchneierFeed`
  - `CVEFeed`
  - `InfostealerFeed`

- **Special Handling for CVEFeed:**  
  The `post_to_discord` function now checks if an entry is from the `CVEFeed` and creates a special embed with an extra severity field, displayed in red.

### Changed
- **Feed Processing Optimization:**  
  Reduced the delay between processing individual feeds from 10 seconds to 1 second to improve the aggregation speed.

- **Refactored Discord Posting:**  
  - Removed posting to the global Discord webhook. Now, entries are posted exclusively through feed-specific webhooks.
  - Updated rate limiting handling: Instead of a maximum of 3 retries, the posting loop will continue retrying until the entry is successfully posted or another error occurs.

- **Documentation and Logging Updates:**  
  Updated module documentation and logging messages to reflect the new features and feeds.

### Removed
- **Global Posting:**  
  Removed functionality for posting entries to a global Discord channel in favor of using only feed-specific channels.

## [v1.0] 

### Initial Release
- Basic RSS Feed Aggregator with the following features:
  - Aggregates feed entries from multiple sources.
  - Ensures each entry is processed only once by maintaining a JSON file with posted entry identifiers.
  - Posts formatted messages to Discord channels using webhooks.
  - Implements basic logging and error handling.
