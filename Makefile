.PHONY: help install lint test run-app run-api clean

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  lint       - Run linters (flake8, black)"
	@echo "  test       - Run test suite"
	@echo "  run-app    - Launch Streamlit dashboard"
	@echo "  run-api    - Launch FastAPI prediction service"
	@echo "  clean      - Remove temporary files and caches"

install:
	pip install -r requirements.txt

lint:
	python -m flake8 . || true

test:
	python -m unittest discover tests

run-app:
	streamlit run lt_hazira_platform/app/app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
