from vc_wrap_v2 import SvetObject
from combine_runs import ConstraintObject

# First, run the baseline scenario
baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      shortname="first run", description="first run with SR + NSR + DA + RA + FR active",
                      Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode=0,
                      FR_active="yes", FR_CombinedMarket="0")
baseline.run_storagevet()

# Then, create NSR constraint by passing baseline shortname and runID
constraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                              shortname=baseline.shortname, baseline_runID=baseline.runID,
                              app_hours=[14, 20],
                              regulation_scenario=1)
constraint.set_NSR_user_constraints()
print(" ", constraint.new_shortname, constraint.new_hourly_timeseries_path, constraint.values)

# Lastly, use the new params to do a new SV run
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=constraint.new_shortname,
                        description="second run - shortname should denote all useful info",
                        Scenario_time_series_filename=constraint.new_hourly_timeseries_path,
                        User_active="yes", User_price=constraint.values,
                        SR_active='yes', NSR_active='no', DA_active='yes', RA_active='yes', RA_dispmode=0,
                        FR_active="yes", FR_CombinedMarket="0")
second_run.run_storagevet()
# TODO need to explicitly mention the updated argument list - is this helpful/redundant?

# Note: we can actually keep iterating
