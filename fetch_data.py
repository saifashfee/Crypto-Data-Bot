import os
import requests
import pandas as pd
from datetime import datetime

def fetch_data():
    api_key = os.getenv('RAPIDAPI_KEY')
    url = "https://cryptocurrency-market.p.rapidapi.com/api/crypto"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "cryptocurrency-market.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json().get('result', [])
    return data

def save_to_csv(data):
    # Convert the data into a DataFrame
    df = pd.DataFrame(data)
    
    # Check if we have required fields and rename them to match CSV column names
    if not df.empty:
        df = df[['name', 'last_updated', 'current_price', 'total_volume', 
                 'high_24h', 'low_24h', 'price_change_percentage_24h', 
                 'market_cap', 'circulating_supply']]
        df.columns = ['Coin Name', 'Last Updated', 'Last Traded Price ($)', 'Total Volume',
                      '24h High ($)', '24h Low ($)', 'Price Change Percentage', 
                      'Market Cap ($)', 'Circulating Supply']

        # Save to CSV with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"crypto_data_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}")
    else:
        print("No data available to save.")

if __name__ == "__main__":
    # Fetch data from the API
    data = fetch_data()
    
    # Save data to CSV
    save_to_csv(data)