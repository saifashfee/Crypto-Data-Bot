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
    if response.status_code == 200:
        print("Data fetched successfully.")
        data = response.json().get('result', [])
        return data
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return []

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

        csv_filename = "crypto_data.csv"

        if os.path.exists(csv_filename):
            df.to_csv(csv_filename, mode='a', header=False, index=False
        else:
            df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}")
        
    else:
        print("No data available to save.")

if __name__ == "__main__":
    # Fetch data from the API
    data = fetch_data()
    
    # Save data to CSV
    save_to_csv(data)
