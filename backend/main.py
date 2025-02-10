from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from models import Query, Response
from constitution_analyzer import ConstitutionAnalyzer

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = ConstitutionAnalyzer()

@app.post("/analyze")
async def analyze_situation(query: Query) -> Response:
    try:
        return analyzer.analyze_situation(query.situation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-batch")
async def analyze_batch(queries: List[Query]) -> List[Response]:
    try:
        situations = [query.situation for query in queries]
        return analyzer.batch_analyze_situations(situations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)