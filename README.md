# Smart Support Bot

An automated ETL pipeline that scrapes Zendesk help articles, converts them to Markdown, and syncs them to an OpenAI Vector Store to power an AI support assistant.

---

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/nameTun/smart-support-bot.git
   cd smart-support-bot
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.sample .env
   ```
   Then open `.env` and fill in your credentials:
   ```
   OPENAI_API_KEY=sk-...
   ZENDESK_API_URL=https://support.optisigns.com/api/v2/help_center/en-us/articles.json
   ```

---

## Run Locally

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

The pipeline will:
1. Scrape articles from the Zendesk API
2. Detect new/updated articles (delta sync via `updated_at`)
3. Upload only the delta to the OpenAI Vector Store
4. Log a summary: `Added: X | Updated: Y | Skipped: Z`

---

## Run with Docker

```bash
docker build -t smart-support-bot .
docker run --rm \
  -e OPENAI_API_KEY=your_key_here \
  -e ZENDESK_API_URL=https://support.optisigns.com/api/v2/help_center/en-us/articles.json \
  smart-support-bot
```

---

## CI/CD — Daily Automated Sync

The bot runs automatically every day at **00:00 UTC** via GitHub Actions.

📋 **Job Logs:** [View latest workflow run](https://github.com/nameTun/smart-support-bot/actions)

To add the required secrets, go to: **GitHub repo → Settings → Secrets and variables → Actions**
- `OPENAI_API_KEY`
- `ZENDESK_API_URL`

---

## Demo

**Pipeline running — 30 articles scraped & uploaded to OpenAI Vector Store:**

![Pipeline Output](./docs/Screenshot%202026-07-04%20at%2019.12.40.png)

**Vector Store on OpenAI Dashboard — 30 files synced successfully:**

![OpenAI Vector Store](./docs/Screenshot%202026-07-04%20at%2019.14.46.png)
