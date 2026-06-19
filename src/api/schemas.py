from pydantic import BaseModel

class HealthResponse(BaseModel):
    message : str

class AnalyzeResponse(BaseModel):
    problem_typr : str
    best_model : str