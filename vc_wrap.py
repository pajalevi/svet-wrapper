"""
vs_wrap.py

This wrapper script encloses calls to run_StorageVET.py in a version control framework.
It does the following
- edit default params based on arguments
- make a results folder for this run that is named with the runID
- save params in Results folder
- note this run in a run log with associated runID and git commit hash

Zhenhua Zhang Jan 30 2021
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
    def __init__(self, SVet_absolute_path, description, shortname,
                 default_params_file="Model_Parameters_2v1-0-2_default.csv",
                 **argument_list):
        # Specify StorageVET related params
        self.SVet_absolute_path = SVet_absolute_path
        self.SVet_script = SVet_absolute_path + "run_StorageVET.py"
        self.default_params_file = SVet_absolute_path + default_params_file
        self.runs_log_file = SVet_absolute_path + "Results/runsLog.csv"
        self.results_path = SVet_absolute_path + "Results/"

        # Initialize params for the current run
        self.description = description
        self.shortname = shortname
        self.argument_list = argument_list
        self.runID = str()
        self.runID_result_folder_path = str()
        self.runID_param_path = str()
        self.runID_dispatch_timeseries_path = str()
        self.new_params = pd.DataFrame()
        self.initial_hourly_timeseries = pd.DataFrame()
        self.discount_rate = float()
        self.npv_new = dict()

    def update_runs_log_csv(self):
        """Creates a new entry in Run Log"""
        # Identify current git hash, this must be called from within the git repo in order to work
        old_path = os.getcwd()
        os.chdir(self.SVet_absolute_path)
        try:
            gitID_raw = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
            gitID = gitID_raw.strip().decode('ascii')
        except:
            gitID = "No git repository"
        os.chdir(old_path)

        # Get date
        date = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

        # Check if run log csv has been created, if not create a new csv with relevant column names
        if not (os.path.exists(self.runs_log_file)):
            runs_log = pd.DataFrame(columns=["runID", "date", "gitID", "shortname", "description", "status"],
                                    index=None)
            runs_log.to_csv(self.runs_log_file, index=None)
            # TODO: add more cols here if we want to track more info
        else:
            runs_log = pd.read_csv(self.runs_log_file)

        # Create entry in runs log TODO: add more cols here if needed
        runID = str(int(runs_log['runID'].max()) + 1) if runs_log['runID'].max() is not np.nan else str(1)
        print("This run has ID number " + runID)
        new_run_log_line = "\n" + str(runID) + "," + date + "," + gitID + "," + \
                           self.shortname.replace(",", ".") + "," + self.description.replace(",", ".")
        with open(self.runs_log_file, 'a') as rl:
            rl.write(new_run_log_line)

        # Update attributes
        self.runID = runID
        self.runID_result_folder_path = self.results_path + "output_run" + self.runID + "_" + self.shortname
        self.runID_param_path = self.runID_result_folder_path + "/params_run" + self.runID + ".csv"
        self.runID_dispatch_timeseries_path = self.runID_result_folder_path + \
                                              "/timeseries_results_runID" + self.runID + ".csv"

    def setup_param_csv(self):
        """This function takes an arbitrary dict of params to modify, creates the appropriate
      params csv, and saves it in result_fol. It returns the full filepath. The keys in params
      must have the format 'Tag_Key'  """

        # Create a runID result folder
        if os.path.exists(self.runID_result_folder_path):
            shutil.rmtree(self.runID_result_folder_path)
        os.makedirs(self.runID_result_folder_path)

        # Add Results_dir_absolute_path and Results_label to argument_list
        self.argument_list['Results_dir_absolute_path'] = self.runID_result_folder_path + "/"
        self.argument_list['Results_label'] = "_runID" + str(self.runID)
        self.argument_list['Results_errors_log_path'] = self.runID_result_folder_path + "/"

        # Load default params csv
        default_params_file = pd.read_csv(self.default_params_file)
        new_params = default_params_file.copy(deep=True)
        # Parse params arg and change params
        for p in self.argument_list:
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
                new_params.loc[filter_all, 'Active'] = self.argument_list[p]
            else:
                # identify correct row, return error if not found
                filter_key = new_params.Key == key
                filter_all = filter_tag & filter_key
                # change value
                new_params.loc[filter_all, 'Value'] = self.argument_list[p]

        # Save initial Scenario_time_series_filename into the results folder
        initial_hourly_timeseries = pd.read_csv(self.argument_list['Scenario_time_series_filename'])
        initial_hourly_timeseries.to_csv(self.runID_result_folder_path + "/_initial_hourly_timeseries_runID{}.csv"
                                         .format(self.runID), index=False)
        self.initial_hourly_timeseries = initial_hourly_timeseries

        # Save new params
        new_params.to_csv(self.runID_param_path, index=False)
        self.new_params = new_params

        # Identify discount rate
        self.discount_rate = (float(new_params.loc[(new_params.Key == "npv_discount_rate") &
                                                   (new_params.Tag == "Finance"),
                                                   'Value'])) / 100

    def run_storagevet(self):
        """Runs StorageVET via command line"""
        # Update runs log csv
        self.update_runs_log_csv()

        # Set up param csv
        self.setup_param_csv()

        # Check that result folder exists with param file in it
        if not (os.path.exists(self.runID_param_path)):
            raise FileNotFoundError("Params file does not exist. Given path was " + self.runID_param_path)

        # Call StorageVET
        print("Running StorageVET for runID" + self.runID + " with parameters in " + self.runID_param_path)
        process = subprocess.Popen(["python", self.SVet_script, self.runID_param_path],
                                   stdout=subprocess.PIPE)

        # Read output in realtime
        while True:
            line = process.stdout.readline()
            print("    ", line)
            if not line:
                break

        # Check if npv in results folder
        all_file_name = ''
        for f in os.listdir(self.runID_result_folder_path + "/"):
            all_file_name += str(f)
        status = "ERROR" if 'npv' not in all_file_name else "COMPLETED"

        # Update npv and proforma results
        if status == "COMPLETED":
            proforma_old = pd.read_csv(self.runID_result_folder_path + "/pro_forma_runID" + self.runID + ".csv")
            npv_old = pd.read_csv(self.runID_result_folder_path + "/npv_runID" + self.runID + ".csv")
            proforma_new, npv_new = update_financial_results(proforma_old, npv_old,
                                                             discount_rate=self.discount_rate,
                                                             growth_rate=0.03)
            proforma_new.to_csv(self.runID_result_folder_path + "/_new_pro_forma_runID" + self.runID + ".csv",
                                index=False)
            npv_new.to_csv(self.runID_result_folder_path + "/_new_npv_runID" + self.runID + ".csv", index=False)
            self.npv_new = npv_new

        # Save status to runlogs, remove entry and folder in cases of failure
        # if status == "ERROR":
        #     shutil.rmtree(self.results_path + result_fol)
        # else:
        #     pass

        # For now, we can log in status in cases of failure as well
        runs_log = pd.read_csv(self.runs_log_file)
        runs_log.loc[runs_log['runID'] == int(self.runID), ['status']] = status
        runs_log.to_csv(self.runs_log_file, index=None)
