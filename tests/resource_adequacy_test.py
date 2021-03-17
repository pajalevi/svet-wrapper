from vc_wrap import SvetObject
from combine_runs import ConstraintObject

path = "/Applications/storagevet2v101/StorageVET-master-git/"
ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv"

############### Resource Adequacy #################
RA_days_peryr = 5
RAconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                #shortname=RAbaseline.shortname, baseline_runID=RAbaseline.runID,
                                shortname="RA baseline",baseline_runID="38",
                                app_hours=[0, 23],
                                regulation_scenario=3,
                                constraint_init=True)
RAconstraint.set_RA0_user_constraints()


RArs3 = SvetObject(SVet_absolute_path=path,
                   shortname=RAconstraint.new_shortname,
                   description="RA SOC management and AS restriction on " + str(RA_days_peryr) + " days per year",
                   Scenario_time_series_filename=RAconstraint.new_hourly_timeseries_path,
                   User_active="yes",User_price=RAconstraint.values,
                   RA_active="no"
                   )
RArs3.run_storagevet()

# test degradation in new svet
new_path ="/Applications/storagevet2v101/StorageVET-master-git/storagevet_dervet/"
RAbaseline = SvetObject(SVet_absolute_path=new_path,
                            shortname="RA_baseline_50days_NOdegradation",
                            description="RA dispmode0 baseline with 50 days per yr. 1 cycle per day",
                            Scenario_time_series_filename=ts,
                            DA_active='yes', RA_active='yes', RA_dispmode='0',
                            RA_days='50',
                            Scenario_n="48", Scenario_end_year="2034",
                            Battery_ccost_kw="0", Battery_ccost_kwh="400",
                            Battery_fixedOM="7",  #Battery_yearly_degrade="1",#Battery_incl_cycle_degrade="1",
                            Battery_hp="0", Battery_daily_cycle_limit="1"
                            )
RAbaseline.run_storagevet()

