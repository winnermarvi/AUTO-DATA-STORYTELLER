from fastapi import FastAPI,File,UploadFile,HTTPException,Form
from fastapi.responses import FileResponse
import pandas as pd
#from src.main_pipeline import main_pipeline
from src.services.pipeline_service import run_pipeline
from src.api.schemas import HealthResponse, AnalyzeResponse, ChatRequest, ChatResponse
from src.services.chat_service import generate_chat_response

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

    #result = main_pipeline(df ,target_col)
    result = run_pipeline(df,target_col)

    return {
        "analysis" : result["analysis"],
        "problem_type": result['analysis']['ml']["problem_info"]["problem_type"],
        "best_model": result['analysis']['ml']["best_model_info"]["best_model"],

        "eda_story": "\n".join(result['analysis']['eda']["eda_story"]),
        "ml_story": "\n".join(result['analysis']['ml']["ml_story"]),
        "feature_importance_story": "\n".join(result['analysis']['ml']["feature_importance_story"]),
        "recommendation_story": "\n".join(result['analysis']['ml']["recommendation_story"]),

        "narrative": result['analysis']['llm']["narrative"],

        "feature_importance": result['analysis']['ml']["feature_importance"],
        "missing_values": result['analysis']['eda']["report"]["missing_values"],
        "target_distribution": result['analysis']['ml']["target_distribution"],
        "target_column": target_col,

        "rows": result['analysis']['eda']["report"]["shape"]["rows"],
        "columns": result['analysis']['eda']["report"]["shape"]["columns"],

        "total_missing": result['analysis']['eda']["report"]["total_missing"],
        "best_score": result['analysis']['ml']["best_model_info"]["best_metric_value"],
        "best_metric": result['analysis']['ml']["best_model_info"]["selection_metric"],

        "health_score": result['analysis']['eda']["report"]["health_score"],
        "missing_pct": result['analysis']['eda']["report"]["missing_pct"]
    }




@app.post("/generate-report")
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

    #result = main_pipeline(df ,target_col)
    result = run_pipeline(df ,target_col)

    return FileResponse(
        path=result['pdf_path'],
        media_type="application/pdf",
        filename="data_report.pdf"
    )

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = generate_chat_response(
            df = pd.DataFrame(request.df),
            analysis=request.analysis,
            question=request.question,
            conversation_history=[
                message.model_dump()
                for message in request.conversation_history
            ]
        )

        return ChatResponse(
            response=response["narrative"],
            chart=response["chart"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Chat generation failed: {str(e)}"
        )
