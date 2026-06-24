from pathlib import Path
import argparse
import pandas as pd


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")


def select_csv_file(raw_data_dir: Path) -> Path:
    """
    Let the user select a CSV file from the raw data directory.
    """
    csv_files = sorted(raw_data_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {raw_data_dir}. "
            "Please add at least one CSV file to data/raw/."
        )

    print("\nAvailable CSV files in data/raw:\n")

    for index, file_path in enumerate(csv_files, start=1):
        print(f"[{index}] {file_path.name}")

    while True:
        choice = input("\nSelect a file number: ")

        if choice.isdigit():
            choice_index = int(choice)

            if 1 <= choice_index <= len(csv_files):
                return csv_files[choice_index - 1]

        print("Invalid choice. Please enter a valid number.")


def build_default_output_path(input_path: Path) -> Path:
    """
    Build the output path based on the selected input file name.

    Example:
    data/raw/insurance_claims_event_log.csv
    becomes:
    data/processed/insurance_claims_event_log_clean.csv
    """
    output_filename = f"{input_path.stem}_clean.csv"
    return PROCESSED_DATA_DIR / output_filename


def load_data(input_path: Path) -> pd.DataFrame:
    """
    Load the raw event log CSV file.
    """
    if not input_path.exists():
        raise FileNotFoundError(
            f"File not found: {input_path}. "
            "Please check the file path or place the dataset in data/raw/."
        )

    return pd.read_csv(input_path)


def inspect_data(df: pd.DataFrame, title: str) -> None:
    """
    Print basic information about the dataset.
    """
    print(f"\n{title}")
    print("-" * len(title))

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst rows:")
    print(df.head())

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nData types:")
    print(df.dtypes)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names:
    - remove leading/trailing spaces
    - convert to lowercase
    - replace spaces with underscores
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply basic cleaning steps to the event log.
    """
    df = df.copy()

    # Remove duplicated rows
    df = df.drop_duplicates()

    # Clean column names
    df = clean_column_names(df)

    return df


def save_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save the cleaned dataset.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"\nCleaned data saved to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preprocess business process event logs."
    )

    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help=(
            "Path to the raw CSV file. "
            "If not provided, the script lets you choose a file from data/raw/."
        ),
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help=(
            "Path where the cleaned CSV file will be saved. "
            "If not provided, it is generated from the input file name."
        ),
    )

    args = parser.parse_args()

    if args.input is None:
        input_path = select_csv_file(RAW_DATA_DIR)
    else:
        input_path = Path(args.input)

    if args.output is None:
        output_path = build_default_output_path(input_path)
    else:
        output_path = Path(args.output)

    print(f"\nSelected input file: {input_path}")
    print(f"Output file: {output_path}")

    raw_df = load_data(input_path)

    inspect_data(raw_df, "Raw dataset overview")

    clean_df = basic_cleaning(raw_df)

    inspect_data(clean_df, "Cleaned dataset overview")

    save_data(clean_df, output_path)


if __name__ == "__main__":
    main()