from fastapi import FastAPI,File,UploadFile,HTTPException,Form
import pandas as pd
from src.main_pipeline import main_pipeline

app = FastAPI()

@app.get("/")
def home():
    return {
        "message" : "Auto Data Story teller is running"
    }

@app.post("/analyze")
def analyze(
    file : UploadFile = File(),
    target_col : str = Form()
):
    
    df = pd.read_csv(file.file)

    result = main_pipeline(df ,target_col)
    
    return result