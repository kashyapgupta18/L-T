# Deployment Guide

## Running with Docker Compose
```bash
docker-compose up --build
```
- Streamlit Dashboard: `http://localhost:8501`
- FastAPI REST Microservice: `http://localhost:8000/docs`

## Local Development
```bash
python -m venv venv
pip install -r requirements.txt
python cli.py run-app
```
