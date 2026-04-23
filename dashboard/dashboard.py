import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# 1. Konfigurasi Dasar & Load Data
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_df = load_data()

# 2. Membuat Sidebar (Filter Waktu)
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png") # Logo opsional
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=all_df["order_purchase_timestamp"].min(),
        max_value=all_df["order_purchase_timestamp"].max(),
        value=[all_df["order_purchase_timestamp"].min(), all_df["order_purchase_timestamp"].max()]
    )

# Filter data berdasarkan tanggal di sidebar
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# 3. Header Utama
st.header('E-Commerce Performance Dashboard 🛍️')

# 4. Menampilkan Metrik Utama (Ringkasan Angka)
col1, col2 = st.columns(2)
with col1:
    total_revenue = format_currency(main_df.payment_value.sum(), "BRL", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
with col2:
    total_orders = main_df.order_id.nunique()
    st.metric("Total Orders", value=total_orders)

# 5. Visualisasi 1: Tren Pendapatan Bulanan
st.subheader('Monthly Revenue Growth')
monthly_rev = main_df.resample(rule='ME', on='order_purchase_timestamp').agg({"payment_value": "sum"})
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(monthly_rev.index, monthly_rev.values, marker='o', linewidth=3, color="#3498DB")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# 6. Visualisasi 2: Metode Pembayaran
st.subheader('Preferred Payment Methods')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x=main_df['payment_type'].value_counts().index, 
    y=main_df['payment_type'].value_counts().values,
    palette="viridis",
    ax=ax
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

st.caption('Copyright © Proyek Analisis Data 2026')