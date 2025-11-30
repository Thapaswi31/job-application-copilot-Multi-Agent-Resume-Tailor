from google.adk.agents.llm_agent import Agent
# my_agent/agent.py
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search, FunctionTool
from google.genai.types import Content, Part

from .tools_job_scraper import scrape_job_posting

MODEL = "gemini-2.0-flash"


job_scraper_tool = FunctionTool(
    func=scrape_job_posting)


def build_agent():
    job_search_agent = LlmAgent(
        name="JobSearchAgent",
        model=MODEL,
        description="Searches for recent job postings for a given role and location.",
        instruction=(
            "The user will provide a role, location, and optional filters.\n"
            "Ask clarifying questions if needed.\n"
            "Use the Google Search tool to find 3–5 relevant job postings.\n"
            "Return a JSON list with: title, company, location, url."
        ),
        tools=[google_search,],
        output_key="job_search_results",
    )

    job_scraper_agent = LlmAgent(
        name="JobScraperAgent",
        model=MODEL,
        description="Scrapes each job posting URL to extract description and skills.",
        instruction=(
            "You receive 'job_search_results' in state.\n"
            "For EACH posting, call scrape_job_posting with its URL.\n"
            "Collect outputs into a JSON list under 'job_details'."
        ),
        tools=[job_scraper_tool],
        output_key="job_details",
    )

    profile_analyzer_agent = LlmAgent(
        name="ProfileAnalyzerAgent",
        model=MODEL,
        description="Matches the user's CV/profile against job requirements.",
        instruction=(
            "You receive 'job_details' and 'user_profile' in state.\n"
            "For each job, compute: match_score, matched_skills, missing_skills, suggestions.\n"
            "Return only a JSON list."
        ),
        tools=[],
        output_key="profile_matches",
    )

    tailoring_agent = LlmAgent(
        name="TailoringAgent",
        model=MODEL,
        description="Generates tailored summaries and talking points per job.",
        instruction=(
            "You receive 'profile_matches' and 'user_profile'.\n"
            "Produce a markdown report with per‑job summary, talking points, and learning gaps."
        ),
        tools=[],
    )

    parallel_stage = ParallelAgent(
        name="ParallelJobStage",
        sub_agents=[job_search_agent],
        description="Runs job search in parallel stage.",
    )

    pipeline = SequentialAgent(
        name="JobApplicationPipeline",
        sub_agents=[
            parallel_stage,
            job_scraper_agent,
            profile_analyzer_agent,
            tailoring_agent,
        ],
        description="Full job application assistant pipeline.",
    )

    return pipeline


root_agent = build_agent()
