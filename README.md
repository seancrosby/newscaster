# Newscaster: Personalized AI News Briefs

Daily personalized news summaries from Google Gemini delivered directly to your inbox.

## Features
- **Personalized:** Tailored to individual preferences and categories.
- **Negative Filtering:** Avoids specific topics or sources as configured.
- **Deduplication:** Tracks sent stories to ensure you don't receive the same news twice.
- **Scheduled:** Optimized for running via cron.

## Setup
1.  **Environment Variables:**
    Copy `.env.example` to `.env` and fill in your details:
    ```bash
    cp .env.example .env
    ```
    - `GEMINI_API_KEY`: Your Google AI Studio API key.
    - `EMAIL_USER`: Your SMTP/Gmail address.
    - `EMAIL_PASS`: Your App Password.
    - `SMTP_HOST`: (Optional) Your SMTP server host (defaults to `smtp.gmail.com`).
    - `SMTP_PORT`: (Optional) Your SMTP server port (defaults to `587`).

2.  **Configuration:**
    Create a JSON file in the `config/` directory for each recipient.
    Example `config/jane_doe.json`:
    ```json
    {
      "name": "Jane Doe",
      "email": "jane.doe@example.com",
      "preferences": ["Tech breakthroughs", "Global economics"],
      "avoid": ["Sports", "Celebrity gossip"],
      "categories": ["World", "Tech", "Finance"]
    }
    ```

3.  **Dependencies:**
    Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the script manually:
```bash
python src/main.py
```

### Cron Integration
To automate daily delivery (e.g., every day at 8:00 AM), add a cron job:
```bash
0 8 * * * /usr/bin/python3 /path/to/newscaster/src/main.py >> /path/to/newscaster/logs/cron.log 2>&1
```

## Directory Structure
- `config/`: JSON configuration files for each user.
- `data/`: History files for deduplication.
- `src/`: Python source code.
- `logs/`: Execution and cron logs.
