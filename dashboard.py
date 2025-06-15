# dashboard.py


import pandas as pd
import streamlit as st
import os
import plotly.express as px
from sklearn.linear_model import LinearRegression


# -----------------------------
# Function to load the processed data
# -----------------------------
@st.cache_data
def load_data():
    path = "data/processed_dataset.csv"
    #st.write("📂 Current working dir:", os.getcwd())
    if not os.path.exists(path):
        st.error(f"❌ File not found: {path}")
        st.stop()
    df = pd.read_csv(path)
    return df




# Main function to run the Streamlit app
def main():
    st.title("📊 Balaji Fast Food Sales Dashboard")
    st.write("This dashboard displays the data and allows stakeholders to filter and search the records.")


    # Load the processed data
    data = load_data()
    if data.empty:
        st.warning("No data to display. Please ensure the dataset is processed and available.")
        return
   
   
    # Filters with 'All' option
    year_options = ["All"] + sorted(data["Year"].dropna().unique().tolist())
    time_options = ["All"] + sorted(data["time_of_sale"].dropna().unique().tolist())

    year = st.selectbox("Select Year", year_options, key="s1")
    time = st.selectbox("Select Time of Sale", time_options, key="s2")

    # Apply filters
    filtered = data.copy()
    if year != "All":
        filtered = filtered[filtered["Year"] == int(year)]
    if time != "All":
        filtered = filtered[filtered["time_of_sale"] == time]

    # -----------------------------
    # Combined Barchart (Sprint 1 & 2)
    # -----------------------------
    st.subheader("Total Sales by Item Type")
    grouped = filtered.groupby("item_type")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False)
    st.metric("Total Sales (₹)", f"{filtered['total_amount'].sum():,.0f}")
    fig = px.bar(grouped, x="item_type", y="total_amount",
                 labels={"item_type": "Item Type", "total_amount": "Total Sales (₹)"},
                 title=f"Sales by Item Type ({year if year != 'All' else 'All Years'}, {time if time != 'All' else 'All Times'})")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------
    # Sprint 3 - Prediction of Total Sales
    # -------------------------------------
    st.subheader("Predict Total Sales for 2024")
    yearly_sales = data.groupby("Year")["total_amount"].sum().reset_index()
    model = LinearRegression()
    X = yearly_sales["Year"].values.reshape(-1, 1)
    y = yearly_sales["total_amount"].values
    model.fit(X, y)
    predicted_2024 = model.predict([[2024]])[0]
    st.metric("Predicted Sales for 2024 (₹)", f"{predicted_2024:,.0f}")

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()