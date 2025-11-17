# Data Engineering Assessment

Welcome!  
This exercise evaluates your core **data-engineering** skills:

| Competency | Focus                                                         |
| ---------- | ------------------------------------------------------------- |
| SQL        | relational modelling, normalisation, DDL/DML scripting        |
| Python ETL | data ingestion, cleaning, transformation, & loading (ELT/ETL) |

---

## 0 Prerequisites & Setup

> **Allowed technologies**

- **Python ≥ 3.8** – all ETL / data-processing code
- **MySQL 8** – the target relational database
- **Pydantic** – For data validation
- List every dependency in **`requirements.txt`** and justify selection of libraries in the submission notes.

---

## 1 Clone the skeleton repo

```
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
```

✏️ Note: Rename the repo after cloning and add your full name.

**Start the MySQL database in Docker:**

```
docker-compose -f docker-compose.initial.yml up --build -d
```

- Database is available on `localhost:3306`
- Credentials/configuration are in the Docker Compose file
- **Do not change** database name or credentials

For MySQL Docker image reference:
[MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

- You are provided with a raw JSON file containing property records is located in data/
- Each row relates to a property. Each row mixes many unrelated attributes (property details, HOA data, rehab estimates, valuations, etc.).
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.
- Use the supplied Field Config.xlsx (in data/) to understand business semantics.

### Task

- **Normalize the data:**

  - Develop a Python ETL script to read, clean, transform, and load data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place your scripts in `src/`
  - The scripts should take the initial json to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

---

## Submission Guidelines

- Edit the section to the bottom of this README with your solutions and instructions for each section at the bottom.
- Ensure all steps are fully **reproducible** using your documentation
- DO NOT MAKE THE REPOSITORY PUBLIC. ANY CANDIDATE WHO DOES IT WILL BE AUTO REJECTED.
- Create a new private repo and invite the reviewer https://github.com/mantreshjain and https://github.com/siddhuorama

---

**Good luck! We look forward to your submission.**

## Solutions and Instructions (Filed by Candidate)

This solution consists of a Python ETL script that performs the following actions:

- Connects to the MySQL database specified in `docker-compose.initial.yml`.

- Executes the `src/sql/create_schema.sql` script to drop any existing tables and create a fresh, normalized 6-table schema (`properties`, `leads`, `valuations`, `hoa`, `rehab`, `taxes`).

- Reads the raw `fake_property_data_new.json` file from the `data/` directory.

- Validates each row of the JSON data using Pydantic models (`src/models.py`) to ensure data integrity and handle type coercion (e.g., converting `Neighborhood_Rating` from an int to a str).

- Transforms each valid raw property object into multiple normalized Pydantic models (e.g., Property, Lead, Valuation, etc.), separating the 1-to-1 and 1-to-many relationships.

- Loads these normalized models into the MySQL database using SQLAlchemy for efficient, transactional insertion.

- Commits the transaction upon successful completion and prints a summary report of all loaded data.

---

## Dependency Justification (`requirements.txt`)

### **pydantic**
Used for robust data validation, parsing, and transformation. It ensures that the raw data from the JSON file conforms to expected types and structures (as defined in `src/models.py`) before any database operations occur. It was essential for catching data-type mismatches (like `Neighborhood_Rating`).

### **sqlalchemy**
Used as the SQL toolkit to communicate with the MySQL database. It provides a reliable way to create an engine, manage sessions, and execute both raw SQL (for schema creation) and parameterized inserts (for data loading).

### **mysql-connector-python**
This is the pure-Python MySQL driver for SQLAlchemy. It was chosen over `mysqlclient` to ensure the project runs on any system (Windows, Mac, Linux) without requiring C++ build tools or other system-level dependencies.

### **pandas**
This library is included in `requirements.txt` as it is an industry-standard tool for data analysis. While not used in the final, optimized ETL script (which processes data row-by-row for memory efficiency), it is invaluable for the initial data exploration and investigation phase.

---

## How to Run the Solution

Ensure you have Python 3.8+ and Docker installed.

---

### 1. Install Python Dependencies

It is highly recommended to use a virtual environment.

# Create a virtual environment
```
python -m venv venv
```
## Activate it
```
venv\Scripts\activate
```

# Install the required libraries
```
pip install -r requirements.txt
```
2. Start the MySQL Database
This command will start the empty MySQL container in the background.


```
docker compose up --build -d
```

3. CRITICAL: Wait for the Database
After running the command, wait 20–30 seconds.
The container starts instantly, but the MySQL server inside it needs time to initialize, create the home_db, and set up the db_user.

4. Run the ETL Script
Run the etl.py script as a Python module from the project's root directory.
This ensures all src... imports work correctly.
```
python -m src.etl
```
You will see log output in your terminal as the script runs.
It will first create the schema and then process and load all 10,088 properties.

The final output should look like this:
```
=== Starting ETL Process ===
Setting up database schema...
Database schema created successfully.
Loading raw data from data/fake_property_data_new.json...
Loaded 10088 raw property records.
Starting data processing and loading...

--- ETL Process Complete ---
Successfully processed and loaded: 10088 properties
Total leads loaded: 10088
Total valuations loaded: 24898
Total rehab items loaded: 20219
Total HOA records loaded: 10100
Total tax records loaded: 10088
=== ETL Process Finished ===
```
---

How to Verify the Data
You can connect to the now-populated database using any SQL client (DBeaver, MySQL Workbench, etc.).

Connection Details:
```
Host: localhost
Port: 3306
Database: home_db
User: db_user
Password: 6equj5_db_user
```
Sample SQL Queries for Verification
1. Check the total counts to match the ETL log
```
SELECT 'properties' AS table_name, COUNT(*) AS total_rows FROM properties
UNION ALL
SELECT 'leads', COUNT(*) FROM leads
UNION ALL
SELECT 'valuations', COUNT(*) FROM valuations
UNION ALL
SELECT 'rehab', COUNT(*) FROM rehab
UNION ALL
SELECT 'hoa', COUNT(*) FROM hoa
UNION ALL
SELECT 'taxes', COUNT(*) FROM taxes;
```
2. View a fully joined property record
```
SELECT
    p.property_title,
    p.city,
    p.state,
    p.neighborhood_rating,
    l.source AS lead_source,
    v.zestimate,
    v.list_price,
    r.paint,
    r.roof_flag,
    h.hoa_fee
FROM
    properties p
LEFT JOIN
    leads l ON p.property_id = l.property_id
LEFT JOIN
    valuations v ON p.property_id = v.property_id
LEFT JOIN
    rehab r ON p.property_id = r.property_id
LEFT JOIN
    hoa h ON p.property_id = h.property_id
WHERE
    p.property_id = 100;
```
Stop the Database
When you are finished, you can stop the database container by running:

```
docker compose down -v
```
