from pydantic import BaseModel, Field
from typing import List

class JobDescription(BaseModel):
    skills: List[str] = Field(description="Key technical and soft skills required")
    experience: str = Field(description="Required experience level and domain")
    qualifications: str = Field(description="Minimum education or certifications")

class DimensionScore(BaseModel):
    score: int = Field(description="Score from 0 to 10")
    justification: str = Field(description="One-line justification explaining the score")

class CandidateEvaluation(BaseModel):
    skills_match_score: int = Field(description="Score from 0 to 10")
    skills_match_justification: str = Field(description="One-line justification")
    experience_relevance_score: int = Field(description="Score from 0 to 10")
    experience_relevance_justification: str = Field(description="One-line justification")
    education_certs_score: int = Field(description="Score from 0 to 10")
    education_certs_justification: str = Field(description="One-line justification")
    project_portfolio_score: int = Field(description="Score from 0 to 10")
    project_portfolio_justification: str = Field(description="One-line justification")
    communication_quality_score: int = Field(description="Score from 0 to 10")
    communication_quality_justification: str = Field(description="One-line justification")
    missing_skills: List[str] = Field(description="List of key skills from the JD that are missing in the resume")
    experience_gaps: str = Field(description="Summary of where the candidate falls short in terms of experience")
    suggested_questions: List[str] = Field(description="3-5 tailored interview questions to probe the candidate's gaps")
