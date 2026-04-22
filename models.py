from pydantic import BaseModel, Field
from typing import List

class JobAnalysisModel(BaseModel):
    job_title: str = Field(description="The extracted job title")
    company_name: str = Field(description="The name of the company hiring")
    required_skills: List[str] = Field(description="List of explicitly required skills")
    preferred_skills: List[str] = Field(description="List of preferred or bonus skills")
    experience_level: str = Field(description="Required experience level (e.g., Senior, Junior, 5+ years)")
    responsibilities: List[str] = Field(description="Key responsibilities of the role")
    match_criteria: str = Field(description="Summary of the main criteria a candidate must meet")

class TailoredResumeModel(BaseModel):
    tailored_summary: str = Field(description="A professional summary optimized for the target job")
    updated_skills: List[str] = Field(description="List of skills tailored to highlight matches with the job description")
    updated_experience: List[str] = Field(description="List of tailored bullet points for work experience")
    keywords_added: List[str] = Field(description="Important keywords added from the job description")

class QualityReviewModel(BaseModel):
    score: int = Field(ge=1, le=10, description="Overall match score from 1 to 10")
    keyword_match_percentage: int = Field(description="Percentage of required keywords present in the tailored resume")
    strengths: List[str] = Field(description="What makes this tailored resume strong")
    improvements: List[str] = Field(description="Actionable feedback to improve the resume further")
    verdict: str = Field(description="Final verdict: 'APPROVED' or 'NEEDS_REVISION'")
