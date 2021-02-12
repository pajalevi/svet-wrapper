from vc_wrap import SvetObject

# Create a storagevet object
# TODO: change the default params file (and update tariff name)
# Note: DA should be turned off due to double counting of enegry arbitrage
test = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                  default_params_file="Model_Parameters_2v1-0-2_default_EA.csv",
                  shortname="EA+DCM on SR on DA on",
                  description="test run",
                  Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                  DCM_active='yes',
                  retailTimeShift_active='yes',
                  DA_active='no',
                  SR_active='yes'
                  )

# Test if storagevet can run
test.run_storagevet()
print(test.runID, test.argument_list)
