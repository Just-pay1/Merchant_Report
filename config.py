import os
from dotenv import load_dotenv

load_dotenv()
DB_PARAMS = {
    'dbname': 'fraud',
    'user': 'postgres',
    'password': os.getenv('DB_PASSWORD'),  # Add your real password here if needed
    'host': 'localhost',
    'port': 5432
}
DB_URL = f"postgresql+psycopg2://postgres:{DB_PARAMS['password']}@localhost:5432/fraud"

# List of image paths
IMAGE_PATHS = [
    "artifacts/payment_analysis_last_month.png",
    "artifacts/transaction_count_analysis_last_month.png",
    "artifacts/financial_performance_analysis.png",
    "artifacts/daily_user_metrics.png",
    "artifacts/user_state_distribution.png"
]

# Output PDF path
PDF_PATH = "artifacts/merchant_report.pdf"