from vc_wrap import SvetObject
from combine_runs import combine_runs

# run NSR for 14-20 (values=636) and SR for 22-23 (values=4790)
# results should match those from test_combine_runs_plus_vc_wrap.py
combine_runs(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
             app_types=["NSR", "SR"],
             app_hours=[[14, 20], [22, 23]],
             regulation_scenario=[1, 1],
             shortname="baseline run", description="first run with SR + NSR + DA + RA + FR active",
             Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
             SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode=0,
             FR_active="yes", FR_CombinedMarket="0")

test1 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                   shortname="test_run", description="test run",
                   Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_nsr133_rs3_14-20.csv",
                   SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0)
# VERIFIED ~636
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test1,
    app_hours=[14, 20],
    regulation_scenario=1).set_NSR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# TODO != 289
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test1,
    app_hours=[14, 20],
    regulation_scenario=3).set_NSR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)

test2 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                   shortname="test_run", description="test run",
                   Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_nsr133_rs3_14-20.csv",
                   SR_active='yes', NSR_active='no', DA_active='yes', RA_active='no', RA_dispmode=0)
# VERIFIED ~17562
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test2,
    app_hours=[14, 20],
    regulation_scenario=1).set_SR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# VERIFIED ~13377
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test2,
    app_hours=[14, 20],
    regulation_scenario=3).set_SR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)

test3 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                   shortname="test_run", description="test run",
                   Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                   SR_active='yes', NSR_active='no', DA_active='yes', RA_active='yes', RA_dispmode=0,
                   FR_active="yes", FR_CombinedMarket="0")
# TODO: verify
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test3,
    app_hours=[14, 20],
    regulation_scenario=3).set_FR_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# TODO: verify
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test3,
    app_hours=[14, 20],
    regulation_scenario=1).set_RA0_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
# TODO: verify
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=test3,
    app_hours=[14, 20],
    regulation_scenario=2).set_RA0_user_constraints()
print(" ", old_svrun_params)
print(" ", new_svrun_params)
print(" ", new_shortname, new_hourly_timeseries_path, values)
