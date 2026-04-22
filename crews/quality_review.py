from crewai import Agent, Task, Crew, Process
from models import TailoredResumeModel, JobAnalysisModel, QualityReviewModel
from typing import Optional

def run_quality_review(tailored_resume: TailoredResumeModel, jd_model: JobAnalysisModel) -> Optional[QualityReviewModel]:
    try:
        reviewer = Agent(
            role='Strict Quality Assurance HR Reviewer',
            goal='Critically evaluate a tailored resume against a job description to ensure it meets a high bar of quality and relevance.',
            backstory='A cynical but highly effective Senior HR Director who demands perfection, strong keyword matching, and clear impact in resumes. Rarely gives a 10/10.',
            verbose=True,
            memory=False,
            allow_delegation=False,
            llm="groq/llama-3.3-70b-versatile"
        )

        task_desc = f"""
        Evaluate the tailored resume against the original job analysis.
        
        Job Analysis (Requirements):
        {jd_model.model_dump_json(indent=2)}
        
        Tailored Resume (To Review):
        {tailored_resume.model_dump_json(indent=2)}
        
        Instructions:
        1. Score the resume from 1 to 10 based on how well it matches the JD. Be strict.
        2. Calculate a keyword match percentage.
        3. List the strengths of the tailored resume.
        4. List specific, actionable improvements needed.
        5. Provide a verdict: "APPROVED" (if score >= 7) or "NEEDS_REVISION" (if score < 7).
        """

        task = Task(
            description=task_desc,
            expected_output='A structured JSON matching the QualityReviewModel schema perfectly.',
            agent=reviewer,
            output_pydantic=QualityReviewModel
        )

        crew = Crew(
            agents=[reviewer],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )

        crew_output = crew.kickoff()
        
        if hasattr(task.output, 'pydantic') and task.output.pydantic:
            return task.output.pydantic
            
        if hasattr(crew_output, 'pydantic') and crew_output.pydantic:
             return crew_output.pydantic

        raise ValueError("Failed to get Pydantic model from Crew output.")
        
    except Exception as e:
        print(f"[Error in Quality Review Crew] {e}")
        return None
