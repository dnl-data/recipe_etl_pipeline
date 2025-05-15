from sqlalchemy import create_engine
from psycopg2 import sql

DB_USER = 'username'
DB_PASS = 'password'
DB_HOST = 'localhost'
DB_PORT = 'xxxx'
DB_NAME = 'your_database'

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# 2. Preparing the DataFrames (example with recipe_ingredient_table)
df = recipe_ingredient_table.copy()

# 3. Optimal data type conversion (example with recipe_ingredient_table)
dtype_mapping = {
    'recipe_id': 'INTEGER',
    'ingredient_id': 'INTEGER'
    # Add other columns as needed
}

# 4. Writing to PostgreSQL with error handling (example with recipe_ingredient_table)
try:
    df.to_sql(
        name='recipe_ingredients',
        con=engine,
        if_exists='replace',
        index=False,
        dtype=dtype_mapping,
        method='multi',
        chunksize=300
    )
    print("Data successfully written to PostgreSQL")
except Exception as e:
    print(f"Error writing to PostgreSQL: {e}")
finally:
    engine.dispose()
