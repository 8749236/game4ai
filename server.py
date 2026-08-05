"""Standalone world server: keeps the town alive as a background process."""
import sys
import time
from world import start_world

log = sys.argv[1] if len(sys.argv) > 1 else "evidence_kitten.jsonl"
w = start_world(log)
print(f"town is up, logging to {log}", flush=True)
while True:
    time.sleep(3600)
