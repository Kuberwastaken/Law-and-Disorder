from pydantic import BaseModel
from typing import List, Dict, Optional

class Query(BaseModel):
    situation: str

class Article(BaseModel):
    article_number: str
    title: str
    content: str
    similarity_score: float

class Response(BaseModel):
    verdict: str
    articles: List[Article]
    reasoning: str
    loopholes: List[str]
    confidence: float

class CacheConfig(BaseModel):
    expiry_time: int = 3600  # Cache expiry time in seconds
    max_size: int = 1000     # Maximum number of items in cache