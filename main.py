import os
from dotenv import load_dotenv
from scraper import fetch_articles
# pyrefly: ignore [missing-import]
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
        # pyrefly: ignore [missing-import]
        from openai_service import sync_to_openai
        sync_to_openai(delta_result)
    else:
        print("No data fetched. Pipeline stopped.")

if __name__ == "__main__":
    main()
