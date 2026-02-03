# FPSci Latency Study - Data Analysis

This directory contains Jupyter notebooks and outputs for analyzing the experimental data from the latency study.

## Directory Structure

```
analysis/
├── data_processing.ipynb          # Data ingestion, cleaning, and preparation
├── statistical_analysis.ipynb     # Correlation, ANOVA, mixed models, effect sizes
├── visualizations.ipynb          # Publication-quality figures
├── methodology.md                # Methodology section for paper
├── processed_data/               # Output from data_processing.ipynb
│   ├── combined_data.csv
│   ├── performance_data.csv
│   ├── qoe_data.csv
│   └── data_inventory.csv
├── results/                      # Output from statistical_analysis.ipynb
│   ├── descriptive_stats_*.csv
│   ├── correlation_results.csv
│   ├── anova_results.csv
│   ├── effect_sizes.csv
│   ├── tukey_*.txt
│   ├── mixed_model_*.txt
│   └── summary_table.*
└── figures/                      # Output from visualizations.ipynb
    ├── performance_vs_latency_by_game.png
    ├── qoe_vs_latency.png
    ├── boxplots_by_latency.png
    ├── individual_trajectories.png
    ├── correlation_heatmap.png
    ├── combined_performance_qoe.png
    └── qoe_by_game_latency.png
```

## Workflow

### Step 1: Data Processing

Run `data_processing.ipynb` to:
- Scan the `../experiment/` directory for all participant data
- Extract performance metrics for each game (Fitts Law throughput, game scores, etc.)
- Extract QoE data (quality ratings and acceptability)
- Merge and clean data
- Generate data quality report
- Export processed datasets to `processed_data/`

**Outputs:**
- `processed_data/combined_data.csv` - Main analysis dataset
- `processed_data/performance_data.csv` - Performance metrics only
- `processed_data/qoe_data.csv` - QoE metrics only
- `processed_data/data_inventory.csv` - Complete data catalog

### Step 2: Statistical Analysis

Run `statistical_analysis.ipynb` to:
- Compute descriptive statistics by latency condition and game
- Perform correlation analyses (latency vs performance, latency vs QoE)
- Conduct repeated measures ANOVA
- Run post-hoc pairwise comparisons (Tukey HSD)
- Calculate effect sizes (Cohen's d)
- Fit linear mixed-effects models accounting for participant random effects

**Outputs:**
- `results/descriptive_stats_*.csv` - Summary statistics tables
- `results/correlation_results.csv` - All correlation coefficients and p-values
- `results/anova_results.csv` - F-statistics and p-values
- `results/effect_sizes.csv` - Cohen's d for all comparisons
- `results/tukey_*.txt` - Pairwise comparison results
- `results/mixed_model_*.txt` - Mixed-effects model summaries
- `results/summary_table.*` - Publication-ready summary (CSV and LaTeX)

### Step 3: Visualizations

Run `visualizations.ipynb` to create:
- Performance vs latency plots (one per game)
- QoE vs latency plots (quality rating and acceptability)
- Box plots showing score distributions
- Individual participant trajectory plots
- Correlation heatmaps
- Combined performance-QoE dual-axis plots
- QoE by game and latency grouped bar charts

**Outputs:**
All figures are saved in both PNG (for presentations) and PDF (for publications) to `figures/`

## Quick Start

```bash
# Make sure you're in the project root
cd /path/to/fpsci-harness

# Install dependencies (if not already done)
uv sync

# Launch Jupyter
jupyter notebook analysis/

# Run notebooks in order:
# 1. data_processing.ipynb
# 2. statistical_analysis.ipynb
# 3. visualizations.ipynb
```

## Data Structure

### Experiment Data (Input)

Raw data is expected in `../experiment/` with this structure:
```
experiment/
└── {participant_id}/
    └── {session_timestamp}/
        └── {game_name}/
            ├── {timestamp}_test/          # Test round
            │   ├── qoe.txt
            │   └── round_end.png
            └── {timestamp}_{latency}ms/   # Measured round
                ├── score.txt / results.csv
                ├── qoe.txt
                ├── kb.csv
                ├── mouse.csv
                ├── nvlatency.stdout.txt
                └── round_end.png
```

### Processed Data (Output)

#### combined_data.csv

Main analysis dataset with columns:
- `participant_id`: Participant identifier (1-17)
- `game`: Game identifier (internal name)
- `game_display`: Game display name (for plots)
- `latency_ms`: Latency condition (0, 75, 150, 225)
- `score`: Raw performance score (game-specific units)
- `score_z`: Z-scored performance (for cross-game comparison)
- `score_pct_of_baseline`: Performance as % of participant's best
- `quality_rating`: QoE quality rating (1-5 scale)
- `acceptable`: Acceptability judgment (0 or 1)

Game-specific columns may also be present (e.g., Fitts Law metrics).

## Key Findings

*[To be filled in after running analyses]*

## Methodology

See `methodology.md` for the complete methodology section suitable for inclusion in a research paper.

## Dependencies

- Python 3.13
- pandas
- numpy
- scipy
- statsmodels
- matplotlib
- seaborn
- jupyter

All dependencies are managed via the project's `pyproject.toml` and can be installed with `uv sync`.

## Notes

- **Missing Data**: Participant 5 is missing Fitts Law data; some participants have incomplete Rocket League data due to automation bugs. The data processing notebook handles these cases gracefully.
- **Statistical Power**: With 17 participants and a within-subjects design, the study has good power to detect medium-to-large effect sizes (d > 0.5).
- **Normalization**: Performance metrics are normalized (z-scored) for cross-game comparisons, but raw scores are used for within-game analyses.

## Citation

If you use these analysis scripts or methods, please cite:

```
[Your paper citation once published]
```

## Contact

For questions about the analysis pipeline, contact [your contact info].
