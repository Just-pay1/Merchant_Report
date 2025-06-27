import os
from dotenv import load_dotenv
import certifi

load_dotenv()
# Database config
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = 3306
DB_NAME = os.getenv('DB_NAME')

# Use certifi to get the trusted CA bundle path
ssl_ca_path = certifi.where()

# SQLAlchemy connection string
DB_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?ssl_ca={ssl_ca_path}"
)

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