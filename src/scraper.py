import os
import requests
from markdownify import markdownify as md
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

ZENDESK_API_URL = os.getenv("ZENDESK_API_URL")

def fetch_articles():
    if not ZENDESK_API_URL:
        print("Error: ZENDESK_API_URL is not set in the environment variables.")
        return

    # Ensure articles directory exists in the root of the project
    project_root = os.path.dirname(os.path.dirname(__file__))
    articles_dir = os.path.join(project_root, "articles")
    os.makedirs(articles_dir, exist_ok=True)

    url = ZENDESK_API_URL
    total_fetched = 0
    scraped_data = []

    print(f"Starting to fetch articles from {ZENDESK_API_URL}...")

    while url:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            break

        data = response.json()
        articles = data.get("articles", [])

        for article in articles:
            article_id = str(article.get("id"))
            title = article.get("title", "Untitled")
            body_html = article.get("body") or ""
            updated_at = article.get("updated_at")

            # Convert HTML to Markdown
            # Default markdownify keeps links, headings, and code blocks.
            markdown_body = md(body_html, heading_style="ATX")

            # Combine Title (H1) with the markdown body
            final_content = f"# {title}\n\n{markdown_body}"

            # Save to articles/{id}.md
            file_path = os.path.join(articles_dir, f"{article_id}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)

            scraped_data.append({
                "id": article_id,
                "updated_at": updated_at
            })
            total_fetched += 1

        # Pagination
        url = data.get("next_page")
        print(f"Fetched {len(articles)} articles from this page. Total so far: {total_fetched}")

    print(f"Finished scraping! Total articles saved to '{articles_dir}': {total_fetched}")
    return scraped_data

if __name__ == "__main__":
    fetch_articles()
