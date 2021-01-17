from vc_wrap import SvetObject
from combine_runs import ConstraintObject

# First, run the baseline scenario
baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      shortname="first run", description="first run with SR + NSR + DA active",
                      Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_nsr133_rs3_14-20.csv",
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0)
# Then, create user constraints (NSR) and obtain params necessary for a second run
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=baseline, app_hours=[14, 20], regulation_scenario=3).set_NSR_user_constraints()
# Lastly, use the new params to do a new SV run
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="second run - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)
# Using the same results from the baseline scenario, we can change regulation scenario
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=baseline, app_hours=[14, 20], regulation_scenario=1).set_NSR_user_constraints()
# Lastly, use the new params to do a new SV run
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="second run - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)
# Using the same results from the baseline scenario, we can change resource type
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=baseline, app_hours=[14, 20], regulation_scenario=1).set_SR_user_constraints()
# Lastly, use the new params to do a new SV run
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="second run - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)
# Similarly, change regulation scenario
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=baseline, app_hours=[14, 20], regulation_scenario=3).set_SR_user_constraints()
# Lastly, use the new params to do a new SV run
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="second run - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)


# First, run the baseline scenario
baseline_2 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname="first run", description="first run with SR + NSR + DA  + FR active",
                        Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_nsr133_rs3_14-20.csv",
                        SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0,
                        FR_active="yes", FR_CombinedMarket="0")
# Then, create user constraints (NSR) and obtain params necessary for a second run
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=baseline_2, app_hours=[0, 23], regulation_scenario=3).set_FR_user_constraints()
# Lastly, use the new params to do a new SV run
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="second run - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)


# First, run the baseline scenario
baseline_3 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname="first run", description="first run with SR + NSR + DA + RA + FR active",
                        Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_nsr133_rs3_14-20.csv",
                        SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode=0,
                        FR_active="yes", FR_CombinedMarket="0")
# Then, create user constraints (NSR) and obtain params necessary for a second run
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=baseline_3, app_hours=[14, 20], regulation_scenario=1).set_RA0_user_constraints()
# Lastly, use the new params to do a new SV run
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="second run - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)
# TODO: we can actually keep iterating
