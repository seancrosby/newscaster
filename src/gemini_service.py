import os
import google.generativeai as genai
from typing import List, Dict, Set
import hashlib

class GeminiNewsService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Use a model that supports grounding if available, otherwise just standard generation
        self.model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(self.model_name)
    
    def fetch_summaries(self, config: Dict, history: Set[str]) -> str:
        name = config.get("name")
        preferences = ", ".join(config.get("preferences", []))
        avoid = ", ".join(config.get("avoid", []))
        categories = ", ".join(config.get("categories", ["World", "Nation", "Tech"]))
        
        # History is a set of story identifiers (e.g., titles or hashes)
        # We'll pass them to the prompt to help Gemini avoid repeats
        history_str = "\n".join(list(history)[-50:]) # Send last 50 story IDs to avoid repeats
        
        prompt = f"""
        You are a personalized news assistant for {name}.
        Retrieve and summarize the most important news stories for today.
        
        Categories: {categories}
        Specific Preferences: {preferences}
        STRICTLY AVOID: {avoid}
        
        PREVIOUSLY SENT STORIES (DO NOT REPEAT):
        {history_str}
        
        Please format the news by Category. For each category, include the top relevant stories.
        Each story should have:
        - A concise title
        - A 2-3 sentence summary
        
        Use the Google Search tool to find current, up-to-date news from today.
        """
        
        # Note: Depending on the specific API version/key, the 'tools' parameter 
        # for google_search might vary. We'll use the standard generation for now
        # and assume the model can search if enabled on the backend or 
        # use the 'google_search_retrieval' tool if available.
        
        try:
            # Standard way to enable Google Search grounding
            # We'll try the simplest way first
            response = self.model.generate_content(
                prompt,
                tools=[{'google_search': {}}]
            )
        except Exception as e:
            print(f"Standard google_search tool failed: {e}. Trying fallback...")
            try:
                # Some versions use a different tool name or format
                response = self.model.generate_content(
                    prompt,
                    tools=[{"google_search_retrieval": {}}]
                )
            except Exception as e2:
                print(f"All grounding tools failed: {e2}. Falling back to standard generation.")
                response = self.model.generate_content(prompt)
            
        return response.text

    def extract_story_ids(self, content: str) -> Set[str]:
        # A simple way to extract story identifiers (like titles) from the generated text
        # This is for deduplication. In a more robust system, we'd have structured output.
        # For now, we'll hash the lines that look like titles or just hash the whole response if needed.
        # Let's try to extract titles by looking for bullet points or specific patterns.
        
        ids = set()
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                # Likely a title or a story item
                clean_line = line.lstrip("- *").strip()
                if len(clean_line) > 10: # Avoid very short fragments
                    # Use a hash of the title to keep history small
                    h = hashlib.md5(clean_line.encode()).hexdigest()
                    ids.add(h)
        return ids
