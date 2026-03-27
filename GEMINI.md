# Newscaster: CrewAI-Driven Personalized News Briefs (Ollama Version)

## Project Overview
Newscaster is a CrewAI-powered system designed to fetch, summarize, and deliver personalized daily news briefs. It utilizes a team of specialized agents to automate the end-to-end news pipeline, from initial search to final email delivery, ensuring recipients receive highly relevant and concise information. This version is powered by local LLMs via Ollama.

## Core Mandates
- **Agentic Orchestration:** The system operates as a "Crew" of specialized agents (Collector, Summarizer, Dispatcher) with clear handoffs.
- **Personalization:** All news must be filtered and prioritized based on individual configuration files in `config/`.
- **Deduplication:** Maintain local state (e.g., `data/state.json`) to track previously sent stories and ensure no repetition.
- **Negative Constraints:** Strictly adhere to the "avoid" list provided in each user's configuration file.
- **Execution:** Optimized for manual execution via cron; logs should be clear and concise.

## Agent Definitions
1.  **News Collector:** Responsible for searching and gathering news articles that align with the user's interests and categories while filtering out "avoid" topics.
2.  **News Summarizer:** Takes the gathered articles and synthesizes them into a categorized, high-quality summary report.
3.  **Email Dispatcher:** Formats the final summary into a clean email and handles delivery via SMTP or an email service.

## Architecture & Tech Stack
- **Language:** Python 3.10+
- **Agent Framework:** CrewAI
- **LLM:** Ollama (Local LLM, e.g., Llama 3)
- **Configuration:** Individual JSON/YAML files per user in `config/`.
- **Storage:** Local file-based storage for story hash tracking to prevent duplicates.

## Configuration File Schema
Each file in `config/` should contain:
- `name`: Recipient's name.
- `email`: Recipient's email address.
- `preferences`: List of interested topics or specific keywords.
- `avoid`: List of topics, keywords, or sources to exclude.
- `categories`: The set of high-level categories to include in the report.

## Directory Structure
- `config/`: Recipient configuration files.
- `data/`: Local state and deduplication tracking.
- `src/`: Application source code and Agent definitions.
- `logs/`: Execution logs.
