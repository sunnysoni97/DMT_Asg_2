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
    
    #dataFrame = dataFrame.drop(['comp2_rate', 'comp5_rate', 'comp8_rate','comp2_inv', 'comp5_inv', 'comp8_inv',
    #                            'comp2_rate_percent_diff', 'comp5_rate_percent_diff', 'comp8_rate_percent_diff'], 1)
    return dataFrame



#THIS IS UNUSED FOR NOW
def replaceNanWithAvg(dataFrame:pd.DataFrame) -> pd.DataFrame:
    out_df = dataFrame.copy()
    out_df = out_df.fillna(out_df.mean())
    return out_df

#EVERYTHING BELOW IS USEFUL
def mergeCompsAll(dataFrame:pd.DataFrame) -> pd.DataFrame:
    out_df = dataFrame.copy()
    rate_cols = [f'comp{i}_rate' for i in range(1,9)]
    inv_cols = [f'comp{i}_inv' for i in range(1,9)]
    rate_per_cols = [f'comp{i}_rate_percent_diff' for i in range(1,9)]

    rate_slice = out_df[rate_cols]
    inv_slice = out_df[inv_cols]
    rate_per_slice = out_df[rate_per_cols]
    out_df['comp_rate'] = rate_slice.mode(axis=1,numeric_only=True,dropna=True).iloc[:,0]
    out_df['comp_inv'] = inv_slice.mode(axis=1,numeric_only=True,dropna=True).iloc[:,0]
    out_df['comp_rate_percent_diff'] = rate_per_slice.mean(axis=1, numeric_only=True, skipna=True)
    return out_df


def fill_comp_rate(dataFrame:pd.DataFrame) -> pd.DataFrame:
    out_df = dataFrame.copy()
    out_df['comp_rate'] = out_df['comp_rate'].fillna(out_df['comp_rate'].mode().values[0])
    return out_df

def fill_comp_inv(dataFrame:pd.DataFrame) -> pd.DataFrame:
    out_df = dataFrame.copy()
    out_df['comp_inv'] = out_df['comp_inv'].fillna(out_df['comp_inv'].mode().values[0])
    return out_df

def fill_rate_diff(dataFrame:pd.DataFrame) -> pd.DataFrame:
    out_df = dataFrame.copy()
    out_df['comp_rate_percent_diff'] = out_df['comp_rate_percent_diff'].fillna(out_df['comp_rate_percent_diff'].mean())
    return out_df
