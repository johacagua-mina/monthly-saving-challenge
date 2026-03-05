from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
SAVINGS_CSV = DATA_DIR / "savings.csv"


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not SAVINGS_CSV.exists():
        pd.DataFrame(columns=["month", "target", "actual"]).to_csv(SAVINGS_CSV, index=False)


def load_data() -> pd.DataFrame:
    """Load savings data from CSV (month, target, actual)."""
    _ensure_storage()
    df = pd.read_csv(SAVINGS_CSV)

    # Ensure correct types
    if not df.empty:
        df["month"] = df["month"].astype(str)
        df["target"] = pd.to_numeric(df["target"], errors="coerce").fillna(0.0)
        df["actual"] = pd.to_numeric(df["actual"], errors="coerce").fillna(0.0)

    # Sort by month for nicer reporting
    df = df.sort_values("month") if not df.empty else df
    return df


def upsert_month(month: str, target: float, actual: float) -> None:
    """Insert or update a month row."""
    month = str(month).strip()
    if not month:
        raise ValueError("Month cannot be empty. Use YYYY-MM.")

    _ensure_storage()
    df = pd.read_csv(SAVINGS_CSV)
    if df.empty:
        df = pd.DataFrame(columns=["month", "target", "actual"])

    # If month exists, update; else append
    if (df["month"] == month).any():
        df.loc[df["month"] == month, ["target", "actual"]] = [float(target), float(actual)]
    else:
        df = pd.concat(
            [df, pd.DataFrame([{"month": month, "target": float(target), "actual": float(actual)}])],
            ignore_index=True,
        )

    df = df.sort_values("month")
    df.to_csv(SAVINGS_CSV, index=False, encoding="utf-8")


def total_savings(df: pd.DataFrame) -> float:
    """Total actual savings across all months."""
    if df.empty:
        return 0.0
    return float(df["actual"].sum())


def build_monthly_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Per-month analysis:
    - gap = actual - target
    - achieved_pct = actual/target * 100
    - cumulative_actual = running sum of actual
    """
    if df.empty:
        return pd.DataFrame(columns=["month", "target", "actual", "gap", "achieved_pct", "cumulative_actual"])

    out = df.copy()
    out["gap"] = out["actual"] - out["target"]
    out["achieved_pct"] = out.apply(
        lambda r: (r["actual"] / r["target"] * 100.0) if r["target"] > 0 else 0.0, axis=1
    )
    out["cumulative_actual"] = out["actual"].cumsum()
    return out