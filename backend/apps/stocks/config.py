"""
Stock configuration for FinLearn.
Easy to modify - just change this list to update tracked stocks.
"""

# List of stocks to track
# Format: (symbol, company_name, sector)
TRACKED_STOCKS = [
    ('AAPL', 'Apple Inc.', 'Technology'),
    ('MSFT', 'Microsoft Corporation', 'Technology'),
    ('GOOGL', 'Alphabet Inc.', 'Technology'),
    ('JPM', 'JPMorgan Chase & Co.', 'Finance'),
    ('V', 'Visa Inc.', 'Finance'),
    ('JNJ', 'Johnson & Johnson', 'Healthcare'),
    ('PG', 'Procter & Gamble Co.', 'Consumer Goods'),
    ('XOM', 'Exxon Mobil Corporation', 'Energy'),
    ('TSLA', 'Tesla Inc.', 'Automotive'),
    ('KO', 'The Coca-Cola Company', 'Consumer Goods'),
]

# Get just the symbols
STOCK_SYMBOLS = [stock[0] for stock in TRACKED_STOCKS]

# Stock update interval in seconds (for WebSocket)
UPDATE_INTERVAL = 30  # Update every 30 seconds

# Initial virtual balance for new users
INITIAL_VIRTUAL_BALANCE = 100000.00
