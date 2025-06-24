# Recipe ETL Pipeline
This small project focuses on an ETL (Extract, Transform, Load) pipeline that pulls data from an API, performs extensive cleaning on a complex and messy dataset, and loads the results into a SQL-based data warehouse. Tackling the cleaning step was a real challenge and an essential part of making the data usable — a task I was proud to complete.

## Technologies Used
**Python/Pandas -** for data manipulation and transformation.

**PostgreSQL -** for relational data storage

## Project Scope
### 1️⃣ EXTRACT
* **API Integration:** Extract data from Recipe API (https://www.themealdb.com/api.php) in JSON format.
* **Data Loading:** Convert JSON response to pandas DataFrame for processing.

### 2️⃣ TRANSFORM
* Data Cleaning: Remove irrelevant columns, rename columns, and standardize case formatting.

● Normalization: Standardize ingredient names (e.g., "sugar" to "granulated sugar") and create separate tables to maintain normalized database structure.

● Data Conversion: Create new columns based on existing data to enhance analytical capabilities.


**Load**

After transformation, the clean data is loaded into PostgreSQL

### 2️⃣ Indexing & Performance Optimization
To ensure fast querying and reporting, indexes are set up for frequently used columns such as recipe_id, ingredient_id... This helps speed up searches and aggregations when performing complex queries or joining multiple tables.

### 3️⃣ Data Validation & Quality Checks
**SQL Constraints**

To maintain data integrity, SQL constraints are applied, such as:

NOT NULL: Ensuring no critical fields are left empty.

FOREIGN KEY: Ensuring referential integrity between related tables (e.g., linking ingredients to specific recipes).

**Data Consistency**

Test queries (aggregate, filter ,join...) are executed to ensure data consistency and to identify any anomalies or errors that might have occurred during the ETL process 


