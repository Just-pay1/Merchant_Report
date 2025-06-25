from pipeline import run_pipeline
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI()

@app.get("/")
def welcome_message():
    return {"Merchant Report Creator": "Welcome to the Merchant Report Creator API"}

@app.get("/report/")
def get_report():
    # Run the pipeline (this should generate the PDF)
    run_pipeline()
    
    # Set the path to the generated PDF
    pdf_path = "artifacts/merchant_report.pdf"
    
    # Ensure the file exists before attempting to return it
    if os.path.exists(pdf_path):
        return FileResponse(
            path=pdf_path,
            filename="merchant_report.pdf",
            media_type="application/pdf"
        )
    else:
        return {"error": "Report not found."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)