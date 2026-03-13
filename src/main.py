import os
import sys
import datetime
from dotenv import load_dotenv

from config_loader import load_configs
from storage import HistoryStore
from gemini_service import GeminiNewsService
from email_service import EmailService

def main():
    # Load environment variables
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_PASS")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    
    if not all([api_key, email_user, email_pass]):
        print("Error: Missing required environment variables. Please check .env.")
        sys.exit(1)
    
    # Initialize services
    configs = load_configs()
    store = HistoryStore()
    gemini = GeminiNewsService(api_key)
    emailer = EmailService(email_user, email_pass, smtp_host, smtp_port)
    
    if not configs:
        print("No configurations found in config/ directory.")
        return
    
    print(f"Starting newscaster for {len(configs)} recipients...")
    
    for config in configs:
        name = config.get("name", "User")
        email = config.get("email")
        file_name = config.get("file_name")
        
        if not email:
            print(f"Skipping {name} due to missing email address.")
            continue
            
        print(f"Processing news for {name} ({email})...")
        
        # 1. Load history for deduplication
        history = store.load_history(file_name)
        
        # 2. Get news summaries from Gemini
        news_content = gemini.fetch_summaries(config, history)
        
        if not news_content:
            print(f"Failed to generate news for {name}.")
            continue
            
        # 3. Extract new story IDs and update history
        new_story_ids = gemini.extract_story_ids(news_content)
        updated_history = history.union(new_story_ids)
        
        # 4. Send the email
        today = datetime.date.today().strftime("%B %d, %Y")
        subject = f"Your Daily News Brief - {today}"
        
        # Prepend a personalized greeting
        full_content = f"# Hello {name},\n\nHere is your personalized news for {today}.\n\n{news_content}"
        
        if emailer.send_brief(email, subject, full_content):
            # 5. Only save history if the email was successfully sent
            store.save_history(file_name, updated_history)
            print(f"Successfully processed {name}.")
        else:
            print(f"Failed to process {name} due to email error.")

if __name__ == "__main__":
    main()
