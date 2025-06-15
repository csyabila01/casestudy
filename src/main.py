# main.py


import pandas as pd
import os


def load_and_process_data(filepath="data/Balaji Fast Food Sales.csv", output_path="data/processed_dataset.csv"):
    """
    Loads the dataset, cleans the dataset, and saves the processed dataset.


    Args:
        filepath (str): Path to the input dataset.
        output_path (str): Path to save the processed dataset.


    Returns:
        pd.DataFrame: Processed DataFrame.
    """
     # Load the dataset
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")

    df = pd.read_csv(filepath)

    # Normalize column names to lowercase
    df.columns = df.columns.str.lower()

    # Check if 'date' exists
    if "date" not in df.columns:
        raise KeyError("Column 'date' not found in the dataset.")

    # Standardize date format by replacing slashes with dashes
    df["date"] = df["date"].astype(str).str.replace("/", "-")
    df["date"] = pd.to_datetime(df["date"], errors='coerce', dayfirst=True)

    # Parse date and extract year, hour
    df["Year"] = df["date"].dt.year
    df["Hour"] = df["date"].dt.hour

    # Fill missing Transaction Types
    df["transaction_type"] = df["transaction_type"].fillna("Credit Card")

    # Calculate total amount
    df["total_amount"] = df["item_price"] * df["quantity"]

    # Save the processed dataset
    output_path = os.path.abspath(output_path)
    try:
        df.to_csv(output_path, index=False)
        print("Processed dataset saved successfully!")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")

    return df

if __name__ == "__main__":
    load_and_process_data()