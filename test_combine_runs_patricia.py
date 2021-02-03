from vc_wrap import SvetObject
from combine_runs import ConstraintObject

Patricia_133 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                          shortname="Patricia 133", description="NSR + DA active",
                          Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                          SR_active='no', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0,
                          FR_active="no", FR_CombinedMarket="0")
# VERIFIED ~636
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=Patricia_133,
    app_hours=[14, 20],
    regulation_scenario=1).set_NSR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# VERIFIED ~289
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=Patricia_133,
    app_hours=[14, 20],
    regulation_scenario=3).set_NSR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)

Patricia_132 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                   shortname="Patricia 132", description="SR + DA active",
                   Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                   SR_active='yes', NSR_active='no', DA_active='yes', RA_active='no', RA_dispmode=0)
# VERIFIED ~17562
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=Patricia_132,
    app_hours=[14, 20],
    regulation_scenario=1).set_SR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# VERIFIED ~13377
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=Patricia_132,
    app_hours=[14, 20],
    regulation_scenario=3).set_SR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# VERIFIED ~143507
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=Patricia_132,
    app_hours=[0, 23],
    regulation_scenario=3).set_SR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)

test3 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                   shortname="test_run", description="test run",
                   Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                   SR_active='yes', NSR_active='no', DA_active='yes', RA_active='yes', RA_dispmode=0,
                   FR_active="yes", FR_CombinedMarket="0")
# TODO: verify == ?
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test3,
    app_hours=[14, 20],
    regulation_scenario=3).set_FR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# TODO: verify == ?
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test3,
    app_hours=[14, 20],
    regulation_scenario=1).set_RA0_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# TODO: verify == ?
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test3,
    app_hours=[14, 20],
    regulation_scenario=2).set_RA0_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
