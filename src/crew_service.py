import os
import hashlib
import datetime
from typing import List, Dict, Set, Any
from crewai import Agent, Task, Crew, Process, LLM
from langchain_community.tools import DuckDuckGoSearchRun

class NewscasterCrew:
    def __init__(self):
        # Use CrewAI's native LLM class for Ollama
        self.llm = LLM(
            model=f"ollama/{os.environ.get('OLLAMA_MODEL', 'llama3:latest')}",
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        )

    def run(self, config: Dict, history: Set[str]) -> (str, bool):
        name = config.get("name", "User")
        email = config.get("email")
        preferences = ", ".join(config.get("preferences", []))
        avoid = ", ".join(config.get("avoid", []))
        categories = ", ".join(config.get("categories", ["World", "Nation", "Tech"]))
        history_str = "\n".join(list(history)[-30:])

        collector = Agent(
            role='News Collector',
            goal=f'Gather information about major news for {name}.',
            backstory=f"Researcher for: {preferences}.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        summarizer = Agent(
            role='News Summarizer',
            goal='Synthesize news into a daily brief.',
            backstory="Editor for concise summaries.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        dispatcher = Agent(
            role='Email Dispatcher',
            goal=f'Prepare the news brief for {email}.',
            backstory="Communications specialist.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        today = datetime.date.today().strftime("%B %d, %Y")
        
        collect_task = Task(
            description=f"Write a list of 2 major news stories for {today} related to {preferences}.",
            expected_output="A list of 2 news stories.",
            agent=collector
        )

        summarize_task = Task(
            description=f"Format these stories into a brief for {name}.",
            expected_output="A Markdown news brief.",
            agent=summarizer,
            context=[collect_task]
        )

        dispatch_task = Task(
            description=f"Confirm the brief is ready for {email}.",
            expected_output="Confirmation message.",
            agent=dispatcher,
            context=[summarize_task]
        )

        crew = Crew(
            agents=[collector, summarizer, dispatcher],
            tasks=[collect_task, summarize_task, dispatch_task],
            process=Process.sequential,
            verbose=True
        )

        crew.kickoff()
        
        from email_service import EmailService
        emailer = EmailService(
            os.environ.get("EMAIL_USER"), 
            os.environ.get("EMAIL_PASS"),
            os.environ.get("SMTP_HOST", "smtp.gmail.com"),
            int(os.environ.get("SMTP_PORT", "587"))
        )
        
        content = summarize_task.output.raw
        subject = f"Your Daily News Brief - {today}"
        success = emailer.send_brief(email, subject, content)
        
        return content, success

    def extract_story_ids(self, content: str) -> Set[str]:
        ids = set()
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* ") or line.startswith("### "):
                clean_line = line.lstrip("- *#").strip()
                if len(clean_line) > 10:
                    h = hashlib.md5(clean_line.encode()).hexdigest()
                    ids.add(h)
        return ids
