# dashboard.py


import pandas as pd
import streamlit as st
import os
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor



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

# Forecasting Function — returns date + forecast dictionary
def get_forecasted_sales(df):
    df['date'] = pd.to_datetime(df['date'])

    # Ensure correct column exists
    if 'total_amount' not in df.columns:
        if 'total_price' in df.columns:
            df.rename(columns={'total_price': 'total_amount'}, inplace=True)
        else:
            return None

    df = df.groupby('date')['total_amount'].sum().reset_index()
    all_days = pd.date_range(start=df['date'].min(), end=df['date'].max())
    df = df.set_index('date').reindex(all_days).rename_axis('date').reset_index()
    df['total_amount'] = df['total_amount'].interpolate(method='linear')

    df_weekly = df.set_index('date').resample('W-FRI').asfreq().reset_index()

    for i in range(1, 9):
        df_weekly[f'lag_{i}'] = df_weekly['total_amount'].shift(i)
    df_model = df_weekly.dropna().reset_index(drop=True)

    features = [f'lag_{i}' for i in range(1, 9)]
    X = df_model[features]
    y = df_model['total_amount']

    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)

    last_known = df_model.iloc[-1][features].values.tolist()
    future_dates = pd.date_range(start=df_weekly['date'].max() + pd.Timedelta(weeks=1), periods=4, freq='W-FRI')
    forecast = []

    for _ in range(4):
        input_df = pd.DataFrame([last_known], columns=features)
        pred = model.predict(input_df)[0]
        forecast.append(round(pred, 2))
        last_known = last_known[1:] + [pred]

    forecast_dict = {str(date.date()): value for date, value in zip(future_dates, forecast)}
    return forecast_dict




# Main function to run the Streamlit app
def main():
    st.title("📊 Balaji Fast Food Sales Dashboard")
    st.write("This dashboard displays the data and allows stakeholders to filter and search the records.")


    # Load the processed data
    data = load_data()
    if data.empty:
        st.warning("No data to display. Please ensure the dataset is processed and available.")
        return
    
    # -----------------------------
    # Combined Barchart (Sprint 1 & 2)
    # -----------------------------   
    st.subheader("Total Sales by Item Type")

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

    #grouped = filtered.groupby("item_type")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False)
    st.metric("Total Sales (₹)", f"{filtered['total_amount'].sum():,.0f}")

    df = filtered.rename(columns={"item_type": "Type of Items", "total_amount": "Total Sales (₹)"})
    summary = df.groupby("Type of Items")["Total Sales (₹)"].sum().reset_index()
    fig2 = px.bar(
        summary,
        x="Type of Items",
        y="Total Sales (₹)",
        title=f"Total Sales by Type of Items ({year if year != 'All' else 'All Years'}, {time if time != 'All' else 'All Times'})",
        labels={"Total Sales (₹)": "Total Sales (₹)", "Type of Items": "Item Type"},
        text_auto=".2s",
        color="Type of Items"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------------
    # Sprint 3 - Forecast Weekly Sales (Next 4 Weeks)
    # -------------------------------------
    
    st.subheader("🔮 Forecast Weekly Sales (Next 4 Weeks)")
    forecast = get_forecasted_sales(data.copy())
    if forecast:
        forecast_df = pd.DataFrame({"Date": list(forecast.keys()), "Forecasted Sales (₹)": list(forecast.values())})
        st.dataframe(forecast_df)
    else:
        st.warning("Unable to forecast. Required column 'total_amount' missing.")


# Entry point for the Streamlit app
if __name__ == "__main__":
    main()