import pandas as pd
import numpy as np
import os


def calc_kwyr_value(proforma, batt_kw):
    # calculate $/kW-yr value for each column
    #kwyr_values = {}
    kwyr_values = pd.DataFrame(columns = proforma.columns[1:-1], index=['0'])

    for col_name in proforma.columns[1:-1]:
        kwyr_values.loc['0',col_name] = proforma.loc[1, col_name] / float(batt_kw)

    return kwyr_values


def eval_run_value_kwyr(runID, results_path):
    # locate output file
    output_folders = os.listdir(results_path)
    output_files = [f for f in output_folders if 'output_run' + runID in f]
    if len(output_files) != 1:
        raise (RuntimeError("more than one output_file identified for this runID"))
    output_file = output_files[0]

    # load params file and ID batt_kw
    params_file = results_path + output_file + "/params_run" + str(runID) + ".csv"
    params = pd.read_csv(params_file)
    filter_key = params.Tag == "Battery"
    filter_tag = params.Key == "dis_max_rated"
    filter_all = filter_tag & filter_key
    batt_kw = params.loc[filter_all, "Value"]

    # load profroma
    proforma = pd.read_csv(results_path + output_file + "/_new_pro_forma_runID" + runID + ".csv")

    # call calc_kwyr_value
    kwyr_values = calc_kwyr_value(proforma, batt_kw)

    # save csv
    kwyr_values.to_csv(results_path + output_file + "/_kwyr_values_run" + runID + ".csv")


runIDs = range(263,362)#150,262)
path = "/Applications/storagevet2v101/StorageVET-master-git/Results/"
for r in runIDs:
    print("evaluating run " + str(r))
    eval_run_value_kwyr(str(r), path)
