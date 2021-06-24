from vc_wrap import SvetObject
from combine_runs import ConstraintObject
from GSA_runs import iterate_sensitivites

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
path = "/Applications/storagevet2v101/StorageVET-master-git/storagevet_dervet/"

# DCM only
DCMonly = SvetObject(SVet_absolute_path=path,
                    shortname="DCM only",
                    description="DCM only run, baseline for DCM priority. optimistic baseline. dervet",
                    Scenario_time_series_filename=ts,
                    Scenario_n="48", Scenario_end_year="2034",
                    Battery_ccost_kw="0", Battery_ccost_kwh="400",
                    Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                    Battery_hp="0", Battery_daily_cycle_limit="0",
                    DCM_active="yes",
                    RA_active="no")
DCMonly.run_storagevet()

# DCM with DR
DCM_DR = SvetObject(SVet_absolute_path=path,
                    Scenario_time_series_filename=ts,
                    Scenario_n="48", Scenario_end_year="2034",
                    Battery_ccost_kw="0", Battery_ccost_kwh="400",
                    Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                    Battery_hp="0", Battery_daily_cycle_limit="0",
                    shortname="DCM_w_DR",
                    description="DCM with DR. optimistic baseline. dervet",
                    DCM_active="yes",
                    DR_active="yes",
                    RA_active="no")
DCM_DR.run_storagevet() #doesnt appear to work

# DCM with FR
DCM_FR = SvetObject(SVet_absolute_path=path,
                     Scenario_time_series_filename=ts,
                     Scenario_n="48", Scenario_end_year="2034",
                     Battery_ccost_kw="0", Battery_ccost_kwh="400",
                     Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                     Battery_hp="0", Battery_daily_cycle_limit="0",
                     shortname="DCM_w_FR",
                     description="DCM with FR. optimistic baseline. dervet",
                     DCM_active="yes", FR_active="yes",FR_CombinedMarket="0")
DCM_FR.run_storagevet()

# DCM with SR, NSR
DCM_SR = SvetObject(SVet_absolute_path=path,
                     Scenario_time_series_filename=ts,
                     Scenario_n="48", Scenario_end_year="2034",
                     Battery_ccost_kw="0", Battery_ccost_kwh="400",
                     Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                     Battery_hp="0", Battery_daily_cycle_limit="0",
                     shortname="DCM_w_SR_NSR",
                     description="DCM with SR and NSR. optimistic baseline. dervet",
                     DCM_active="yes", SR_active="yes",NSR_active="yes")
DCM_SR.run_storagevet()

# DCM with wholesale, no FR
DCM_wholesale = SvetObject(SVet_absolute_path=path,
                           Scenario_time_series_filename=ts,
                           Scenario_n="48", Scenario_end_year="2034",
                           Battery_ccost_kw="0", Battery_ccost_kwh="400",
                           Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                           Battery_hp="0", Battery_daily_cycle_limit="0",
                           shortname="DCM_w_wholesale",
                           description="DCM with full wholesale. optimistic baseline. dervet",
                           DCM_active="yes",
                           # FR_active="yes", FR_CombinedMarket="0",
                           RA_active="yes", SR_active="yes", NSR_active="yes")
DCM_wholesale.run_storagevet()

# DCM with wholesale
DCM_wholesale = SvetObject(SVet_absolute_path=path,
                     Scenario_time_series_filename=ts,
                     Scenario_n="48", Scenario_end_year="2034",
                     Battery_ccost_kw="0", Battery_ccost_kwh="400",
                     Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                     Battery_hp="0", Battery_daily_cycle_limit="0",
                     shortname="DCM_w_wholesale",
                     description="DCM with full wholesale. optimistic baseline. dervet",
                     DCM_active="yes", FR_active="yes",FR_CombinedMarket="0",
                     RA_active="yes",SR_active="yes",NSR_active="yes")
DCM_wholesale.run_storagevet()

# DCM Priority constraints
DCMconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                 shortname=DCMonly.shortname, baseline_runID=DCMonly.runID,
                                 app_hours=[0, 23],
                                 regulation_scenario=3,
                                 constraint_init=True)
DCMconstraint.set_DCM_user_constraints()
DCMpriority = SvetObject(SVet_absolute_path=path,
                         shortname=DCMconstraint.new_shortname,
                         description="DCM Priority with wholesale. dervet",
                         Scenario_time_series_filename=DCMconstraint.new_hourly_timeseries_path,
                         User_active="yes", User_price=DCMconstraint.values,
                         FR_active="yes", RA_active="yes",
                         DCM_active="no",FR_combinedMarket="0",SR_active="yes",
                         NSR_active="yes")
DCMpriority.run_storagevet()


# DCM only sanity check


############### Resource Adequacy #################
# iterate over RA_days_peryr
# RA_days_range = [10,20,30,40]
RA_days_range = [0,10,200]
isos = ["caiso","pjm","ercot","isone","nyiso"]
iso_FR = ["0","0","1","1","1",]
# senslist_names1 = ["Battery_ccost_kwh","Battery_daily_cycle_limit","Finance_npv_discount_rate","Battery_fixedOM","User_price"]
# senslist1 = [["400","450"],["0","1","2"],["0.11","0.08"],["40","80"],[str(3*12*2000),str(6*12*2000)]]
senslist_names1 = ["Battery_daily_cycle_limit"]
senslist1 = [["0","1","2"]]
price_filename_ending = ["2019.csv","0.25_FR-prices.csv"]
path = "/Applications/storagevet2v101/StorageVET-master-git/"
for i in range(len(isos)):
    iso=isos[i]
    FR_combined = iso_FR[i]
    ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ iso + "_" + price_filename_ending[1]
    for RA_days_peryr in RA_days_range:
        RAbaseline = SvetObject(SVet_absolute_path=path,
                                shortname="RA_baseline_"+str(RA_days_peryr)+"days_"+iso,
                                description="RA dispmode0 baseline with " + str(RA_days_peryr) + "days per yr. no cycle limit. " + iso + " data. cycLim of 2",
                                Scenario_time_series_filename=ts,
                                DA_active='yes', RA_active='yes', RA_dispmode='0',
                                RA_days=RA_days_peryr,
                                Scenario_n="48", Scenario_end_year="2034",
                                Battery_ccost_kw="0", Battery_ccost_kwh="400",
                                Battery_ene_max_rated="8000", Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                                Battery_hp="0", Battery_daily_cycle_limit="2"
                                )
        RAbaseline.run_storagevet()

        RAconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                        shortname=RAbaseline.shortname, baseline_runID=RAbaseline.runID,
                                        #shortname="RA baseline",baseline_runID="38",
                                        app_hours=[0, 23],
                                        regulation_scenario=3,
                                        constraint_init=True)
        RAconstraint.set_RA0_user_constraints(RA_monthly_values_per_kW=3) #unfortunately this is hardcoded... but can just set User_price so its not a big deal

        RArs3 = SvetObject(SVet_absolute_path=path,
                           shortname=RAconstraint.new_shortname,
                           description="RA SOC management and AS restriction on " + str(RA_days_peryr) + " days per year. no cycle limit. FR combined. "+iso+" data. cycLim of 2",
                           Scenario_time_series_filename=RAconstraint.new_hourly_timeseries_path,
                           User_active="yes", User_price=RAconstraint.values,
                           RA_active="no", FR_active="yes", SR_Active="yes", NSR_active="yes",
                           FR_CombinedMarket=FR_combined,
                           Scenario_n="48", Scenario_end_year="2034",
                           Battery_ccost_kw="0", Battery_ccost_kwh="400",
                           Battery_ene_max_rated="8000", Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                           Battery_hp="0", Battery_daily_cycle_limit="2"
                           )
        iterate_sensitivites(RArs3,senslist_names1,senslist1,"RA_SCOM_"+str(RA_days_peryr)+"days")

############### Resource Adequacy, Low FR #################
# iterate over RA_days_peryr
# RA_days_range = [10,20,30,40]
RA_days_range = [0,50,100,200,300]
isos = ["caiso","ercot","pjm","isone","nyiso"]
iso_FR = ["0","0","1","1","1",]
senslist_names1 = ["Battery_ccost_kwh","Battery_daily_cycle_limit","Finance_npv_discount_rate","Battery_fixedOM","Scenario_monthly_data_filename", ]
senslist1 = [["400","450"],["1","2"],["0.11","0.08"],["40","80"],["/Applications/storagevet2v101/StorageVET-master-git/Data/Monthly_Data_6-kW_RA.csv","/Applications/storagevet2v101/StorageVET-master-git/Data/Monthly_Data.csv"]]

for i in range(len(isos)):
    iso=isos[i]
    FR_combined = iso_FR[i]
    ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ iso + "_0.25_FR-prices.csv"
    for RA_days_peryr in RA_days_range:
        RAbaseline = SvetObject(SVet_absolute_path=path,
                                shortname="RA_baseline_"+str(RA_days_peryr)+"days_"+iso,
                                description="RA dispmode0 baseline with " + str(RA_days_peryr) + "days per yr. no cycle limit. " + iso + " data",
                                Scenario_time_series_filename=ts,
                                DA_active='yes', RA_active='yes', RA_dispmode='0',
                                RA_days=RA_days_peryr,
                                Scenario_n="48", Scenario_end_year="2034",
                                Battery_ccost_kw="0", Battery_ccost_kwh="400",
                                Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                                Battery_hp="0", Battery_daily_cycle_limit="0"
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
                           description="RA SOC management and AS restriction on " + str(RA_days_peryr) + " days per year. no cycle limit. FR combined. "+iso+" data",
                           Scenario_time_series_filename=RAconstraint.new_hourly_timeseries_path,
                           User_active="yes", User_price=RAconstraint.values,
                           RA_active="no", FR_active="yes", SR_Active="yes", NSR_active="yes",
                           FR_CombinedMarket=FR_combined,
                           Scenario_n="48", Scenario_end_year="2034",
                           Battery_ccost_kw="0", Battery_ccost_kwh="400",
                           Battery_fixedOM="7",  # Battery_incl_cycle_degrade="0",
                           Battery_hp="0", Battery_daily_cycle_limit="0"
                           )
        #RArs3.run_storagevet()
        iterate_sensitivites(RArs3,senslist_names1,senslist1,"RA_SCOM_"+str(RA_days_peryr)+"days")

# now do RA events with SOC management x hours in advance of the event