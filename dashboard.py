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
   
   
    year = st.selectbox("Select Year", sorted(data["Year"].dropna().unique()), key="s1")


    # Layout: Sprint 1 and Sprint 2 side by side
    col1, col2 = st.columns(2)




# -----------------------------
# Sprint 1 - MVD
# -----------------------------
    with col1:
        st.subheader("Total Sales by Item Type")


        filtered = data[data["Year"] == year]
        grouped = filtered.groupby("item_type")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False)


        st.metric("Total Sales (₹)", f"{filtered['total_amount'].sum():,.0f}")


        fig = px.bar(
            grouped,
            x="item_type",
            y="total_amount",
            labels={"item_type": "Item Type", "total_amount": "Total Sales (₹)"},
            title=f"Total Sales by Item Type for {year}"
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Sprint 2 - Add Time Filter
# -----------------------------
    with col2:
        st.subheader("🕒 Sales by Time of Day")
        available_times = sorted(data["time_of_sale"].dropna().unique())
        selected_time = st.selectbox("Select Time of Sale", available_times)




        filtered2 = data[(data["Year"] == year) & (data["time_of_sale"] == selected_time)]
        grouped2 = filtered2.groupby("item_type")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False)


        st.metric("Total Sales (₹)", f"{filtered2['total_amount'].sum():,.0f}")


        fig2 = px.bar(
            grouped,
            x="item_type",
            y="total_amount",
            labels={"item_type": "Item Type", "total_amount": "Total Sales (₹)"},
            title=f"Sales by Item Type for {year} at {selected_time}"
        )
        st.plotly_chart(fig2, use_container_width=True)

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
