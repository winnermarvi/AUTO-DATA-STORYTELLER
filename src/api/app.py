from fastapi import FastAPI,File,UploadFile,HTTPException,Form
from fastapi.responses import FileResponse
import pandas as pd
from src.main_pipeline import main_pipeline
from src.api.schemas import HealthResponse,AnalyzeResponse

app = FastAPI()

@app.get("/", response_model=HealthResponse)
def home():
    return {
        "message" : "Auto Data Story teller is running"
    }

@app.post("/analyze")
def analyze(
    file : UploadFile = File(),
    target_col : str = Form()
): 
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )
    
    df = pd.read_csv(file.file)
    
    if target_col not in df.columns:
        raise HTTPException(
            status_code=400,
            detail="Target column not found"
        )

    result = main_pipeline(df ,target_col)

    return {
        "problem_type": result['analysis']["problem_info"]["problem_type"],
        "best_model": result['analysis']["best_model_info"]["best_model"],

        "eda_story": "\n".join(result['analysis']["eda_story"]),
        "ml_story": "\n".join(result['analysis']["ml_story"]),
        "feature_importance_story": "\n".join(result['analysis']["feature_importance_story"]),
        "recommendation_story": "\n".join(result['analysis']["recommendation_story"]),

        "narrative": result['analysis']["llm_report"]["narrative"]
    }


@app.post("/genrate-report")
def generate_report(
    file : UploadFile = File(),
    target_col : str = Form()
): 
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )
    
    df = pd.read_csv(file.file)
    
    if target_col not in df.columns:
        raise HTTPException(
            status_code=400,
            detail="Target column not found"
        )

    result = main_pipeline(df ,target_col)

    return FileResponse(
        path=result['pdf_path'],
        media_type="application/pdf",
        filename="data_report.pdf"
    )
