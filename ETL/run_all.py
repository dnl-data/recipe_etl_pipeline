from recipe_extraction import extract_recipes
from recipe_transformation import transform_recipes
from recipe_load import load_to_postgres

def run_etl():
    print("\n🚀 Starting full ETL process...\n")

    # Step 1: Extraction
    print("🔍 Step 1: Extracting recipes...")
    try:
        extracted_data = extract_recipes()
        if not extracted_data:
            print("⚠️ No data extracted. Check the source or API.")
            return
        print(f"✅ Extracted {len(extracted_data)} recipes.\n")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return

    # Step 2: Transformation
    print("🛠️ Step 2: Transforming data...")
    try:
        transformed_data = transform_recipes()
        print("✅ Data transformed successfully.\n")
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        return

    # Step 3: Load into PostgreSQL
    print("📦 Step 3: Loading data into PostgreSQL...")
    try:
        load_to_postgres(transformed_data)
        print("✅ Data loaded successfully.\n")
    except Exception as e:
        print(f"❌ Loading failed: {e}")
        return

    print("🎉 ETL process completed successfully.")

if __name__ == "__main__":
    run_etl()
