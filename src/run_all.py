from recipe_extraction import extract_recipes
from recipe_transformation import transform_recipes
from recipe_load import load_to_duckdb

def run_etl():
    print("\n🚀 Starting full ETL process...\n")

    # Step 1: Extraction
    print("Step 1: Extracting recipes from API...")
    try:
        extracted_data = extract_recipes()
        if not extracted_data:
            print("❌ No data extracted. Check the API connection.")
            return False
        print(f"✅ Extracted {len(extracted_data)} recipes.\n")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False

    # Step 2: Transformation
    print("Step 2: Transforming data...")
    try:
        transformed_data = transform_recipes(extracted_data)
        print("✅ Data transformed successfully.\n")
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        return False

    # Step 3: Load into DuckDB
    print("Step 3: Loading data into DuckDB...")
    try:
        load_to_duckdb(transformed_data)
        print("✅ Data loaded successfully.\n")
    except Exception as e:
        print(f"❌ Loading failed: {e}")
        return False

    print("🎉 ETL process completed successfully!")
    return True

if __name__ == "__main__":
    success = run_etl()
    if not success:
        print("\n⚠️ ETL pipeline failed. Please check the errors above.")
        exit(1)
    else:
        print("\n✨ Pipeline finished. Database ready for queries!")
        exit(0)