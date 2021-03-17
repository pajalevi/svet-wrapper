from vc_wrap import SvetObject
from combine_runs import ConstraintObject

path = "/Applications/storagevet2v101/StorageVET-master-git/"
ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv"

# make baseline params file

# baseline run
baseline = SvetObject(SVet_absolute_path=path,
                      shortname="first run", description="first run with SR + NSR + DA + RA + FR active",
                      Scenario_time_series_filename=ts,
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode='0',
                      FR_active="yes", FR_CombinedMarket="0")
baseline.run_storagevet()

############## Spinning Reserves ##################

# SR_only run
SRonly = SvetObject(SVet_absolute_path=path,
                    shortname="SR only",
                    description="first run with SR only",
                    Scenario_time_series_filename=ts,
                    SR_active='yes')
SRonly.run_storagevet()

# SR_only constraints
SRconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                shortname=SRonly.shortname, baseline_runID=SRonly.runID,
                                app_hours=[0, 23],
                                regulation_scenario=3,
                                constraint_init=True)
SRconstraint.set_SR_user_constraints()

# SR priority run based on SR_only
SRpriority = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                        shortname=SRconstraint.new_shortname,
                        description="SR priority run based on SR only run",
                        Scenario_time_series_filename=SRconstraint.new_hourly_timeseries_path,
                        User_active="yes", User_price=SRconstraint.values,
                        SR_active='no', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0,
                        FR_active="yes", FR_CombinedMarket="0")
SRpriority.run_storagevet()

# SR priority run based on run 132
# SRconstraint2 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
#                                  shortname="SR_only", baseline_runID="132",
#                                  app_hours=[0, 23],
#                                  regulation_scenario=3,
#                                  constraint_init=True)
# SRconstraint2.set_SR_user_constraints()
SRconstraint2 = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                 shortname="SR_only", baseline_runID="132",
                                 app_hours=[0, 23],
                                 regulation_scenario=3,
                                 constraint_init=True)
SRconstraint2.set_SR_user_constraints()
SRpriority2 = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                         shortname=SRconstraint2.new_shortname,
                         description="SR priority run based on SR only run",
                         Scenario_time_series_filename=SRconstraint2.new_hourly_timeseries_path,
                         User_active="yes", User_price=SRconstraint2.values,
                         SR_active='no', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0,
                         FR_active="yes", FR_CombinedMarket="0")
SRpriority2.run_storagevet()

# SR only sanity check
SRsanity = SvetObject(SVet_absolute_path=path,
                      shortname=SRconstraint.new_shortname + "_SRonly",
                      description="SR only sanity check with user constraints",
                      Scenario_time_series_filename=SRconstraint.new_hourly_timeseries_path,
                      User_active="yes", User_price=SRconstraint.values)
SRsanity.run_storagevet()

########### Frequency Regulation ###############
# FR_only
FRonly = SvetObject(SVet_absolute_path=path,
                    shortname="FR only",
                    description="FR only run, baseline for FR priority",
                    Scenario_time_series_filename=ts,
                    FR_active="yes", FR_CombinedMarket="0",
                    DA_active="yes", RA_active="no")
FRonly.run_storagevet()

# FR Priority constraints
FRconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                shortname=FRonly.shortname, baseline_runID=FRonly.runID,
                                app_hours=[21, 23],
                                regulation_scenario=3,
                                constraint_init=True)
FRconstraint.set_FR_user_constraints()
FRpriority = SvetObject(SVet_absolute_path=path,
                        shortname=FRconstraint.new_shortname,
                        description="FR Priority run based on FR only",
                        Scenario_time_series_filename=FRconstraint.new_hourly_timeseries_path,
                        User_active="yes", User_price=FRconstraint.values,
                        FR_active="no", RA_active="no")
FRpriority.run_storagevet()

# FR only sanity check
FRsanity = SvetObject(SVet_absolute_path=path,
                      shortname=FRconstraint.new_shortname + "_FRonly",
                      description="FR only sanity check with user constraints",
                      Scenario_time_series_filename=FRconstraint.new_hourly_timeseries_path,
                      User_active="yes", User_price=FRconstraint.values,
                      FR_active="no", RA_active="no")
FRsanity.run_storagevet()

############### Demand Charge Management ##############
# DCM only

# DCM Priority constraints

# DCM only sanity check


############### Resource Adequacy #################
# iterate over RA_days_peryr
# RA_days_range = [10,20,30,40]
RA_days_range = [0,10,20,30,40,60,80,100,150,200,250,300,350,365]
for RA_days_peryr in RA_days_range:
    RAbaseline = SvetObject(SVet_absolute_path=path,
                            shortname="RA_baseline_"+str(RA_days_peryr)+"days",
                            description="RA dispmode0 baseline with " + str(RA_days_peryr) + "days per yr. 1 cycle per day",
                            Scenario_time_series_filename=ts,
                            DA_active='yes', RA_active='yes', RA_dispmode='0',
                            RA_days=RA_days_peryr,
                            Scenario_n="48", Scenario_end_year="2034",
                            Battery_ccost_kw="0", Battery_ccost_kwh="400",
                            Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                            Battery_hp="0"#, Battery_daily_cycle_limit="1"
                            )
    RAbaseline.run_storagevet()

    RAconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                    shortname=RAbaseline.shortname, baseline_runID=RAbaseline.runID,
                                    #shortname="RA baseline",baseline_runID="38",
                                    app_hours=[0, 23],
                                    regulation_scenario=3,
                                    constraint_init=True)
    RAconstraint.set_RA0_user_constraints()

    RArs3 = SvetObject(SVet_absolute_path=path,
                       shortname=RAconstraint.new_shortname,
                       description="RA SOC management and AS restriction on " + str(RA_days_peryr) + " days per year. 1 cycle per day",
                       Scenario_time_series_filename=RAconstraint.new_hourly_timeseries_path,
                       User_active="yes", User_price=RAconstraint.values,
                       RA_active="no", FR_active="yes", SR_Active="yes", NSR_active="yes",
                       FR_CombinedMarket='0',
                       Scenario_n="48", Scenario_end_year="2034",
                       Battery_ccost_kw="0", Battery_ccost_kwh="400",
                       Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                       Battery_hp="0"#, Battery_daily_cycle_limit="1"
                       )
    RArs3.run_storagevet()

# now do RA events with SOC management x hours in advance of the event