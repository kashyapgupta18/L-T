# Troubleshooting & FAQ

## Common Issues
1. **SQLite Database Locked**: WAL mode is enabled by default to prevent read/write locks.
2. **Missing Dependencies**: Run `pip install -r requirements.txt` to sync requirements.
3. **Model Prediction Fallback**: If `failure_model.joblib` is not yet trained, the system utilizes heuristic scoring.
