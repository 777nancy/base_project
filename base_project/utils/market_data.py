import pandas_datareader as pdr


def fetch_stock_data(ticker_symbol, data_source, start_date, end_date=None, drop_na=True):
    """データソースから株価のデータを取得する

    Args:
        ticker_symbol: 取得する企業のシンボル
        data_source: データソース
        start_date: 取得開始日時
        end_date: 終了日
        drop_na: 欠損データを削除可否(デフォルト: True)

    Returns:
        pandas.DataFrame
            カラム
                High
                Low
                Close
                Volume
                Adj Close
    """
    stock_data_df = pdr.DataReader(ticker_symbol, data_source, start_date, end_date)

    if drop_na:
        stock_data_df = stock_data_df.dropna()

    return stock_data_df


def fetch_stock_data_from_yf(ticker_symbol, start_date, end_date=None, drop_na=True):
    """yahoo financeから株価のデータを取得する

    Args:
        ticker_symbol: 取得する企業のシンボル
        start_date: 取得開始日時
        end_date: 終了日
        drop_na: 欠損データを削除可否(デフォルト: True)

    Returns:
        pandas.DataFrame
            カラム
                High
                Low
                Close
                Volume
                Adj Close

    """

    df = fetch_stock_data(ticker_symbol, 'yahoo', start_date, end_date, drop_na)
    return df[df.index >= start_date]
