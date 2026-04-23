# Dicoding Collection Dashboard

Dashboard interaktif untuk analisis performa e-commerce menggunakan Streamlit.

## Struktur Proyek

submission/
|- dashboard/
|  |- dashboard.py
|  |- main_data.csv
|- data/
|  |- orders_dataset.csv
|  |- order_payments_dataset.csv
|- Proyek_Analisis_Data.ipynb
|- requirements.txt
|- README.md
|- url.txt

## Setup Environment - Anaconda

conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Shell/Terminal

mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

## Menjalankan Streamlit App

Jalankan perintah dari root folder submission:

streamlit run dashboard/dashboard.py

## Deployment URL

URL deployment aplikasi disimpan pada file url.txt.
