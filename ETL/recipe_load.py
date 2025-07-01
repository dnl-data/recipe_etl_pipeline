import pandas as pd
from sqlalchemy import create_engine
from psycopg2 import sql

from recipe_transformation import transform_recipes

# Get all transformed data in one line (just like extraction example)
transformed_data = transform_recipes()


# Database connection parameters
DB_USER = 'username'
DB_PASS = 'password'
DB_HOST = 'localhost'
DB_PORT = 'xxxx'
DB_NAME = 'your_database'


# Create SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


def load_dataframe_to_db(df, table_name, if_exists='replace'):
    """
    Load DataFrame to PostgreSQL database
    
    Parameters:
    df: pandas DataFrame - the data to load
    table_name: str - name of the target table in database
    if_exists: str - 'replace', 'append', or 'fail'
    """
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


def load_all_recipe_tables():
    """Load all transformed recipe tables to database"""
    
    # Dictionary of DataFrames and their corresponding table names
    tables_to_load = {
        'recipe_table': recipe_table,
        'ingredient_table': ingredient_table,
        'recipe_ingredient_table': recipe_ingredient_table,
        'type_diet_tables': type_diet_table,
        'type_course_table': type_course_table,
        'type_cuisine_table': type_cuisine_table
    }
    
    print("Starting database load process...")

    
    # Load each table
    for table_name, df in tables_to_load.items():
        print(f"Loading {table_name}...")
        load_dataframe_to_db(df, table_name)
    
    print("✅ All recipe tables loaded successfully!")

