import os
import sys
import pandas as pd
import tempfile


# Add project root to path to import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from main import load_and_process_data


def test_fill_missing_transaction_type():
    """Test that missing 'transaction_type' values are filled with 'Credit Card'."""

    df = pd.DataFrame({
        "transaction_type": [None, "Cash", None]
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.csv")
        output_path = os.path.join(tmpdir, "output.csv")

        df.to_csv(input_path, index=False)
        processed_df = load_and_process_data(input_path, output_path)

        assert processed_df["transaction_type"].isnull().sum() == 0, "❌ There are still missing transaction_type values."
        assert (processed_df["transaction_type"] == "Credit Card").sum() == 2, "❌ Not all missing values filled with 'Credit Card'."
        print("✅ Test passed: All missing 'transaction_type' values filled with 'Credit Card'.")

if __name__ == "__main__":
    test_fill_missing_transaction_type()

