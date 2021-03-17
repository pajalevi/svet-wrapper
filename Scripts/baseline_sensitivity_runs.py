from vc_wrap import SvetObject
from combine_runs import ConstraintObject
import copy
import pandas as pd

path = "/Applications/storagevet2v101/StorageVET-master-git/"
ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv"

# baseline run
baseline1 = SvetObject(SVet_absolute_path=path,
                      shortname="baseline1", description="optimistic baseline run",
                      Scenario_time_series_filename=ts,
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode='0',
                      FR_active="yes", FR_CombinedMarket="0",
                      Scenario_n="48",Scenario_end_year="2034",
                      Battery_ccost_kw="0", Battery_ccost_kwh="400",
                      Battery_fixedOM="7", #Battery_incl_cycle_degrade="0",
                      Battery_hp="0", Battery_daily_cycle_limit="0")
baseline1.run_storagevet()

# pessimistic baseline run
baseline2 = SvetObject(SVet_absolute_path=path,
                      shortname="baseline2", description="pessimistic baseline",
                      Scenario_time_series_filename=ts,
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode='0',
                      FR_active="yes", FR_CombinedMarket="0",
                      Scenario_n="48",Scenario_end_year="2029",
                      Battery_ccost_kw="0", Battery_ccost_kwh="500",
                      Battery_fixedOM="14", #Battery_incl_cycle_degrade="1",# cycle degradation does not work
                      Battery_hp="100", Battery_daily_cycle_limit="1")
baseline2.run_storagevet()

# optimistic baseline run with 4 h battery
baseline3 = SvetObject(SVet_absolute_path=path,
                      shortname="baseline1_4hbatt", description="optimistic baseline run with 4h batt",
                      Scenario_time_series_filename=ts,
                      SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode='0',
                      FR_active="yes", FR_CombinedMarket="0",
                      Scenario_n="48",Scenario_end_year="2034",
                      Battery_ccost_kw="0", Battery_ccost_kwh="400",
                      Battery_fixedOM="7", #Battery_incl_cycle_degrade="0",
                      Battery_hp="0", Battery_daily_cycle_limit="0",
                      Battery_ene_max_rated="8000", Battery_llsoc="0")
baseline3.run_storagevet()

#optimistic baseline with new svet, 120 hours
#optimistic baseline with new svet and using battery degradation


# Sensitivities over baseline 1: 11 total runs
# - discount rate: 5%, 10%
# - cost / kwh: 500
# - lifetime: 10, 20
# - length of simulation: 120
# - cycling degradation: yes
# - daily cycle limit: 1
# - housekeeping pwr: 100
# - RA prices: 6
# - FR prices: 1/10th

# read sensitivity csv
sens1 = pd.read_csv(path + "Data/baseline1_sensitivities.csv")

for i in range(len(sens1)):
    sens_run = copy.deepcopy(baseline1)
    sens_run.argument_list[sens1.loc[i,"var"]]=sens1.loc[i,"new_value"]
    sens_run.shortname= "baseline1_sens"+str(i)+"_" + sens1.loc[i,"var"]
    sens_run.description= "baseline1 sensitivity number "+ str(i) + " with " + sens1.loc[i,"var"] + " set to " + sens1.loc[i,"var"]
    sens_run.run_storagevet()


# Sensitivities over baseline 2: 8 total runs
# - discount rate: 5%
# - cost / kwh: 400
# - lifetime: 20
# - length of simulation: 120
# - cycling degradation: no
# - daily cycle limit: 0
# - RA prices: 6
# - FR prices: 1x

sens2 = pd.read_csv(path + "Data/baseline2_sensitivities.csv")

for i in range(len(sens2)):
    sens_run = copy.deepcopy(baseline2)
    sens_run.argument_list[sens2.loc[i,"var"]]=sens2.loc[i,"new_value"]
    sens_run.shortname= "baseline2_sens"+str(i)+"_" + sens2.loc[i,"var"]
    sens_run.description= "baseline2 sensitivity number "+ str(i) + " with " + sens2.loc[i,"var"] + " set to " + sens2.loc[i,"var"]
    sens_run.run_storagevet()