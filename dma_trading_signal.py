import pandas as pd
from tia.bbg import LocalTerminal
import pandas as pd

# Single SID, Multiple Valid Fields
resp = LocalTerminal.get_reference_data(['EURUSD Curncy', 'USDAUD Curncy'], ['MOV_AVG_30D','MOV_AVG_50D', 'MOV_AVG_100D','MOV_AVG_200D'])
df = resp.as_frame()

mov_avg_30d = df['MOV_AVG_30D']
mov_avg_100d = df['MOV_AVG_100D']
#print(df.describe())
print(mov_avg_30d)
print(mov_avg_100d)
head = df.head()
print(head)

print("my name is james ")