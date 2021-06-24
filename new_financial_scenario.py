import pandas as pd
import numpy as np
from vc_wrap import SvetObject

pd.options.display.width = 0
pd.options.mode.chained_assignment = None


def new_financial_scenario(proforma_old, npv_old, discount_rate=0.1, growth_rate=0.03):
    # make a SVET object so that we can call update_runs_log_csv(), setup_param_csv()

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


SvetObject.new_financial_scenario = new_financial_scenario
