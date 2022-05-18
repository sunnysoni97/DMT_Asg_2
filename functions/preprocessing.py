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
    dataFrame = dataFrame.drop(useless_columns, 1)
    dataFrame = dataFrame.drop(['comp3_rate','comp3_inv'], 1)
    return dataFrame, useless_columns

def mergeComps(dataFrame):
    ## when using a threshold of 90%, we remove data from comp : 1, 3, 4, 6, 7
    dataFrame['comp_rate'] = dataFrame[['comp2_rate', 'comp5_rate', ## we take the minimum,  
                                        'comp8_rate']].min(axis=1)  ##because taking mean could make us lose data about competitors cheaper price
    dataFrame['comp_inv'] = dataFrame[['comp2_inv', 'comp5_inv', 
                                       'comp8_inv']].mean(axis=1) ## we take the mean because it tells us how many competitors have the same room
    dataFrame['comp_rate_percent_diff'] = dataFrame[['comp2_rate_percent_diff', 'comp5_rate_percent_diff', 
                                       'comp8_rate_percent_diff']].max(axis=1) ## we take max to find the competitor with the best deal
    
    dataFrame = dataFrame.drop(['comp2_rate', 'comp5_rate', 'comp8_rate','comp2_inv', 'comp5_inv', 'comp8_inv',
                                'comp2_rate_percent_diff', 'comp5_rate_percent_diff', 'comp8_rate_percent_diff'], 1)
    return dataFrame
    
    