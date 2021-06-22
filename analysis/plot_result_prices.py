import pandas as pd
import numpy as np
import os
from plotly import graph_objs as go
from plotly.subplots import make_subplots

caiso = pd.read_csv("/Applications/storagevet2v101/StorageVET-master-git/Results/output_run7_caiso DA+SR+DCM on/timeseries_results_runID7.csv")
retail = pd.read_csv("/Applications/storagevet2v101/StorageVET-master-git/Results/output_run9_caiso RS+SR+DCM on/timeseries_results_runID9.csv")
caiso["date"] = pd.to_datetime(caiso["Start Datetime (hb)"]).dt.date
caiso["hour (hb)"] = pd.to_datetime(caiso["Start Datetime (hb)"]).dt.hour
retail["date"] = pd.to_datetime(caiso["Start Datetime (hb)"]).dt.date
retail["hour (hb)"] = pd.to_datetime(caiso["Start Datetime (hb)"]).dt.hour


fig = make_subplots(rows=2, cols=2,
                    subplot_titles=("DA and retail", "SR",
                                    "DA as signal, RS to double count",
                                    "RS as signal, DA to double count"))
for date in set(caiso["date"]):
    data = caiso[caiso["date"] == date].reset_index()
    fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["DA Price Signal ($/kWh)"], line=dict(color='blue'),
                             opacity=0.2, name=str(date)), row=1, col=1)
    fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["SR Price Signal ($/kW)"], line=dict(color='green'),
                             opacity=0.5, name=str(date)), row=1, col=2)
    fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["2MW-5hr Power (kW)"], line=dict(color='blue'),
                             opacity=0.2, name=str(date)), row=2, col=1)
    data2 = retail[retail["date"] == date].reset_index()
    fig.add_trace(go.Scatter(x=data2["hour (hb)"], y=data2["Energy Price ($/kWh)"], line=dict(color='red'),
                             opacity=0.5, name=str(date)), row=1, col=1)
    fig.add_trace(go.Scatter(x=data2["hour (hb)"], y=data2["2MW-5hr Power (kW)"], line=dict(color='blue'),
                             opacity=0.2, name=str(date)), row=2, col=2)
fig.update_layout(title="CAISO 5-11pm")
fig.show()


