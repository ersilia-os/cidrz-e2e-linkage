import pandas as pd
import numpy as np
import logging

class Data:

    def __init__(self, dataframe, name=None):
        self.data = dataframe
        self.name = name

    def column_summary(self, column_name):
        """returns: tuple colname, count total, count unique"""
        return (column_name, self.data[column_name].count(), self.data[column_name].nunique())

    def summary(self, cols=None):
        summary = []
        if cols is None:
            cols = list(self.data)
        for col in cols:
            summary.append(self.column_summary(col))
        return summary

    def comp_table_inserts(self, dataframe, field, data_state, metric, value):
        dataframe = dataframe.append({'field': field,
                                      'data_state': data_state,
                                      'metric': metric,
                                      'value': value
                          }, ignore_index=True)

        return dataframe

    def compare_to_counts(self, secondobj, comp_mapping):
        results = pd.DataFrame(columns=['field', 'data_state', 'metric', 'value'])

        for orig_col_name, mapped_col_name in comp_mapping.items():
            results = self.comp_table_inserts(results, orig_col_name, 'cleaned', 'number unique', secondobj[mapped_col_name].nunique())
            results = self.comp_table_inserts(results, orig_col_name, 'raw', 'number unique', self.data[orig_col_name].nunique())

            results = self.comp_table_inserts(results, orig_col_name, 'cleaned', 'total_counts', secondobj[mapped_col_name].count())
            results = self.comp_table_inserts(results, orig_col_name, 'raw', 'total_counts', self.data[orig_col_name].count())

        return results


    def compare_summaries(self, dataframe, columns=None, column_names=None):
        tocomparedf = Data(dataframe)
        tocomparedf.name = 'object to compare'
        tmpsummary = tocomparedf.summary()

        currentsummary = self.summary()

        comparison = {}

        for colname, count, unique in currentsummary:
            comparison[colname.lower()] = [(count, unique)]

        for colname, count, unique in tmpsummary:
            if colname.lower() in comparison:
                comparison[colname.lower()].append((count, unique))
            else:
                comparison[colname.lower()] = [(np.NaN, np.NaN)]
                comparison[colname.lower()].append((count, unique))

        print("Comparing {0} vs {1}".format(self.name, tocomparedf.name))
        print("{:<20}{:<30}{:<30}".format("colname", "before (count, unique)", "after (count, unique"))
        for key, value in comparison.items():
            #if value is None:
                #print("{:<20}{:<30}{:<30}".format(key, str(value[0]), str(value[1])))
            print("{:<20}{:<30}{:<30}".format(key, str(value[0]), str(value[1])))

        return comparison

    def pretty_print(self):
        summary = self.summary()
        rows, columns = self.data.shape
        print("Files Details - Total row {0}, total columns {1}".format(rows, columns))
        print('{:<20}{:<20}{:<10}'.format("Col_name","Count", "Unique"))
        for col, count, unique in summary:
            print('{:<20}{:<20}{:<10}'.format(col, count, unique))
