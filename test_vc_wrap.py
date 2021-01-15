from wrapper_zhenhua.vc_wrap import SVetObject

SVetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
           shortname="test_run",
           description="DA + SR + NSR + RA + FR + FRcombined active",
           Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
           SR_active='yes',
           NSR_active='yes',
           DA_active='yes',
           RA_active='yes',
           RA_dispmode=0,
           User_active='no',
           FR_active="yes",
           FR_CombinedMarket="1"
           ).run_storagevet_with_vc()
