import os
import sys
from dotenv import load_dotenv

# Ensure src modules are importable when running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scraper import fetch_articles
from delta_sync import process_delta

def main():
    load_dotenv()
    print("Starting Smart Support Bot Pipeline...")

    # Step 2: Scrape data from Zendesk
    scraped_data = fetch_articles()

    if scraped_data:
        # Step 3: Filter data using Delta Sync
        delta_result = process_delta(scraped_data)

        # Step 4: Sync to OpenAI Vector Store
        from openai_service import sync_to_openai
        sync_to_openai(delta_result)
    else:
        print("No data fetched. Pipeline stopped.")

if __name__ == "__main__":
    main()
