import os
import json
from dotenv import load_dotenv

from crews.job_analysis import run_job_analysis
from crews.resume_tailoring import run_resume_tailoring
from crews.quality_review import run_quality_review

def main():
    # Load environment variables (e.g., OPENAI_API_KEY or GROQ_API_KEY)
    load_dotenv()
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    print("=======================================")
    print(" Starting Job Application AI Pipeline")
    print("=======================================\n")

    # 1. Load JD + Resume
    try:
        with open("data/sample_jd.txt", "r") as f:
            jd_text = f.read()
        with open("data/sample_resume.txt", "r") as f:
            resume_text = f.read()
    except FileNotFoundError as e:
        print(f"[Error] Missing input files: {e}")
        return

    # 2. Run Job Analysis Crew
    print("-> Running Job Analysis Crew...")
    jd_model = run_job_analysis(jd_text)
    if not jd_model:
        print("Pipeline failed at Job Analysis stage.")
        return
    print(f"   [Success] Extracted Job Title: {jd_model.job_title}\n")

    # Prepare for Rewrite Loop
    max_retries = 2
    attempt = 0
    feedback = ""
    tailored_resume = None
    review_model = None

    while attempt <= max_retries:
        print(f"--- Attempt {attempt + 1} of {max_retries + 1} ---")
        
        # 3. Run Resume Tailoring Crew
        print("-> Running Resume Tailoring Crew...")
        tailored_resume = run_resume_tailoring(jd_model, resume_text, feedback)
        if not tailored_resume:
            print("Pipeline failed at Resume Tailoring stage.")
            return
        print("   [Success] Resume Tailored.\n")

        # 4. Run Quality Review Crew
        print("-> Running Quality Review Crew...")
        review_model = run_quality_review(tailored_resume, jd_model)
        if not review_model:
            print("Pipeline failed at Quality Review stage.")
            return
        
        print(f"   [Score]: {review_model.score}/10")
        print(f"   [Verdict]: {review_model.verdict}")
        
        # 5. Check Score and Verdict
        if review_model.score >= 7 and review_model.verdict == "APPROVED":
            print("\n✅ Resume met quality standards!")
            break
        else:
            print("\n⚠️ Resume needs revision.")
            feedback = "; ".join(review_model.improvements)
            print(f"   [Feedback for next loop]: {feedback}\n")
            attempt += 1

    if attempt > max_retries:
        print("\n❌ Max retries reached. Using the last generated resume.")

    # 6. Save output to file
    final_output = {
        "job_analysis": jd_model.model_dump(),
        "tailored_resume": tailored_resume.model_dump(),
        "quality_review": review_model.model_dump()
    }
    
    with open("output/final_resume.json", "w") as f:
        json.dump(final_output, f, indent=4)
        
    print("\n=======================================")
    print(" Pipeline Complete!")
    print(" Final resume saved to: output/final_resume.json")
    print("=======================================")

if __name__ == "__main__":
    main()
