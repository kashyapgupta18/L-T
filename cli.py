"""Unified Command Line Interface for L&T Hazira Platform."""
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="L&T Hazira Smart Manufacturing CLI")
    parser.add_argument("command", choices=["test", "verify-db", "run-app", "run-api"], help="Command to execute")
    args = parser.parse_args()

    if args.command == "test":
        sys.exit(subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"]).returncode)
    elif args.command == "verify-db":
        from lt_hazira_platform.sql.verify_database import verify_tables
        verify_tables()
    elif args.command == "run-app":
        subprocess.run(["streamlit", "run", "lt_hazira_platform/app/app.py"])
    elif args.command == "run-api":
        subprocess.run(["uvicorn", "lt_hazira_platform.api.main:app", "--reload"])

if __name__ == "__main__":
    main()
