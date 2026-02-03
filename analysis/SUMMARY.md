# FPSci Latency Study - Analysis Pipeline Summary

## What Was Created

I've built a complete data processing and analysis pipeline for your latency study. Here's what you now have:

### 📊 Three Jupyter Notebooks

1. **`data_processing.ipynb`** (~250 lines)
   - Scans all 17 participants' data from `experiment/` directory
   - Extracts performance metrics (game-specific parsing)
   - Extracts QoE data (quality ratings + acceptability)
   - Handles missing data gracefully (Participant 5 issues, buggy games)
   - Creates normalized scores (z-scores, percent of baseline)
   - Generates comprehensive data quality report
   - Exports clean CSVs to `analysis/processed_data/`

2. **`statistical_analysis.ipynb`** (~300 lines)
   - Descriptive statistics by latency and game
   - Correlation analyses (Pearson & Spearman)
   - Repeated measures ANOVA (overall and per-game)
   - Tukey HSD post-hoc tests
   - Cohen's d effect sizes
   - Linear mixed-effects models (accounts for participant random effects)
   - Exports results to `analysis/results/`

3. **`visualizations.ipynb`** (~400 lines)
   - Performance vs latency (5 subplots, one per game)
   - QoE vs latency (quality rating + acceptability bar chart)
   - Box plots with swarm overlays
   - Individual participant trajectories (17 subplots)
   - Correlation heatmap (game-specific)
   - Combined performance-QoE dual-axis plot
   - QoE by game and latency grouped bar chart
   - All figures exported as PNG + PDF to `analysis/figures/`

### 📝 Documentation

4. **`methodology.md`**
   - Complete methodology section for your paper
   - Hardware specs from DxDiag.txt
   - Software and latency injection details
   - Experimental design (within-subjects, Latin square)
   - Game descriptions with rationale
   - Detailed procedure
   - Data collection methods
   - Statistical analysis plan

5. **`analysis/README.md`**
   - Quick start guide
   - Workflow instructions
   - Directory structure overview
   - Data format documentation
   - Dependency information

## How to Use

### Step 1: Run Data Processing

```bash
# From project root
cd fpsci-harness
jupyter notebook analysis/data_processing.ipynb
```

Run all cells. This will:
- ✅ Scan experiment directory
- ✅ Generate data quality report (missing data inventory)
- ✅ Extract all performance metrics
- ✅ Extract all QoE responses
- ✅ Create `analysis/processed_data/combined_data.csv`

**Expected output:** ~200-300 rows (17 participants × 5 games × 4 latencies, minus missing data)

### Step 2: Run Statistical Analysis

```bash
jupyter notebook analysis/statistical_analysis.ipynb
```

Run all cells. This will:
- ✅ Calculate descriptive stats
- ✅ Test correlations between latency and outcomes
- ✅ Run ANOVA to test significance
- ✅ Compute effect sizes (how big is the latency impact?)
- ✅ Fit mixed-effects models
- ✅ Save all results to `analysis/results/`

**Key outputs:**
- `correlation_results.csv` - r values and p-values
- `anova_results.csv` - F-statistics
- `effect_sizes.csv` - Cohen's d values
- `summary_table.csv` + `.tex` - Publication table

### Step 3: Generate Visualizations

```bash
jupyter notebook analysis/visualizations.ipynb
```

Run all cells. This will:
- ✅ Create 7 publication-quality figures
- ✅ Save as both PNG (presentations) and PDF (papers)
- ✅ All figures in `analysis/figures/`

## What You'll Learn

### Expected Findings (Based on Literature)

1. **Performance Degrades with Latency**
   - Negative correlation: Higher latency → Lower performance
   - Effect likely strongest in Fitts Law and Half-Life 2 (aiming tasks)
   - May be weaker in Dave the Diver (mixed mechanics)

2. **QoE Decreases with Latency**
   - Negative correlation: Higher latency → Lower quality ratings
   - Acceptability threshold somewhere between 75-150ms (based on prior work)
   - May see individual differences (some players more tolerant)

3. **Game-Specific Sensitivity**
   - FPS and pointing tasks most affected
   - Casual games (Feeding Frenzy) moderately affected
   - Some games may show non-linear effects

4. **Performance ≠ QoE (Always)**
   - Performance may degrade objectively, but QoE may not drop until threshold
   - Or vice versa: Players notice latency before performance suffers

### Key Metrics to Report in Your Paper

From the analysis outputs, you'll have:

1. **Correlation coefficients** (r values)
   - Latency → Performance: r = ? (expect negative)
   - Latency → QoE: r = ? (expect negative)
   - Per-game variations

2. **ANOVA results** (significance testing)
   - F-statistic and p-value for latency effect
   - Tells you if differences are statistically significant

3. **Effect sizes** (practical significance)
   - Cohen's d for 0ms vs 225ms: d = ? 
   - Interpretation: Small (0.2), Medium (0.5), Large (0.8)

4. **Descriptive stats** (the numbers)
   - Mean ± SD for each latency condition
   - Acceptability percentages

## Integration with Your Paper

### Background Section (Already Written)
Your background section is excellent! It covers:
- ✅ Latency injection methods (EvLag, NvLatency)
- ✅ QoE measurement approaches (subjective + objective)
- ✅ Game selection criteria (genre, FOV, input modality)

### Related Work (Already Written)
Good coverage of:
- ✅ Prior latency studies (FPS focus)
- ✅ Multi-game studies (Flanagan et al., Liu et al.)

### Methodology (Now Complete)
Use `analysis/methodology.md` - it includes:
- ✅ Participants (N=17)
- ✅ Apparatus (hardware from DxDiag.txt)
- ✅ Experimental design (within-subjects, counterbalancing)
- ✅ Games & tasks (descriptions + rationale)
- ✅ Procedure (step-by-step)
- ✅ Data collection (automated metrics)
- ✅ Analysis plan (statistical methods)

### Results Section (To Be Written After Running Notebooks)

**Suggested structure:**

#### 4. Results

**4.1 Data Quality**
- Report N final (after exclusions)
- Note missing data (Participant 5, etc.)

**4.2 Descriptive Statistics**
- Table 1: Mean ± SD for each latency condition (use `summary_table.csv`)
- Report overall trends

**4.3 Effect of Latency on Performance**
- Figure 1: Performance vs latency by game (use `performance_vs_latency_by_game.png`)
- Report correlation: "Latency was negatively correlated with performance (r = X, p < .001)"
- ANOVA: "Latency had a significant effect on performance, F(3, N) = X, p < .001"
- Effect size: "The effect of 225ms latency compared to baseline was large, d = X"

**4.4 Effect of Latency on QoE**
- Figure 2: QoE vs latency (use `qoe_vs_latency.png`)
- Report correlation and ANOVA
- Acceptability threshold: "Acceptability dropped below 50% at Xms"

**4.5 Game-Specific Effects**
- Figure 3: Correlation heatmap (use `correlation_heatmap.png`)
- Discuss which games were most/least affected
- Rocket League vs Feeding Frenzy comparison

**4.6 Individual Differences**
- Figure 4: Individual trajectories (use `individual_trajectories.png`)
- Note variability: Some participants more latency-tolerant

**4.7 Relationship Between Performance and QoE**
- Figure 5: Combined plot (use `combined_performance_qoe.png`)
- Mixed-effects model: "Performance predicted QoE, β = X, p < .001"

### Discussion Section (To Be Written)

**Suggested points:**
- How do your findings compare to prior work (Liu & Claypool, Long & Gutwin)?
- Which games were most sensitive? Why?
- Did you find a latency threshold for acceptability?
- Individual differences: Why are some players more tolerant?
- Limitations: Automation bugs, sample size, lab setting
- Implications: Game developers, cloud gaming platforms

## File Checklist

✅ `analysis/data_processing.ipynb` - Data ingestion and cleaning
✅ `analysis/statistical_analysis.ipynb` - Statistics and hypothesis testing
✅ `analysis/visualizations.ipynb` - Publication figures
✅ `analysis/methodology.md` - Methodology section for paper
✅ `analysis/README.md` - Usage guide
✅ `analysis/SUMMARY.md` - This file

## Next Steps

1. **Run the notebooks** (in order: processing → statistics → visualizations)
2. **Review outputs** (check figures, verify results make sense)
3. **Write Results section** using generated tables and figures
4. **Write Discussion section** interpreting your findings
5. **Proofread Methodology** (customize `methodology.md` as needed)

## Questions?

If you encounter issues:
- Check `analysis/README.md` for troubleshooting
- Verify experiment data is in `../experiment/` directory
- Ensure Python dependencies are installed (`uv sync`)

Good luck with your paper! 🚀
