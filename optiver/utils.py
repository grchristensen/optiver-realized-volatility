import os

import numpy as np
import pandas as pd


def realized_volatility(book_data: pd.DataFrame):
    wap = (
        book_data["bid_price1"] * book_data["ask_size1"]
        + book_data["ask_price1"] * book_data["bid_size1"]
    ) / (book_data["bid_size1"] + book_data["ask_size1"])
    log_wap = np.log(wap)

    log_returns = log_wap.groupby(level=("time_id")).diff().dropna()

    return np.sqrt((log_returns ** 2).groupby(level="time_id").sum())


def generate_dfs(source):
    def generate_df(hdf_file):
        # Filename format: stock_#.h5
        stock_id = int(hdf_file[6:-3])
        df = pd.read_hdf(source / hdf_file)

        return stock_id, df.loc[stock_id]

    return (
        (stock_id, df)
        for stock_id, df in (generate_df(hdf_file) for hdf_file in os.listdir(source))
    )
