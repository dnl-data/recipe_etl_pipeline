import pandas as pd
import duckdb
from recipe_transformation import transform_recipes

# Get transformed data
transformed_data = transform_recipes()

# Create DuckDB connection
conn = duckdb.connect()

def load_dataframe_to_duckdb(conn, df, table_name, if_exists='replace'):
    try:
        if if_exists == 'replace':
            conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Register DataFrame and create table from it
        conn.register('temp_df', df)
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_df")
        conn.unregister('temp_df')
        
        print(f"✅ Successfully loaded {len(df)} records to table '{table_name}'")
    except Exception as e:
        print(f"❌ Error loading {table_name}: {str(e)}")
        raise

def load_to_duckdb(data_dict):
    print("Starting DuckDB load process...\n")
    for table_name, df in data_dict.items():
        print(f"Loading {table_name}...")
        load_dataframe_to_duckdb(conn, df, table_name)
    
    return conn

# Run 
if __name__ == "__main__":
    conn = load_to_duckdb(transformed_data)