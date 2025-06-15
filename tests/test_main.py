import os
import sys
import pandas as pd
import tempfile


# Add project root to path to import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from main import load_and_process_data


def test_no_duplicates():
    """Test if duplicate rows are removed during processing."""


    # Create a temporary CSV with duplicate rows
    df = pd.DataFrame({
        "date": ["2023-01-01", "2023-01-01"],
        "item_type": ["Burger", "Burger"],
        "item_price": [100, 100],
        "quantity": [1, 1],
        "transaction_type": [None, None],
        "time_of_sale": ["10:00:00", "10:00:00"]
    })


    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.csv")
        output_path = os.path.join(tmpdir, "output.csv")


        df.to_csv(input_path, index=False)


        processed_df = load_and_process_data(filepath=input_path, output_path=output_path)


        assert processed_df.duplicated().sum() == 0, "❌ Duplicate rows were not removed"
        print("✅ Test passed: No duplicate rows found after processing.")


if __name__ == "__main__":
    test_no_duplicates()
