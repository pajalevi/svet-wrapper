from vc_wrap import SvetObject
from combine_runs import ConstraintObject

# testing a comparison to run 132 + others in combine_and_run_script.py
SVet_path = "/Applications/storagevet2v101/StorageVET-master-git/"
# unrestricted, RAdisp0
baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      shortname="baseline run", description="first run with SR + NSR + DA active",
                      Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_nsr133_rs3_14-20.csv",
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode=0, FR_active='yes')
                      
#SR Only
sronly = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      shortname="sr only", description="SR only",
                      Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                      SR_active='yes', NSR_active='no', DA_active='no', RA_active='no', RA_dispmode=0, FR_active='no')

# SR priority 24h
# Then, create user constraints (SR) and obtain params necessary for a second run
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(SvetObject=baseline, app_hours=[0, 23], regulation_scenario=3).set_SR_user_constraints()
# Lastly, use the new params to do a new SV run
new_svrun_params["RA_active"]='no' 
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="SR priority - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)

# FR priority 24h
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(SvetObject=baseline, app_hours=[0, 23], regulation_scenario=3).set_FR_user_constraints()
new_svrun_params["RA_active"]='no'
FR_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="FR priority - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)

# unrestricted + RA disp1
baselineRA1 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      shortname="first run", description="first run with SR + NSR + DA active",
                      Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_nsr133_rs3_14-20.csv",
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode=1, FR_active='yes')
# Lastly, use the new params to do a new SV run
second_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="SR priority - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)

# FR priority 24h
old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = ConstraintObject(
    SvetObject=baseline, app_hours=[0, 23], regulation_scenario=3).set_FR_user_constraints()
FR_run = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=new_shortname, description="FR priority - shortname should denote all useful info",
                        Scenario_time_series_filename=new_hourly_timeseries_path,
                        User_active="yes", User_price=values,
                        **new_svrun_params)

# unrestricted + RA disp1
baselineRA1 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      shortname="first run", description="first run with SR + NSR + DA active",
                      Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_nsr133_rs3_14-20.csv",
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode=1, FR_active='yes')


#testing new storagevet
SVet_path = "/Applications/storagevet2v101/StorageVET-master-git/storagevet_dervet_1.0/"
ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv"
baseline1 = SvetObject(SVet_absolute_path=SVet_path,
                       default_params_file="Model_Parameters_Template2v1-0-2 copy.csv",
                       shortname="simple test-degrad-all-services-cyclelim", description="simple 4h batt - all services with degradation and daily cycle limit of 2",
                       Scenario_time_series_filename=ts,
                       SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode='0',
                       FR_active="yes", FR_CombinedMarket="0",
                       Scenario_n="24",Scenario_end_year="2034",
                       Battery_ccost_kw="0", Battery_ccost_kwh="400",
                       Battery_fixedOM="7", Battery_incl_cycle_degrade="1",
                       Battery_hp="0", Battery_daily_cycle_limit="2",
                       Battery_ene_max_rated="8000", Battery_llsoc="0")
baseline1.run_storagevet()
