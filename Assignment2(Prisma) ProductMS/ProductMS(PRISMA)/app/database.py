# app/database.py
from prisma import Prisma

# Step 1: Create Prisma instance
prisma = Prisma()

# Step 2: Startup - connect to DB
async def connect_db():
    """
    Connects to the PostgreSQL database using Prisma ORM.
    Called once when the app starts.
    """
    await prisma.connect()
    print("Database connection established successfully!")

# Step 3: Shutdown - disconnect
async def disconnect_db():
    """
    Gracefully closes the Prisma database connection when the app stops.
    """
    await prisma.disconnect()
    print("Database connection closed successfully!")
