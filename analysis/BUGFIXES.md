# Data Processing Notebook - Bug Fixes Applied

## Issues Fixed

### 1. Rocket League Replay Parsing Error
**Problem:** The replay parsing function was returning a dictionary instead of extracting specific score values, causing `TypeError: complex() first argument must be a string or a number, not 'list'` when calculating z-scores.

**Solution:** 
- Updated `parse_rocket_league_replay()` to properly extract player statistics from `properties.PlayerStats[0]`
- Extracts: goals, score, shots, saves, assists
- Falls back to `Team1Score` if PlayerStats not available
- Primary metric is now `goals` (number of goals scored)

### 2. Score Extraction Logic
**Problem:** When replay data was extracted, the score assignment used `replay_data.get("goals", replay_data.get("score"))` which could return the entire dictionary if neither key existed.

**Solution:**
- Added explicit type checking to ensure score is a number (int or float)
- Only assigns score if it's a valid numeric value
- Prevents non-numeric values from entering the dataset

### 3. Z-Score Calculation Robustness
**Problem:** If all scores in a game were identical (std = 0), z-score calculation would fail with division by zero.

**Solution:**
- Created `safe_zscore()` function that handles edge cases:
  - Returns 0 for all values when std = 0 (all scores identical)
  - Handles NaN values gracefully
  - Uses proper pandas Series return

### 4. Percent of Baseline Calculation
**Problem:** Lambda function inside transform was not returning proper pandas Series.

**Solution:**
- Created `safe_pct_of_max()` function
- Returns proper pandas Series with correct index
- Handles zero/negative max values

## Files Modified

- `analysis/data_processing.ipynb` - Updated parsing functions and normalization logic

## Files Created

- `analysis/check_rocket_league.py` - Diagnostic script to inspect replay JSON structure

## Testing Recommendations

After these fixes, run the notebook again and verify:

1. ✅ No TypeError when calculating z-scores
2. ✅ Rocket League data appears in performance_df
3. ✅ All score values are numeric (no lists or dicts)
4. ✅ Z-scores calculated successfully for all games
5. ✅ No warnings about division by zero

## Rocket League Metrics Available

From the replay files, you can now access:
- **goals**: Primary performance metric (recommended)
- **score**: In-game score (includes goals, assists, saves, etc.)
- **shots**: Number of shot attempts
- **saves**: Number of saves made
- **assists**: Number of assists

**Recommendation:** Use `goals` as the primary metric for Rocket League since it's the clearest measure of successful performance.

## Next Steps

1. Re-run `data_processing.ipynb` from the beginning
2. Check the output to ensure Rocket League data is properly extracted
3. Proceed to `statistical_analysis.ipynb`
4. If any games still have issues, you can skip them or use alternative metrics

## Known Limitations

- Participant 5 is still missing Fitts Law data (as expected)
- Some participants may have incomplete Rocket League data due to automation bugs
- The notebook handles these gracefully by excluding affected rounds from analysis
