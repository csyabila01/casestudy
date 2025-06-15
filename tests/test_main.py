import os
import sys
import pandas as pd
import tempfile


# Add project root to path to import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from main import load_and_process_data


def test_fill_missing_transaction_type():
    df = pd.DataFrame({
        "date": ["01/01/2023", "02/01/2023"],
        "item_price": [100, 150],
        "quantity": [2, 3],
        "transaction_type": [None, "Cash"],
        "item_type": ["Burger", "Fries"],
        "time_of_sale": ["10:00", "12:00"]
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.csv")
        output_path = os.path.join(tmpdir, "output.csv")
        df.to_csv(input_path, index=False)

        processed_df = load_and_process_data(input_path, output_path)

        assert "transaction_type" in processed_df.columns
        assert "Credit Card" in processed_df["transaction_type"].values
        print("✅ Test passed: Missing transaction_type filled as 'Credit Card'")

if __name__ == "__main__":
    test_fill_missing_transaction_type()

