from vc_wrap import SvetObject
from combine_runs import ConstraintObject

# Test if we can just usepre-existing baseline run for creating constraints by specifying shortname and baseline runID
# # VERIFIED ~143507
# sr4 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                        shortname="Patricia 132", baseline_runID="4",
#                        app_hours=[-1, 23], regulation_scenario=3, constraint_init=True)
# sr4.set_SR_user_constraints()
# print(" ", sr4.new_shortname, sr4.new_hourly_timeseries_path, sr4.values)

# Patricia_133 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                           shortname="Patricia 133", description="NSR + DA active",
#                           Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
#                           SR_active='no', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0,
#                           FR_active="no", FR_CombinedMarket="0")
# Patricia_133.run_storagevet()
# # VERIFIED ~636
# nsr1 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                         shortname=Patricia_133.shortname, baseline_runID=Patricia_133.runID,
#                         app_hours=[14, 20], regulation_scenario=1, constraint_init=True)
# nsr1.set_NSR_user_constraints()
# print(" ", nsr1.new_shortname, nsr1.new_hourly_timeseries_path, nsr1.values)
# # VERIFIED ~289
# nsr3 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                         shortname=Patricia_133.shortname, baseline_runID=Patricia_133.runID,
#                         app_hours=[14, 20], regulation_scenario=3, constraint_init=True)
# nsr3.set_NSR_user_constraints()
# print(" ", nsr3.new_shortname, nsr3.new_hourly_timeseries_path, nsr3.values)

# Patricia_132 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                           shortname="Patricia 132", description="SR + DA active",
#                           Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
#                           SR_active='yes', NSR_active='no', DA_active='yes', RA_active='no', RA_dispmode=0)
# Patricia_132.run_storagevet()
# # VERIFIED ~17562
# sr1 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                        shortname=Patricia_132.shortname, baseline_runID=Patricia_132.runID,
#                        app_hours=[14, 20], regulation_scenario=1, constraint_init=True)
# sr1.set_SR_user_constraints()
# print(" ", sr1.new_shortname, sr1.new_hourly_timeseries_path, sr1.values)
# # VERIFIED ~13377
# sr3 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                        shortname=Patricia_132.shortname, baseline_runID=Patricia_132.runID,
#                        app_hours=[14, 20], regulation_scenario=3, constraint_init=True)
# sr3.set_SR_user_constraints()
# print(" ", sr3.new_shortname, sr3.new_hourly_timeseries_path, sr3.values)
# # VERIFIED ~143507
# sr4 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                        shortname=Patricia_132.shortname, baseline_runID=Patricia_132.runID,
#                        app_hours=[-1, 23], # start from -1 as we need to incorporate 00:00
#                        regulation_scenario=3, constraint_init=True)
# sr4.set_SR_user_constraints()
# print(" ", sr4.new_shortname, sr4.new_hourly_timeseries_path, sr4.values)

# test3 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                    shortname="test_run", description="test run",
#                    Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
#                    SR_active='yes', NSR_active='no', DA_active='yes', RA_active='yes', RA_dispmode=0,
#                    FR_active="yes", FR_CombinedMarket="0")
# # TODO: verify == ?
# old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
#     SvetObject=test3,
#     app_hours=[14, 20],
#     regulation_scenario=3).set_FR_user_constraints()
# print(" ", old_svrun_params)
# print(" ", new_svrun_params)
# print(" ", new_shortname, new_hourly_timeseries_path, values)
# # TODO: verify == ?
# old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
#     SvetObject=test3,
#     app_hours=[14, 20],
#     regulation_scenario=1).set_RA0_user_constraints()
# print(" ", old_svrun_params)
# print(" ", new_svrun_params)
# print(" ", new_shortname, new_hourly_timeseries_path, values)
# # TODO: verify == ?
# old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
#     SvetObject=test3,
#     app_hours=[14, 20],
#     regulation_scenario=2).set_RA0_user_constraints()
# print(" ", old_svrun_params)
# print(" ", new_svrun_params)
# print(" ", new_shortname, new_hourly_timeseries_path, values)
