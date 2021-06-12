import pandas as pd
import numpy as np
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

# da_fig = go.Figure()
# for col in da.columns[1:]:
#     da_fig.add_trace(go.Scatter(x=da["datetime"], y=da[col], mode='lines', name=col))
# da_fig.update_layout(title="DA prices")
# da_fig.show()
#
# res_fig = go.Figure()
# for col in res.columns[1:]:
#     res_fig.add_trace(go.Scatter(x=res["datetime"], y=res[col], mode='lines', name=col))
# res_fig.update_layout(title="SR and NSR prices")
# res_fig.show()
#
# fr_fig = go.Figure()
# for col in fr.columns[1:]:
#     fr_fig.add_trace(go.Scatter(x=fr["datetime"], y=fr[col], mode='lines', name=col))
# fr_fig.update_layout(title="FR prices")
# fr_fig.show()

pjm = pd.read_csv("/Users/zhenhua/Desktop/price_data/hourly_timeseries_pjm_2019.csv")
pjm["date"] = pd.to_datetime(pjm["Datetime (he)"]).dt.date
pjm["hour (hb)"] = pd.to_datetime(pjm["Datetime (he)"]).dt.hour - 1
jan_retail = [0.10531, 0.10531, 0.10531, 0.10531, 0.10531, 0.10531, 0.10531, 0.10531, 0.10531, 0.10531, 0.10531,
              0.10531, 0.10531, 0.10531, 0.10531, 0.10531, 0.13592, 0.13592, 0.13592, 0.13592, 0.13592, 0.10531,
              0.10531, 0.10531]

fig = go.Figure()
for date in set(pjm["date"]):
    data = pjm[pjm["date"] == date].reset_index()
    fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["DA Price ($/kWh)"], line=dict(color='blue'),
                             opacity=0.2, name=str(date)))
    fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["SR Price ($/kW)"], line=dict(color='green'),
                             opacity=0.5, name=str(date)))
fig.add_trace(go.Scatter(x=np.arange(0, 24), y=jan_retail, line=dict(color='red'), name="retails"))
fig.update_layout(title="PJM DA prices")
fig.show()

caiso["date"] = pd.to_datetime(caiso["Datetime (he)"]).dt.date
caiso["hour (hb)"] = pd.to_datetime(caiso["Datetime (he)"]).dt.hour - 1
fig = go.Figure()
for date in set(caiso["date"]):
    data = caiso[caiso["date"] == date].reset_index()
    fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["DA Price ($/kWh)"], line=dict(color='blue'),
                             opacity=0.2, name=str(date)))
    fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["SR Price ($/kW)"], line=dict(color='green'),
                             opacity=0.5, name=str(date)))
fig.add_trace(go.Scatter(x=np.arange(0, 24), y=jan_retail, line=dict(color='red'), name="retails"))
fig.update_layout(title="CAISO DA prices")
fig.show()


