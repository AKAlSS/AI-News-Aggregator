import schedule
import time
from datetime import datetime
from collectors.rss_collector import collect_rss_feeds
from collectors.twitter_collector import collect_tweets
from processors.summarizer import summarize_texts
from presenters.notion_presenter import create_notion_page
from config import RSS_FEEDS, TWITTER_LIST_ID

def main():
    print(f"Running digest creation at {datetime.now()}")
    
    # Collect data
    rss_data = collect_rss_feeds(RSS_FEEDS)
    twitter_data = collect_tweets(TWITTER_LIST_ID, max_tweets=10)
    
    # Combine and summarize data
    all_data = rss_data + twitter_data
    summarized_data = summarize_texts(all_data)
    
    # Create Notion page
    create_notion_page(f"AI News Digest - {datetime.now().strftime('%Y-%m-%d')}", summarized_data)
    
    print(f"Daily digest created successfully! Twitter API calls: {len(twitter_data)}")

if __name__ == "__main__":
    # Run once immediately
    main()
    
    # Then schedule daily runs
    schedule.every().day.at("08:00").do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Sleep for an hour between checks