from vc_wrap import SvetObject

from plotly import graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import os

folder_path = "/Users/zhenhua/Downloads/COMMERCIAL_LOAD_DATA_E_PLUS_OUTPUT.part1/USA_CA_Oakland.Intl.AP.724930_TMY3/"

fig = make_subplots(rows=16, cols=1, subplot_titles=os.listdir(folder_path))
for i in range(len(os.listdir(folder_path))):
    file = os.listdir(folder_path)[i]
    data = pd.read_csv(folder_path + file)
    data["date"] = data["Date/Time"].map(lambda x: x[1:6])
    data["month"] = data["Date/Time"].map(lambda x: x[1:3])
    data["hour_he"] = data["Date/Time"].map(lambda x: x[8:10])
    for month in list(set(data["month"])):
        data_sub = data[data["month"] == month].reset_index()
        fig.add_trace(
            go.Scatter(x=data_sub["hour_he"], y=data_sub["Electricity:Facility [kW](Hourly)"], line=dict(color='blue'),
                       name="cef " + str(month)),
            row=i + 1, col=1)
fig.update_layout(height=6400, showlegend=False)
fig.show()
