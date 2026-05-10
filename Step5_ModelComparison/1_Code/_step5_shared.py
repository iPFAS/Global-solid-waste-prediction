from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score


TARGET_COL = "Target_Log"
TARGET_RAW_COL = "Waste_Generation_t"
INNER_FOLDS = 3
OUTER_FOLDS = (1, 2, 3, 4, 5)
META_COLUMNS = ["row_uid", "Country Code", "Year", "WasteFlag", "outer_fold"]
INNER_INDEX_REQUIRED_COLUMNS = ["row_uid", "Year", "inner_fold", "split"]
PRED_LOG_COL = "Prediction_Log"
PRED_RAW_COL = "Prediction_Raw"
FAMILY_RESULT_DIRS = {
    "input_contract": "0_input_contract_check",
    "ml": "1_ml_family_compare",
    "dl": "2_dl_family_compare",
    "tabpfn": "3_tabpfn_family_compare",
    "collect": "4_collect_family_ranking",
}


def _require_columns(frame: pd.DataFrame, required_columns: list[str], frame_name: str) -> None:
    missing_columns = [column for column in required_columns if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"{frame_name} is missing required columns: {missing_columns}")


def load_full_feature_processed(
    step4_root: Path,
    outer_fold: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[str]]:
    processed_dir = step4_root / f"fold_{int(outer_fold)}" / "full_feature_unified" / "processed"
    train_df = pd.read_csv(processed_dir / "0_train_processed.csv")
    test_df = pd.read_csv(processed_dir / "0_test_processed.csv")
    inner_index = pd.read_csv(processed_dir / "0_inner_timeseries_fold_index.csv")
    feature_columns = pd.read_csv(processed_dir / "0_feature_columns.csv")

    if "feature" not in feature_columns.columns:
        raise KeyError("0_feature_columns.csv must contain a 'feature' column")

    required_model_columns = [*META_COLUMNS, TARGET_COL, TARGET_RAW_COL]
    _require_columns(train_df, required_model_columns, "train_df")
    _require_columns(test_df, required_model_columns, "test_df")
    _require_columns(inner_index, INNER_INDEX_REQUIRED_COLUMNS, "inner_index")

    selected_features = feature_columns["feature"].astype(str).tolist()
    train_feature_missing = [feature for feature in selected_features if feature not in train_df.columns]
    test_feature_missing = [feature for feature in selected_features if feature not in test_df.columns]
    if train_feature_missing or test_feature_missing:
        raise ValueError(
            "feature contract contains columns missing from processed inputs: "
            f"train_missing={train_feature_missing}, test_missing={test_feature_missing}"
        )

    return (
        train_df,
        test_df,
        inner_index,
        selected_features,
    )


def build_pycaret_setup_kwargs(
    model_train: pd.DataFrame,
    target_col: str,
    keep_features: list[str],
    ignore_features: list[str],
    categorical_features: list[str],
    session_id: int,
) -> dict[str, object]:
    return {
        "data": model_train,
        "target": target_col,
        "ignore_features": list(ignore_features),
        "keep_features": list(keep_features),
        "categorical_features": list(categorical_features),
        "imputation_type": "simple",
        "numeric_imputation": "median",
        "normalize": True,
        "remove_multicollinearity": False,
        "fold_strategy": "timeseries",
        "fold": INNER_FOLDS,
        "data_split_shuffle": False,
        "fold_shuffle": False,
        "train_size": 0.999999,
        "memory": False,
        "verbose": False,
        "html": False,
        "n_jobs": 4,
        "session_id": int(session_id),
    }


def save_model_artifact(model, artifact_path: Path) -> None:
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, artifact_path)


def batched_predict_log(model, x, batch_size: int = 256) -> np.ndarray:
    if hasattr(x, "to_numpy"):
        x = x.to_numpy()
    x = np.asarray(x)
    if x.ndim != 2:
        raise RuntimeError(f"expected 2D feature matrix, got shape={x.shape}")
    if len(x) == 0:
        return np.asarray([], dtype=float)
    if len(x) <= int(batch_size):
        return np.asarray(model.predict(x), dtype=float).reshape(-1)

    prediction_parts: list[np.ndarray] = []
    for start in range(0, len(x), int(batch_size)):
        end = min(start + int(batch_size), len(x))
        prediction_parts.append(np.asarray(model.predict(x[start:end]), dtype=float).reshape(-1))
    return np.concatenate(prediction_parts, axis=0)


def ensure_family_result_dir(step5_root: Path, family_key: str) -> Path:
    if family_key not in FAMILY_RESULT_DIRS:
        raise KeyError(f"unknown family_key: {family_key}")
    result_dir = Path(step5_root) / "2_Results" / FAMILY_RESULT_DIRS[family_key]
    result_dir.mkdir(parents=True, exist_ok=True)
    return result_dir


def build_prediction_frame(
    test_df: pd.DataFrame,
    prediction_log: np.ndarray,
    outer_fold: int,
    model_family: str,
    model_id: str,
    run_role: str,
) -> pd.DataFrame:
    actual_log = pd.to_numeric(test_df[TARGET_COL], errors="raise").to_numpy(dtype=float)
    actual_raw = pd.to_numeric(test_df[TARGET_RAW_COL], errors="raise").to_numpy(dtype=float)
    prediction_log = np.asarray(prediction_log, dtype=float).reshape(-1)
    if len(prediction_log) != len(test_df):
        raise ValueError(
            f"prediction length mismatch: expected {len(test_df)}, got {len(prediction_log)}"
        )

    prediction_raw = np.expm1(prediction_log)
    return pd.DataFrame(
        {
            "outer_fold": int(outer_fold),
            "model_family": str(model_family),
            "model_id": str(model_id),
            "run_role": str(run_role),
            "row_uid": test_df["row_uid"].astype(str),
            "Country Code": test_df["Country Code"].astype(str),
            "Year": pd.to_numeric(test_df["Year"], errors="raise").astype(int),
            "WasteFlag": test_df["WasteFlag"].astype(str),
            "Actual_Log": actual_log,
            "Actual_Raw": actual_raw,
            PRED_LOG_COL: prediction_log,
            PRED_RAW_COL: prediction_raw,
        }
    )


def compute_regression_metrics(prediction_frame: pd.DataFrame) -> dict[str, float]:
    actual_raw = pd.to_numeric(prediction_frame["Actual_Raw"], errors="raise").to_numpy(dtype=float)
    pred_raw = pd.to_numeric(prediction_frame[PRED_RAW_COL], errors="raise").to_numpy(dtype=float)
    actual_log = pd.to_numeric(prediction_frame["Actual_Log"], errors="raise").to_numpy(dtype=float)
    pred_log = pd.to_numeric(prediction_frame[PRED_LOG_COL], errors="raise").to_numpy(dtype=float)

    denom = max(float(np.abs(actual_raw).sum()), 1e-9)
    waste_rows: list[float] = []
    for _, waste_group in prediction_frame.groupby("WasteFlag", sort=True):
        waste_actual = pd.to_numeric(waste_group["Actual_Raw"], errors="raise").to_numpy(dtype=float)
        waste_pred = pd.to_numeric(waste_group[PRED_RAW_COL], errors="raise").to_numpy(dtype=float)
        waste_denom = max(float(np.abs(waste_actual).sum()), 1e-9)
        waste_rows.append(float(np.abs(waste_actual - waste_pred).sum()) / waste_denom)

    return {
        "WAPE_micro": float(np.abs(actual_raw - pred_raw).sum()) / denom,
        "R2_log": float(r2_score(actual_log, pred_log)),
        "WAPE_macro": float(np.mean(waste_rows)),
        "R2_original": float(r2_score(actual_raw, pred_raw)),
        "MAE_original": float(mean_absolute_error(actual_raw, pred_raw)),
    }


def summarize_fold_metrics(metrics_df: pd.DataFrame) -> pd.DataFrame:
    if metrics_df.empty:
        raise ValueError("metrics_df must not be empty")

    summary_df = (
        metrics_df.groupby(["model_family", "model_id", "run_role"], as_index=False)
        .agg(
            WAPE_micro_mean=("WAPE_micro", "mean"),
            WAPE_micro_std=("WAPE_micro", "std"),
            R2_log_mean=("R2_log", "mean"),
            R2_log_std=("R2_log", "std"),
            WAPE_macro_mean=("WAPE_macro", "mean"),
            WAPE_macro_std=("WAPE_macro", "std"),
            R2_original_mean=("R2_original", "mean"),
            R2_original_std=("R2_original", "std"),
            MAE_original_mean=("MAE_original", "mean"),
            MAE_original_std=("MAE_original", "std"),
        )
        .sort_values(
            ["WAPE_micro_mean", "R2_log_mean", "WAPE_macro_mean", "model_id", "run_role"],
            ascending=[True, False, True, True, True],
            kind="mergesort",
        )
        .reset_index(drop=True)
    )
    summary_df = summary_df.fillna(0.0)
    return summary_df
