import os
import sys
import pandas as pd
import tempfile


# Add project root to path to import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from main import load_and_process_data


def test_no_nulls_in_critical_fields():
    """Ensure no null values exist in critical columns after processing."""

    df = pd.DataFrame({
        "date": ["2023-01-01", "2023-01-01"],
        "item_type": ["Burger", "Pizza"],
        "item_price": [100, 150],
        "quantity": [1, 2],
        "transaction_type": [None, None],
        "time_of_sale": ["10:00:00", "11:00:00"]
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.csv")
        output_path = os.path.join(tmpdir, "output.csv")

        df.to_csv(input_path, index=False)
        processed_df = load_and_process_data(input_path, output_path)

        critical_fields = ["date", "item_type", "item_price", "quantity", "transaction_type", "total_amount"]
        null_counts = processed_df[critical_fields].isnull().sum()

        assert null_counts.sum() == 0, f"❌ Nulls found in critical fields: {null_counts[null_counts > 0].to_dict()}"
        print("✅ Test passed: No nulls in critical fields.")

if __name__ == "__main__":
    test_no_nulls_in_critical_fields()

