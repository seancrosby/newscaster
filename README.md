# Newscaster: CrewAI-Powered Personalized News Briefs (Ollama)

Daily personalized news summaries delivered by a specialized team of AI agents, powered by local LLMs via Ollama.

## Features
- **Agentic Pipeline:** Specialized CrewAI agents for news collection, summarization, and email dispatch.
- **Local LLM:** Powered by Ollama for privacy and offline capability.
- **Personalized:** Tailored to individual preferences and categories for each recipient.
- **Negative Filtering:** Strictly avoids topics or sources as specified in each user's "avoid" list.
- **Deduplication:** Maintains persistent state to ensure you never receive the same story twice.

## Setup
1.  **Ollama:**
    Ensure you have [Ollama](https://ollama.com/) installed and running. Pull the desired model (e.g., `llama3`):
    ```bash
    ollama pull llama3
    ```

2.  **Environment Variables:**
    Copy `.env.example` to `.env` and fill in your details:
    ```bash
    cp .env.example .env
    ```
    - `OLLAMA_MODEL`: The model name (defaults to `llama3`).
    - `OLLAMA_BASE_URL`: The URL for your Ollama instance (defaults to `http://localhost:11434`).
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
