from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import DATABASE_URL

try:
    engine = create_engine(DATABASE_URL, pool_recycle=3600)
except ImportError:
    print("MySQL client not found. Please install mysqlclient.")
    exit(1)
except Exception as e:
    print(f"Error creating database engine: {e}")
    print("Please ensure the MySQL container is running and accessible.")
    exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session_factory = scoped_session(SessionLocal)

def get_db_session():
    """
    Provides a new database session.
    It's the caller's responsibility to close it.
    """
    session = session_factory()
    try:
        yield session
    finally:
        session.close()

def setup_database():
    """
    Executes the create_schema.sql script to set up the database tables.
    """
    print("Setting up database schema...")
    try:
        with open("src/sql/create_schema.sql", "r") as f:
            sql_script = f.read()

        with engine.connect() as connection:
            statements = [s for s in sql_script.split(';') if s.strip()]
            for statement in statements:
                # FIX: Wrap the raw SQL string in text()
                connection.execute(text(statement))
        print("Database schema created successfully.")
    except FileNotFoundError:
        print("ERROR: src/sql/create_schema.sql not found.")
        exit(1)
    except Exception as e:
        print(f"ERROR: Could not set up database schema: {e}")
        exit(1)
