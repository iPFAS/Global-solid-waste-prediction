# Step5_ModelComparison — model-family evaluation

## What this step does

Step5 compares model families under the fixed Step4 outer-CV design. It checks the input contract, evaluates classical machine-learning models, deep-learning baselines, and TabPFN variants, then collects a unified family ranking.

The step identifies the modeling strategy used for explainability and final training in later steps.

## Run order

1. `1_Code/0_input_contract_check.ipynb` — validates required input files and feature contracts.
2. `1_Code/1_ml_family_compare.ipynb` — evaluates classical ML models.
3. `1_Code/2_dl_family_compare.ipynb` — evaluates deep-learning models.
4. `1_Code/3_tabpfn_family_compare.ipynb` — evaluates TabPFN candidates.
5. `1_Code/4_collect_family_ranking.ipynb` — consolidates metrics and ranks model families.

## Main inputs

- Processed fold inputs and feature contracts from `Step4_ModelInputs/2_Results/`.
- Shared Step5 utilities in `1_Code/_step5_shared.py`.

## Main outputs

- Per-family metrics, predictions, and artifacts under `2_Results/`.
- Consolidated model-family ranking tables.

## Validation focus

- Confirm that all model families evaluate the same outer folds.
- Confirm that metrics use the same raw and log target definitions.
- Confirm that ranking uses stable metric priority rules.

## Reproducibility notes

- `_step5_shared.py` is intentionally retained because multiple notebooks import common metric and artifact helpers.
- Some model evaluations can be compute intensive and environment-sensitive.
