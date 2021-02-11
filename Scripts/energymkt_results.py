from vc_wrap_v2 import SvetObject
from combine_runs import ConstraintObject

# baseline run
baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      shortname="first run", description="first run with SR + NSR + DA + RA + FR active",
                      Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode='0',
                      FR_active="yes", FR_CombinedMarket="0")
baseline.run_storagevet()

# SR_only constraints
SRconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                              shortname=baseline.shortname, baseline_runID=baseline.runID,
                              app_hours=[0, 23],
                              regulation_scenario=3)
SRconstraint.set_SR_user_constraints()

# SR priority run based on SR_only
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=SRconstraint.new_shortname,
                        description="SR priority run based on baseline run",
                        Scenario_time_series_filename=SRconstraint.new_hourly_timeseries_path,
                        User_active="yes", User_price=SRconstraint.values,
                        SR_active='no', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0,
                        FR_active="yes", FR_CombinedMarket="0")
second_run.run_storagevet()
#could I create the second_run object by passing it a constraint object? SvetObject would need to accept
# different collections of inputs for that to work. I know I can do that in Julia, what about Python?

# SR priority run based on run 132
SRconstraint2 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                              shortname="SR_only", baseline_runID="132",
                              app_hours=[0, 23],
                              regulation_scenario=3)
SRconstraint2.set_SR_user_constraints()
third_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=SRconstraint2.new_shortname,
                        description="SR priority run based on baseline run",
                        Scenario_time_series_filename=SRconstraint2.new_hourly_timeseries_path,
                        User_active="yes", User_price=SRconstraint2.values,
                        SR_active='no', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0,
                        FR_active="yes", FR_CombinedMarket="0")
third_run.run_storagevet()
# run proforma_update
# plot (ahhhhh)