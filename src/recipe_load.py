import duckdb

def load_dataframe_to_duckdb(conn, df, table_name, schema='recipes'):
    """Load a DataFrame into DuckDB table"""
    try:
        # Create schema if it doesn't exist
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        
        # Drop table if exists (replace behavior)
        conn.execute(f"DROP TABLE IF EXISTS {schema}.{table_name}")
        
        # Create table from DataFrame
        conn.register('temp_df', df)
        conn.execute(f"CREATE TABLE {schema}.{table_name} AS SELECT * FROM temp_df")
        conn.unregister('temp_df')
        
        print(f"✅ Successfully loaded {len(df)} records to table '{schema}.{table_name}'")
        return True
    except Exception as e:
        print(f"❌ Error loading {table_name}: {str(e)}")
        return False

def load_to_duckdb(data_dict, schema='recipes', db_path='recipe_datawarehouse.duckdb'):
    """Load all transformed DataFrames into DuckDB database"""
    
    print("Starting DuckDB load process...\n")
    print(f"📁 Database file: {db_path}")
    print(f"📂 Schema: {schema}\n")
    
    # Create connection
    conn = duckdb.connect(db_path)
    
    try:
        # Load each table
        for table_name, df in data_dict.items():
            print(f"Loading {table_name}...")
            success = load_dataframe_to_duckdb(conn, df, table_name, schema)
            if not success:
                print(f"⚠️ Failed to load {table_name}")
        
        # Show summary of loaded tables
        print("\n📊 Loaded tables summary:")
        for table_name in data_dict.keys():
            try:
                result = conn.execute(f"SELECT COUNT(*) FROM {schema}.{table_name}").fetchone()
                print(f"  - {schema}.{table_name}: {result[0]} rows")
            except:
                print(f"  - {schema}.{table_name}: Failed to read")
        
        print("\n✅ All recipe tables loaded successfully!")
        
        # Show list of all tables in database (CORRECTED SYNTAX)
        print("\n📋 All tables in database:")
        try:
            # Method 1: Using SHOW TABLES (lists all tables from all schemas)
            tables = conn.execute("SHOW TABLES").df()
            print(tables.to_string(index=False))
            
            # Method 2: Filter by schema using information_schema (more precise)
            print(f"\n📋 Tables in '{schema}' schema only:")
            tables_filtered = conn.execute(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = '{schema}'
            """).df()
            print(tables_filtered.to_string(index=False))
            
        except Exception as e:
            print(f"Could not list tables: {e}")
        
    except Exception as e:
        print(f"❌ Load process failed: {e}")
        raise
    finally:
        conn.close()
        print("\n🔒 Connection closed.")

# For testing standalone
if __name__ == "__main__":
    from recipe_transformation import transform_recipes
    from recipe_extraction import extract_recipes
    
    print("Testing load module...")
    raw_data = extract_recipes()
    transformed = transform_recipes(raw_data)
    load_to_duckdb(transformed)