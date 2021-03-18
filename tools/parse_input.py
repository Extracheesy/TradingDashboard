import os, fnmatch
import pandas as pd
import numpy as np


def addRow(df,ls):
    """
    Given a dataframe and a list, append the list as a new row to the dataframe.

    :param df: <DataFrame> The original dataframe
    :param ls: <list> The new row to be added
    :return: <DataFrame> The dataframe with the newly appended row
    """

    numEl = len(ls)

    newRow = pd.DataFrame(np.array(ls).reshape(1,numEl), columns = list(df.columns))

    df = df.append(newRow, ignore_index=True)

    return df

def parse_input_directory():

    print("current path:",os.getcwd())
    os.chdir("./inputfile")
    print("working path:",os.getcwd())

    df_trade_list = pd.DataFrame()
    df_trade_list.insert(0, "file", 0)
    df_trade_list.insert(len(df_trade_list.columns), "date", 0)
    df_trade_list.insert(len(df_trade_list.columns), "iter", 0)
    df_trade_list.insert(len(df_trade_list.columns), "$_daily", 0)
    df_trade_list.insert(len(df_trade_list.columns), "%_daily", 0)
    df_trade_list.insert(len(df_trade_list.columns), "$_max", 0)
    df_trade_list.insert(len(df_trade_list.columns), "%_max", 0)
    df_trade_list.insert(len(df_trade_list.columns), "$_min", 0)
    df_trade_list.insert(len(df_trade_list.columns), "%_min", 0)
    df_trade_list.insert(len(df_trade_list.columns), "$_mean", 0)
    df_trade_list.insert(len(df_trade_list.columns), "%_mean", 0)

    listOfFilesToRemove = os.listdir('./')
    pattern = "*.csv"
    for entry in listOfFilesToRemove:
        list_data = []
        if fnmatch.fnmatch(entry, pattern) and (entry.startswith('trace_test_csv_')):
            print("csv input file : ",entry)
            df = pd.read_csv(entry, index_col=None, header=0)
            list_data.append(entry)
            date = df.date.unique()[0][0:10]
            list_data.append(date)
            iter = len(df["total_$"])
            list_data.append(iter - 1)

            end_of_day = round(df["total_$"][iter - 1],0)
            list_data.append(end_of_day)
            end_of_day = round(df["total_$"][iter - 1] * 100 / df["total_$"][0],3)
            list_data.append(end_of_day)

            max = round(df["total_$"].max(),0)
            list_data.append(max)
            max = round(df["total_$"].max() * 100 / df["total_$"][0],3)
            list_data.append(max)
            min = round(df["total_$"].min(),0)
            list_data.append(min)
            min = round(df["total_$"].min() * 100 / df["total_$"][0],3)
            list_data.append(min)
            mean = round(df["total_$"].mean(),0)
            list_data.append(mean)
            mean = round(df["total_$"].mean() * 100 / df["total_$"][0],1)
            list_data.append(mean)
            df_trade_list = addRow(df_trade_list, list_data)

    #df_trade_list = df_trade_list.sort_values(['%_daily'], ascending=True, ignore_index=True)
    #df_trade_list = df_trade_list.sort_values(['%_daily'], ascending=True)

    os.chdir("./..")
    print("back to root: ", os.getcwd())

    return df_trade_list

def get_df_data_from_date(date):

    print("current path:",os.getcwd())
    os.chdir("./inputfile")
    print("working path:",os.getcwd())

    data_file = "trace_test_csv_" + date + ".csv"

    df = pd.read_csv(data_file)

    df = get_df_buy_cell(df)

    df = get_df_profit_line(df)

    df_stocks = get_stocks_table(df)

    os.chdir("./..")
    print("back to root: ", os.getcwd())

    return df, df_stocks

def get_df_buy_cell(df):

    df.insert(len(df.columns), "buy", 0)
    df.insert(len(df.columns), "sell", 0)
    df.insert(len(df.columns), "sum", 0)

    for i in range(0, len(df), 1):
        sum = 0
        buy = 0
        sell = 0
        for column in df.columns:
            if column.endswith('_nb'):
                sum = sum + df[column][i]
            if column.endswith('_act'):
                if(df[column][i] >= 0):
                    buy = buy + df[column][i]
                else:
                    column_nb = column[:-3] + "nb"
                    if (df[column_nb][i] != 0):
                        sell = sell + df[column][i]
        df["sum"][i] = sum
        df["buy"][i] = buy * 100
        df["sell"][i] = sell * 100

    return df

def get_df_profit_line(df):

    df.insert(len(df.columns), "profit_0.05", df["total_$"][0] * 0.05 / 100 + df["total_$"][0])
    df.insert(len(df.columns), "profit_0.1", df["total_$"][0] * 0.1 / 100 + df["total_$"][0])
    df.insert(len(df.columns), "profit_0", df["total_$"][0])

    return df

def get_stocks_table(df):

    df_stk = pd.DataFrame()

    df_stk.insert(0, "date", 0)
    df_stk.insert(len(df_stk.columns), "tic", 0)
    df_stk.insert(len(df_stk.columns), "open", 0)
    df_stk.insert(len(df_stk.columns), "close", 0)
    df_stk.insert(len(df_stk.columns), "trend", 0)
    df_stk.insert(len(df_stk.columns), "high", 0)
    df_stk.insert(len(df_stk.columns), "low", 0)
    df_stk.insert(len(df_stk.columns), "earning", 0)

    for column in df.columns:
        list_data = []
        if column.endswith('_val_$'):
            date = df["date"][0]
            list_data.append(date[:10])
            tic = column[:-6]
            list_data.append(tic)
            open = round(df[column][0],2)
            list_data.append(open)
            close = round(df[column][len(df) - 2],2)
            list_data.append(close)
            toto = df[column][len(df) - 1]
            titi = df[column][0]
            tata = toto - titi
            if(( df[column][len(df) - 2] - df[column][0] ) >= 0):
                list_data.append("up")
            else:
                list_data.append("down")
            high = round(df[column].max(),2)
            list_data.append(high)
            low = round(df[column].min(),2)
            list_data.append(low)

            earning = round(df[tic + "_flow_$"].sum(), 2)
            list_data.append(earning)

            df_stk = addRow(df_stk, list_data)

    return df_stk

def get_percent( init_val, result):

    return ( (result - init_val) * 100 / init_val )