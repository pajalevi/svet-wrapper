"""
vs_wrap.py

This wrapper script encloses calls to run_StorageVET.py in a version control framework.
It does the following
- edit default params based on arguments
- make a results folder for this run that is named with the runID
- save params in Results folder
- note this run in a run log with associated runID and git commit hash

Zhenhua Zhang Jan 8 2021
"""

import pandas as pd
import numpy as np
import os
import subprocess
import datetime
import shutil

from proforma_update import update_financial_results

pd.options.mode.chained_assignment = None

class SvetObject:
    def __init__(self, SVet_absolute_path, description, shortname, **params):
        self.SVet_absolute_path = SVet_absolute_path
        self.SVet_script = SVet_absolute_path + "run_StorageVET.py"
        self.default_params_file = SVet_absolute_path + "Model_Parameters_2v1-0-2_default.csv"
        self.runs_log_file = SVet_absolute_path + "Results/runsLog.csv"
        self.results_path = SVet_absolute_path + "Results/"

        self.description = description
        self.shortname = shortname

        self.params = params

        # Check if run log csv has been created, if not create a new csv with relevant column names
        if not (os.path.exists(self.runs_log_file)):
            runsLog = pd.DataFrame(columns=["runID", "date", "gitID", "shortname", "description", "status"], index=None)
            runsLog.to_csv(self.runs_log_file, index=None)
            # TODO: add more cols here if we want to track more info
        else:
            runsLog = pd.read_csv(self.runs_log_file)

        # Identify new runID by examining runs log, and update runs log
        self.runID = str(int(runsLog['runID'].max()) + 1) if runsLog['runID'].max() is not np.nan else str(1)
        print("This run has ID number " + self.runID)
        update_runlog_csv(self.SVet_absolute_path, self.runs_log_file, self.runID, self.shortname, self.description)

        # Create param csv from default param csv
        self.runID_result_folder_path = self.results_path + "output_run" + self.runID + "_" + self.shortname
        self.runID_param_path = self.runID_result_folder_path + "/params_run" + self.runID + ".csv"
        self.runID_dispatch_timeseries_path = self.runID_result_folder_path + \
                                              "/timeseries_results_runID" + self.runID + ".csv"
        self.new_params = setup_param_csv(self.params, self.default_params_file, self.runID,
                                          self.runID_result_folder_path, self.runID_param_path)
        # TODO: add npv or payback file path here if needed

        # Save initial Scenario_time_series_filename into the results folder
        initial_hourly_timeseries = pd.read_csv(self.params['Scenario_time_series_filename'])
        initial_hourly_timeseries.to_csv(self.runID_result_folder_path + "/_initial_hourly_timeseries_runID{}.csv"
                                         .format(self.runID), index=False)
        self.initial_hourly_timeseries = initial_hourly_timeseries

        # Run StorageVET with version control
        run_storagevet(self.SVet_script, self.runs_log_file, self.runID,
                       self.runID_result_folder_path, self.runID_param_path)


def update_runlog_csv(SVet_absolute_path, runs_log_file, runID, shortname, description):
    """Creates a new entry in Run Log"""
    # Identify current git hash
    # this must be called from within the git repo in order to work
    old_path = os.getcwd()
    os.chdir(SVet_absolute_path)
    try:
        gitID_raw = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
        gitID = gitID_raw.strip().decode('ascii')
    except:
        gitID = "No git repository"
    os.chdir(old_path)

    # Get date
    date = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    # Create entry in runs log TODO: add more cols here if needed
    new_run_log_line = "\n" + str(runID) + "," + date + "," + gitID + "," + \
                       shortname.replace(",", ".") + "," + description.replace(",", ".")
    # Append line
    with open(runs_log_file, 'a') as rl:
        rl.write(new_run_log_line)


def setup_param_csv(params, default_params_file, runID, runID_result_folder_path, runID_param_path):
    """This function takes an arbitrary dict of params to modify, creates the appropriate
  params csv, and saves it in result_fol. It returns the full filepath. The keys in params
  must have the format 'Tag_Key'  """

    # Create a runID result folder
    if os.path.exists(runID_result_folder_path):
        shutil.rmtree(runID_result_folder_path)
    os.makedirs(runID_result_folder_path)

    # Add Results_dir_absolute_path and Results_label to params
    params['Results_dir_absolute_path'] = runID_result_folder_path + "/"
    params['Results_label'] = "_runID" + str(runID)
    params['Results_errors_log_path'] = runID_result_folder_path + "/"

    # Load default params csv
    default_params_file = pd.read_csv(default_params_file)
    new_params = default_params_file.copy(deep=True)

    # parse params arg and change params
    for p in params:
        # parse out tag from key
        tag, key = p.split("_", 1)
        filter_tag = new_params.Tag == tag

        if key == "Active" or key == "active":
            # change activity of that tag
            filter_activation = new_params.Active != "."
            filter_all = filter_tag & filter_activation
            if sum(filter_all) != 1:
                raise RuntimeError(
                    "Identified the wrong number of rows to change for Active status for tag " + str(tag))
            new_params.loc[filter_all, 'Active'] = params[p]
        else:
            # identify correct row, return error if not found
            filter_key = new_params.Key == key
            filter_all = filter_tag & filter_key
            # change value
            new_params.loc[filter_all, 'Value'] = params[p]

    # Save new params
    new_params.to_csv(runID_param_path, index=False)
    return new_params


def run_storagevet(SVet_script, runs_log_file, runID, runID_result_folder_path, runID_param_path):
    """Runs StorageVET via command line"""
    # Check that result folder exists with param file in it
    if not (os.path.exists(runID_param_path)):
        raise FileNotFoundError("Params file does not exist. Given path was " + runID_param_path)

    # Call StorageVET
    print("Running StorageVET for runID" + runID + " with parameters in " + runID_param_path)
    process = subprocess.Popen(["python", SVet_script, runID_param_path],
                               stdout=subprocess.PIPE)

    # Read output in realtime
    while True:
        line = process.stdout.readline()
        if not line:
            break

    # Check error log file for the current run
    with open(runID_result_folder_path + r"/\errors_log.log", 'r') as f:
        lines = [str(line) for line in f]
        if len(lines) != 1:
            status = "ERROR"
        else:
            status = "COMPLETED"
    # Check if npv in results folder
    all_file_name = ''
    for f in os.listdir(runID_result_folder_path + "/"):
        all_file_name += str(f)
    status = "ERROR" if 'npv' not in all_file_name else "COMPLETED"

    # Update npv and proforma results
    if status == "COMPLETED":
        proforma_old = pd.read_csv(runID_result_folder_path + "/pro_forma_runID" + runID + ".csv")
        npv_old = pd.read_csv(runID_result_folder_path + "/npv_runID" + runID + ".csv")
        proforma_new, npv_new = update_financial_results(proforma_old, npv_old,
                                                         discount_rate=0.1, growth_rate=0.03)
        proforma_new.to_csv(runID_result_folder_path + "/_new_pro_forma_runID" + runID + ".csv", index=False)
        npv_new.to_csv(runID_result_folder_path + "/_new_npv_runID" + runID + ".csv", index=False)

    # Save status to runlogs, remove entry and folder in cases of failure
    # if status == "ERROR":
    #     shutil.rmtree(self.results_path + result_fol)
    # else:
    #     pass

    # For now, we can log in status in cases of failure as well
    runsLog = pd.read_csv(runs_log_file)
    runsLog.loc[runsLog['runID'] == int(runID), ['status']] = status
    runsLog.to_csv(runs_log_file, index=None)
