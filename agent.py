import json
from arcadepy import Arcade
from pydantic import BaseModel
from typing import List, Optional

API_KEY = "arc_o179fQfXwKEj1ZRCxkX7Gp2W8PnivedMfkXg2QajL382Ya6W4QrB"
USER_ID = "nithishkumar3210@gmail.com"

client = Arcade(
    api_key=API_KEY
)

# Authorize the tool
auth_response = client.tools.authorize(
    tool_name="Gmail.ListEmails@3.0.0",
    user_id=USER_ID,
)

# Check if authorization is completed
if auth_response.status != "completed":
    print(f"Click this link to authorize: {auth_response.url}")

# Wait for the authorization to complete
auth_response = client.auth.wait_for_completion(auth_response)

if auth_response.status != "completed":
    raise Exception("Authorization failed")

print("🚀 Authorization successful!")

def get_all_interview_email():
    result = client.tools.execute(
        tool_name="Gmail.ListEmails@3.0.0",
        input={
            "owner": "ArcadeAI",
            "name": "arcade-ai",
            "starred": "true",
            "n_emails": "1"
        },
        user_id=USER_ID,
    )
    client.chat
    #print(result.output.value) # Dict
    all_email_body = []
    for e in result.output.value.get("emails"):
        all_email_body.append(e.get("body"))
    return all_email_body

# Pydantic Models for Research Data
class CompanySummary(BaseModel):
    overview: str
    industry: str
    size: str
    culture: str
    recent_news: str

class InterviewPreparation(BaseModel):
    company_specific_questions: List[str]
    role_specific_insights: str
    interview_tips: str
    research_sources: str

class CompetitiveAnalysis(BaseModel):
    competitors: str
    market_position: str
    growth_trends: str

class ResearchData(BaseModel):
    company_summary: CompanySummary
    interview_preparation: InterviewPreparation
    competitive_analysis: CompetitiveAnalysis

class ResearchResponse(BaseModel):
    success: bool
    data: Optional[ResearchData] = None
    error: Optional[str] = None
    raw_response: Optional[str] = None

class FilteredInterviews(BaseModel):
    company_name: str
    role: str
    type: str
    interview_date: str
    skills: List[str]

class InterviewEmails(BaseModel):
    interview_emails: List[FilteredInterviews]

class CompleteInterviewResearch(BaseModel):
    interview_info: FilteredInterviews
    research_data: ResearchData

def research_company_for_interview(client, company_name: str, role: str, interview_type: str, skills: List[str]) -> ResearchResponse:
    """
    Perform deep research on a company for interview preparation
    """
    
    # Create context-specific research prompt
    research_prompt = f"""
    You are an expert business analyst and career coach. Please provide a comprehensive analysis of {company_name} 
    specifically for a {interview_type.lower()} interview for the role of {role}.
    
    Required skills for this role: {', '.join(skills) if skills else 'Not specified'}
    
    Please provide your analysis in the following JSON format:
    {{
        "company_summary": {{
            "overview": "Brief company description",
            "industry": "Primary industry and sector",
            "size": "Company size (employees, revenue if known)",
            "culture": "Company culture and values",
            "recent_news": "Recent significant news or developments"
        }},
        "interview_preparation": {{
            "company_specific_questions": [
                "Questions specific to {company_name} and their business"
            ],
            "role_specific_insights": "How {company_name} typically approaches {role} positions",
            "interview_tips": "Specific tips for {interview_type.lower()} interviews at {company_name}",
            "research_sources": "Key areas to research about {company_name}"
        }},
        "competitive_analysis": {{
            "competitors": "Main competitors in their space",
            "market_position": "Where {company_name} stands in the market",
            "growth_trends": "Recent growth or challenges"
        }}
    }}
    
    Focus on information that would be most relevant for a {interview_type.lower()} interview for a {role} position.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert business analyst with deep knowledge of companies, industries, and interview preparation. Provide accurate, well-researched information that would be valuable for interview preparation."
                },
                {
                    "role": "user",
                    "content": research_prompt
                }
            ],
            temperature=0.2,  # Low temperature for factual, consistent information
        )
        
        # Parse the response
        research_content = response.choices[0].message.content
        
        # Try to parse as JSON, if it fails, return the raw content
        try:
            research_data = json.loads(research_content)
            # Validate with Pydantic
            validated_data = ResearchData.model_validate(research_data)
            return ResearchResponse(
                success=True,
                data=validated_data,
                raw_response=research_content
            )
        except (json.JSONDecodeError, Exception) as e:
            return ResearchResponse(
                success=False,
                error=f"Failed to parse JSON response: {str(e)}",
                raw_response=research_content
            )
            
    except Exception as e:
        return ResearchResponse(
            success=False,
            error=str(e),
            raw_response=None
        )

# Improved prompt with proper role and better structure
def filter_email(all_email_body):
    response = client.chat.completions.create(
        model="gpt-4",  # You can use any model available on Arcade
        messages=[
            {
                "role": "system",
                "content": """You are an expert email classifier specializing in identifying and categorizing job interview emails. 
                Your task is to analyze email content and extract relevant interview information.
                
                Please return your response in the following JSON format:
                {
                    "interview_emails": [
                        {
                            "company_name": "string",
                            "role": "string", 
                            "type": "TECH" | "BEHAVIORAL" | "INTRODUCTION_CALL",
                            "interview_date": "YYYY-MM-DDThh:mm:ss",
                            "skills": ["string"]
                        }
                    ]
                }
                
                Guidelines:
                - Only include emails that are clearly related to job interviews
                - For interview type: TECH = technical interviews, BEHAVIORAL = behavioral/culture fit, INTRODUCTION_CALL = initial screening calls
                - Extract skills mentioned in the email or implied by the role
                - If no specific date is mentioned, use null for interview_date
                - If no skills are mentioned, use an empty array"""
            },
            {
                "role": "user",
                "content": f"Please analyze the following emails from my inbox and identify any job interview related emails:\n\n{all_email_body}"
            }
        ],
        temperature=0.3,  # Lower temperature for more consistent classification
    )

    print("Basic Chat Completion:")
    print(f"Model: {response.model}")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Usage: {response.usage}")
    print("-" * 50)

    interviews = InterviewEmails.model_validate_json(
        response.choices[0].message.content)

    return interviews

def make_deep_research():
    # Perform deep research for each interview
    print("\n🔍 Performing Deep Research on Companies...")
    print("=" * 60)
    
    inter = filter_email(get_all_interview_email())
    for i, interview in enumerate(inter.interview_emails):
        print(f"\n📧 Interview {i+1}: {interview.role} at {interview.company_name}")
        print(f"Type: {interview.type} | Date: {interview.interview_date}")
        print(f"Skills: {', '.join(interview.skills) if interview.skills else 'Not specified'}")
        
        # Perform company research
        research_result = research_company_for_interview(
            client=client,
            company_name=interview.company_name,
            role=interview.role,
            interview_type=interview.type,
            skills=interview.skills
        )
        
        if research_result.success and research_result.data:
            data = research_result.data
            
            print(f"\n🏢 Company Summary for {interview.company_name}:")
            print(f"Industry: {data.company_summary.industry}")
            print(f"Size: {data.company_summary.size}")
            print(f"Culture: {data.company_summary.culture}")
            
            print(f"\n💡 Interview Preparation Tips:")
            print(f"Role-specific insights: {data.interview_preparation.role_specific_insights}")
            print(f"Interview tips: {data.interview_preparation.interview_tips}")
            
            print(f"\n📊 Competitive Analysis:")
            print(f"Competitors: {data.competitive_analysis.competitors}")
            print(f"Market position: {data.competitive_analysis.market_position}")
            
            # Create complete research object
            complete_research = CompleteInterviewResearch(
                interview_info=interview,
                research_data=data
            )
            return complete_research
            # Save detailed research to file
            research_filename = f"research_{interview.company_name.replace(' ', '_').lower()}_{interview.type.lower()}.json"
            with open(research_filename, 'w') as f:
                json.dump(complete_research.model_dump(), f, indent=2)
            print(f"📁 Detailed research saved to: {research_filename}")
            
        else:
            print(f"❌ Research failed: {research_result.error}")
            if research_result.raw_response:
                print(f"Raw response: {research_result.raw_response}")
        
        print("-" * 60)

    print("\n✅ Research completed for all interviews!")
