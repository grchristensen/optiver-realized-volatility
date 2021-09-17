import numpy as np
import pandas as pd


def realized_volatility(book_data: pd.DataFrame):
    wap = (
        book_data["bid_price1"] * book_data["ask_size1"]
        + book_data["ask_price1"] * book_data["bid_size1"]
    ) / (book_data["bid_size1"] + book_data["ask_size1"])
    log_wap = np.log(wap)

    log_returns = log_wap.groupby(level="time_id").diff().dropna()

    return np.sqrt((log_returns ** 2).groupby(level="time_id").sum())
