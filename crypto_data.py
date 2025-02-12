import requests
import pandas as pd
import schedule
import time

# Function to fetch live cryptocurrency data
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1&sparkline=false"
    response = requests.get(url)
    data = response.json()
    
    # Extract relevant fields
    crypto_data = []
    for coin in data:
        crypto_data.append({
            "Name": coin["name"],
            "Symbol": coin["symbol"],
            "Current Price (USD)": coin["current_price"],
            "Market Cap (USD)": coin["market_cap"],
            "24h Volume (USD)": coin["total_volume"],
            "24h Price Change (%)": coin["price_change_percentage_24h"]
        })
    
    return pd.DataFrame(crypto_data)

# Function to update the Excel sheet with live data
def update_excel():
    # Fetch live data
    df = fetch_crypto_data()
    
    # Save data to Excel
    df.to_excel("crypto_data.xlsx", index=False)
    print("Excel sheet updated at:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Perform data analysis
    analyze_data(df)

# Function to analyze the fetched data
def analyze_data(df):
    # Top 5 cryptocurrencies by market cap
    top_5_by_market_cap = df.sort_values(by="Market Cap (USD)", ascending=False).head(5)
    print("\nTop 5 Cryptocurrencies by Market Cap:")
    print(top_5_by_market_cap)
    
    # Average price of the top 50 cryptocurrencies
    average_price = df["Current Price (USD)"].mean()
    print(f"\nAverage Price of Top 50 Cryptocurrencies: ${average_price:.2f}")
    
    # Highest and lowest 24-hour price change
    highest_price_change = df.loc[df["24h Price Change (%)"].idxmax()]
    lowest_price_change = df.loc[df["24h Price Change (%)"].idxmin()]
    print("\nCryptocurrency with Highest 24h Price Change:")
    print(highest_price_change)
    print("\nCryptocurrency with Lowest 24h Price Change:")
    print(lowest_price_change)

# Initial data fetch and Excel update
print("Fetching initial data and creating Excel sheet...")
update_excel()

# Schedule periodic updates every 5 minutes
schedule.every(5).minutes.do(update_excel)

# Keep the script running to allow scheduled updates
print("Live updating started. Press Ctrl+C to stop.")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Script stopped.")