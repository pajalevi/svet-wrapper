from vc_wrap_v2 import SvetObject
from combine_runs import ConstraintObject, combine_runs

# First, run the baseline scenario
baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      shortname="baseline run", description="SR + NSR + DA active",
                      Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0)
# Then, run NSR for 14-20 and SR for 20-23
combine_runs(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
             baseline_svetobject=baseline,
             app_types=["NSR", "SR"],
             app_hours=[[14, 20], [21, 23]],
             regulation_scenario=[1, 1])




