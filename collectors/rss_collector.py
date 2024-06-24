import feedparser
import requests
from bs4 import BeautifulSoup

def parse_rss(feed_url):
    """Parse the RSS feed and return the entries."""
    feed = feedparser.parse(feed_url)
    return feed.entries

def scrape_website(url):
    """Scrape the website for content when RSS feed is not available."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')  # Adjust tag as per the website's structure
    titles = [article.find('h2').text for article in articles if article.find('h2')]  # Adjust tag as needed
    return titles

def collect_data(feed_urls):
    """Collect data from either RSS or by scraping."""
    all_data = []
    for url in feed_urls:
        try:
            # Attempt to parse the RSS feed first
            entries = parse_rss(url)
            all_data.extend(entries)
        except Exception as e:
            print(f"Failed to parse RSS for {url}, attempting to scrape. Error: {e}")
            # If RSS parsing fails, attempt to scrape
            try:
                titles = scrape_website(url)
                all_data.extend(titles)
            except Exception as e:
                print(f"Failed to scrape {url}. Error: {e}")
    return all_data

# List of URLs to collect data from
RSS_FEEDS = [
    "https://ai.googleblog.com",  # Assuming direct scraping needed
    "https://openai.com/blog/rss.xml",
    "https://blogs.microsoft.com/ai",  # Assuming direct scraping needed
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://venturebeat.com/category/ai/feed/"
]

data_collected = collect_data(RSS_FEEDS)
for data in data_collected:
    print(data)
