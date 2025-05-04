import plaid_transactions
import plaid_assets
from dotenv import load_dotenv
import pandas as pd
import os

# Load .env file
load_dotenv()

# Get your token
token = os.getenv('lunchmoney_token')


print(type(plaid_transactions.transactions(token)))

# print(plaid_assets.assets(token))