import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

st.header("Indian Stock Dashboard")

ticker = st.sidebar.text_input("Symbol Code", 'INFY')
exchange = st.sidebar.text_input("Exchange", "NSE")

url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

def safe_find(class_name):
    element = soup.find(class_=class_name)
    if element:
        return element.text.strip()
    return 'N/A'

try:
    price = float(safe_find("YMlKec fxKbKc").replace('₹', '').replace(',', ""))
    previous_close = float(safe_find("P6K39c").replace('₹', '').replace(',', ""))
    revenue = safe_find("QXDnM")
    news = safe_find("Yfwt5")
    about = safe_find("bLLb2d")

    dict1 = {'Price': [price],
             'Previous Close': [previous_close],
             'Revenue': [revenue],
             'News': [news],
             'About': [about]}

    df = pd.DataFrame(dict1).T
    st.write(df)

except Exception as e:
    st.error(f"An error occurred: {e}")

