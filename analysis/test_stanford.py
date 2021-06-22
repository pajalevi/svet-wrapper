from vc_wrap import SvetObject
from plotly import graph_objs as go
import pandas as pd

Scenario_time_series_filename = "/Users/zhenhua/Desktop/price_data/stanford_data/hourly_timeseries_2019_eCEF.csv"
# Finance_customer_tariff_filename = "/Users/zhenhua/Desktop/price_data/tariff_data_fake/e5d4.csv"
Finance_customer_tariff_filename = "/Users/zhenhua/Desktop/price_data/tariff_data/original_documents/caiso_pge_b20_2020.csv"

# # value stacking, should be the best scenario
# for power in [100, 200, 500, 1000, 2000, 3000, 4000, 5000, 6000, 8000]:
#     site = "eCEF"
#     size = power * 4
#     Scenario_n = "36"
#     Finance_npv_discount_rate = "7"
#
#     stanford = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                           default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
#                           shortname=site + " RS+DCM on",
#                           description=site,
#                           Battery_ch_max_rated=power, Battery_dis_max_rated=power, Battery_ene_max_rated=size,
#                           Scenario_n=Scenario_n,
#                           Finance_npv_discount_rate=Finance_npv_discount_rate,
#                           Scenario_time_series_filename=Scenario_time_series_filename,
#                           Finance_customer_tariff_filename=Finance_customer_tariff_filename,
#                           DCM_active='yes', retailTimeShift_active='yes',
#                           DA_active='no', SR_active='no', NSR_active='no', FR_active="no", FR_CombinedMarket="1"
#                           )
#     stanford.run_storagevet()

site = "eCEF"
Scenario_n = "36"
Finance_npv_discount_rate = "7"
Scenario_time_series_filename = "/Users/zhenhua/Desktop/price_data/stanford_data/hourly_timeseries_2019_eCEF.csv"

cef = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                 default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                 shortname=site + " RS+DCM on",
                 description=site,
                 Battery_ch_max_rated=2000, Battery_dis_max_rated=2000, Battery_ene_max_rated=8000,
                 Scenario_n=Scenario_n,
                 Finance_npv_discount_rate=Finance_npv_discount_rate,
                 Scenario_time_series_filename=Scenario_time_series_filename,
                 Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                 DCM_active='yes', retailTimeShift_active='yes',
                 DA_active='no', SR_active='no', NSR_active='no', FR_active="no", FR_CombinedMarket="1"
                 )
cef.run_storagevet()

site = "eCampus"
Scenario_n = "36"
Finance_npv_discount_rate = "7"
Scenario_time_series_filename = "/Users/zhenhua/Desktop/price_data/stanford_data/hourly_timeseries_2019_eCampus.csv"

campus = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                    default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                    shortname=site + " RS+DCM on",
                    description=site,
                    Battery_ch_max_rated=2000, Battery_dis_max_rated=2000, Battery_ene_max_rated=8000,
                    Scenario_n=Scenario_n,
                    Finance_npv_discount_rate=Finance_npv_discount_rate,
                    Scenario_time_series_filename=Scenario_time_series_filename,
                    Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                    DCM_active='yes', retailTimeShift_active='yes',
                    DA_active='no', SR_active='no', NSR_active='no', FR_active="no", FR_CombinedMarket="1"
                    )
campus.run_storagevet()

cef_results = pd.read_csv(cef.runID_dispatch_timeseries_path)
cef_results["date"] = pd.to_datetime(cef_results["Start Datetime (hb)"]).dt.date
cef_results["hour (hb)"] = pd.to_datetime(cef_results["Start Datetime (hb)"]).dt.hour
campus_results = pd.read_csv(campus.runID_dispatch_timeseries_path)
campus_results["date"] = pd.to_datetime(campus_results["Start Datetime (hb)"]).dt.date
campus_results["hour (hb)"] = pd.to_datetime(campus_results["Start Datetime (hb)"]).dt.hour

fig = go.Figure()
fig.add_trace(go.Scatter(x=cef_results["Start Datetime (hb)"], y=cef_results["Load (kW)"], name="CEF load"))
fig.add_trace(go.Scatter(x=cef_results["Start Datetime (hb)"], y=cef_results["Net Load (kW)"], name="CEF Net load"))
fig.add_trace(go.Scatter(x=campus_results["Start Datetime (hb)"], y=campus_results["Load (kW)"], name="Campus load"))
fig.add_trace(
    go.Scatter(x=campus_results["Start Datetime (hb)"], y=campus_results["Net Load (kW)"], name="Campus Net load"))
fig.show()

daily = go.Figure()
for date in (set(cef_results["date"][720:1440])):
    data = cef_results[cef_results["date"] == date].reset_index()
    daily.add_trace(go.Scatter(x=data["hour (hb)"], y=data["Load (kW)"], line=dict(color='skyblue'),
                               name="cef " + str(date)))
    daily.add_trace(go.Scatter(x=data["hour (hb)"], y=data["Net Load (kW)"], line=dict(color='darkblue'),
                               name="cef net" + str(date)))
    data_2 = campus_results[campus_results["date"] == date].reset_index()
    daily.add_trace(go.Scatter(x=data_2["hour (hb)"], y=data_2["Load (kW)"], line=dict(color='orange'),
                               name="campus " + str(date)))
    daily.add_trace(go.Scatter(x=data_2["hour (hb)"], y=data_2["Net Load (kW)"], line=dict(color='purple'),
                               name="campus net" + str(date)))
daily.show()

battery = go.Figure()
for date in (set(cef_results["date"][720:1440])):
    data = cef_results[cef_results["date"] == date].reset_index()
    battery.add_trace(go.Scatter(x=data["hour (hb)"], y=data["Total Storage Power (kW)"], line=dict(color='blue'),
                                 name="battery@cef " + str(date)))
    data_2 = campus_results[campus_results["date"] == date].reset_index()
    battery.add_trace(go.Scatter(x=data_2["hour (hb)"], y=data_2["Total Storage Power (kW)"], line=dict(color='darkgreen'),
                                 name="battery@campus " + str(date)))
battery.show()
