#!/usr/bin/env python3
"""
Quick diagnostic script to check Rocket League replay data structure.
Run this to understand what's in the replay JSON files.
"""

from pathlib import Path
import json

# Find a Rocket League replay file
experiment_dir = Path("experiment")
replay_files = list(experiment_dir.glob("*/*/rocket_league/*/*.replay.json"))

if not replay_files:
    print("No Rocket League replay files found!")
else:
    print(f"Found {len(replay_files)} Rocket League replay files\n")

    # Check first replay file
    replay_file = replay_files[0]
    print(f"Examining: {replay_file}\n")

    with open(replay_file, "r") as f:
        data = json.load(f)

    print("Top-level keys:")
    for key in data.keys():
        print(f"  - {key}")

    print("\nProperties (if exists):")
    if "properties" in data:
        props = data["properties"]
        print(f"  Type: {type(props)}")
        if isinstance(props, dict):
            for key, value in list(props.items())[:10]:  # First 10 keys
                print(f"  - {key}: {type(value).__name__} = {value if not isinstance(value, (dict, list)) else '...'}")
        elif isinstance(props, list):
            print(f"  List with {len(props)} items")
            if props:
                print(f"  First item type: {type(props[0])}")

    print("\nLooking for score-related fields...")

    def find_score_fields(d, prefix=""):
        """Recursively find fields that might contain scores."""
        if isinstance(d, dict):
            for key, value in d.items():
                key_lower = key.lower()
                if any(term in key_lower for term in ["goal", "score", "point", "stat"]):
                    print(f"  {prefix}{key}: {value}")
                if isinstance(value, (dict, list)) and prefix.count(".") < 2:  # Limit depth
                    find_score_fields(value, f"{prefix}{key}.")
        elif isinstance(d, list) and d and prefix.count(".") < 2:
            find_score_fields(d[0], f"{prefix}[0].")

    find_score_fields(data)

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
print("If Rocket League replays don't have clear score data,")
print("you may need to either:")
print("1. Skip Rocket League in the analysis")
print("2. Use a different metric (e.g., number of shots, saves)")
print("3. Manually extract scores from screenshots")
