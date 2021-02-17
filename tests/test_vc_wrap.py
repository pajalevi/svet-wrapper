from vc_wrap import SvetObject

# Create a storagevet object
test = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/storagevet_dervet/",
                  default_params_file="Model_Parameters_2v1-0-2_default.csv",
                  shortname="test_run",
                  description="test run",
                  Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                  SR_active='yes',
                  NSR_active='yes',
                  DA_active='yes',
                  RA_active='no',
                  RA_dispmode=0,
                  User_active='no',
                  FR_active="no",
                  FR_CombinedMarket="0"
                  )

print(test.runID_param_path)
