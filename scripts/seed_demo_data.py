"""Utility script to verify and seed demo data environment."""
from lt_hazira_platform.core.logging_config import setup_logger
from lt_hazira_platform.sql.verify_database import verify_tables

logger = setup_logger("seed_demo")

def run():
    logger.info("Verifying existing database state...")
    success = verify_tables()
    if success:
        logger.info("Demo environment is primed and healthy.")
    else:
        logger.warning("Database requires regeneration via etl/generate_data.py.")

if __name__ == "__main__":
    run()
