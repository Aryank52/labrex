"""CLI Runner for LABREX database seed framework."""
import asyncio
import logging
from backend.app.core.database import AsyncSessionFactory
from backend.app.services.data.seed_framework import seed_reference_and_fixtures

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("labrex.seed_runner")


async def main():
    logger.info("Starting LABREX reference and benchmark fixture seed...")
    async with AsyncSessionFactory() as session:
        try:
            stats = await seed_reference_and_fixtures(session)
            logger.info("Seed completed successfully! Summary of records processed:")
            for table, count in stats.items():
                logger.info(f" - {table}: {count} records verified")
        except Exception as e:
            logger.error(f"Seed execution failed: {e}", exc_info=True)
            raise


if __name__ == "__main__":
    asyncio.run(main())
