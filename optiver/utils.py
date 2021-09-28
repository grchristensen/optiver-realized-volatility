import os

import numpy as np
import pandas as pd


def group_bucket(df):
    return df.groupby(level="time_id")


def agg_df(series, name: str):
    data_dict = {}

    data_dict[f"{name}_mean"] = series.mean()
    data_dict[f"{name}_std"] = series.std()
    data_dict[f"{name}_min"] = series.min()
    data_dict[f"{name}_med"] = series.median()
    data_dict[f"{name}_max"] = series.max()

    return pd.DataFrame(data_dict)


def realized_volatility1(order_book):
    log_returns = lr1(order_book)

    return get_realized_volatility(log_returns)


def realized_volatility2(order_book):
    log_returns = lr2(order_book)

    return get_realized_volatility(log_returns)


def wap1(order_book):
    return get_wap(
        order_book["bid_price1"],
        order_book["bid_size1"],
        order_book["ask_price1"],
        order_book["ask_size1"],
    )


def wap2(order_book):
    return get_wap(
        order_book["bid_price2"],
        order_book["bid_size2"],
        order_book["ask_price2"],
        order_book["ask_size2"],
    )


def lr1(order_book):
    wap = wap1(order_book)
    return get_log_returns(wap)


def lr2(order_book):
    wap = wap2(order_book)
    return get_log_returns(wap)


def bas1(order_book):
    return get_bas(order_book["bid_price1"], order_book["ask_price1"])


def bas2(order_book):
    return get_bas(order_book["bid_price2"], order_book["ask_price2"])


def exchange(trade_book):
    return get_exchanges(trade_book["price"], trade_book["size"])


def exchange_total(trade_book):
    return exchange(trade_book).groupby(level="time_id").sum()


def get_realized_volatility(log_returns):
    return np.sqrt((log_returns ** 2).groupby(level="time_id").sum())


def get_log_returns(wap):
    return np.log(wap).groupby(level="time_id").diff().dropna()


def get_wap(bid_price, bid_size, ask_price, ask_size):
    return (bid_price * ask_size + ask_price * bid_size) / (bid_size + ask_size)


def get_bas(bid_price, ask_price):
    return ask_price / bid_price - 1


def get_exchanges(price, size):
    return price * size


def preprocess_dfs(order_source, trade_source, preprocess_fn, tqdm=None):
    stock_ids = []
    preprocessed_dfs = []

    if tqdm is not None:
        iterator = tqdm(os.listdir(order_source))
    else:
        iterator = os.listdir(order_source)

    for hdf_file in iterator:
        stock_id = int(hdf_file[6:-3])

        order_book = pd.read_hdf(order_source / hdf_file).loc[stock_id]

        try:
            trade_book = pd.read_hdf(trade_source / hdf_file).loc[stock_id]
            trade_book = fix_index(trade_book, order_book)
        except FileNotFoundError:
            trade_book = pd.DataFrame(
                {"price": None, "size": None, "order_count": None},
                index=order_book.index,
            )

        stock_ids.append(stock_id)
        preprocessed_dfs.append(preprocess_fn(order_book, trade_book))

    preprocessed_df = pd.concat(
        {
            stock_id: preprocessed_df
            for stock_id, preprocessed_df in zip(stock_ids, preprocessed_dfs)
        },
        names=("stock_id", "time_id"),
    )

    return preprocessed_df


def fix_index(trade_book, order_book):
    order_buckets = group_bucket(order_book).mean()
    trade_buckets = group_bucket(trade_book).mean()

    leftover = order_buckets.drop(trade_buckets.index)

    if len(leftover) != 0:
        for time_bucket in leftover.index.get_level_values("time_id"):
            trade_book.loc[(time_bucket, 0), :] = {
                "price": None,
                "size": None,
                "order_count": None,
            }

    return trade_book


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
