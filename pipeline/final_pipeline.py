import sys
import os
# Add the root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

from pipeline.total_amount import total_amount_calc
from pipeline.total_count import total_count_calc
from pipeline.status_analysis import transaction_status_analysis
from pipeline.user_analysis import user_analysis_metrics
from pipeline.user_distriution import user_state_distribution
from pipeline.create_pdf import save_images_to_pdf
from config import IMAGE_PATHS, PDF_PATH
from config import DB_URL
import pandas as pd
from sqlalchemy import create_engine


def run_pipeline(merchant_id):
    # Connect and query
    engine = create_engine(DB_URL)
    merged_df = pd.read_sql("SELECT * FROM `reporting-db`.v3_full_report", engine)
    df = merged_df.copy()
    
    # Calculate total amount
    total_amount = total_amount_calc(merged_df, merchant_id)
    print(f"Total Amount: {total_amount}")

    # Calculate total count
    total_count = total_count_calc(merged_df, merchant_id)
    print(f"Total Count: {total_count}")

    # Analyze transaction status
    status_analysis = transaction_status_analysis(merged_df, merchant_id)
    print("Transaction Status Analysis:")
    print(status_analysis)

    # Analyze user metrics
    user_metrics = user_analysis_metrics(df, merged_df, merchant_id)
    print("User Analysis Metrics:")
    print(user_metrics)

    # Analyze user state distribution
    user_distribution = user_state_distribution(merged_df, merchant_id)
    print("User State Distribution:")
    print(user_distribution)

    # Save all images to PDF
    save_images_to_pdf(IMAGE_PATHS, PDF_PATH)

if __name__ == "__main__":
    run_pipeline(merchent_id=3)
    print("Pipeline execution completed successfully.")