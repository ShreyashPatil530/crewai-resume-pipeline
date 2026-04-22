from crewai import Agent, Task, Crew, Process
from models import TailoredResumeModel, JobAnalysisModel
from tools import KeywordExtractorTool, SkillMatchingTool
from typing import Optional

def run_resume_tailoring(jd_model: JobAnalysisModel, resume_text: str, feedback: str = "") -> Optional[TailoredResumeModel]:
    try:
        optimizer = Agent(
            role='Expert Resume Optimizer',
            goal='Tailor a candidate resume to perfectly match a job description based on HR analysis.',
            backstory='A professional tech career coach who has helped thousands of candidates land top-tier tech jobs by optimizing their resumes to pass ATS systems.',
            verbose=True,
            memory=False,
            tools=[KeywordExtractorTool(), SkillMatchingTool()],
            allow_delegation=False,
            llm="groq/llama-3.3-70b-versatile"
        )

        feedback_instruction = f"\n\nCRITICAL FEEDBACK FROM PREVIOUS REVIEW (You MUST address these improvements):\n{feedback}" if feedback else ""

        task_desc = f"""
        Tailor the provided resume to the job description analysis.
        
        Job Analysis (Target):
        {jd_model.model_dump_json(indent=2)}
        
        Original Resume (Candidate):
        {resume_text}
        {feedback_instruction}
        
        Instructions:
        1. Use the Keyword Extractor Tool to find important keywords in the JD.
        2. Use the Skill Matching Tool to see what skills are missing.
        3. Provide a completely revamped professional summary.
        4. Update the skills list to highlight matches.
        5. Enhance the experience bullet points to align with the JD responsibilities.
        6. Note which keywords you successfully added.
        """

        task = Task(
            description=task_desc,
            expected_output='A structured JSON matching the TailoredResumeModel schema perfectly.',
            agent=optimizer,
            output_pydantic=TailoredResumeModel
        )

        crew = Crew(
            agents=[optimizer],
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
        print(f"[Error in Resume Tailoring Crew] {e}")
        return None
