from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from agent import make_deep_research, CompleteInterviewResearch, FilteredInterviews, ResearchData, CompanySummary, InterviewPreparation, CompetitiveAnalysis

app = FastAPI(
    title="Interview Research API",
    description="API for getting comprehensive interview research data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API responses
class CompanySummaryResponse(BaseModel):
    overview: str
    industry: str
    size: str
    culture: str
    recent_news: str

class InterviewPreparationResponse(BaseModel):
    company_specific_questions: List[str]
    role_specific_insights: str
    interview_tips: str
    research_sources: str

class CompetitiveAnalysisResponse(BaseModel):
    competitors: str
    market_position: str
    growth_trends: str

class ResearchDataResponse(BaseModel):
    company_summary: CompanySummaryResponse
    interview_preparation: InterviewPreparationResponse
    competitive_analysis: CompetitiveAnalysisResponse

class FilteredInterviewsResponse(BaseModel):
    company_name: str
    role: str
    type: str
    interview_date: str
    skills: List[str]

class CompleteInterviewResearchResponse(BaseModel):
    interview_info: FilteredInterviewsResponse
    research_data: ResearchDataResponse

@app.get("/")
async def root():
    return {"message": "Interview Research API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/interview-research", response_model=CompleteInterviewResearchResponse)
async def get_interview_research():
    """
    Get comprehensive interview research data for the latest interview email.
    
    Returns:
        CompleteInterviewResearchResponse: Complete research data including company info, 
        interview preparation tips, and competitive analysis
    """
    try:
        # Call the research function from agent.py
        research_result = make_deep_research()
        
        if research_result is None:
            raise HTTPException(
                status_code=404, 
                detail="No interview emails found or research failed"
            )
        
        # Convert the research result to response format
        response = CompleteInterviewResearchResponse(
            interview_info=FilteredInterviewsResponse(
                company_name=research_result.interview_info.company_name,
                role=research_result.interview_info.role,
                type=research_result.interview_info.type,
                interview_date=research_result.interview_info.interview_date,
                skills=research_result.interview_info.skills
            ),
            research_data=ResearchDataResponse(
                company_summary=CompanySummaryResponse(
                    overview=research_result.research_data.company_summary.overview,
                    industry=research_result.research_data.company_summary.industry,
                    size=research_result.research_data.company_summary.size,
                    culture=research_result.research_data.company_summary.culture,
                    recent_news=research_result.research_data.company_summary.recent_news
                ),
                interview_preparation=InterviewPreparationResponse(
                    company_specific_questions=research_result.research_data.interview_preparation.company_specific_questions,
                    role_specific_insights=research_result.research_data.interview_preparation.role_specific_insights,
                    interview_tips=research_result.research_data.interview_preparation.interview_tips,
                    research_sources=research_result.research_data.interview_preparation.research_sources
                ),
                competitive_analysis=CompetitiveAnalysisResponse(
                    competitors=research_result.research_data.competitive_analysis.competitors,
                    market_position=research_result.research_data.competitive_analysis.market_position,
                    growth_trends=research_result.research_data.competitive_analysis.growth_trends
                )
            )
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving interview research: {str(e)}"
        )

@app.get("/interview-research/company/{company_name}")
async def get_interview_research_by_company(company_name: str):
    """
    Get interview research data for a specific company.
    
    Args:
        company_name (str): Name of the company to research
        
    Returns:
        CompleteInterviewResearchResponse: Research data for the specified company
    """
    try:
        # For now, this will return the same research as the main endpoint
        # In the future, you could modify the agent to accept company_name as parameter
        research_result = make_deep_research()
        
        if research_result is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No research data found for company: {company_name}"
            )
        
        # Check if the research is for the requested company
        if research_result.interview_info.company_name.lower() != company_name.lower():
            raise HTTPException(
                status_code=404,
                detail=f"Research data not available for company: {company_name}"
            )
        
        # Convert to response format (same as above)
        response = CompleteInterviewResearchResponse(
            interview_info=FilteredInterviewsResponse(
                company_name=research_result.interview_info.company_name,
                role=research_result.interview_info.role,
                type=research_result.interview_info.type,
                interview_date=research_result.interview_info.interview_date,
                skills=research_result.interview_info.skills
            ),
            research_data=ResearchDataResponse(
                company_summary=CompanySummaryResponse(
                    overview=research_result.research_data.company_summary.overview,
                    industry=research_result.research_data.company_summary.industry,
                    size=research_result.research_data.company_summary.size,
                    culture=research_result.research_data.company_summary.culture,
                    recent_news=research_result.research_data.company_summary.recent_news
                ),
                interview_preparation=InterviewPreparationResponse(
                    company_specific_questions=research_result.research_data.interview_preparation.company_specific_questions,
                    role_specific_insights=research_result.research_data.interview_preparation.role_specific_insights,
                    interview_tips=research_result.research_data.interview_preparation.interview_tips,
                    research_sources=research_result.research_data.interview_preparation.research_sources
                ),
                competitive_analysis=CompetitiveAnalysisResponse(
                    competitors=research_result.research_data.competitive_analysis.competitors,
                    market_position=research_result.research_data.competitive_analysis.market_position,
                    growth_trends=research_result.research_data.competitive_analysis.growth_trends
                )
            )
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving interview research for {company_name}: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
