from vc_wrap import SvetObject
from combine_runs import ConstraintObject
import copy
import pandas as pd
import itertools

def iterate_sensitivites(svet_object,senslist_names, sens_list, name):
    all_runs = list(itertools.product(*sens_list))

    thisrun = copy.deepcopy(svet_object)
    #print("length of allruns is "+ str(len(all_runs)))
    for i in range(len(all_runs)):
        #print("i is "+ str(i))
        for j in range(len(all_runs[i])):
            #print("j is "+ str(j))
            thisrun.argument_list[senslist_names[j]]=all_runs[i][j]
        #print(thisrun.argument_list)
        thisrun.shortname = name + "sens"+str(i)
        thisrun.description = name + "sens"+str(i)+" GSA sensitivity, check parameters"
        thisrun.run_storagevet()


# senslist_names1 = ["Battery_ccost_kwh","Battery_daily_cycle_limit","Finance_npv_discount_rate","Battery_fixedOM","Scenario_monthly_data_filename", ]
# senslist1 = [["400","450"],["1","2"],["0.11","0.08"],["40","80"],["/Applications/storagevet2v101/StorageVET-master-git/Data/Monthly_Data_6-kW_RA.csv","/Applications/storagevet2v101/StorageVET-master-git/Data/Monthly_Data.csv"]]

# # senslist_names1 = ["Battery_ccost_kwh","Battery_daily_cycle_limit"]
# # senslist1 = [["400","450"],["1","2"]]
#
# path = "/Applications/storagevet2v101/StorageVET-master-git/"
# ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv"
# testbase = SvetObject(SVet_absolute_path=path,
#                       shortname="testbase_4hbatt", description="baseline run with 4h batt",
#                       Scenario_time_series_filename=ts,
#                       SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode='0',
#                       FR_active="yes", FR_CombinedMarket="0",
#                       Scenario_n="48",Scenario_end_year="2034",
#                       Battery_ccost_kw="0", Battery_ccost_kwh="400",
#                       Battery_fixedOM="40", #Battery_incl_cycle_degrade="0",
#                       Battery_hp="0", Battery_daily_cycle_limit="0",
#                       Battery_ene_max_rated="8000", Battery_llsoc="0")
#
# iterate_sensitivites(testbase,senslist_names1,senslist1)