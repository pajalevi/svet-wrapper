import pandas as pd
import numpy as np

pd.options.display.width = 0
pd.options.mode.chained_assignment = None


def update_financial_results(proforma_old, npv_old, discount_rate=0.1, growth_rate=0.03):
    proforma_csv = proforma_old.copy(deep=True)
    proforma_csv['project_year'] = np.arange(0, proforma_csv.shape[0])

    # Check if there is a user constraint column: if so, fix it
    if "User Constraints Value" in proforma_csv.columns:
        proforma_csv["User Constraints Value"] = proforma_csv['project_year']. \
            apply(lambda i: max(proforma_csv["User Constraints Value"]) * (1 + growth_rate) ** (i - 1))
        proforma_csv["User Constraints Value"][0] = 0
        proforma_csv["Yearly Net Value"] = proforma_csv.iloc[:, 1:-2].sum(axis=1)

    # Calculate NPV for each column
    npv_csv = npv_old.copy(deep=True)
    npv_values = {}
    for col_name in proforma_csv.columns[1:-1]:
        npv_values[col_name] = np.npv(discount_rate, proforma_csv[col_name])
        if col_name != "Yearly Net Value":
            npv_csv[col_name] = npv_values[col_name]
        else:
            npv_csv["Lifetime Present Value"] = npv_values[col_name]

    return proforma_csv, npv_csv


def new_financial_results(proforma_old, npv_old, params_path, ra_constraint=True):
    params = pd.read_csv(params_path)

    discount_rate = float(params.loc[(params['Key'] == "npv_discount_rate") &
                                     (params['Tag'] == "Finance"), 'Value'].values[0])/100
    growth_rate = float(params.loc[(params['Key'] == "inflation_rate") &
                                   (params['Tag'] == "Finance"), 'Value'].values[0])/100
    start_yr = float(params.loc[(params['Key'] == "start_year") &
                                (params['Tag'] == "Scenario"), 'Value'].values[0])
    end_yr = float(params.loc[(params['Key'] == "end_year") &
                              (params['Tag'] == "Scenario"), 'Value'].values[0])
    om_cost = float(params.loc[(params['Key'] == "fixedOM") &
                               (params['Tag'] == "Battery"), 'Value'].values[0])
    ccost = float(params.loc[(params['Key'] == "ccost_kwh") &
                             (params['Tag'] == "Battery"), 'Value'].values[0])
    monthly_data_file = str(params.loc[(params['Key'] == "monthly_data_filename") &
                                       (params['Tag'] == "Scenario"), 'Value'].values[0])
    batt_kw = float(params.loc[(params['Key'] == "ch_max_rated") &
                               (params['Tag'] == "Battery"), 'Value'].values[0])
    batt_kwh = float(params.loc[(params['Key'] == "ene_max_rated") &
                                (params['Tag'] == "Battery"), 'Value'].values[0])
    lifetime = int(end_yr - start_yr + 1)

    # get RA price
    monthly_data = pd.read_csv(monthly_data_file)
    ra_value = max(monthly_data['RA Capacity Price ($/kW)'])

    # copy over proforma, make it the correct size
    proforma_old.rename(columns={'Unnamed: 0': 'Year'}, inplace=True)
    proforma_old.iloc[0, 0] = np.NaN
    proforma_old["Year"] = pd.to_numeric(proforma_old["Year"], errors='coerce')
    if lifetime == proforma_old.shape[0] + 1:
        proforma_csv = proforma_old.copy(deep=True)
        proforma_csv['project_year'] = np.arange(0, proforma_csv.shape[0])
    elif lifetime < proforma_old.shape[0 + 1]:
        # subtract rows
        proforma_csv = proforma_old.copy(deep=True).iloc[0:(lifetime + 1), :]
        proforma_csv['project_year'] = np.arange(0, proforma_csv.shape[0])
    else:
        # add rows, propagate existing values for year
        proforma_csv = proforma_old.copy(deep=True).reindex(np.arange(0, lifetime + 1))
        proforma_csv['project_year'] = np.arange(0, proforma_csv.shape[0])
        proforma_csv.iloc[1:, 0] = proforma_csv['project_year']. \
            apply(lambda i: str(int(proforma_csv.iloc[1:, 0].min()) - 1 + int(i)))

    # Check if there is a user constraint column: if so, fix it
    if "User Constraints Value" in proforma_csv.columns:
        proforma_csv["User Constraints Value"] = proforma_csv['project_year']. \
            apply(lambda i: max(proforma_csv["User Constraints Value"]) * (1 + growth_rate) ** (i - 1))
        proforma_csv["User Constraints Value"][0] = 0
        proforma_csv["Yearly Net Value"] = proforma_csv.iloc[:, 1:-2].sum(axis=1)

    # change capital cost
    ind1 = proforma_csv.columns.str.contains("Capital Cost")
    ind2 = np.logical_not(proforma_csv.columns.str.contains("Site Load"))
    ind3 = ind1 & ind2
    proforma_csv.loc[0, ind3] = ccost * batt_kwh

    # change om cost
    ind1 = proforma_csv.columns.str.contains("Fixed O&M Cost")
    ind2 = np.logical_not(proforma_csv.columns.str.contains("Site Load"))
    ind3 = ind1 & ind2
    proforma_csv.loc[1, ind3] = om_cost * batt_kw

    # change RA value
    if "Resource AdequacyCapacity Payment" in proforma_csv.columns:
        ind1 = proforma_csv.columns.str.contains("Resource Adequacy")
        proforma_csv.loc[1, ind1] = ra_value * batt_kw * 12
    elif ra_constraint & ("User Constraints Value" in proforma_csv.columns):
        ind1 = proforma_csv.columns.str.contains("User Constraints")
        proforma_csv.loc[1, ind1] = ra_value * batt_kw * 12

    # extend all rows (except first and last two) accordingly
    for c in proforma_csv.columns[1:-2]:
        proforma_csv.loc[1:,c] = proforma_csv.loc[1:,"project_year"]. \
            apply(lambda i: proforma_csv.loc[1, c] * (1 + growth_rate) ** (i - 1))

    # Calculate NPV for each column
    npv_csv = npv_old.copy(deep=True)
    npv_values = {}
    for col_name in proforma_csv.columns[1:-1]:
        npv_values[col_name] = np.npv(discount_rate, proforma_csv[col_name])
        if col_name != "Yearly Net Value":
            npv_csv[col_name] = npv_values[col_name]
        else:
            npv_csv["Lifetime Present Value"] = npv_values[col_name]

    # TODO: payback period calculation
    cost = proforma_csv.iloc[0,1:-2].sum(axis=0)
    yearly_revenue = proforma_csv.iloc[1,1:-2].sum(axis=0)
    d = {'Payback_Years': [cost/yearly_revenue]}
    payback_csv = pd.DataFrame(data=d)

    return proforma_csv, npv_csv, payback_csv
