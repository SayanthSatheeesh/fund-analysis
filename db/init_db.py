from db.connection import get_engine
from sqlalchemy import text
import os

def init_db():
    engine = get_engine()
    migrations_dir = 'db/migrations'
    
    if not os.path.exists(migrations_dir):
        print(f"Migrations directory not found at {migrations_dir}")
        return

    # Get all .sql files sorted
    migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
    
    db_type = os.getenv('DB_TYPE', 'sqlite').lower()
    
    with engine.connect() as conn:
        print(f"Initializing {db_type} database...")
        
        for migration_file in migration_files:
            print(f"Running migration: {migration_file}")
            path = os.path.join(migrations_dir, migration_file)
            
            with open(path, 'r') as f:
                sql = f.read()
            
            # Dialect adjustments for SQLite
            if db_type == 'sqlite':
                sql = sql.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
            
            # Execute statements
            for statement in sql.split(';'):
                clean_statement = statement.strip()
                if clean_statement:
                    try:
                        conn.execute(text(clean_statement))
                    except Exception as e:
                        # For SQLite, ignore "already exists" errors during re-runs
                        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                            continue
                        print(f"Error in {migration_file}: {e}")
            
            conn.commit()
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
