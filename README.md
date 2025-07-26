# Interview Research API

A FastAPI application that provides comprehensive interview research data by analyzing Gmail emails and performing deep research on companies.

## Features

- **Email Analysis**: Automatically scans Gmail for interview-related emails
- **Company Research**: Performs deep research on companies for interview preparation
- **Comprehensive Data**: Provides company summary, interview preparation tips, and competitive analysis
- **RESTful API**: Clean REST endpoints for easy integration

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Arcade API credentials in `agent.py`:
   - Update `API_KEY` with your Arcade API key
   - Update `USER_ID` with your email address

## Running the API

Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check
- **GET** `/`
- **GET** `/health`
- Returns basic status information

### 2. Get Interview Research
- **GET** `/interview-research`
- Returns comprehensive research data for the latest interview email
- Response includes:
  - Company information (overview, industry, size, culture, recent news)
  - Interview preparation (questions, insights, tips, research sources)
  - Competitive analysis (competitors, market position, growth trends)

### 3. Get Research by Company
- **GET** `/interview-research/company/{company_name}`
- Returns research data for a specific company
- Replace `{company_name}` with the company name you want to research

## API Response Format

```json
{
  "interview_info": {
    "company_name": "Example Corp",
    "role": "Software Engineer",
    "type": "TECH",
    "interview_date": "2024-01-15T10:00:00",
    "skills": ["Python", "FastAPI", "React"]
  },
  "research_data": {
    "company_summary": {
      "overview": "Company description...",
      "industry": "Technology",
      "size": "500-1000 employees",
      "culture": "Fast-paced, innovative...",
      "recent_news": "Recent developments..."
    },
    "interview_preparation": {
      "company_specific_questions": ["Question 1", "Question 2"],
      "role_specific_insights": "How the company approaches this role...",
      "interview_tips": "Specific tips for this company...",
      "research_sources": "Key areas to research..."
    },
    "competitive_analysis": {
      "competitors": "Main competitors...",
      "market_position": "Market position...",
      "growth_trends": "Recent growth or challenges..."
    }
  }
}
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `404`: No interview emails found or company not found
- `500`: Internal server error

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations
- **ArcadePy**: Gmail integration for email analysis
- **Python-multipart**: For handling form data

## Notes

- The API requires Gmail authorization through Arcade
- Research is performed using GPT-4 for comprehensive analysis
- Results are cached and returned in a structured format
- The API automatically handles email filtering and company research 