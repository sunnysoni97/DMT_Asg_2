import pandas as pd
def replaceNaN(dataFrame):
    return dataFrame.fillna(0)

def parseDateTime(dataFrame):
    dataFrame["date_time"] = pd.to_datetime(dataFrame["date_time"])
    dataFrame["year"] = dataFrame["date_time"].dt.year
    dataFrame["month"] = dataFrame["date_time"].dt.month
    return dataFrame.drop('date_time', 1)    

def removeUselessColumns(dataFrame, threshold=90):
    sum_of_nulls = dataFrame.isnull().sum()
    number_of_records = len(dataFrame)
    percentages_of_nulls = (sum_of_nulls / number_of_records) * 100
    useless_columns = []
    for index, value in percentages_of_nulls.items():
        if value > threshold:
            useless_columns.append(index)
    return dataFrame.drop(useless_columns, 1)