import pandas as pd
from tia.bbg import LocalTerminal
import pandas as pd

# Single SID, Multiple Valid Fields
resp = LocalTerminal.get_reference_data(['EURUSD Curncy', 'USDAUD Curncy'], ['MOV_AVG_30D','MOV_AVG_50D', 'MOV_AVG_100D','MOV_AVG_200D'])
df = resp.as_frame()

z = df['MOV_AVG_30D']
print(df.describe())

print(z)