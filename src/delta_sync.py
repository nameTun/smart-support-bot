import os
import json

STATE_FILE = "sync_state.json"

def process_delta(scraped_articles):
    """
    Compare the scraped articles with the state saved in sync_state.json
    to classify them as Added, Updated, or Skipped.
    """
    project_root = os.path.dirname(os.path.dirname(__file__))
    state_path = os.path.join(project_root, STATE_FILE)

    # Read the old state file if it exists
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            try:
                state = json.load(f)
            except json.JSONDecodeError:
                state = {}
    else:
        state = {}

    added = []
    updated = []
    skipped = []

    for article in scraped_articles:
        article_id = str(article["id"])
        updated_at = article.get("updated_at")

        if article_id not in state:
            added.append(article_id)
            state[article_id] = {
                "updated_at": updated_at,
                "gemini_file_name": ""
            }
        else:
            # Compare timestamps
            old_updated_at = state[article_id].get("updated_at")
            if updated_at != old_updated_at:
                updated.append(article_id)
                state[article_id]["updated_at"] = updated_at
                # Keep gemini_file_name for Step 4 to delete the old file
            else:
                skipped.append(article_id)

    # Write the new state
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

    # Print the report
    print(f"=> Delta Sync Result: Added: {len(added)} | Updated: {len(updated)} | Skipped: {len(skipped)}")
    
    return {
        "added": added,
        "updated": updated,
        "skipped": skipped,
        "state_path": state_path
    }

if __name__ == "__main__":
    # Quick test using mock data
    test_data = [
        {"id": "1", "updated_at": "2024-05-12T10:00:00Z"},
        {"id": "2", "updated_at": "2024-05-12T10:00:00Z"}
    ]
    process_delta(test_data)
