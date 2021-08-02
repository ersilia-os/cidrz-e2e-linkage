import pandas as pd
import numpy as np


file_ca_source = "/Users/mwansa.lumpa/PhD/Datasets/excel_registers/Lusaka/"
file_dic_map = "/Users/mwansa.lumpa/PhD/Datasets/excel_registers/filemap.xlsx"

filestomerge = []
columns_of_interest = []


def merge_sources(sourcedir, filemap):
    mymap = pd.read_excel(filemap)

    tmp_df_lst = []

    for ind, row in mymap.iterrows():
        (
            filename,
            cols_str,
            col_names,
            comments,
            sheetname,
            facilityname,
            visittype,
        ) = mymap.iloc[ind]

        pathofinterest = file_ca_source + "/" + filename

        dataframe = file_to_dataframe(
            pathofinterest, cols_str=cols_str, sheetname=sheetname
        )

        tmpcols = list(dataframe)
        columns = col_names.split(",")
        cols_dict = {tmpcols[i]: columns[i].strip() for i in range(len(columns))}

        dataframe.rename(columns=cols_dict, inplace=True)

        print(filename, sheetname)
        print("before {0}".format(dataframe.shape))
        dataframe.dropna(subset=["enrol_date", "name"], how="all", inplace=True)
        print("after {0}".format(dataframe.shape))

        dataframe["facility"] = facilityname
        tmp_df_lst.append(dataframe)

    tmp_df = pd.DataFrame(columns=dataframe.columns)

    for df in tmp_df_lst:
        tmp_df = tmp_df.append(df, ignore_index=True)

    print("ALL merged files")
    print(tmp_df.shape)
    print(tmp_df.sample(10))

    return tmp_df


def file_to_dataframe(filepath, cols=None, sheetname=None, cols_str=None):
    parts = filepath.split(".")
    ext = parts[-1]

    dataframe = None

    if ext == "xlsx" or ext == "xls":
        dataframe = process_excel(filepath, sheetname=sheetname, cols_str=cols_str)

    return dataframe


def process_excel(filepath, cols=None, sheetname=None, cols_str=None):
    if cols:
        dataframe = pd.read_excel(filepath, names=cols, sheet_name=sheetname)
    if cols_str:
        dataframe = pd.read_excel(filepath, usecols=cols_str, sheet_name=sheetname)
    else:
        dataframe = pd.read_excel(filepath)

    return dataframe
