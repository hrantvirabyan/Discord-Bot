import yfinance as yf
import pandas as pd

def get_market_movers():
    # Fetch the list of S&P 500 companies
    sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(sp500_url)
    sp500_df = sp500_table[0]
    symbols = sp500_df['Symbol'].tolist()

    # Fetch market data for these companies in bulk
    data = yf.download(symbols, period="1d")

    # Filter for daily movers with market cap above 500 million
    movers = []
    for symbol in symbols:
        try:
            stock = data['Adj Close'][symbol]
            if not stock.empty:
                close_price = stock[-1]
                ticker = yf.Ticker(symbol)
                info = ticker.info
                market_cap = info.get('marketCap', 0)
                prev_close = info.get('previousClose', 0)
                percent_change = (close_price - prev_close) / prev_close  if prev_close else 0

                if abs(percent_change) > 0.05:
                    movers.append({
                        'Symbol': symbol,
                        'Previous Close': prev_close,
                        'Close': close_price,
                        'Percent Change': percent_change * 100,
                        'Market Cap': market_cap
                    })

        except Exception as e:
            print(f"Could not process {symbol}: {e}")

    return pd.DataFrame(movers)
"""
def get_qqq_data():
    symbol = 'AAPL'
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d")  # Fetches data for the last two days

    if not data.empty and len(data['Close']) > 1 and 'Open' in data.columns:
        close_price = data['Close'].iloc[-1]  # Latest close price
        open_price = data['Open'].iloc[-1]  # Open price for the current day

        # Calculate the percent change correctly using close and open prices
        percent_change = ((close_price - open_price) / open_price) * 100 if open_price else 'N/A'

        # Attempt to fetch the market cap
        info = ticker.info
        market_cap = info.get('marketCap', 'N/A')

        return {
            'Symbol': symbol,
            'Open': open_price,
            'Close': close_price,
            'Percent Change': percent_change,
            'Market Cap': market_cap
        }
    else:
        return {
            'Symbol': symbol,
            'Open': 'N/A',
            'Close': 'N/A',
            'Percent Change': 'N/A',
            'Market Cap': 'N/A'
        }
    """
"""
def get_spy_data():
    symbol = 'SPY'
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d")  # Fetches data for the last two days

    if not data.empty and len(data['Close']) > 1:
        close_price = data['Close'].iloc[-1]  # Latest close price
        prev_close = data['Close'].iloc[-2]  # Previous close price

        # Calculate the percent change correctly
        percent_change = ((close_price - prev_close) / prev_close) * 100

        # Attempt to fetch the market cap
        info = ticker.info
        market_cap = info.get('marketCap')

        return {
            'Symbol': symbol,
            'Previous Close': prev_close,
            'Close': close_price,
            'Percent Change': percent_change,
            'Market Cap': market_cap if market_cap else 'N/A'
        }
    else:
        return {
            'Symbol': symbol,
            'Previous Close': 'N/A',
            'Close': 'N/A',
            'Percent Change': 'N/A',
            'Market Cap': 'N/A'
        }
    """



def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    #print(info)
    curr_price = info.get('currentPrice', 0)
    close_price = info.get('previousClose', 0)

    # Calculate percent change if both open and close prices are available
    if curr_price and close_price:
        percent_change = round(((curr_price - close_price) / close_price) * 100, 2)
    else:
        percent_change = 'N/A'
    # Extract necessary details, handle cases where data may not be available
    data = {
        'name': info.get('longName', 'N/A'),
        'current_price': info.get('currentPrice', 'N/A'),
        'open': info.get('open', 'N/A'),
        'close': info.get('previousClose', 'N/A'),
        'percent_change': percent_change,
        'market_cap': info.get('marketCap', 'N/A'),
        'index_name': info.get('indexName', 'N/A')  # 'indexName' might not always be available
    }

    return data
    

# Example usage
#movers_df = get_market_movers()
#print(movers_df)

