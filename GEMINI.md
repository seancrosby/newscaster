# Newscaster: AI-Driven Personalized News Briefs

## Project Overview
Newscaster is a Python-based utility designed to fetch, categorize, and summarize daily news using Google Gemini, then deliver personalized briefs to recipients via email. It is designed to run as a scheduled task (cron).

## Core Mandates
- **Personalization:** All news must be filtered and prioritized based on individual configuration files located in the `config/` directory.
- **Deduplication:** The system must maintain a local state (e.g., `state.json` or a SQLite database) to track previously sent stories and ensure no repetition across sessions.
- **Categorization:** News must be organized into high-level topics: World, Nation, Tech, etc.
- **Negative Constraints:** Strictly adhere to the "avoid" list provided in each user's configuration file.
- **Execution:** Optimized for manual execution via cron; logs should be clear and concise.

## Architecture & Tech Stack
- **Language:** Python 3.10+
- **LLM:** Google Gemini API (via `google-generativeai` package)
- **Configuration:** Individual JSON or YAML files per user in `config/`.
- **Email Delivery:** SMTP (Standard Library `smtplib`) or a preferred mail service.
- **Storage:** Local file-based storage for story hash tracking to prevent duplicates.

## Configuration File Schema
Each file in `config/` (e.g., `config/john_doe.json`) should contain:
- `name`: Recipient's name.
- `email`: Recipient's email address.
- `preferences`: List of interested topics or specific keywords.
- `avoid`: List of topics, keywords, or sources to exclude.
- `categories`: The set of high-level categories to include in the report.

## Directory Structure
- `config/`: Recipient configuration files.
- `data/`: Local state and deduplication tracking.
- `src/`: Application source code.
- `logs/`: Execution logs.
