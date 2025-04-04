# Recipe ETL Pipeline
This small project focuses on building an ETL (Extract, Transform, Load) pipeline to pull data from an API, clean it, and load it into a SQL-based data warehouse.

This repository outlines the setup of an ETL pipeline for a recipe database.

## 1️⃣ ETL Pipeline [Python : pandas]
**Extract**

Data is pulled from an Recipe API (https://www.themealdb.com/api.php) | json to dataframe

**Transform**

Cleaning: Removing irrelevant columns, renaming columns and lowering cases.

Normalization: Standardizing ingredient names (e.g., "sugar" to "granulated sugar") & Creating separate tables to maintain a normalized database structure.

Data Conversion: Creating new columns based on a column.


**Load**

After transformation, the clean data is loaded into PostgreSQL

## 2️⃣ Indexing & Performance Optimization [PostgreSQL]
To ensure fast querying and reporting, indexes are set up for frequently used columns such as recipe_id, ingredient_id... This helps speed up searches and aggregations when performing complex queries or joining multiple tables.

## 3️⃣ Data Validation & Quality Checks  [PostgreSQL]
**SQL Constraints**

To maintain data integrity, SQL constraints are applied, such as:

NOT NULL: Ensuring no critical fields are left empty.

FOREIGN KEY: Ensuring referential integrity between related tables (e.g., linking ingredients to specific recipes).

**Data Consistency**

+ Test queries (aggregate, filter ,join...) are executed to ensure data consistency and to identify any anomalies or errors that might have occurred during the ETL process 

+ Data visualisation to see what is in the data warehouse. (PowerBI dashboard connected to the PostgreSQL database)
