import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_engine():
    """
    Returns a SQLAlchemy engine based on environment configuration.
    Defaults to SQLite if PostgreSQL is not configured or unavailable.
    """
    db_type = os.getenv('DB_TYPE', 'sqlite').lower()
    
    if db_type == 'postgresql':
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASS', 'password')
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        name = os.getenv('DB_NAME', 'fund_analysis')
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    else:
        # Default to local SQLite database
        db_url = "sqlite:///fund_analysis.db"
        print(f"Connecting to {db_url}")
    
    return create_engine(db_url)

def get_session():
    """
    Creates and returns a new SQLAlchemy session.
    """
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    # Test connection
    try:
        engine = get_engine()
        with engine.connect() as conn:
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"Database connection failed: {e}")
