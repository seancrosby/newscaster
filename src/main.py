import os
import sys
from dotenv import load_dotenv

from config_loader import load_configs
from storage import HistoryStore
from crew_service import NewscasterCrew

def main():
    # Load environment variables
    load_dotenv()
    
    # Email credentials are used inside the Crew tools
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_PASS")
    
    if not all([email_user, email_pass]):
        print("Error: Missing required environment variables (EMAIL_USER, EMAIL_PASS).")
        sys.exit(1)
    
    # Initialize services
    configs = load_configs()
    store = HistoryStore()
    crew_service = NewscasterCrew()
    
    if not configs:
        print("No configurations found in config/ directory.")
        return
    
    print(f"Starting Newscaster Crew (Ollama) for {len(configs)} recipients...")
    
    for config in configs:
        name = config.get("name", "User")
        email = config.get("email")
        file_name = config.get("file_name")
        
        if not email:
            print(f"Skipping {name} due to missing email address.")
            continue
            
        print(f"\n--- Processing news for {name} ({email}) ---")
        
        # 1. Load history for deduplication
        history = store.load_history(file_name)
        
        # 2. Run the Crew AI process
        try:
            news_content, success = crew_service.run(config, history)
            
            if success:
                # 3. Extract new story IDs and update history
                new_story_ids = crew_service.extract_story_ids(news_content)
                updated_history = history.union(new_story_ids)
                
                # 4. Save history
                store.save_history(file_name, updated_history)
                print(f"Successfully processed {name}.")
            else:
                print(f"Crew failed to successfully dispatch email for {name}.")
                
        except Exception as e:
            print(f"An error occurred while running the crew for {name}: {e}")

if __name__ == "__main__":
    main()
