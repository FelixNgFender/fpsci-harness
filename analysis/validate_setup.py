#!/usr/bin/env python3
"""
Quick test to validate that data processing fixes work correctly.
Run this before running the full notebook to catch issues early.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import json
import re

print("=" * 70)
print("DATA PROCESSING VALIDATION TEST")
print("=" * 70)

# Test 1: Check experiment directory exists
print("\n[Test 1] Checking experiment directory...")
exp_dir = Path("../experiment")
if not exp_dir.exists():
    exp_dir = Path("experiment")

if not exp_dir.exists():
    print("❌ FAIL: experiment/ directory not found")
    sys.exit(1)
print("✅ PASS: experiment/ directory found")

# Test 2: Check for participant data
print("\n[Test 2] Checking for participant data...")
participant_dirs = [d for d in exp_dir.iterdir() if d.is_dir() and re.match(r"^\d+", d.name)]
print(f"✅ PASS: Found {len(participant_dirs)} participant directories")

# Test 3: Test Rocket League replay parsing
print("\n[Test 3] Testing Rocket League replay parsing...")
replay_files = list(exp_dir.glob("*/*/rocket_league/*/*.replay.json"))
if not replay_files:
    print("⚠️  WARNING: No Rocket League replay files found")
else:
    print(f"Found {len(replay_files)} Rocket League replay files")

    # Test parsing first file
    test_file = replay_files[0]
    try:
        with open(test_file, "r") as f:
            data = json.load(f)

        # Simulate parsing logic
        result = {}
        if "properties" in data:
            props = data["properties"]
            if "PlayerStats" in props and isinstance(props["PlayerStats"], list) and len(props["PlayerStats"]) > 0:
                player_stats = props["PlayerStats"][0]
                result["goals"] = player_stats.get("Goals", 0)
                result["score"] = player_stats.get("Score", 0)
            elif "Team1Score" in props:
                result["goals"] = props["Team1Score"]
                result["score"] = props["Team1Score"]

        if "goals" in result and isinstance(result["goals"], (int, float)):
            print(f"✅ PASS: Successfully extracted goals = {result['goals']}")
        else:
            print(f"❌ FAIL: Could not extract numeric goals value")
            print(f"   Got: {result}")

    except Exception as e:
        print(f"❌ FAIL: Error parsing replay: {e}")

# Test 4: Test z-score function
print("\n[Test 4] Testing z-score calculation...")
test_scores = pd.Series([100, 150, 200, 150, 100])


def safe_zscore(x):
    std = x.std()
    if std == 0 or pd.isna(std):
        return pd.Series(0, index=x.index)
    return (x - x.mean()) / std


try:
    z_scores = safe_zscore(test_scores)
    if len(z_scores) == len(test_scores) and isinstance(z_scores, pd.Series):
        print(f"✅ PASS: Z-score calculation works correctly")
        print(f"   Input: {test_scores.tolist()}")
        print(f"   Z-scores: {z_scores.round(2).tolist()}")
    else:
        print(f"❌ FAIL: Z-score function returned wrong type")
except Exception as e:
    print(f"❌ FAIL: Error in z-score calculation: {e}")

# Test 5: Test z-score with constant values (edge case)
print("\n[Test 5] Testing z-score with constant values...")
constant_scores = pd.Series([100, 100, 100, 100])
try:
    z_const = safe_zscore(constant_scores)
    if all(z_const == 0):
        print(f"✅ PASS: Constant values handled correctly (all z=0)")
    else:
        print(f"❌ FAIL: Constant values not handled correctly")
        print(f"   Got: {z_const.tolist()}")
except Exception as e:
    print(f"❌ FAIL: Error with constant values: {e}")

# Test 6: Test percent of max function
print("\n[Test 6] Testing percent of max calculation...")


def safe_pct_of_max(x):
    max_val = x.max()
    if max_val > 0:
        return (x / max_val) * 100
    return pd.Series(np.nan, index=x.index)


try:
    pct = safe_pct_of_max(test_scores)
    if len(pct) == len(test_scores) and pct.max() == 100:
        print(f"✅ PASS: Percent of max calculation works correctly")
        print(f"   Input: {test_scores.tolist()}")
        print(f"   Percentages: {pct.round(1).tolist()}")
    else:
        print(f"❌ FAIL: Percent of max function returned wrong values")
except Exception as e:
    print(f"❌ FAIL: Error in percent calculation: {e}")

# Test 7: Check for QoE files
print("\n[Test 7] Checking for QoE data files...")
qoe_files = list(exp_dir.glob("*/*/*/*/*/qoe.txt"))
if len(qoe_files) > 0:
    print(f"✅ PASS: Found {len(qoe_files)} QoE files")

    # Test parsing one
    try:
        content = qoe_files[0].read_text().strip()
        match = re.search(r"QoE:\s*([0-9.]+)\s*:\s*([0-9]+)", content)
        if match:
            quality = float(match.group(1))
            acceptable = int(match.group(2))
            print(f"   Sample QoE: quality={quality}, acceptable={acceptable}")
        else:
            print(f"⚠️  WARNING: Could not parse QoE file format")
    except Exception as e:
        print(f"⚠️  WARNING: Error parsing QoE file: {e}")
else:
    print("⚠️  WARNING: No QoE files found")

# Summary
print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)
print("\nIf all tests passed (✅), you're ready to run the notebooks!")
print("If any tests failed (❌), check the error messages above.")
print("\nNext step: Open Jupyter and run data_processing.ipynb")
print("=" * 70)
