from pydantic import BaseModel
from typing import List, Dict, Any

class HealthResponse(BaseModel):
    message : str

class AnalyzeResponse(BaseModel):
    # Meta & Problem Info
    problem_type: str
    best_model: str
    target_column: str
    
    # Generated Stories / Narratives
    eda_story: str
    ml_story: str
    feature_importance_story: str
    recommendation_story: str
    narrative: str
    
    # Raw Data / Metrics
    feature_importance: Dict[str, Any]
    missing_values: Dict[str, Any]
    target_distribution: Dict[str, Any]
    
    # Dataset Shapes & Health Metrics
    rows: int
    columns: int
    total_missing: int
    best_score: float
    best_metric: str
    health_score: float
    missing_pct: float

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    df: List[Dict[str, Any]]
    analysis: Dict[str, Any]
    question: str
    conversation_history: List[ChatMessage]
    


class ChatResponse(BaseModel):
    response: str