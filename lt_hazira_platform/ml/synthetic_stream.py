"""Synthetic IoT telemetry streaming simulator."""
import random
import time
from typing import Generator, Dict, Any

def stream_telemetry_events(machine_id: int, count: int = 10) -> Generator[Dict[str, Any], None, None]:
    base_wear = random.uniform(20.0, 75.0)
    for i in range(count):
        base_wear += random.uniform(0.1, 0.5)
        yield {
            "timestamp": time.time(),
            "machine_id": machine_id,
            "vibration_rms": round(random.uniform(1.2, 4.5), 2),
            "bearing_temp_c": round(random.uniform(55.0, 88.0), 1),
            "simulated_wear": round(base_wear, 2)
        }
