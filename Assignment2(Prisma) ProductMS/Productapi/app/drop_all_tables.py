from app.database import engine, Base
from app.models import company, category, product

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print(" All tables dropped successfully.")
