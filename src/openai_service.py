import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def sync_to_openai(delta_result):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is not set in .env")
        return

    client = OpenAI(api_key=api_key)

    project_root = os.path.dirname(os.path.dirname(__file__))
    state_path = os.path.join(project_root, "sync_state.json")
    articles_dir = os.path.join(project_root, "articles")

    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)

    # 1. Manage Global Vector Store ID
    global_state = state.get("_global_", {})
    vector_store_id = global_state.get("vector_store_id")

    if not vector_store_id:
        print("Creating a new Vector Store on OpenAI...")
        vs = client.vector_stores.create(name="OptiSigns Knowledge Base")
        vector_store_id = vs.id
        global_state["vector_store_id"] = vector_store_id
        state["_global_"] = global_state
    else:
        print(f"Using existing Vector Store: {vector_store_id}")

    added_count = 0
    updated_count = 0

    print("Syncing 'Added' articles to OpenAI...")
    for article_id in delta_result.get("added", []):
        file_path = os.path.join(articles_dir, f"{article_id}.md")
        if os.path.exists(file_path):
            try:
                # Upload file to OpenAI
                with open(file_path, "rb") as f:
                    uploaded_file = client.files.create(file=f, purpose="assistants")
                
                # Attach to Vector Store
                client.vector_stores.files.create(
                    vector_store_id=vector_store_id, 
                    file_id=uploaded_file.id
                )
                
                state[article_id] = state.get(article_id, {})
                state[article_id]["openai_file_id"] = uploaded_file.id
                added_count += 1
                print(f"Uploaded {added_count}/{len(delta_result.get('added', []))} (Added): {article_id}")
                
            except Exception as e:
                print(f"Error uploading {article_id}: {e}")

    print("Syncing 'Updated' articles to OpenAI...")
    for article_id in delta_result.get("updated", []):
        file_path = os.path.join(articles_dir, f"{article_id}.md")
        old_file_id = state.get(article_id, {}).get("openai_file_id")
        
        if old_file_id:
            try:
                # Delete old file from OpenAI
                client.files.delete(file_id=old_file_id)
            except Exception as e:
                print(f"Warning: Could not delete old file {old_file_id}: {e}")
        
        if os.path.exists(file_path):
            try:
                # Upload new file
                with open(file_path, "rb") as f:
                    uploaded_file = client.files.create(file=f, purpose="assistants")
                
                # Attach to Vector Store
                client.vector_stores.files.create(
                    vector_store_id=vector_store_id, 
                    file_id=uploaded_file.id
                )
                
                state[article_id]["openai_file_id"] = uploaded_file.id
                updated_count += 1
                print(f"Uploaded {updated_count}/{len(delta_result.get('updated', []))} (Updated): {article_id}")
            except Exception as e:
                print(f"Error uploading {article_id}: {e}")

    # Write new state back to disk
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)
        
    print(f"=> OpenAI Sync Complete! Uploaded {added_count} files, Replaced {updated_count} files.")
    print(f"   Check your Vector Store on OpenAI Dashboard: {vector_store_id}")
