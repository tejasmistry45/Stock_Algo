import streamlit as st
import requests
import pandas as pd

# Define your Twelve Data API key
API_KEY = '01aabeb46755445aa63e38a6e254bdbd'

# Fetch live stock data
def fetch_stock_data(symbol):
    url = f'https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

# Fetch historical stock data
def fetch_historical_data(symbol, start_date, end_date):
    url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&start_date={start_date}&end_date={end_date}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

# Fetch currency conversion rate
def fetch_currency_conversion(base_currency, target_currency):
    url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
    response = requests.get(url)
    data = response.json()
    return data['rates'].get(target_currency, 1)

# Streamlit application layout
st.title("Twelve Data API Dashboard")

# Sidebar for user input
st.sidebar.header("User Input")
symbol = st.sidebar.text_input("Ticker Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('2024-01-01'))
country = st.sidebar.text_input("Country Code for Economic Calendar", "US")

# Container for displaying results
main_area = st.container()

# Button actions
if st.sidebar.button("Get Real-Time Data"):
    with main_area:
        data = fetch_stock_data(symbol)
        if 'error' in data:
            st.error(f"Error: {data['error']['message']}")
        else:
            # Extract relevant fields from API response
            name = data.get('name', 'N/A')
            currency = data.get('currency', 'USD')
            datetime = data.get('datetime', 'N/A')
            timestamp = data.get('timestamp', 'N/A')
            open_price = data.get('open', 'N/A')
            high = data.get('high', 'N/A')
            low = data.get('low', 'N/A')
            close = data.get('close', 'N/A')
            volume = data.get('volume', 'N/A')
            previous_close = data.get('previous_close', 'N/A')
            change = data.get('change', 'N/A')
            percent_change = data.get('percent_change', 'N/A')
            average_volume = data.get('average_volume', 'N/A')
            is_market_open = data.get('is_market_open', False)
            fifty_two_week = data.get('fifty_two_week', {})

            # Extract data from 'fifty_two_week'
            low_52_week = fifty_two_week.get('low', 'N/A')
            high_52_week = fifty_two_week.get('high', 'N/A')
            low_change = fifty_two_week.get('low_change', 'N/A')
            high_change = fifty_two_week.get('high_change', 'N/A')
            low_change_percent = fifty_two_week.get('low_change_percent', 'N/A')
            high_change_percent = fifty_two_week.get('high_change_percent', 'N/A')
            week_range = fifty_two_week.get('range', 'N/A')

            # Determine currency based on country code
            if country.upper() == 'IN':
                currency_label = 'INR'
                if open_price != 'N/A' and currency == 'USD':
                    conversion_rate = fetch_currency_conversion('USD', 'INR')
                    open_converted = float(open_price) * conversion_rate
                    close_converted = float(close) * conversion_rate
                else:
                    open_converted = 'N/A'
                    close_converted = 'N/A'
            else:
                currency_label = 'USD'
                open_converted = open_price
                close_converted = close

            # Display real-time stock data
            st.subheader(f"Real-Time Stock Data for {name} ({symbol})")
            st.write(f"**Currency:** {currency_label}")
            st.write(f"**Date & Time:** {datetime}")
            st.write(f"**Open Price ({currency_label}):** {open_converted}")
            st.write(f"**High Price ({currency_label}):** {high}")
            st.write(f"**Low Price ({currency_label}):** {low}")
            st.write(f"**Close Price ({currency_label}):** {close_converted}")
            st.write(f"**Volume:** {volume}")
            st.write(f"**Previous Close:** {previous_close}")
            st.write(f"**Change:** {change}")
            st.write(f"**Percent Change:** {percent_change}")
            st.write(f"**Average Volume:** {average_volume}")
            st.write(f"**Is Market Open:** {'Yes' if is_market_open else 'No'}")
            st.write(f"**52-Week Low:** {low_52_week}")
            st.write(f"**52-Week High:** {high_52_week}")
            st.write(f"**52-Week Low Change:** {low_change}")
            st.write(f"**52-Week High Change:** {high_change}")
            st.write(f"**52-Week Low Change Percent:** {low_change_percent}")
            st.write(f"**52-Week High Change Percent:** {high_change_percent}")
            st.write(f"**52-Week Range:** {week_range}")

if st.sidebar.button("Get Historical Data"):
    with main_area:
        data = fetch_historical_data(symbol, start_date, end_date)
        if 'error' in data:
            st.error(f"Error: {data['error']['message']}")
        else:
            values = data.get('values', [])
            if not values:
                st.error("No historical data found.")
            else:
                # Convert the list of dictionaries to a DataFrame
                df = pd.DataFrame(values)
                # Ensure the datetime column is properly formatted
                df['datetime'] = pd.to_datetime(df['datetime'])
                # Display the historical data
                st.subheader(f"Historical Data for {symbol} from {start_date} to {end_date}")
                st.write(df)
                # Display data as a line chart for better visualization
                st.line_chart(df[['datetime', 'close']].set_index('datetime'))
