"""Sample Python client script querying the Hazira REST API."""
import json
import urllib.request

def test_api_client(base_url: str = "http://localhost:8000"):
    # Health check
    with urllib.request.urlopen(f"{base_url}/health") as resp:
        print("Health status:", resp.read().decode())

    # Prediction
    payload = json.dumps({
        "wear_index": 78.5,
        "days_since_last_maintenance": 14.0,
        "prev_shift_downtime": 1.5,
        "avg_downtime_last_5_shifts": 0.8,
        "machine_age_years": 6.2
    }).encode("utf-8")
    
    req = urllib.request.Request(
        f"{base_url}/predictions/risk",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print("Prediction output:", resp.read().decode())
    except Exception as e:
        print("API server not active; client demo ready.")

if __name__ == "__main__":
    test_api_client()
