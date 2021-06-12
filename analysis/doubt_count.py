import pandas as pd
import numpy as np

from plotly import graph_objs as go
from plotly.subplots import make_subplots

from vc_wrap import SvetObject


def run_double_count(iso_name, tariff):
    # Initialize results
    Finance_customer_tariff_filename = "/Users/zhenhua/Desktop/price_data/tariff_data_fake/{}.csv".format(
        tariff)
    Scenario_time_series_filename = "/Users/zhenhua/Desktop/price_data/hourly_timeseries_{}_2019_200x.csv".format(
        iso_name)
    results = pd.DataFrame(columns=["Case #", "DA ETS", "SR", "NSR",
                                    "Avoided Demand", "Avoided Energy", "Capex", "O&M Cost", "NPV"])

    # Case 0a: use retail rates for RS
    case0a = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                        shortname="{} RS on".format(iso_name),
                        description="{} 200x".format(iso_name),
                        Scenario_n="36",
                        Finance_npv_discount_rate="7",
                        Scenario_time_series_filename=Scenario_time_series_filename,
                        Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                        DCM_active='no', retailTimeShift_active='yes', DA_active='no',
                        SR_active='no', NSR_active='no', FR_active="no", FR_CombinedMarket="1")
    case0a.run_storagevet()

    results = results.append({"Case #": "0 - RS",
                              "Avoided Demand": case0a.npv_new["Avoided Demand Charge"][0],
                              "Avoided Energy": case0a.npv_new["Avoided Energy Charge"][0],
                              "Capex": case0a.npv_new["2MW-5hr Capital Cost"][0],
                              "O&M Cost": case0a.npv_new["2MW-5hr Fixed O&M Cost"][0],
                              "NPV": case0a.npv_new["Lifetime Present Value"][0]}, ignore_index=True)

    # Case 0b: use retail rates for RS+DCM
    case0b = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                        shortname="{} RS+DCM on".format(iso_name),
                        description="{} 200x".format(iso_name),
                        Scenario_n="36",
                        Finance_npv_discount_rate="7",
                        Scenario_time_series_filename=Scenario_time_series_filename,
                        Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                        DCM_active='yes', retailTimeShift_active='yes', DA_active='no',
                        SR_active='no', NSR_active='no', FR_active="no", FR_CombinedMarket="1")
    case0b.run_storagevet()

    results = results.append({"Case #": "0 - RS+DCM",
                              "Avoided Demand": case0b.npv_new["Avoided Demand Charge"][0],
                              "Avoided Energy": case0b.npv_new["Avoided Energy Charge"][0],
                              "Capex": case0b.npv_new["2MW-5hr Capital Cost"][0],
                              "O&M Cost": case0b.npv_new["2MW-5hr Fixed O&M Cost"][0],
                              "NPV": case0b.npv_new["Lifetime Present Value"][0]}, ignore_index=True)

    # Case 0c: use DA rates for wholesale participation only
    case0c = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                        shortname="{} DA+SR on".format(iso_name),
                        description="{} 200x".format(iso_name),
                        Scenario_n="36",
                        Finance_npv_discount_rate="7",
                        Scenario_time_series_filename=Scenario_time_series_filename,
                        Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                        DCM_active='no', retailTimeShift_active='no', DA_active='yes',
                        SR_active='yes', NSR_active='no', FR_active="no", FR_CombinedMarket="1")
    case0c.run_storagevet()

    results = results.append({"Case #": "0 - DA+SR",
                              "DA ETS": case0c.npv_new["DA ETS"][0],
                              "SR": case0c.npv_new["Spinning Reserves"][0],
                              "Capex": case0c.npv_new["2MW-5hr Capital Cost"][0],
                              "O&M Cost": case0c.npv_new["2MW-5hr Fixed O&M Cost"][0],
                              "NPV": case0c.npv_new["Lifetime Present Value"][0]}, ignore_index=True)

    case1b = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                        shortname="{} DA+SR+DCM on".format(iso_name),
                        description="{} 200x".format(iso_name),
                        Scenario_n="36",
                        Finance_npv_discount_rate="7",
                        Scenario_time_series_filename=Scenario_time_series_filename,
                        Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                        DCM_active='yes', retailTimeShift_active='no', DA_active='yes',
                        SR_active='yes', NSR_active='no', FR_active="no", FR_CombinedMarket="1")
    case1b.run_storagevet()

    results = results.append({"Case #": "1 - use DA for DA+SR+DCM after double counting", "DA ETS": case1b.npv_new["DA ETS"][0],
                              "SR": case1b.npv_new["Spinning Reserves"][0],
                              "Avoided Demand": case1b.npv_new["Avoided Demand Charge"][0],
                              "Avoided Energy": case1b.npv_new["Avoided Energy Charge"][0],
                              "Capex": case1b.npv_new["2MW-5hr Capital Cost"][0],
                              "O&M Cost": case1b.npv_new["2MW-5hr Fixed O&M Cost"][0],
                              "NPV": case1b.npv_new["Lifetime Present Value"][0]}, ignore_index=True)
    results = results.append({"Case #": "1 - use DA for DA+SR+DCM before double counting", "DA ETS": case1b.npv_new["DA ETS"][0],
                              "SR": case1b.npv_new["Spinning Reserves"][0],
                              "Avoided Demand": case1b.npv_new["Avoided Demand Charge"][0],
                              "Avoided Energy": 0,
                              "Capex": case1b.npv_new["2MW-5hr Capital Cost"][0],
                              "O&M Cost": case1b.npv_new["2MW-5hr Fixed O&M Cost"][0],
                              "NPV": case1b.npv_new["Lifetime Present Value"][0] -
                                     case1b.npv_new["Avoided Energy Charge"][0]}, ignore_index=True)
    results = results.append({"Case #": "1 - double count delta",
                              "NPV": case1b.npv_new["Avoided Energy Charge"][0]}, ignore_index=True)

    case2a = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                        shortname="{} RS+SR+DCM on".format(iso_name),
                        description="{} 200x".format(iso_name),
                        Scenario_n="36",
                        Finance_npv_discount_rate="7",
                        Scenario_time_series_filename=Scenario_time_series_filename,
                        Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                        DCM_active='yes', retailTimeShift_active='yes', DA_active='no',
                        SR_active='yes', NSR_active='no', FR_active="no", FR_CombinedMarket="1")
    case2a.run_storagevet()

    results = results.append({"Case #": "2 - use RS for RS+SR+DCM before double counting",
                              "SR": case2a.npv_new["Spinning Reserves"][0],
                              "Avoided Demand": case2a.npv_new["Avoided Demand Charge"][0],
                              "Avoided Energy": case2a.npv_new["Avoided Energy Charge"][0],
                              "Capex": case2a.npv_new["2MW-5hr Capital Cost"][0],
                              "O&M Cost": case2a.npv_new["2MW-5hr Fixed O&M Cost"][0],
                              "NPV": case2a.npv_new["Lifetime Present Value"][0]}, ignore_index=True)

    # TODO
    case2a_ts_results = pd.read_csv(case2a.runID_dispatch_timeseries_path)
    da_ets_corrected_yearly = np.dot(case2a.initial_hourly_timeseries["DA Price ($/kWh)"],
                                     case2a_ts_results["Load (kW)"]) - \
                              np.dot(case2a.initial_hourly_timeseries["DA Price ($/kWh)"],
                                     case2a_ts_results["Net Load (kW)"])
    da_ets_corrected_npv_list = []
    for i in range(0, 15):
        da_ets_corrected_npv_list.append(da_ets_corrected_yearly * (1 + 0.03) ** i)
    da_ets_corrected_npv_list = [0] + da_ets_corrected_npv_list
    da_ets_corrected_npv = np.npv(0.07, da_ets_corrected_npv_list)
    results = results.append({"Case #": "2 - use RS for RS+SR+DCM after double counting",
                              "DA ETS": da_ets_corrected_npv,
                              "SR": case2a.npv_new["Spinning Reserves"][0],
                              "Avoided Demand": case2a.npv_new["Avoided Demand Charge"][0],
                              "Avoided Energy": case2a.npv_new["Avoided Energy Charge"][0],
                              "Capex": case2a.npv_new["2MW-5hr Capital Cost"][0],
                              "O&M Cost": case2a.npv_new["2MW-5hr Fixed O&M Cost"][0],
                              "NPV": case2a.npv_new["Lifetime Present Value"][0] + da_ets_corrected_npv},
                             ignore_index=True)
    results = results.append({"Case #": "2 - double count delta",
                              "NPV": da_ets_corrected_npv},
                             ignore_index=True)

    case3 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                       default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                       shortname="{} DA+RS+DCM+SR on".format(iso_name),
                       description="{} 200x".format(iso_name),
                       Scenario_n="36",
                       Finance_npv_discount_rate="7",
                       Scenario_time_series_filename=Scenario_time_series_filename,
                       Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                       DCM_active='yes', retailTimeShift_active='yes', DA_active='yes',
                       SR_active='yes', NSR_active='no', FR_active="no", FR_CombinedMarket="1")
    case3.run_storagevet()

    results = results.append({"Case #": "3 - use DA and RS for DA+SR+RS+DCM",
                              "DA ETS": case3.npv_new["DA ETS"][0],
                              "SR": case3.npv_new["Spinning Reserves"][0],
                              "Avoided Demand": case3.npv_new["Avoided Demand Charge"][0],
                              "Avoided Energy": case3.npv_new["Avoided Energy Charge"][0],
                              "Capex": case3.npv_new["2MW-5hr Capital Cost"][0],
                              "O&M Cost": case3.npv_new["2MW-5hr Fixed O&M Cost"][0],
                              "NPV": case3.npv_new["Lifetime Present Value"][0]}, ignore_index=True)
    results.sort_values(by="Case #").reset_index(drop=True)\
        .to_csv("/Users/zhenhua/Desktop/double_count_results_0410/{}_{}.csv".format(iso_name, tariff))

    # Plot prices & results
    case1b_ts_results = pd.read_csv(case1b.runID_dispatch_timeseries_path)
    case2a_ts_results = pd.read_csv(case2a.runID_dispatch_timeseries_path)
    case1b_ts_results["date"] = pd.to_datetime(case1b_ts_results["Start Datetime (hb)"]).dt.date
    case1b_ts_results["hour (hb)"] = pd.to_datetime(case1b_ts_results["Start Datetime (hb)"]).dt.hour
    case2a_ts_results["date"] = pd.to_datetime(case2a_ts_results["Start Datetime (hb)"]).dt.date
    case2a_ts_results["hour (hb)"] = pd.to_datetime(case2a_ts_results["Start Datetime (hb)"]).dt.hour

    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=("DA and retail", "SR",
                                        "DA as signal, RS to double count",
                                        "RS as signal, DA to double count"))
    for date in set(case1b_ts_results["date"]):
        data = case1b_ts_results[case1b_ts_results["date"] == date].reset_index()
        fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["DA Price Signal ($/kWh)"], line=dict(color='blue'),
                                 opacity=0.2, name=str(date)), row=1, col=1)
        fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["SR Price Signal ($/kW)"], line=dict(color='green'),
                                 opacity=0.5, name=str(date)), row=1, col=2)
        fig.add_trace(go.Scatter(x=data["hour (hb)"], y=data["2MW-5hr Power (kW)"], line=dict(color='blue'),
                                 opacity=0.2, name=str(date)), row=2, col=1)
        data2 = case2a_ts_results[case2a_ts_results["date"] == date].reset_index()
        fig.add_trace(go.Scatter(x=data2["hour (hb)"], y=data2["Energy Price ($/kWh)"], line=dict(color='red'),
                                 opacity=0.5, name=str(date)), row=1, col=1)
        fig.add_trace(go.Scatter(x=data2["hour (hb)"], y=data2["2MW-5hr Power (kW)"], line=dict(color='blue'),
                                 opacity=0.2, name=str(date)), row=2, col=2)
    fig.update_layout(title="{}_{}".format(iso_name, tariff))

    return results, fig


# results, fig = run_double_count(iso_name="caiso", tariff="peak4-14-18")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak4-15-19")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak4-16-20")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak4-17-21")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak4-18-22")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak4-19-23")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak4-20-24")
# fig.show()

# results, fig = run_double_count(iso_name="caiso", tariff="peak12-18")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak13-19")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak14-20")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak15-21")
# fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak16-22")
# fig.show()
results, fig = run_double_count(iso_name="caiso", tariff="peak17-23")
fig.show()
# results, fig = run_double_count(iso_name="caiso", tariff="peak18-24")
# fig.show()
