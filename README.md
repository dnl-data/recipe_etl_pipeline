# Recipe ETL Pipeline

This small project focuses on a one-time ETL (Extract, Transform, Load) pipeline that pulls data from an API, performs extensive cleaning on a complex and messy dataset, and loads the results into a local SQL-based data warehouse. Tackling the cleaning step was a real challenge and an essential part of making the data usable — a task I was proud to complete.

## Stack
- **Python/Pandas** - for data extraction and transformation
- **DuckDB** - for lightweight, embedded SQL-based data storage

## Project Scope

<img width="500" height="300" alt="Project Process Schema" src="https://github.com/user-attachments/assets/de7815a8-accd-4dbe-9280-1e6811286498" />

### 1️⃣ EXTRACT

- **API Integration:** Extracting data from Recipe API (https://www.themealdb.com/api.php) in JSON format
- **Data Loading:** Converting JSON response to pandas DataFrame for processing

### 2️⃣ TRANSFORM

- **Data Cleaning:** Removing irrelevant columns, renaming columns, and standardizing case formatting
- **Normalization:** Standardizing ingredient names (e.g., from "almonds" to "almond") and creating separate tables to maintain a normalized database structure
- **Data Conversion:** Creating new columns based on existing data to enhance analytical capabilities

### 3️⃣ LOAD

- **DuckDB Integration:** Loading the cleaned and normalized dataset into a DuckDB data warehouse (embedded SQL database)
- **Data Validation:** Using schema-based organization (`recipes` schema) to maintain data integrity
- **Indexing & Performance Optimization:** DuckDB automatically optimizes columnar storage for fast analytical queries
- **Test Queries:** Ensuring data consistency and identifying any anomalies or errors during the ETL process

## ERD Schema

![image](https://github.com/user-attachments/assets/b29da60a-112d-4d84-8e84-d2c6810145e9)

## How to Run the ETL Project Locally

Follow these steps to run the full ETL pipeline on your machine.

### 1. Clone the repository

Clone the project and navigate into the directory:

```bash
git clone https://github.com/dnl-data/recipe_etl_pipeline.git
cd recipe_etl_pipeline
````

### 2. Create a virtual environment and install dependencies

Create a virtual environment and install required Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the entire ETL pipeline

```bash
python src/run_all.py
```

This script will:

- Extract data from TheMealDB API

- Transform and clean the data

- Load the final data into a DuckDB database (recipe_datawarehouse.duckdb)

### 4. Explore the results

After running the pipeline, you can query the database directly from Python.

Example :

```python
import duckdb
conn = duckdb.connect('recipe_datawarehouse.duckdb')
conn.execute("SELECT * FROM recipes.recipe_table LIMIT 5").df()
```

Or use any DuckDB-compatible tool to explore the data.


**Please consult *data/structured/* to get to the cleaned tables quicker !**

### Optional : Run steps individually
```bash
python src/recipe_extraction.py
python src/recipe_transformation.py
python src/recipe_load.py
```

### Output Files

After a successful run, you will find:

**recipe_datawarehouse.duckdb - The complete DuckDB database**

### Use Cases

Classification models to predict cuisine type from ingredients

Diet classification models based on ingredient combinations

Unsupervised clustering to group similar recipes

NLP techniques for ingredient description analysis

Recipe recommendation systems

Implementation of the data in culinary applications

### Connect with Me

LinkedIn: www.linkedin.com/in/d-ngoma-l-8a8670240

Kaggle Dataset: https://www.kaggle.com/datasets/merveillenl04/recipe-data
