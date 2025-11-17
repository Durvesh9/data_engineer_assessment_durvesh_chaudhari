DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "db_user"
DB_PASSWORD = "6equj5_db_user"
DB_NAME = "home_db"

# Construct the SQLAlchemy database URL
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
