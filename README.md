# Global Solid Waste Prediction

![Project workflow](workflow.jpg)

This repository is the complete release package for a global solid-waste
prediction workflow.
It provides cleaned input data, executable notebooks, trained model artifacts,
and release-ready result tables for reconstructing historical waste generation
and projecting future waste generation under Shared Socioeconomic Pathway
scenarios.

The workflow covers four main waste streams:

- municipal solid waste (MSW),
- industrial waste (IW),
- construction & demolition waste (CDW)
- agricultural waste (AW).

The pipeline starts from harmonised country-year source data, builds WDI-based
driver features, evaluates model families, selects a TabPFN-based modelling
route, trains final waste-specific models, reconstructs the historical panel,
and produces SSP1-5 projections with uncertainty bands through 2100.

---

## What is included

This release is designed as a self-contained research repository.
It includes the data and model artifacts required to inspect the published
workflow without rerunning every computationally intensive model search.

| Component | Description |
|---|---|
| `workflow.jpg` | Visual roadmap of the data, modelling, reconstruction, and projection workflow. |
| `Step0_Data/` | Source-data staging and baseline cleaning. |
| `Step1_FeaturePool/` | WDI coverage scan and selected feature-panel construction. |
| `Step2_WDI_Features/` | Missing-value treatment for WDI feature panels. |
| `Step3_BuildLongTable/` | Wide-to-long supervised-learning table construction. |
| `Step4_ModelInputs/` | Outer-CV folds, processed train/test inputs, and feature contracts. |
| `Step5_ModelComparison/` | Classical ML, deep-learning, and TabPFN family comparison. |
| `Step6_TabPFNExplainability/` | TabPFN feature analysis, ablation, and route diagnostics. |
| `Step7_ModelTraining/` | Final training assets, preprocessing pipelines, and model artifacts. |
| `Step8_HistoricalCompletion/` | Completed 1990-2024 historical waste panel. |
| `Step9_FutureProjection/` | SSP1-5 future projections and uncertainty bands for 2025-2100. |

Each step directory contains its own `README.md` with step-specific inputs,
outputs, run order, and validation checks.

---

## Main outputs

The most important release outputs are:

- `Step8_HistoricalCompletion/2_Results/0_historical_panel_completed.csv`
  
  A completed country-year historical panel for 1990-2024.
  Observed values are preserved where available, and missing values are filled
  with final model predictions.

- `Step9_FutureProjection/2_Results/1_super_panel_1990_2100.csv`
  
  A historical-plus-future panel before anchor-bias correction.

- `Step9_FutureProjection/2_Results/2_super_panel_1990_2100.csv`
  
  The anchor-corrected super panel used for final scenario analysis.

- `Step9_FutureProjection/2_Results/4_ssp_with_uncertainty_bands.csv`
  
  SSP-level global totals with uncertainty bands derived from temporal
  backtesting.

- `Step9_FutureProjection/2_Results/4_ssp_global_total_summary.csv`
  
  A compact summary table of global SSP trajectories.

---

## Repository design

The repository is organised as an ordered workflow rather than as a software
package.
Each numbered step consumes upstream outputs and writes its own release outputs.
The naming convention is intentionally stable:

- `1_Code/` or `2_Code/` contains executable notebooks,
- `1_Data/` contains staged source data when needed, and
- `2_Results/` or `3_Results/` contains generated release outputs.

The notebooks are committed with cleared execution outputs.
This keeps the repository readable and avoids embedding machine-specific paths
or local runtime state in notebook metadata.

---

## Environment setup

The workflow uses two Python environments.
This separation is intentional because PyCaret and TabPFN/PyTorch have different
dependency constraints.

### Environment A: PyCaret and data-preparation environment

Use this environment for data preparation, WDI feature processing, outer-CV input
construction, PyCaret preprocessing, and classical machine-learning comparisons.
It is used mainly by Steps 0-5 and by the preprocessing parts of Step7.

Recommended environment name: `pycaret3.0`.

```bash
conda create -n pycaret3.0 python=3.8 -y
conda activate pycaret3.0
python -m pip install --upgrade pip
python -m pip install \
  numpy==1.24.4 \
  pandas==1.5.3 \
  scipy==1.10.1 \
  scikit-learn==1.2.2 \
  pycaret==3.2.0 \
  xgboost \
  lightgbm \
  catboost \
  openpyxl \
  joblib \
  tqdm \
  matplotlib
```

Register the environment as a Jupyter kernel:

```bash
python -m pip install ipykernel
python -m ipykernel install --user --name pycaret3.0 --display-name pycaret3.0
```

### Environment B: TabPFN and PyTorch environment

Use this environment for TabPFN model evaluation, explanation, final model
training, historical completion, and SSP projection.
It is used mainly by Steps 5-9 whenever a notebook imports `tabpfn` or `torch`.

Recommended environment name: `tabpfn_env_clean`.

```bash
conda create -n tabpfn_env_clean python=3.10 -y
conda activate tabpfn_env_clean
python -m pip install --upgrade pip
python -m pip install \
  numpy \
  pandas \
  scipy \
  scikit-learn \
  torch \
  tabpfn \
  pycountry \
  openpyxl \
  joblib \
  tqdm \
  matplotlib
```

Register the environment as a Jupyter kernel:

```bash
python -m pip install ipykernel
python -m ipykernel install --user --name tabpfn_env_clean --display-name tabpfn_env_clean
```

For GPU execution, install the PyTorch build that matches your CUDA runtime.
The notebooks automatically use CUDA when it is available and fall back to CPU
otherwise.
GPU execution is recommended for TabPFN-heavy notebooks.

---

## Quick start

Clone the repository:

```bash
git clone https://github.com/iPFAS/Global-solid-waste-prediction.git
cd Global-solid-waste-prediction
```

Open JupyterLab or Jupyter Notebook from the repository root:

```bash
jupyter lab
```

Run notebooks in numerical order from Step0 to Step9.
The recommended order is:

```text
Step0_Data
Step1_FeaturePool
Step2_WDI_Features
Step3_BuildLongTable
Step4_ModelInputs
Step5_ModelComparison
Step6_TabPFNExplainability
Step7_ModelTraining
Step8_HistoricalCompletion
Step9_FutureProjection
```

Each step directory contains a local `README.md` with the exact notebook order.
When a notebook has a preselected kernel, use that kernel.
When no kernel is preselected, use the environment implied by its imports:

- use `pycaret3.0` for PyCaret, preprocessing, and classical ML notebooks, and
- use `tabpfn_env_clean` for TabPFN, PyTorch, historical completion, and future
  projection notebooks.

---

## Step-by-step workflow

### Step0_Data

Stages source data and runs baseline cleaning.
The main output is `3_Results/0_cleaned_baseline.csv`, which defines the cleaned
country-year baseline used by Step1.

### Step1_FeaturePool

Scans World Development Indicators for country-year coverage and constructs the
selected feature panel.
This fixes the feature pool before missing-value treatment.

### Step2_WDI_Features

Fills missing values in the selected WDI feature panel.
The output `2_Results/1_imputed_features_data.csv` is the complete wide feature
table consumed by Step3.

### Step3_BuildLongTable

Converts the wide country-year table into a long supervised-learning table.
The four waste targets are reshaped into waste-type rows with a unified target
column and waste-type indicators.

### Step4_ModelInputs

Builds reproducible outer-CV folds and processed train/test inputs.
This step defines the evaluation frame used by all model-family comparisons.

### Step5_ModelComparison

Compares classical machine-learning models, deep-learning baselines, and TabPFN
candidates under the same Step4 folds.
The consolidated rankings identify the modelling route used downstream.

### Step6_TabPFNExplainability

Analyses the selected TabPFN route using feature ranking, core-feature ablation,
and pooled-versus-per-waste diagnostics.
This step supports the final feature and route choices used by Step7.

### Step7_ModelTraining

Prepares final training assets and exports final preprocessing pipelines and
waste-specific model artifacts.
These artifacts are used directly by historical completion and future projection.

### Step8_HistoricalCompletion

Combines observed records and final model predictions into a completed
1990-2024 historical panel.
Observed values are preserved and only missing historical values are filled.

### Step9_FutureProjection

Builds SSP future drivers, transforms future feature matrices, predicts waste
generation, applies 2024 anchor-bias correction, estimates temporal-backtest
uncertainty, and exports SSP1-5 projections through 2100.

---

## Reproducibility notes

This repository includes both executable notebooks and release output files.
Some model searches and final model training runs are computationally intensive
and can vary across hardware, CUDA availability, and package versions.

For exact inspection of the release results, start from the included outputs in
each `2_Results/` or `3_Results/` directory.
For full recomputation, run notebooks in the ordered workflow above and use the
step-level README files for validation checks.

The final notebooks are committed without stored cell outputs.
If you rerun notebooks, clear outputs again before committing changes.

---

## Citation

If you use this repository, cite the associated study and the GitHub repository.
The repository citation should include the project title, repository URL, and
release date or commit hash used for analysis.

---

## Contact

For questions about the repository, open an issue at:

<https://github.com/iPFAS/Global-solid-waste-prediction/issues>
