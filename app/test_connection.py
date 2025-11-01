from app.config.database import engine, SessionLocal
from sqlalchemy import text

print("Testing database connection...")

try:
    # Test 1: Engine connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()
        print("✅ Database connected successfully!")
        print(f"PostgreSQL version: {version[0][:50]}...")  # First 50 chars
    
    # Test 2: Session creation
    db = SessionLocal()
    print("✅ Session created successfully!")
    db.close()
    
    print("\n🎉 All tests passed! Database is ready.")
    
except Exception as e:
    print(f"\n❌ Connection failed!")
    print(f"Error: {e}")
    print("\nCheck:")
    print("1. PostgreSQL is running")
    print("2. Database 'product_management' exists")
    print("3. .env file has correct DATABASE_URL")
