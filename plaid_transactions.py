import requests
import pandas as pd
from datetime import datetime
    
def transactions(token):

    # Set API endpoint
    url = "https://api.lunchmoney.app/v1/transactions"

    # Set headers
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Set starting parameters (really old start date + today's date)
    params = {
        "start_date": "2000-01-01",
        "end_date": datetime.today().strftime('%Y-%m-%d'),
        "limit": 500,
        "offset": 0
    }

    # Empty list to hold all transactions
    all_transactions = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            transactions = data.get('transactions', [])
            
            if not transactions:
                print("No more transactions found.")
                break
            
            all_transactions.extend(transactions)
            
            # Move to next page
            params['offset'] += len(transactions)
        
        elif response.status_code == 404:
            print("Error 404: Endpoint not found or no transactions available.")
            break
        
        else:
            print(f"Error {response.status_code}: {response.text}")
            break

    # Convert all collected transactions into a single DataFrame
    df = pd.DataFrame(all_transactions)

    # Save the dataframe
    output_path = '/Users/m1max/Downloads/plaid_transactions.csv'
    df.to_csv(output_path, index=False)

    print(f"✅ Downloaded {len(df)} transactions to {output_path}")

    # Show preview of dataframe
    print(df)
    print('transactions downloaded successfully')
    return df