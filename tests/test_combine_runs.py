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




