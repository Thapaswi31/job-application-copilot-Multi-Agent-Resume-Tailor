# Job Application Copilot: Multi-Agent Resume Tailor

An AI-powered multi-agent system that automates job search, extracts job requirements, matches your profile, and generates personalized resume tailoring recommendations.

## 🎯 Problem Statement

Job hunting is time-consuming and manual:
- **Searching**: Manually browse multiple job boards (LinkedIn, Indeed, etc.)
- **Extracting**: Copy-paste job requirements from each posting
- **Matching**: Manually compare skills against requirements
- **Tailoring**: Write custom cover letters and talking points for each role

**Result**: 5-10 hours per week wasted on repetitive, low-value work.

## ✨ Solution: Multi-Agent Automation

This system automates the entire job application workflow using a **4-agent parallel + sequential pipeline**:

1. **JobSearchAgent** → Finds relevant jobs via Google Search
2. **JobScraperAgent** → Extracts job details (skills, requirements, responsibilities)
3. **ProfileAnalyzerAgent** → Matches your CV against each job
4. **TailoringAgent** → Generates tailored cover letters, talking points, and learning recommendations

## 🏗️ Architecture

┌──────────────────────────────────┐
│ User Input + CV/Profile │
└──────────────────────┬────────────┘
│
┌─────────────▼──────────────┐
│ ParallelJobStage │
├────────────────────────────┤
│ JobSearchAgent │
│ (Google Search Tool) │
└──────────────┬─────────────┘
│
┌─────────────▼──────────────┐
│ JobScraperAgent │
│ (Custom Scraper Tool) │
│ - Extracts skills │
│ - Parses requirements │
└──────────────┬─────────────┘
│
┌──────────────▼──────────────┐
│ ProfileAnalyzerAgent │
│ - Computes match_score │
│ - Maps matched skills │
│ - Identifies gaps │
└──────────────┬──────────────┘
│
┌──────────────▼──────────────┐
│ TailoringAgent │
│ - Tailored summary │
│ - Interview talking pts │
│ - Learning checklist │
└──────────────┬──────────────┘
│
┌────────────────▼─────────────┐
│ Final Markdown Report │
│ (Ready for user) │
└─────────────────────────────┘

text

## 🔑 Key Concepts Demonstrated

✅ **Multi-Agent System** - 4 LLM agents + ParallelAgent + SequentialAgent orchestration  
✅ **Tools** - Google Search (built-in) + custom FunctionTool (web scraper)  
✅ **Sessions & Memory** - User profile persists in session state across agent turns  
✅ **Error Handling** - Gracefully handles blocked job sites (HTTP 403)  
✅ **Structured Output** - JSON at each agent stage for downstream processing  

## 📋 System Design

### **Agent 1: JobSearchAgent**
- **Tool**: `google_search` (built-in ADK tool)
- **Input**: Role, location, work mode (Remote/Hybrid/On-site), seniority level
- **Output**: JSON list of job postings with title, company, location, URL
- **Example Output**:
[
{
"title": "Senior Python Engineer",
"company": "Hudson River Trading",
"location": "New York, NY",
"url": "https://..."
}
]

text

### **Agent 2: JobScraperAgent**
- **Tool**: `scrape_job_posting` (custom FunctionTool)
- **Input**: Job URLs from JobSearchAgent
- **Output**: Extracted job details (title, description, skills, responsibilities)
- **Error Handling**: Returns `{"error": "http_status_403"}` instead of crashing on blocked sites
- **Example Output**:
{
"url": "https://...",
"title": "Senior Python Engineer",
"job_description": "Full page text...",
"skills": ["python", "django", "aws", "docker"],
"error": null
}
