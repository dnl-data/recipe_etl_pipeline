# Recipe ETL Pipeline
This small project focuses on an one-time ETL (Extract, Transform, Load) pipeline that pulls data from an API, performs extensive cleaning on a complex and messy dataset, and loads the results into a SQL-based data warehouse. Tackling the cleaning step was a real challenge and an essential part of making the data usable — a task I was proud to complete.


## Technologies Used
**Python/Pandas -** for data extraction and transformation.

**PostgreSQL -** for relational data storage


## Project Scope

![Project Process Schema](https://github.com/user-attachments/assets/5d06e28b-6846-44ea-9ea1-2f59434057f7)

### 1️⃣ EXTRACT

* **API Integration:** Extracting data from Recipe API (https://www.themealdb.com/api.php) in JSON format.
* **Data Loading:** Converting JSON response to pandas DataFrame for processing.


### 2️⃣ TRANSFORM

* **Data Cleaning:** Removing irrelevant columns, rename columns, and standardize case formatting.

* **Normalization:** Standardizing ingredient names (e.g., from "granulated sugar" to "sugar") and create separate tables to maintain normalized database structure.

* **Data Conversion:** Creating new columns based on existing data to enhance analytical capabilities.


### 3️⃣ LOAD

* **PostgreSQL Integration:** Loading the cleaned and normalized dataset into PostgreSQL data warehouse.
  
* **Data Validation:** Applying SQL constraints (FOREIGN KEY) to maintain data integrity and ensure referential integrity between related tables. 
  
* **Indexing & Performance Optimization:** Setting up indexes for frequently used columns such as recipe_id, ingredient_id to ensure fast querying and reporting, speeding up searches and aggregations for complex queries and table joins.

* **Test Queries:** Ensuring data consistency and identify any anomalies or errors during the ETL process.

## ERD Schema

![image](https://github.com/user-attachments/assets/b29da60a-112d-4d84-8e84-d2c6810145e9)

## How to Run the ETL Project Locally

Follow these steps to run the full ETL pipeline on your machine.

### 1. Clone the repository

Clone the project and navigate into the directory:

```
git clone https://github.com/dnl-data/recipe_etl_pipeline.git
cd recipe_etl_pipeline
```

### 2. 🐍 Create a virtual environment and install dependencies

Create a virtual environment and install required Python packages:

```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows: venv\Scripts\activate
```
Install dependencies:

```
pip install -r requirements.txt
```

### 3. Set up your PostgreSQL database

Make sure PostgreSQL is installed and running.  
Then create a new database (e.g., `recipes_db`) using your preferred tool (pgAdmin, DBeaver, CLI, etc.).

### 4. Configure your `.env` file

Create a `.env` file in the root directory and add your PostgreSQL credentials:

```
DB_USER=your_username
DB_PASS=your_password
DB_HOST=your_host
DB_PORT=your_port #5432 by default
DB_NAME=recipes_db
```

### 5. Run the entire ETL pipeline

Execute the main pipeline script:

```
python ETL/run_all.py
```

This script will:

* Extract data from TheMealDB API  
* Transform and clean the data  
* Load the final data into your PostgreSQL database  

### Optional: Run steps individually

You can also run each script separately if needed:

```
python ETL/recipe_extraction.py
python ETL/recipe_transformation.py
python ETL/recipe_load.py
```


## Use cases
Classification models to predict cuisine type from ingredients

Diet classification models based on ingredient combinations

Unsupervised clustering to group similar recipes

NLP techniques for ingredient description analysis

Recipe recommendation systems

Implementation of the data in culinary applications



### Connect with me
**LinkedIn :** www.linkedin.com/in/d-ngoma-l-8a8670240 

**Datasets also available on Kaggle :** https://www.kaggle.com/datasets/merveillenl04/recipe-data/data
