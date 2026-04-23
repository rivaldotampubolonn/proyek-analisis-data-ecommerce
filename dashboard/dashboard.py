from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')


# 1. Load data
def load_data():
    data_path = Path(__file__).resolve().parent / "main_data.csv"
    all_df = pd.read_csv(data_path)
    all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

    # rfm_df dibentuk dari main_data.csv agar app tetap jalan tanpa file rfm_data.csv terpisah.
    snapshot_date = all_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm_df = all_df.groupby("customer_id", as_index=False).agg(
        recency=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("payment_value", "sum"),
    )

    return all_df, rfm_df


all_df, rfm_df = load_data()

# 2. Sidebar (Filter Waktu)
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=all_df["order_purchase_timestamp"].min(),
        max_value=all_df["order_purchase_timestamp"].max(),
        value=[all_df["order_purchase_timestamp"].min(), all_df["order_purchase_timestamp"].max()]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) &
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# 3. Header
st.header('E-Commerce Public Dashboard')

# 4. Metrik Utama (Revenue & Orders)
st.subheader('Daily Orders & Revenue')

col1, col2 = st.columns(2)

with col1:
    total_orders = main_df.order_id.nunique()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = format_currency(main_df.payment_value.sum(), "BRL", locale='pt_BR')
    st.metric("Total Revenue", value=total_revenue)

# 5. Chart Tren Pendapatan Bulanan
st.subheader("Monthly Revenue Trend")
fig, ax = plt.subplots(figsize=(16, 8))
monthly_df = main_df.resample(rule='ME', on='order_purchase_timestamp').agg({"payment_value": "sum"}).reset_index()
monthly_df['order_purchase_timestamp'] = monthly_df['order_purchase_timestamp'].dt.strftime('%Y-%m')

ax.plot(monthly_df["order_purchase_timestamp"], monthly_df["payment_value"], marker='o', linewidth=3, color="#72BCD4")
ax.set_title("Revenue Trend per Month", fontsize=25)
plt.xticks(rotation=45, fontsize=15)
plt.yticks(fontsize=15)
st.pyplot(fig)

# 6. Chart Metode Pembayaran
st.subheader("Customer Payment Methods")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x=main_df.groupby("payment_type").order_id.nunique().sort_values(ascending=False).values,
    y=main_df.groupby("payment_type").order_id.nunique().sort_values(ascending=False).index,
    palette="viridis",
    ax=ax
)
ax.set_title("Number of Transactions by Payment Type", fontsize=15)
st.pyplot(fig)

# 7. RFM Analysis Best Customers
st.subheader("Best Customer Based on RFM Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Avg Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Avg Frequency", value=avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR')
    st.metric("Avg Monetary", value=avg_monetary)

# Visualisasi RFM Top 5
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_title("By Recency (days)", loc="center", fontsize=30)
ax[0].tick_params(axis='x', rotation=90, labelsize=15)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_title("By Frequency", loc="center", fontsize=30)
ax[1].tick_params(axis='x', rotation=90, labelsize=15)

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_title("By Monetary (BRL)", loc="center", fontsize=30)
ax[2].tick_params(axis='x', rotation=90, labelsize=15)

st.pyplot(fig)

st.caption('Copyright (c) Dicoding Collection 2026')
