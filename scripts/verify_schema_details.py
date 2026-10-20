"""Verify schema details: spatial indexes, foreign keys, and check constraints."""
import asyncio
from backend.app.core.database import engine
from sqlalchemy import text


async def main():
    async with engine.connect() as conn:
        # 1. Spatial Indexes
        res_idx = await conn.execute(text("""
            SELECT tablename, indexname, indexdef 
            FROM pg_indexes 
            WHERE tablename IN ('dim_state', 'dim_district', 'dim_training_center') 
              AND indexdef LIKE '%gist%'
        """))
        print("=== SPATIAL GIST INDEXES ===")
        for row in res_idx.fetchall():
            print(f" - {row[0]}: {row[1]}")

        # 2. Check Constraints
        res_chk = await conn.execute(text("""
            SELECT conrelid::regclass AS table_name, conname, pg_get_constraintdef(oid)
            FROM pg_constraint
            WHERE contype = 'c'
            ORDER BY table_name, conname
        """))
        print("\n=== CHECK CONSTRAINTS ===")
        for row in res_chk.fetchall():
            print(f" - {row[0]}: {row[1]} -> {row[2]}")

        # 3. Foreign Keys
        res_fk = await conn.execute(text("""
            SELECT conrelid::regclass AS table_name, conname, pg_get_constraintdef(oid)
            FROM pg_constraint
            WHERE contype = 'f'
            ORDER BY table_name, conname
        """))
        print(f"\n=== FOREIGN KEYS (Total: {len(res_fk.fetchall())}) ===")


if __name__ == "__main__":
    asyncio.run(main())
