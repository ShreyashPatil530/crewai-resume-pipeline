from crewai import Agent, Task, Crew, Process
from models import JobAnalysisModel
from typing import Optional

def run_job_analysis(jd_text: str) -> Optional[JobAnalysisModel]:
    try:
        analyst = Agent(
            role='Senior Job Profile Analyst',
            goal='Analyze job descriptions to extract key requirements, skills, and criteria in a structured format.',
            backstory='An expert technical HR recruiter who perfectly understands what hiring managers are looking for in candidates.',
            verbose=True,
            memory=False,
            allow_delegation=False,
            llm="groq/llama-3.3-70b-versatile"
        )

        task = Task(
            description=f'Analyze the following Job Description and extract the structured information required.\n\nJob Description:\n{jd_text}',
            expected_output='A structured JSON matching the JobAnalysisModel schema perfectly.',
            agent=analyst,
            output_pydantic=JobAnalysisModel
        )

        crew = Crew(
            agents=[analyst],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )

        crew_output = crew.kickoff()
        # The output_pydantic is automatically mapped when we set it in the Task
        if hasattr(task.output, 'pydantic') and task.output.pydantic:
            return task.output.pydantic
        
        # Fallback if accessed via crew output
        if hasattr(crew_output, 'pydantic') and crew_output.pydantic:
             return crew_output.pydantic

        # Raise if we didn't get the pydantic model
        raise ValueError("Failed to get Pydantic model from Crew output.")
        
    except Exception as e:
        print(f"[Error in Job Analysis Crew] {e}")
        return None
