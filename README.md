# Recipe ETL Pipeline
This small project focuses on an ETL (Extract, Transform, Load) pipeline that pulls data from an API, performs extensive cleaning on a complex and messy dataset, and loads the results into a SQL-based data warehouse. Tackling the cleaning step was a real challenge and an essential part of making the data usable — a task I was proud to complete.

## Technologies Used
**Python/Pandas -** for data manipulation and transformation.

**PostgreSQL -** for relational data storage

## Project Scope
### 1️⃣ EXTRACT

* **API Integration:** Extracting data from Recipe API (https://www.themealdb.com/api.php) in JSON format.
* **Data Loading:** Converting JSON response to pandas DataFrame for processing.


### 2️⃣ TRANSFORM

* **Data Cleaning:** Removing irrelevant columns, rename columns, and standardize case formatting.

* **Normalization:** Standardizing ingredient names (e.g., "sugar" to "granulated sugar") and create separate tables to maintain normalized database structure.

* **Data Conversion:** Creating new columns based on existing data to enhance analytical capabilities.


### 3️⃣ LOAD

* **PostgreSQL Integration:** Loading the cleaned and normalized dataset into PostgreSQL data warehouse.
  
* **Indexing & Performance Optimization:** Setting up indexes for frequently used columns such as recipe_id, ingredient_id to ensure fast querying and reporting, speeding up searches and aggregations for complex queries and table joins.
  
* **Data Validation & Quality Checks:** Applying SQL constraints (NOT NULL, FOREIGN KEY) to maintain data integrity and ensure referential integrity between related tables. Execute test queries (aggregate, filter, join) to ensure data consistency and identify any anomalies or errors during the ETL process.



