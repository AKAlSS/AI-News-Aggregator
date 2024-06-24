import schedule
import time
from collectors.rss_collector import collect_rss_feeds
from collectors.twitter_collector import collect_tweets
from processors.summarizer import summarize_texts
from presenters.notion_presenter import create_notion_page
from config import RSS_FEEDS, TWITTER_LIST_ID

def main():
    # Collect data
    rss_data = collect_rss_feeds(RSS_FEEDS)
    twitter_data = collect_tweets(TWITTER_LIST_ID)
    
    # Combine and summarize data
    all_data = rss_data + twitter_data
    summarized_data = summarize_texts(all_data)
    
    # Create Notion page
    create_notion_page("AI News Digest", summarized_data)
    
    print("Daily digest created successfully!")

if __name__ == "__main__":
    schedule.every().day.at("08:00").do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(60)