import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from .models import JobDescription, CandidateEvaluation

WEIGHTS = {
    "skills_match": 0.30,
    "experience_relevance": 0.25,
    "education_certs": 0.15,
    "project_portfolio": 0.20,
    "communication_quality": 0.10
}

def extract_jd_requirements(jd_text: str) -> JobDescription:
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    structured_llm = llm.with_structured_output(JobDescription)
    
    prompt = f"""You are an expert HR recruiter. Extract key requirements from the following Job Description.
    
JD:
{jd_text}"""
    
    return structured_llm.invoke(prompt)

def score_candidate(candidate_text: str, jd: JobDescription) -> dict:
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    structured_llm = llm.with_structured_output(CandidateEvaluation)
    
    prompt = f"""You are an expert HR recruiter evaluating a candidate resume against a Job Description.

Requirements:
Skills: {", ".join(jd.skills)}
Experience: {jd.experience}
Qualifications: {jd.qualifications}

Resume:
{candidate_text}

Evaluate the candidate on the 5 dimensions. Provide a score from 0-10 and a one-line justification for: Skills Match, Experience Relevance, Education & Certs, Project/Portfolio, Communication Quality.
Also identify any missing skills and experience gaps."""

    eval_result = structured_llm.invoke(prompt)
    
    scores = {
        "skills_match": {"score": eval_result.skills_match_score, "justification": eval_result.skills_match_justification},
        "experience_relevance": {"score": eval_result.experience_relevance_score, "justification": eval_result.experience_relevance_justification},
        "education_certs": {"score": eval_result.education_certs_score, "justification": eval_result.education_certs_justification},
        "project_portfolio": {"score": eval_result.project_portfolio_score, "justification": eval_result.project_portfolio_justification},
        "communication_quality": {"score": eval_result.communication_quality_score, "justification": eval_result.communication_quality_justification},
        "missing_skills": eval_result.missing_skills,
        "experience_gaps": eval_result.experience_gaps,
        "suggested_questions": eval_result.suggested_questions
    }
    
    total = sum(scores[k]["score"] * w for k, w in WEIGHTS.items() if k in WEIGHTS)
    scores["total_score"] = round(total, 2)
    return scores

def compare_top_candidates(top_candidates: list, jd: JobDescription) -> str:
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.3)
    
    candidates_summary = ""
    for idx, c in enumerate(top_candidates):
        candidates_summary += f"Candidate {idx+1}: {c['name']} (Score: {c['total_score']}/10)\n"
        candidates_summary += f"Strengths: {c['skills_match']['justification']}\n"
        candidates_summary += f"Gaps: {c['experience_gaps']}\n\n"

    prompt = f"""You are a senior hiring manager. Compare the following top candidates for the role based on their summaries and the JD requirements.
    
JD Requirements:
Skills: {", ".join(jd.skills)}
Experience: {jd.experience}

Candidates:
{candidates_summary}

Provide a concise (2-3 paragraph) executive summary explaining why the #1 candidate is the preferred choice and how they edge out the others. Use a professional, decisive tone."""

    response = llm.invoke(prompt)
    return response.content
