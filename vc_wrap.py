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


class SVetObject:
    def __init__(self, SVet_absolute_path, description, shortname, **params):
        self.SVet_absolute_path = SVet_absolute_path
        self.SVet_script = SVet_absolute_path + "run_StorageVET.py"
        self.default_params_file = SVet_absolute_path + "Model_Parameters_2v1-0-2_default.csv"
        self.runs_log_file = SVet_absolute_path + "Results/runsLog.csv"
        self.results_path = SVet_absolute_path + "Results/"

        self.description = description
        self.shortname = shortname

        self.params = params

    def update_runlog_csv(self):
        """Creates a new entry in Run Log, returns runID of current run"""

        # check if runlog_csv has been created, if not create a new csv with relevant column names
        if not (os.path.exists(self.runs_log_file)):
            runsLog = pd.DataFrame(columns=["runID", "date", "gitID", "shortname", "description", "status"], index=None)
            runsLog.to_csv(self.runs_log_file, index=None)
        else:
            runsLog = pd.read_csv(self.runs_log_file)

        # identify new runID by examining runs log
        runID = str(int(runsLog['runID'].max()) + 1) if runsLog['runID'].max() is not np.nan else str(1)
        print("This run has ID number " + runID)

        # identify current git hash
        # this must be called from within the git repo in order to work
        old_path = os.getcwd()
        os.chdir(self.SVet_absolute_path)
        try:
            gitID_raw = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
            gitID = gitID_raw.strip().decode('ascii')
        except:
            gitID = "No git repository"
        os.chdir(old_path)

        # get date
        date = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

        # create entry in runs log
        new_run_log_line = "\n" + str(runID) + "," + date + "," + gitID + "," + \
                           self.shortname.replace(",", ".") + "," + self.description.replace(",", ".")
        # append line
        with open(self.runs_log_file, 'a') as rl:
            rl.write(new_run_log_line)

        return runID

    def setup_param_csv(self):
        """This function takes an arbitrary dict of params to modify, creates the appropriate
      params csv, and saves it in result_fol. It returns the full filepath. The keys in params
      must have the format 'Tag_Key'  """

        # read params and save folders
        runID = self.update_runlog_csv()
        result_fol = "output_run" + runID + "_" + self.shortname
        params = self.params
        if os.path.exists(self.results_path + result_fol):
            shutil.rmtree(self.results_path + result_fol)
        os.makedirs(self.results_path + result_fol)

        # add Results_dir_absolute_path and Results_label to params
        params['Results_dir_absolute_path'] = self.results_path + result_fol + "/"
        params['Results_label'] = "_runID" + str(runID)
        params['Results_errors_log_path'] = self.results_path + result_fol + "/"

        # load default params csv
        default_params = pd.read_csv(self.default_params_file)

        # parse params arg and change params
        for p in params:
            # parse out tag from key
            tag, key = p.split("_", 1)
            filter_tag = default_params.Tag == tag

            if key == "Active" or key == "active":
                # change activity of that tag
                filter_activation = default_params.Active != "."
                filter_all = filter_tag & filter_activation
                if sum(filter_all) != 1:
                    raise RuntimeError(
                        "Identified the wrong number of rows to change for Active status for tag " + str(tag))
                default_params.loc[filter_all, 'Active'] = params[p]
            else:
                # identify correct row, return error if not found
                filter_key = default_params.Key == key
                filter_all = filter_tag & filter_key
                # change value
                default_params.loc[filter_all, 'Value'] = params[p]

        # save new params in results folder
        param_filepath = self.results_path + result_fol + "/params_run" + str(runID) + ".csv"
        default_params.to_csv(param_filepath, index=False)

        # return params file path
        return param_filepath, runID, result_fol

    def run_storagevet(self):
        """Runs StorageVET via command line"""

        # obtain params
        param_filepath, runID, result_fol = self.setup_param_csv()

        # check that result folder exists with param file in it
        if not (os.path.exists(param_filepath)):
            raise FileNotFoundError("Params file does not exist. Given path was " + param_filepath)

        # call StorageVET
        print("Running StorageVET for runID" + runID + " with parameters in " + param_filepath)
        process = subprocess.Popen(["python", self.SVet_script, param_filepath],
                                   stdout=subprocess.PIPE)

        # read output in realtime
        while True:
            line = process.stdout.readline()
            if not line:
                break

        # check error log file for the current run
        with open(self.results_path + result_fol + r"/\errors_log.log", 'r') as f:
            lines = [str(line) for line in f]
            if len(lines) != 1:
                status = "ERROR"
            else:
                status = "COMPLETED"
        return status, runID, result_fol

    def run_storagevet_with_vc(self):
        """calls paramSetup, creates result folder, updates runsLog, and runs StorageVET
      params arguments should have the format 'Tag_Key = 'Value' """
        print(self.params)

        # call storageVET
        status, runID, result_fol = self.run_storagevet()

        # save status to runlogs, remove entry and folder in cases of failure
        # if status == "ERROR":
        #     shutil.rmtree(self.results_path + result_fol)
        # else:
        #     pass

        # for now, we can log in status in cases of failure as well
        runsLog = pd.read_csv(self.runs_log_file)
        runsLog.loc[runsLog['runID'] == int(runID), ['status']] = status
        runsLog.to_csv(self.runs_log_file, index=None)
