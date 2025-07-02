import pandas as pd
from sqlalchemy import create_engine
from recipe_transformation import transform_recipes
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get transformed data
transformed_data = transform_recipes()


# Database connection parameters from environment
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


# Create SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def load_dataframe_to_db(df, table_name, if_exists='replace'):
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,
            index=False,
            method='multi',
            chunksize=1000
        )
        print(f"✅ Successfully loaded {len(df)} records to table '{table_name}'")
    except Exception as e:
        print(f"❌ Error loading {table_name}: {str(e)}")
        raise

def load_to_postgres(data_dict):
    print("Starting database load process...\n")
    for table_name, df in data_dict.items():
        print(f"Loading {table_name}...")
        load_dataframe_to_db(df, table_name)
    print("✅ All recipe tables loaded successfully!\n")


# Run 
if __name__ == "__main__":
    load_to_postgres(transformed_data)
