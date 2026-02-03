# Quick Start Guide - FPSci Latency Analysis

## Prerequisites

```bash
# Make sure you're in the project root
cd /path/to/fpsci-harness

# Install dependencies (if needed)
uv sync
```

## Running the Analysis (3 Steps)

### Step 1: Process Raw Data (5-10 minutes)

```bash
jupyter notebook analysis/data_processing.ipynb
```

**What it does:**
- Scans `experiment/` directory for all participant data
- Extracts performance metrics from each game
- Extracts QoE responses
- Cleans and merges data
- Generates data quality report

**Output:**
- `analysis/processed_data/combined_data.csv` (main dataset)
- `analysis/processed_data/performance_data.csv`
- `analysis/processed_data/qoe_data.csv`
- `analysis/processed_data/data_inventory.csv`

**Look for:** Data quality report showing missing data, completeness by participant/game

### Step 2: Run Statistical Tests (2-5 minutes)

```bash
jupyter notebook analysis/statistical_analysis.ipynb
```

**What it does:**
- Descriptive statistics
- Correlation analysis (Pearson & Spearman)
- ANOVA (repeated measures)
- Post-hoc tests (Tukey HSD)
- Effect sizes (Cohen's d)
- Mixed-effects models

**Output:**
- `analysis/results/correlation_results.csv` ← **Report these r values!**
- `analysis/results/anova_results.csv` ← **Report F and p values!**
- `analysis/results/effect_sizes.csv` ← **Report Cohen's d!**
- `analysis/results/summary_table.csv` ← **Use in paper!**
- `analysis/results/tukey_*.txt`
- `analysis/results/mixed_model_*.txt`

**Look for:** p-values < 0.05 (significant), correlation strengths, effect sizes

### Step 3: Generate Figures (2-5 minutes)

```bash
jupyter notebook analysis/visualizations.ipynb
```

**What it does:**
- Creates 7 publication-quality figures
- Saves as PNG (presentations) and PDF (papers)

**Output:**
- `analysis/figures/performance_vs_latency_by_game.png` ← **Figure 1**
- `analysis/figures/qoe_vs_latency.png` ← **Figure 2**
- `analysis/figures/boxplots_by_latency.png` ← **Figure 3**
- `analysis/figures/individual_trajectories.png` ← **Figure 4**
- `analysis/figures/correlation_heatmap.png` ← **Figure 5**
- `analysis/figures/combined_performance_qoe.png` ← **Figure 6**
- `analysis/figures/qoe_by_game_latency.png` ← **Figure 7**

**Look for:** Clear trends, significant differences, outliers

## Key Results to Report

After running all three notebooks, you'll have:

### 1. Sample & Data Quality
- **N** = ? participants (after exclusions)
- **Total observations** = ? (participants × games × latencies)
- **Missing data:** Document which participants/games

### 2. Main Effects (From ANOVA)
- **Performance:** F(?, ?) = ?, p = ? ← Is latency effect significant?
- **QoE Quality:** F(?, ?) = ?, p = ?

### 3. Correlations (From correlation_results.csv)
- **Latency vs Performance:** r = ?, p = ? ← Negative? Strong?
- **Latency vs QoE:** r = ?, p = ?
- **Performance vs QoE:** r = ?, p = ?

### 4. Effect Sizes (From effect_sizes.csv)
- **0ms vs 75ms:** d = ? ← Small (0.2), Medium (0.5), or Large (0.8)?
- **0ms vs 150ms:** d = ?
- **0ms vs 225ms:** d = ?

### 5. Per-Game Differences (From figures)
- Which game was **most affected** by latency?
- Which game was **least affected**?
- Why? (Discuss game mechanics)

### 6. Acceptability Threshold (From QoE plot)
- At what latency did acceptability drop below 50%?
- What % found 225ms acceptable?

## Typical Results Pattern (Based on Literature)

**You'll likely see:**
- ✅ Negative correlation between latency and performance (r ≈ -0.3 to -0.7)
- ✅ Negative correlation between latency and QoE (r ≈ -0.5 to -0.8)
- ✅ Significant ANOVA (p < .001)
- ✅ Medium to large effect sizes (d > 0.5) for 225ms vs 0ms
- ✅ FPS/pointing games most affected
- ✅ Casual games moderately affected
- ✅ High individual variability

## Paper Sections

### Methodology
Use `analysis/methodology.md` - it's already written!

### Results
Structure:
1. Data quality (N, exclusions)
2. Descriptive stats (Table 1: summary_table.csv)
3. Latency effects on performance (Figure 1, correlations, ANOVA)
4. Latency effects on QoE (Figure 2, correlations, ANOVA)
5. Game-specific effects (Figure 5: heatmap)
6. Individual differences (Figure 4)
7. Performance-QoE relationship (Figure 6)

### Discussion
- Compare to Liu & Claypool, Long & Gutwin
- Explain game-specific differences
- Discuss acceptability threshold
- Note limitations (sample size, automation bugs)
- Implications for game design, cloud gaming

## Troubleshooting

**Problem:** Notebooks won't run
- **Solution:** `uv sync` to install dependencies

**Problem:** No data found
- **Solution:** Check that `experiment/` directory exists with participant folders

**Problem:** Missing performance metrics
- **Solution:** Check data quality report in Step 1 - some games have bugs

**Problem:** Figures look weird
- **Solution:** Adjust matplotlib parameters in visualizations.ipynb

**Problem:** Statistical results seem off
- **Solution:** Check for outliers, verify data cleaning in Step 1

## Quick Commands

```bash
# Create output directories (if needed)
mkdir -p analysis/processed_data analysis/results analysis/figures

# Run all notebooks from command line (requires nbconvert)
jupyter nbconvert --to notebook --execute analysis/data_processing.ipynb
jupyter nbconvert --to notebook --execute analysis/statistical_analysis.ipynb
jupyter nbconvert --to notebook --execute analysis/visualizations.ipynb

# Or use Jupyter Lab for better experience
jupyter lab analysis/
```

## Time Estimates

- **Setup:** 5 minutes (dependencies)
- **Data processing:** 5-10 minutes (depends on data size)
- **Statistical analysis:** 2-5 minutes
- **Visualizations:** 2-5 minutes
- **Interpreting results:** 30-60 minutes
- **Writing Results section:** 2-4 hours
- **Total:** ~3-5 hours to complete analysis and draft results

## Need Help?

See `analysis/README.md` for detailed documentation.

Good luck! 📊🎮
