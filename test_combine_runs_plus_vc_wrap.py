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

# Then, create NSR constraint by passing baseline shortname and runID
constraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                              shortname=baseline.shortname, baseline_runID=baseline.runID,
                              app_hours=[14, 20], regulation_scenario=1, constraint_init=True)
constraint.set_NSR_user_constraints()
print(" ", constraint.new_shortname, constraint.new_hourly_timeseries_path, constraint.values)

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


# Then, create SR constraint by passing baseline shortname and runID
# Note: no need to initialize constraints
constraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                              shortname=second_run.shortname, baseline_runID=second_run.runID,
                              app_hours=[22, 23], regulation_scenario=1, constraint_init=False)
constraint.set_SR_user_constraints()
print(" ", constraint.new_shortname, constraint.new_hourly_timeseries_path, constraint.values)
