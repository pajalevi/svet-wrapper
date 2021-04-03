import pandas as pd
import os
from plotly import graph_objs as go

price_path = "/Users/zhenhua/Desktop/price_data/"

caiso = pd.read_csv("/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv")
da = pd.DataFrame()
da["datetime"] = caiso["Datetime (he)"]
da["caiso"] = caiso["DA Price ($/kWh)"]

res = pd.DataFrame()
res["datetime"] = caiso["Datetime (he)"]
res["caiso sr"] = caiso["SR Price ($/kW)"]
res["caiso nsr"] = caiso["NSR Price ($/kW)"]

fr = pd.DataFrame()
fr["datetime"] = caiso["Datetime (he)"]
fr["caiso up"] = caiso["Reg Up Price ($/kW)"]
fr["caiso down"] = caiso["Reg Down Price ($/kW)"]

ts_list = []
for file in os.listdir(price_path):
    if "hourly_timeseries" in file:
        ts_list.append(file)

for file in ts_list:
    name = file[18:]
    data = pd.read_csv(price_path + file)
    da[name] = data["DA Price ($/kWh)"]
    res[name + " sr"] = data["SR Price ($/kW)"]
    res[name + " nsr"] = data["NSR Price ($/kW)"]
    if "ercot" in file:
        fr["ercor up"] = data["Reg Up Price ($/kW)"]
        fr["ercor down"] = data["Reg Down Price ($/kW)"]
    else:
        fr[name] = data["FR Price ($/kW)"]

da_fig = go.Figure()
for col in da.columns[1:]:
    da_fig.add_trace(go.Scatter(x=da["datetime"], y=da[col], mode='lines', name=col))
da_fig.show()

res_fig = go.Figure()
for col in res.columns[1:]:
    res_fig.add_trace(go.Scatter(x=res["datetime"], y=res[col], mode='lines', name=col))
res_fig.show()

fr_fig = go.Figure()
for col in fr.columns[1:]:
    fr_fig.add_trace(go.Scatter(x=fr["datetime"], y=fr[col], mode='lines', name=col))
fr_fig.show()

