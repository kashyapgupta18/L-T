"""ETL execution benchmark script."""
import time
from lt_hazira_platform.core.logging_config import setup_logger
from lt_hazira_platform.core.db_connection import execute_query

logger = setup_logger("benchmark_etl")

def run_benchmarks():
    logger.info("Starting analytical query performance benchmarks...")
    start = time.time()
    execute_query("SELECT COUNT(*) FROM fact_production;")
    read_dur = (time.time() - start) * 1000
    logger.info(f"Production row count read completed in {read_dur:.2f}ms")

if __name__ == "__main__":
    run_benchmarks()
