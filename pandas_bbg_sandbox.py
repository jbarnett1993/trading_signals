import pandas as pd
from tia.bbg import LocalTerminal


# Single SID, Multiple Valid Fields
resp = LocalTerminal.get_reference_data(['EURUSD Curncy', 'AUDUSD Curncy'], ['MOV_AVG_30D','MOV_AVG_50D', 'MOV_AVG_100D','MOV_AVG_200D'])
df = resp.as_frame()

#mov_avg_30d = df['MOV_AVG_30D']
#mov_avg_100d = df['MOV_AVG_100D']
#print(mov_avg_30d)
#print(mov_avg_100d)




# Adding a new column to the dataframe based on a calculation from other columns
df['30d - 100d'] = df['MOV_AVG_30D'] - df ['MOV_AVG_100D']

# testing the use of iloc and loc for indexing a specific cell
test = df.loc['EURUSD Curncy', '30d - 100d']
test1 =df.iloc[0,4]
print(test)
print(test1)
print(df)

## adding a column to the dataframe to say 'B' when the 30dma is higher than the 100dma

df['bs'] = 'NA'
df['bs'][df['30d - 100d'] > 0] ='B'
df['bs'][df['30d - 100d'] < 0] ='S'

#eurusd = df.loc['EURUSD Curncy']
#eurusd1 = df.iloc[0]
#print(eurusd)
#print('space between printing rows')
#print(eurusd1)
#print(df.index)
print(df)


#TODO: index the dataframe correctly
#TODO: append a column based on a calculation from the indexed dataframe object
#TODO: push out to pdf
#TODO: graph and highlight where the dma's cross
