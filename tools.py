import re
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class KeywordExtractorToolInput(BaseModel):
    text: str = Field(..., description="The text from which to extract important keywords (e.g., JD or Resume).")

class KeywordExtractorTool(BaseTool):
    name: str = "Keyword Extractor Tool"
    description: str = "Extracts top important keywords from a given text. Useful for identifying key skills and requirements."
    args_schema: Type[BaseModel] = KeywordExtractorToolInput

    def _run(self, text: str) -> str:
        # Simple extraction logic for demo purposes
        words = re.findall(r'\b[A-Za-z]+\b', text.lower())
        stop_words = {'and', 'the', 'is', 'in', 'to', 'with', 'for', 'of', 'a', 'an', 'or', 'on', 'as', 'at'}
        # Filter and count
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        unique_keywords = list(set(keywords))
        return ", ".join(unique_keywords[:20])  # Return top 20 keywords

class SkillMatchingToolInput(BaseModel):
    resume_skills: str = Field(..., description="Comma-separated list of skills from the resume.")
    jd_skills: str = Field(..., description="Comma-separated list of skills from the job description.")

class SkillMatchingTool(BaseTool):
    name: str = "Skill Matching Tool"
    description: str = "Compares skills from a resume against job description skills and returns missing skills and match percentage."
    args_schema: Type[BaseModel] = SkillMatchingToolInput

    def _run(self, resume_skills: str, jd_skills: str) -> str:
        r_skills = {s.strip().lower() for s in resume_skills.split(",") if s.strip()}
        j_skills = {s.strip().lower() for s in jd_skills.split(",") if s.strip()}
        
        if not j_skills:
            return "No JD skills provided to match against."
            
        matched = r_skills.intersection(j_skills)
        missing = j_skills.difference(r_skills)
        match_percentage = int((len(matched) / len(j_skills)) * 100)
        
        return f"Match Percentage: {match_percentage}%. Missing skills to add if applicable: {', '.join(missing)}"
