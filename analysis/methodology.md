# Methodology

## 3.1 Participants

A total of 17 participants (N = 17) were recruited for this study. Participants were volunteers who provided informed consent before participation. All experimental procedures were conducted in accordance with institutional review board guidelines.

## 3.2 Apparatus

### 3.2.1 Hardware Configuration

The experimental setup utilized a high-performance gaming workstation to ensure consistent performance across all test conditions:

- **CPU**: Intel Core i9-11900K @ 3.5GHz (16 logical cores)
- **GPU**: NVIDIA GeForce RTX 4070 SUPER with 12GB VRAM
- **RAM**: 32GB DDR4
- **Storage**: Samsung SSD 970 EVO Plus 2TB (NVMe)
- **Operating System**: Windows 11 Pro (Build 26200), 64-bit

**Display**:
- Monitor: Alienware AW2524H
- Resolution: 1920×1080 pixels
- Refresh Rate: 500Hz native capability
- Response Time: 0.5ms (G2G)
- Display Interface: DisplayPort

**Input Devices**:
- Mouse: Logitech G502 HERO Gaming Mouse (25,600 DPI sensor)
- Keyboard: Logitech Gaming Keyboard G910 (mechanical switches)
- Audio: onn. USB Headset

### 3.2.2 Software and Latency Injection

**Latency Injection Tool**: NVIDIA NvLatency (input-injector.exe)
- Function: Injects controlled artificial input latency at kernel level
- Precision: Millisecond-accurate latency addition
- Scope: Affects both keyboard and mouse input devices

**Automation Framework**: Custom Python harness (Python 3.13)
- Automated game launching and session management
- Input event monitoring (keyboard and mouse)
- Performance metric extraction (OCR, replay parsing, score capture)
- QoE questionnaire administration

**Games Tested**:
1. Fitts Law Pointing Task (custom browser-based implementation)
2. Feeding Frenzy 2 (casual arcade game)
3. Rocket League (competitive vehicular soccer)
4. Dave the Diver (action-adventure game)
5. Half-Life 2 (first-person shooter)

All games were run at consistent graphical settings to maintain uniform performance across conditions.

## 3.3 Experimental Design

### 3.3.1 Design Overview

The study employed a **within-subjects repeated measures design** where each participant experienced all experimental conditions. This design choice maximizes statistical power and controls for individual differences in gaming skill and latency sensitivity.

**Independent Variable**: Added input latency
- Levels: 0ms (baseline), 75ms, 150ms, 225ms

**Dependent Variables**:
1. **Performance Metrics** (objective, game-specific):
   - Fitts Law: Throughput (bits/second)
   - Feeding Frenzy: Game score
   - Rocket League: Goals scored, replay-derived metrics
   - Dave the Diver: Resource collection (kg)
   - Half-Life 2: Enemies eliminated

2. **Quality of Experience (QoE)** (subjective):
   - Quality Rating: 1-5 Likert scale (1 = very poor, 5 = excellent)
   - Acceptability: Binary response (acceptable/not acceptable)

### 3.3.2 Counterbalancing

To control for order effects, the experiment used **Latin square counterbalancing** at two levels:

1. **Game Order**: The sequence in which games were presented was counterbalanced across participants using a Latin square design (5 games = 5 unique orders).

2. **Latency Order**: Within each game, the order of latency conditions was counterbalanced using a Latin square design (4 latencies = 4 unique orders).

A total of 20 unique experimental schedules were generated (5 game orders × 4 latency orders), ensuring systematic counterbalancing across the participant pool (schedule assigned as `participant_id mod 20`).

### 3.3.3 Trial Structure

For each game, participants completed:

1. **Test Round** (familiarization):
   - No latency injection
   - No performance tracking
   - Purpose: Familiarize participant with game mechanics
   - Duration: Variable (until participant felt comfortable)

2. **Four Measured Rounds**:
   - One round per latency condition (0, 75, 150, 225ms)
   - Performance metrics automatically captured
   - Duration (per game):
     - Fitts Law: 30 seconds
     - Feeding Frenzy: 30 seconds
     - Rocket League: 90 seconds
     - Dave the Diver: 60 seconds
     - Half-Life 2: 30 seconds

After each measured round, participants completed a brief QoE questionnaire before proceeding to the next latency condition.

## 3.4 Games and Tasks

### 3.4.1 Fitts Law Pointing Task

**Genre**: Custom pointing task (browser-based)

**Description**: A custom implementation of the classic Fitts' Law paradigm, where participants rapidly clicked between targets of varying sizes and distances. This task isolates fundamental pointing performance, a critical component of gaming interaction.

**Performance Metric**: Throughput (bits/second), calculated as Index of Difficulty (ID) divided by movement time. Higher throughput indicates better pointing performance.

**Latency Sensitivity Rationale**: Pointing tasks are highly sensitive to latency as they require precise visuomotor coordination. Fitts' Law provides a well-established theoretical framework for understanding speed-accuracy tradeoffs.

**Trial Duration**: 30 seconds per round

### 3.4.2 Feeding Frenzy 2

**Genre**: Casual arcade game

**Description**: Players control a fish that grows by consuming smaller fish while avoiding larger predators. The game demands continuous tracking, rapid directional changes, and opportunistic decision-making.

**Performance Metric**: Game score (accumulated points)

**Latency Sensitivity Rationale**: Fast-paced arcade games require constant visuomotor adjustments and split-second reactions to environmental changes, making them moderately sensitive to input latency.

**Trial Duration**: 30 seconds per round

### 3.4.3 Rocket League

**Genre**: Competitive vehicular soccer game

**Description**: Players control rocket-powered cars to hit a ball into the opponent's goal. Success requires precise timing, spatial prediction, and continuous fine-motor control for both navigation and ball manipulation.

**Performance Metric**: Goals scored; replay data captured for secondary analyses (boost usage, positioning)

**Latency Sensitivity Rationale**: Competitive games with physics-based mechanics are known to be highly sensitive to latency. The game's esports popularity and ranking system indicate the importance of precise timing in competitive play.

**Trial Duration**: 90 seconds per round (longer to allow for meaningful goal-scoring opportunities)

### 3.4.4 Dave the Diver

**Genre**: Action-adventure game with resource management

**Description**: An underwater exploration game where players catch fish using harpoons while managing oxygen and avoiding hazards. Combines aiming mechanics with strategic resource management.

**Performance Metric**: Total weight of fish caught (kg)

**Latency Sensitivity Rationale**: The game blends aim-dependent (harpoon throwing) and navigation-dependent tasks, providing insight into how latency affects gameplay requiring both precision targeting and continuous movement.

**Trial Duration**: 60 seconds per round

### 3.4.5 Half-Life 2

**Genre**: First-person shooter (FPS)

**Description**: A classic FPS where players engage in combat against enemy NPCs using various weapons. Participants played a standardized combat scenario designed for repeatable performance measurement.

**Performance Metric**: Number of enemies eliminated

**Latency Sensitivity Rationale**: FPS games represent one of the most latency-sensitive game genres, requiring rapid target acquisition, tracking, and shooting accuracy. Prior research consistently shows strong latency effects in FPS gameplay.

**Trial Duration**: 30 seconds per round

## 3.5 Procedure

1. **Introduction and Consent** (~5 minutes)
   - Participants arrived at the testing location
   - Study purpose and procedures explained
   - Informed consent obtained
   - Basic demographic information collected (if applicable)

2. **Equipment Familiarization** (~5 minutes)
   - Participants adjusted seating, monitor position, and peripherals
   - Brief overview of the experimental session structure

3. **Game Testing Sequence** (~10-15 minutes per game; ~50-75 minutes total)
   
   For each game (order counterbalanced):
   
   a. **Game Introduction** (~1 minute)
      - Experimenter explained game mechanics and objectives
      - Performance metric clarified
   
   b. **Test Round** (~2-3 minutes)
      - Participant played practice round (no latency injection)
      - Participant indicated readiness to proceed
   
   c. **Post-Test QoE Survey** (~30 seconds)
      - Quality rating (1-5 scale)
      - Acceptability judgment (binary)
   
   d. **Four Measured Rounds** (~30-90 seconds each, depending on game)
      - Latency condition applied (order counterbalanced)
      - Performance automatically captured
      - Inter-round interval: ~10-15 seconds
   
   e. **Post-Round QoE Survey** (after each measured round; ~30 seconds)
      - Quality rating (1-5 scale)
      - Acceptability judgment (binary)

4. **Session Completion** (~2 minutes)
   - Brief debrief
   - Opportunity for participant questions
   - Thanks and dismissal

**Total Session Duration**: Approximately 70-90 minutes per participant

## 3.6 Data Collection

### 3.6.1 Performance Metrics

Performance data were automatically captured using a combination of techniques tailored to each game:

- **Fitts Law**: Results saved directly to CSV by browser-based application
- **Feeding Frenzy & Half-Life 2**: On-screen score extraction via Optical Character Recognition (OCR) using PyTesseract
- **Rocket League**: Replay files (.replay) parsed to JSON format using the `rrrocket` replay parser
- **Dave the Diver**: In-game console commands to extract score, with OCR backup

Screenshots were captured at the end of each round to verify automated data extraction.

### 3.6.2 Quality of Experience (QoE) Data

After each round (test and measured), participants completed a brief questionnaire displayed via a Tkinter GUI:

1. **Quality Rating**: "How would you rate the quality of your experience?" (1-5 scale)
2. **Acceptability**: "Was the experience acceptable?" (Yes/No)

Responses were automatically logged with timestamps.

### 3.6.3 Input Event Logging

Complete input event streams were captured for all measured rounds:

- **Keyboard events**: Timestamp, event type (press/release), key identifier
- **Mouse events**: Timestamp, event type (move/click/scroll), position, button identifier

Input logs enable potential secondary analyses of behavioral adaptation to latency (e.g., changes in mouse velocity, input frequency).

### 3.6.4 Latency Verification

The NvLatency tool logged all injected latency events to stdout/stderr, which were captured to files for each round. These logs serve as verification that the intended latency was correctly applied.

### 3.6.5 Data Backup and Storage

All experimental data were automatically:
- Saved to local storage in a hierarchical directory structure: `experiment/{participant_id}/{session_timestamp}/{game}/{round_timestamp}/`
- Backed up to `~/Documents/fpsci-2025-backup/` after each session

## 3.7 Data Analysis

### 3.7.1 Data Processing

Raw experimental data were processed using custom Python scripts (see `analysis/data_processing.ipynb`):

1. **Data Ingestion**: Automated scanning of experiment directory to catalog all collected data
2. **Quality Control**: Identification of missing or corrupted data files
3. **Metric Extraction**: Game-specific parsing of performance metrics
4. **QoE Extraction**: Parsing of questionnaire responses
5. **Data Merging**: Combination of performance and QoE data into unified analysis datasets
6. **Normalization**: Z-score transformation of performance metrics for cross-game comparisons

### 3.7.2 Statistical Analyses

The following statistical analyses were conducted (see `analysis/statistical_analysis.ipynb`):

1. **Descriptive Statistics**: Means, standard deviations, and ranges for all conditions

2. **Correlation Analysis**: Pearson and Spearman correlations between:
   - Latency and performance
   - Latency and QoE ratings
   - Performance and QoE ratings

3. **Repeated Measures Analysis**: 
   - One-way repeated measures ANOVA with latency as the within-subjects factor
   - Separate analyses for each game and overall (across games)
   - Linear mixed-effects models to account for participant random effects

4. **Post-hoc Comparisons**: Tukey HSD tests for pairwise latency comparisons

5. **Effect Sizes**: Cohen's d calculated for baseline (0ms) vs. each elevated latency condition

Statistical significance was assessed at α = 0.05. All analyses were conducted using Python 3.13 with libraries: pandas, numpy, scipy, statsmodels, matplotlib, and seaborn.

---

## References

Software and tools used:
- Python 3.13 with scientific computing libraries
- NVIDIA NvLatency tool for latency injection
- PyTesseract for OCR
- rrrocket for Rocket League replay parsing
- Custom automation harness (available at: [repository URL if applicable])
