import pandas as pd
import numpy as np
import os
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px


# CAISO
folder = "/Users/zhenhua/Desktop/price_data/caiso_2019/AS_SP26/"

folder_data = pd.DataFrame()
for file in os.listdir(folder + "original_data_2019/"):
    print(file)
    data = pd.read_csv(folder + "original_data_2019/" + file)
    folder_data = folder_data.append(data, ignore_index=True)
    folder_data = folder_data.sort_values(by="INTERVALSTARTTIME_GMT").reset_index(drop=True)

data = folder_data.pivot_table(index=['INTERVALSTARTTIME_GMT'], columns="ANC_TYPE",
                               values="MW").reset_index().rename_axis(None, axis=1)

data["Datetime (hb)"] = pd.to_datetime(data["INTERVALSTARTTIME_GMT"]).dt.tz_convert('America/Los_Angeles')
data["SR Price ($/kW)"] = data["SR"]
data["NSR Price ($/kW)"] = data["NR"]
data["Reg Up Price ($/kW)"] = data["RU"]
data["Reg Down Price ($/kW)"] = data["RD"]
data.to_csv(folder + "2019_processed.csv")
