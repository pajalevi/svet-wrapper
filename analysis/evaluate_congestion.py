import pandas as pd
import numpy as np
import os
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px


def plot_congestion_by_node(iso_name, data_all_nodes):
    zones = set(data_all_nodes["node_name"])
    # bins = [-np.inf, -1.0, -0.5, -0.1, 0, 0.1, 0.5, 1.0]
    # names = ['A: < -1.0', 'B: -1.0 ~ -0.5', 'C: -0.5 ~ -0.1', 'D: -0.1 ~ 0', 'E: 0 ~ 0.1', 'F: 0.1 ~ 0.5',
    #          'G: 0.5 ~ 1.0', 'H: 1.0 +']
    bins = [-np.inf, -1.0, -0.5, -0.1, 0, 0.1]
    names = ['A: < -1.0', 'B: -1.0 ~ -0.5', 'C: -0.5 ~ -0.1', 'D: -0.1 ~ 0', 'E: 0 ~ 0.1', 'F: 0.1 +']
    d = dict(enumerate(names, 1))

    data_all_nodes["congestion_ratio_to_total"] = data_all_nodes["congestion_price"] / data_all_nodes["lmp_total"]
    data_all_nodes["congestion_ratio_to_energy"] = data_all_nodes["congestion_price"] / data_all_nodes["energy_price"]
    data_all_nodes['congestion_ratio_to_total_bin'] = np.vectorize(d.get)\
        (np.digitize(data_all_nodes['congestion_ratio_to_total'], bins))
    data_all_nodes['congestion_ratio_to_energy_bin'] = np.vectorize(d.get)\
        (np.digitize(data_all_nodes['congestion_ratio_to_energy'], bins))

    summary = data_all_nodes.groupby(["node_name", "congestion_ratio_to_total_bin"])["congestion_ratio_to_total"]\
        .count().reset_index().sort_values(by="congestion_ratio_to_total_bin")
    summary["to_total_percentage"] = 100 * summary['congestion_ratio_to_total'] / 8784

    summary_2 = data_all_nodes.groupby(["node_name", "congestion_ratio_to_energy_bin"])["congestion_ratio_to_energy"]\
        .count().reset_index().sort_values(by="congestion_ratio_to_energy_bin")
    summary_2["to_energy_percentage"] = 100 * summary_2['congestion_ratio_to_energy'] / 8784

    # summary = data_all_nodes.groupby(["node_name"])["congestion_price"]\
    #     .mean().reset_index().sort_values(by="congestion_price")
    # summary["congestion_ratio_to_total_bin"] = "A"
    # summary["to_total_percentage"] = 0
    #
    # summary_2 = data_all_nodes.groupby(["node_name"])["congestion_price"]\
    #     .mean().reset_index().sort_values(by="congestion_price")
    # summary_2["congestion_ratio_to_energy_bin"] = "A"
    # summary_2["to_energy_percentage"] = 0


    fig = make_subplots(rows=len(list(zones)), cols=3)
    for i in range(len(list(zones))):
        zone = list(zones)[i]
        print(zone)
        data = data_all_nodes[data_all_nodes["node_name"] == zone].reset_index(drop=True).sort_values(
            by="datetime (hb)")
        fig.add_trace(go.Scatter(x=data["datetime (hb)"], y=data["congestion_ratio_to_total"], name=zone),
                      row=i + 1, col=1)
        fig.update_yaxes(range=[-2, 2], row=i + 1, col=1)
        data = data.sort_values(by="congestion_ratio_to_total_bin")

        fig.add_trace(go.Histogram(x=data["congestion_ratio_to_total"], name=zone, xbins=dict(size=0.1)),
                      row=i + 1, col=2)
        fig.update_xaxes(range=[-2, 2], row=i + 1, col=2)

        fig.add_trace(go.Histogram(histfunc="count", x=data["congestion_ratio_to_total_bin"], name=zone),
                      row=i + 1, col=3)
    fig.update_layout(height=len(list(zones)) * 400, title=iso_name, showlegend=False)

    return fig, summary, summary_2

# NYISO
nyiso_raw_all_zones = pd.read_csv("/Users/zhenhua/Desktop/price_data/nyiso_2019-20/OASIS_Day-Ahead_Market_Zonal_LBMP_allZones.csv")
nyiso_raw_all_zones["datetime (hb)"] = nyiso_raw_all_zones["Eastern Date Hour"]
nyiso_raw_all_zones["node_name"] = nyiso_raw_all_zones["Zone Name"]
nyiso_raw_all_zones["lmp_total"] = nyiso_raw_all_zones["DAM Zonal LBMP"]
nyiso_raw_all_zones["congestion_price"] = np.absolute(nyiso_raw_all_zones["DAM Zonal Congestion"])
nyiso_raw_all_zones["loss_price"] = nyiso_raw_all_zones["DAM Zonal Losses"]
nyiso_raw_all_zones["energy_price"] = nyiso_raw_all_zones["lmp_total"] - \
                                      nyiso_raw_all_zones["congestion_price"] - \
                                      nyiso_raw_all_zones["loss_price"]
fig, summary, summary_2 = plot_congestion_by_node(iso_name="nyiso", data_all_nodes=nyiso_raw_all_zones)
fig.show()
summary.to_csv("/Users/zhenhua/Desktop/price_data/nyiso_2019-20/summary_2019_all_nodes_abs.csv")
summary_2.to_csv("/Users/zhenhua/Desktop/price_data/nyiso_2019-20/summary_2_2019_all_nodes_abs.csv")
fig = px.bar(summary, x="node_name", y="to_total_percentage",
             color='congestion_ratio_to_total_bin', barmode='group',
             height=400)
fig.show()
fig = px.bar(summary_2, x="node_name", y="to_energy_percentage",
             color='congestion_ratio_to_energy_bin', barmode='group',
             height=400)
fig.show()

# PJM
pjm_raw_all_zones = pd.read_csv("/Users/zhenhua/Desktop/price_data/pjm_2019-20/da_hrl_lmps_2019_all_nodes.csv")
pjm_raw_all_zones["datetime (hb)"] = pjm_raw_all_zones["datetime_beginning_ept"]
pjm_raw_all_zones["node_name"] = pjm_raw_all_zones["pnode_name"]
pjm_raw_all_zones["lmp_total"] = pjm_raw_all_zones["total_lmp_da"]
pjm_raw_all_zones["congestion_price"] = np.absolute(pjm_raw_all_zones["congestion_price_da"])
pjm_raw_all_zones["energy_price"] = pjm_raw_all_zones["system_energy_price_da"]
pjm_raw_all_zones["loss_price"] = pjm_raw_all_zones["marginal_loss_price_da"]
fig, summary, summary_2 = plot_congestion_by_node(iso_name="pjm", data_all_nodes=pjm_raw_all_zones)
fig.show()
summary.to_csv("/Users/zhenhua/Desktop/price_data/pjm_2019-20/summary_2019_all_nodes_abs.csv")
summary_2.to_csv("/Users/zhenhua/Desktop/price_data/pjm_2019-20/summary_2_2019_all_nodes_abs.csv")
fig = px.bar(summary, x="node_name", y="to_total_percentage",
             color='congestion_ratio_to_total_bin', barmode='group',
             height=400)
fig.show()
fig = px.bar(summary_2, x="node_name", y="to_energy_percentage",
             color='congestion_ratio_to_energy_bin', barmode='group',
             height=400)
fig.show()

# ISO NE
# zones = ["ISO NE CA", "ME", "NH", "VT", "CT", "RI", "SEMA", "WCMA", "NEMA"]
# data = pd.DataFrame()
# for i in range(len(list(zones))):
#     isone_raw = pd.read_excel("/Users/zhenhua/Desktop/price_data/isone_2019-20/2019_smd_hourly.xlsx",
#                               zones[i])
#     isone_raw["node_name"] = str(zones[i])
#     print(str(zones[i]))
#     data = data.append(isone_raw, ignore_index=True)
# data.to_csv("/Users/zhenhua/Desktop/price_data/isone_2019-20/2019_smd_hourly_processed.csv")
isone_raw_all_zones = pd.read_csv("/Users/zhenhua/Desktop/price_data/isone_2019-20/2019_smd_hourly_processed.csv")
isone_raw_all_zones['datetime (hb)'] = pd.to_datetime(isone_raw_all_zones['Date'].astype(str) + ' ' +
                                                      (isone_raw_all_zones['Hr_End'].astype(int) - 1).astype(str) +
                                                      ':00:00')
isone_raw_all_zones["node_name"] = isone_raw_all_zones["node_name"]
isone_raw_all_zones["lmp_total"] = isone_raw_all_zones["DA_LMP"]
isone_raw_all_zones["congestion_price"] = np.absolute(isone_raw_all_zones["DA_CC"])
isone_raw_all_zones["energy_price"] = isone_raw_all_zones["DA_EC"]
isone_raw_all_zones["loss_price"] = isone_raw_all_zones["DA_MLC"]
fig, summary, summary_2 = plot_congestion_by_node(iso_name="iso ne", data_all_nodes=isone_raw_all_zones)
fig.show()
summary.to_csv("/Users/zhenhua/Desktop/price_data/isone_2019-20/summary_2019_all_nodes_abs.csv")
summary_2.to_csv("/Users/zhenhua/Desktop/price_data/isone_2019-20/summary_2_2019_all_nodes_abs.csv")
fig = px.bar(summary, x="node_name", y="to_total_percentage",
             color='congestion_ratio_to_total_bin', barmode='group',
             height=400)
fig.show()
fig = px.bar(summary_2, x="node_name", y="to_energy_percentage",
             color='congestion_ratio_to_energy_bin', barmode='group',
             height=400)
fig.show()

# CAISO
# folder = "/Users/zhenhua/Desktop/price_data/caiso_2019/MANVILLE_1_N001/"
# folder_data = pd.DataFrame()
# for file in os.listdir(folder + "original_data_2019/"):
#     print(file)
#     data = pd.read_csv(folder + "original_data_2019/" + file)
#     folder_data = folder_data.append(data, ignore_index=True)
#     folder_data = folder_data.sort_values(by="INTERVALSTARTTIME_GMT").reset_index(drop=True)
# folder_data.to_csv(folder + "2019_processed.csv")
oakland = pd.read_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/OAKLAND_1_B1/2019_PRC_LMP_DAM_processed.csv")
merced = pd.read_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/MERCED_1_N001/2019_PRC_LMP_DAM_processed.csv")
kearny = pd.read_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/KEARNY_6_B1/2019_PRC_LMP_DAM_processed.csv")
midway = pd.read_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/MIDWAY_1_B1/2019_processed.csv")
bervlly = pd.read_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/BERVLLY_6_N001/2019_processed.csv")
garcia = pd.read_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/GARCIA_6_N001/2019_processed.csv")
eastwood = pd.read_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/EASTWOOD_7_B1/2019_processed.csv")
manville = pd.read_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/MANVILLE_1_N001/2019_processed.csv")
data = oakland.append(merced, ignore_index=True)
data = data.append(kearny, ignore_index=True)
data = data.append(midway, ignore_index=True)
data = data.append(bervlly, ignore_index=True)
data = data.append(garcia, ignore_index=True)
data = data.append(eastwood, ignore_index=True)
data = data.append(manville, ignore_index=True)
data["node_name"] = data["PNODE_RESMRID"]
data = data.pivot_table(index=['INTERVALSTARTTIME_GMT', 'node_name'], columns="LMP_TYPE",
                                                      values="MW").reset_index().rename_axis(None, axis=1)
caiso_raw_all_zones = data.copy(deep=True)
caiso_raw_all_zones["datetime (hb)"] = caiso_raw_all_zones["INTERVALSTARTTIME_GMT"]
caiso_raw_all_zones["lmp_total"] = caiso_raw_all_zones["LMP"]
caiso_raw_all_zones["congestion_price"] = np.absolute(caiso_raw_all_zones["MCC"])
caiso_raw_all_zones["energy_price"] = caiso_raw_all_zones["MCE"]
caiso_raw_all_zones["loss_price"] = caiso_raw_all_zones["MCL"]
fig, summary, summary_2 = plot_congestion_by_node(iso_name="caiso", data_all_nodes=caiso_raw_all_zones)
fig.show()
summary.to_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/summary_2019_all_nodes_abs.csv")
summary_2.to_csv("/Users/zhenhua/Desktop/price_data/caiso_2019/summary_2_2019_all_nodes_abs.csv")
fig = px.bar(summary, x="node_name", y="to_total_percentage",
             color='congestion_ratio_to_total_bin', barmode='group',
             height=400)
fig.show()
fig = px.bar(summary_2, x="node_name", y="to_energy_percentage",
             color='congestion_ratio_to_energy_bin', barmode='group',
             height=400)
fig.show()
