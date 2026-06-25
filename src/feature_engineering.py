from pathlib import Path
import argparse
import pandas as pd


PROCESSED_DATA_DIR = Path("data/processed")


def build_default_output_path(input_path: Path) -> Path:
    """
    Build the output path based on the selected cleaned file name.

    Example:
    data/processed/insurance_claims_event_log_clean.csv
    becomes:
    data/processed/insurance_claims_event_log_features.csv
    """
    if input_path.stem.endswith("_clean"):
        output_filename = input_path.stem.replace("_clean", "_features") + ".csv"
    else:
        output_filename = f"{input_path.stem}_features.csv"

    return PROCESSED_DATA_DIR / output_filename


def load_clean_data(input_path: Path) -> pd.DataFrame:
    """
    Load the cleaned event log.
    """
    if not input_path.exists():
        raise FileNotFoundError(
            f"File not found: {input_path}. "
            "Please run data_preprocessing.py first."
        )

    return pd.read_csv(input_path)


def validate_required_columns(df: pd.DataFrame) -> None:
    """
    Check that the minimum required columns exist.
    """
    print("\nAvailable columns:")
    print(df.columns.tolist())

    required_columns = ["case_id", "activity", "timestamp"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            "Please check the column names printed above."
        )

def standardize_event_log_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename common event log column names to the names expected by the pipeline.
    """
    df = df.copy()

    column_mapping = {
        "case": "case_id",
        "caseid": "case_id",
        "case_id": "case_id",
        "claim_id": "case_id",

        "task": "activity",
        "event": "activity",
        "step": "activity",
        "activity_name": "activity",
        "concept:name": "activity",

        "time": "timestamp",
        "datetime": "timestamp",
        "date": "timestamp",
        "event_time": "timestamp",
        "time:timestamp": "timestamp",
    }

    df = df.rename(
        columns={
            column: column_mapping[column]
            for column in df.columns
            if column in column_mapping
        }
    )

    return df


def prepare_event_log(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the event log before feature engineering.
    """
    df = df.copy()

    df = standardize_event_log_columns(df)

    validate_required_columns(df)

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    if df["timestamp"].isna().any():
        invalid_rows = df[df["timestamp"].isna()]
        raise ValueError(
            f"Some timestamps could not be converted. "
            f"Number of invalid rows: {len(invalid_rows)}"
        )

    df = df.sort_values(["case_id", "timestamp"])

    return df

def create_case_features(df: pd.DataFrame, late_threshold_hours: float = 72.0) -> pd.DataFrame:
    """
    Create one row per case_id with process-level features.

    late_threshold_hours:
    A case is considered late if its total duration is above this threshold.
    Default: 72 hours = 3 days.
    """
    df = df.copy()

    grouped = df.groupby("case_id")

    features = grouped.agg(
        case_start=("timestamp", "min"),
        case_end=("timestamp", "max"),
        number_of_events=("activity", "count"),
        number_of_unique_activities=("activity", "nunique"),
        first_activity=("activity", "first"),
        last_activity=("activity", "last"),
    ).reset_index()

    features["case_duration_hours"] = (
        features["case_end"] - features["case_start"]
    ).dt.total_seconds() / 3600

    features["is_late"] = (
        features["case_duration_hours"] > late_threshold_hours
    ).astype(int)

    if "department" in df.columns:
        department_features = grouped.agg(
            number_of_departments=("department", "nunique"),
            main_department=("department", lambda x: x.mode().iloc[0] if not x.mode().empty else None),
        ).reset_index()

        features = features.merge(department_features, on="case_id", how="left")

    if "user_id" in df.columns:
        user_features = grouped.agg(
            number_of_users=("user_id", "nunique"),
        ).reset_index()

        features = features.merge(user_features, on="case_id", how="left")

    if "duration" in df.columns:
        duration_features = grouped.agg(
            total_activity_duration=("duration", "sum"),
            average_activity_duration=("duration", "mean"),
            max_activity_duration=("duration", "max"),
        ).reset_index()

        features = features.merge(duration_features, on="case_id", how="left")

    if "cost" in df.columns:
        cost_features = grouped.agg(
            total_cost=("cost", "sum"),
            average_cost=("cost", "mean"),
        ).reset_index()

        features = features.merge(cost_features, on="case_id", how="left")

    if "priority" in df.columns:
        priority_features = grouped.agg(
            priority=("priority", "first"),
        ).reset_index()

        features = features.merge(priority_features, on="case_id", how="left")

    if "status" in df.columns:
        status_features = grouped.agg(
            final_status=("status", "last"),
        ).reset_index()

        features = features.merge(status_features, on="case_id", how="left")

    loop_features = grouped["activity"].apply(
        lambda activities: int(activities.duplicated().any())
    ).reset_index(name="has_loop")

    features = features.merge(loop_features, on="case_id", how="left")

    return features


def save_features(features: pd.DataFrame, output_path: Path) -> None:
    """
    Save the case-level features.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(output_path, index=False)

    print(f"\nFeature dataset saved to: {output_path}")


def inspect_features(features: pd.DataFrame) -> None:
    """
    Print a quick overview of the feature dataset.
    """
    print("\nFeature dataset overview")
    print("------------------------")

    print("\nShape:")
    print(features.shape)

    print("\nColumns:")
    print(features.columns.tolist())

    print("\nFirst rows:")
    print(features.head())

    if "is_late" in features.columns:
        print("\nLate case distribution:")
        print(features["is_late"].value_counts())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create case-level features from a cleaned event log."
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the cleaned CSV file.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help=(
            "Path where the feature dataset will be saved. "
            "If not provided, it is generated from the input file name."
        ),
    )

    parser.add_argument(
        "--late-threshold-hours",
        type=float,
        default=72.0,
        help="Threshold used to define whether a case is late. Default: 72 hours.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if args.output is None:
        output_path = build_default_output_path(input_path)
    else:
        output_path = Path(args.output)

    print(f"\nSelected input file: {input_path}")
    print(f"Output file: {output_path}")
    print(f"Late threshold: {args.late_threshold_hours} hours")

    df = load_clean_data(input_path)
    df = prepare_event_log(df)

    features = create_case_features(
        df,
        late_threshold_hours=args.late_threshold_hours,
    )

    inspect_features(features)
    save_features(features, output_path)


if __name__ == "__main__":
    main()