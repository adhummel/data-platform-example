"""Initialize database schemas and tables."""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    """Create necessary schemas in the database."""
    db_url = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    
    engine = create_engine(db_url)
    
    schemas = ['raw_data', 'staging', 'intermediate', 'marts']
    
    with engine.connect() as conn:
        for schema in schemas:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            print(f"✓ Created schema: {schema}")
        conn.commit()
    
    print("\n✅ Database setup complete!")
    print("\n📋 Next steps:")
    print("  1. Download GTD data from https://www.start.umd.edu/gtd/contact/")
    print("  2. Place the file at: data/raw/globalterrorismdb.xlsx")
    print("  3. Run: dagster dev")

if __name__ == "__main__":
    setup_database()
