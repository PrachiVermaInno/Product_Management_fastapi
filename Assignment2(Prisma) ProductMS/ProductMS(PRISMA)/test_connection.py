from prisma import Prisma
import asyncio

db = Prisma()

async def main():
    try:
        await db.connect()
        print("✅ Connected successfully to PostgreSQL via Prisma!")
    except Exception as e:
        print("❌ Connection failed:", e)
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
