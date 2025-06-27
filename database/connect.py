import pandas as pd
from sqlalchemy import create_engine
import os
import sys

# Add the root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)
from config import DB_URL

# Connect and query
engine = create_engine(DB_URL)
query = "SELECT * FROM `reporting-db`.v3_full_report"

df = pd.read_sql(query, engine)
print(df.head())