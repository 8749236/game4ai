"""Standalone world server: keeps the town alive as a background process.

Usage: python3 server.py [log_path] [--config cfg.json] [--port-offset N]
"""
import argparse
import time

from config import load_config
from world import start_world

p = argparse.ArgumentParser()
p.add_argument("log", nargs="?", default="evidence.jsonl")
p.add_argument("--config", default=None, help="experiment config JSON")
p.add_argument("--port-offset", type=int, default=0,
               help="shift every port; parallel towns use steps of >=100")
args = p.parse_args()

cfg = load_config(args.config) if args.config else None
w = start_world(args.log, config=cfg, port_offset=args.port_offset)
print(f"town is up (ports +{args.port_offset}), logging to {args.log}", flush=True)
while True:
    time.sleep(3600)
