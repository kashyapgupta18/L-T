"""ETL pipeline orchestrator coordinating validation, transformation, and load."""
import time
from lt_hazira_platform.core.logging_config import setup_logger
from lt_hazira_platform.etl.audit_logger import ETLAuditor, ETLAuditRecord

logger = setup_logger("etl_pipeline")

class HaziraETLPipeline:
    def __init__(self):
        self.auditor = ETLAuditor()

    def run_stage(self, name: str, stage_func, *args, **kwargs):
        start = time.time()
        logger.info(f"Starting stage: {name}")
        try:
            result = stage_func(*args, **kwargs)
            duration = round(time.time() - start, 3)
            logger.info(f"Stage completed: {name} in {duration}s")
            self.auditor.log_record(ETLAuditRecord(
                stage=name,
                records_processed=getattr(result, "__len__", lambda: 0)(),
                records_rejected=0,
                duration_seconds=duration,
                status="SUCCESS"
            ))
            return result
        except Exception as e:
            duration = round(time.time() - start, 3)
            logger.error(f"Stage failed: {name} with error: {e}")
            self.auditor.log_record(ETLAuditRecord(
                stage=name,
                records_processed=0,
                records_rejected=0,
                duration_seconds=duration,
                status="FAILED",
                error_message=str(e)
            ))
            raise
