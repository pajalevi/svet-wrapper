# running examples, Jan 13 2021

from wrapper.vc_wrap import SVetObject

SVetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
           shortname="FR_2019", description="only FR 2019 data",
           Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
           SR_active='no', NSR_active='no', DA_active='yes', RA_active='no', RA_dispmode=0, User_active='no',
           FR_active="yes", FR_CombinedMarket="0").run_storagevet_with_vc()

SVetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
           shortname="FR+SR+NSR+RA_2019", description="Baseline for FR+SR+NSR+RA 2019 data",
           Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
           SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode=0, User_active='no',
           FR_active="yes", FR_CombinedMarket="0").run_storagevet_with_vc()

SVetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
           shortname="FR+SR+NSR_2019", description="Baseline for FR+SR+NSR 2019 data",
           Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
           SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0, User_active='no',
           FR_active="yes", FR_CombinedMarket="0").run_storagevet_with_vc()

SVetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
           shortname="SR+NSR+RA_2019", description="Baseline for SR+NSR+RA 2019 data",
           Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
           SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='yes', RA_dispmode=0, User_active='no',
           FR_active="no", FR_CombinedMarket="0").run_storagevet_with_vc()

SVetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
           shortname="SR+NSR_2019", description="Baseline for SR+NSR 2019 data",
           Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
           SR_active='yes', NSR_active='yes', DA_active='yes', RA_active='no', RA_dispmode=0, User_active='no',
           FR_active="no", FR_CombinedMarket="0").run_storagevet_with_vc()



x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(133) +"_NSR_only/",runID=133,resHour=[0,23],regScenario=3)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr133_rs3_0-23.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr133_rs3_0-23.csv")
ID = "nsr133_RS3_0-23"
basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
basedata = basedata.set_index(x.index)
basedata['Power Min (kW)'] = x['chgMin_kW']
basedata['Power Max (kW)'] = x['chgMax_kW']
basedata['Energy Max (kWh)'] = x['eMax_kWh']
basedata['Energy Min (kWh)'] = x['eMin_kWh']
basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# f.write("ID,value\n")
f.write(ID + "," + str(y)+"\n")
f.close()
vc.runWithVC(shortname = "nsr_RS3_24h", description = "user constraints for nsr based on run 133 for all hours. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
             NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
             # infeasible at  2017-06-09 00:00:00 hb
vc.runWithVC(shortname = "nsr_RS3_24h", description = "user constraints for nsr based on run 133 for all hours. RA dispmode 1",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
             NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
# infeasible at 2017-05-22 00:00:00 hb
#
#
# x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(133) +"_NSR_only/",runID=133,resHour=[14,20],regScenario=1)
# # x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr133_rs1_14-20.csv")
# # pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr133_rs1_14-20.csv")
# ID = "nsr133_rs1_14-20"
# basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
# basedata = basedata.set_index(x.index)
# basedata['Power Min (kW)'] = x['chgMin_kW']
# basedata['Power Max (kW)'] = x['chgMax_kW']
# basedata['Energy Max (kWh)'] = x['eMax_kWh']
# basedata['Energy Min (kWh)'] = x['eMin_kWh']
# basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
# f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# # f.write("ID,value\n")
# f.write(ID + "," + str(y)+"\n")
# f.close()
# vc.runWithVC(shortname = "nsr_RS1_14-20", description = "user constraints for nsr based on run 133 for 14h-20h. RA dispmode 0. 2019",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
#              NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
# # OH THANK GOD THIS RAN
# vc.runWithVC(shortname = "nsr_RS1_noRA_14-20", description = "user constraints for nsr based on run 133 for 14h-20h. no RA. 2019",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
#              NSR_active='no',DA_active = 'yes', RA_active='no', RA_dispmode = 0, User_active = 'yes', User_price = y)
#
# vc.runWithVC(shortname = "nsr_RS1_14-20", description = "user constraints for nsr based on run 133 for 14h-20h. RA dispmode 1",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
#              NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
# #infeasible at 2017-07-24 00:00:00 hb
#
#
# x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(133) +"_NSR_only/",runID=133,resHour=[14,20],regScenario=3)
# # x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr133_rs3_14-20.csv")
# # pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr133_rs3_14-20.csv")
# ID = "nsr133_rs3_14-20"
# basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
# basedata = basedata.set_index(x.index)
# basedata['Power Min (kW)'] = x['chgMin_kW']
# basedata['Power Max (kW)'] = x['chgMax_kW']
# basedata['Energy Max (kWh)'] = x['eMax_kWh']
# basedata['Energy Min (kWh)'] = x['eMin_kWh']
# basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
# f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# # f.write("ID,value\n")
# f.write(ID + "," + str(y)+"\n")
# f.close()
# vc.runWithVC(shortname = "nsr_RS3_14-20", description = "user constraints for nsr based on run 133 for 14h-20h. RA dispmode 0",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
#              NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
# #YAY THIS RAN TOO
# vc.runWithVC(shortname = "nsr_RS3_14-20", description = "user constraints for nsr based on run 133 for 14h-20h. no RA",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
#              NSR_active='no',DA_active = 'yes', RA_active='no', RA_dispmode = 0, User_active = 'yes', User_price = y)
#
# vc.runWithVC(shortname = "nsr_RS3_14-20", description = "user constraints for nsr based on run 133 for 14h-20h. RA dispmode 1",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
#              NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
# # infeasible at 2017-07-25 12:00:00 hb
#
# # x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(132) +"_SR_only/",runID=132,resHour=[0,23],regScenario=1)
# # x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr132_rs1_0-23.csv")
# # pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr132_rs1_0-23.csv")
# x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(132) +"_SR_only/",runID=132,resHour=[0,23],regScenario=3)
# # x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr132_rs3_0-23.csv")
# # pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr132_rs3_0-23.csv")
# ID = "sr132_rs3_24h"
# basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
# basedata = basedata.set_index(x.index)
# basedata['Power Min (kW)'] = x['chgMin_kW']
# basedata['Power Max (kW)'] = x['chgMax_kW']
# basedata['Energy Max (kWh)'] = x['eMax_kWh']
# basedata['Energy Min (kWh)'] = x['eMin_kWh']
# basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
# f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# # f.write("ID,value\n")
# f.write(ID + "," + str(y)+"\n")
# f.close()
# vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 132 for 24h. RA dispmode 0. 2019 data",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
#              NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
# #frig this didn't run even though it ran before. Infeasible at 2017-06-09 00:00:00 hb
# vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 132 for 24h. RA dispmode 1",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
#              NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
# # also infeasible at 2017-07-25 12:00:00 hb
# # ok this time it was infeasible at t 2017-05-22 00:00:00 hb
#
#
# x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(132) +"_SR_only/",runID=132,resHour=[14,20],regScenario=1)
# # x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr132_rs1_14-20.csv")
# # pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr132_rs1_14-20.csv")
# ID = "sr132_rs1_14-20"
# basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
# basedata = basedata.set_index(x.index)
# basedata['Power Min (kW)'] = x['chgMin_kW']
# basedata['Power Max (kW)'] = x['chgMax_kW']
# basedata['Energy Max (kWh)'] = x['eMax_kWh']
# basedata['Energy Min (kWh)'] = x['eMin_kWh']
# basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
# f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# # f.write("ID,value\n")
# f.write(ID + "," + str(y)+"\n")
# f.close()
# vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 132 for 14-20. RA dispmode 0. 2019 data",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
#              NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
# #THIS RAN TOO WHOOP
# vc.runWithVC(shortname = ID+"_noRA", description = "user constraints for sr based on run 132 for 14-20. no RA. 2019 data",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
#              NSR_active='yes',DA_active = 'yes', RA_active='no', RA_dispmode = 0, User_active = 'yes', User_price = y)
#
# vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 132 for 14-20. RA dispmode 1",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
#              NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
# #infeasible at 2017-07-24 00:00:00 hb
#
# x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(132) +"_SR_only/",runID=132,resHour=[14,20],regScenario=3)
# # x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr132_rs3_14-20.csv")
# # pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr132_rs3_14-20.csv")
# ID = "sr132_rs3_14-20"
# basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
# basedata = basedata.set_index(x.index)
# basedata['Power Min (kW)'] = x['chgMin_kW']
# basedata['Power Max (kW)'] = x['chgMax_kW']
# basedata['Energy Max (kWh)'] = x['eMax_kWh']
# basedata['Energy Min (kWh)'] = x['eMin_kWh']
# basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
# f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# # f.write("ID,value\n")
# f.write(ID + "," + str(y)+"\n")
# f.close()
# vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 132 for 14-20. RA dispmode 0. 2019 data",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
#              NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
# #THIS RAN TOO WHOOP!
# vc.runWithVC(shortname = ID+"_noRA", description = "user constraints for sr based on run 132 for 14-20. no RA. 2019 data",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
#              NSR_active='yes',DA_active = 'yes', RA_active='no', RA_dispmode = 0, User_active = 'yes', User_price = y)
#
# vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 132 for 14-20. RA dispmode 1",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
#              NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
#              #infeasible at 2017-07-25 12:00:00 hb
#
# #### RA test
# ID = "RA_rs1_13-19"
# x,y=combineRuns.ra0Fn(resultsPath = SVet_Path + "Results/output_run" + str(132) +"_SR_only/",runID=132,resHour=[13,19],regScenario=1)
# x.to_csv(SVet_Path+"Data/hourly_timeseries"+ID+".csv", index=False)
#
# vc.runWithVC(shortname = ID, description = "user constraints for RA every day 13-19",
#              Scenario_time_series_filename = SVet_Path+"Data/hourly_timeseries"+ID+".csv", SR_active='no',
#              NSR_active='no',DA_active = 'yes', RA_active='no', RA_dispmode = 1, User_active = 'yes', User_price = y)
#
# ID = "RA_rs2_13-19"
# x,y=combineRuns.ra0Fn(resultsPath = SVet_Path + "Results/output_run" + str(132) +"_SR_only/",runID=132,resHour=[13,19],regScenario=2)
# x.to_csv(SVet_Path+"Data/hourly_timeseries"+ID+".csv", index=False)
#
# vc.runWithVC(shortname = ID, description = "user constraints for RA every day 13-19. rs2",
#              Scenario_time_series_filename = SVet_Path+"Data/hourly_timeseries"+ID+".csv", SR_active='no',
#              NSR_active='no',DA_active = 'no', RA_active='no', User_active = 'yes', User_price = y)
#
# ## FR scenarios, Dec 8th
# runID  = 154
# resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_FR_only2019/"
# x,y = cr.frFn(resultsPath, runID, [0,23],3)
# ID = "fr154_rs3_24h"
# basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
# basedata = basedata.set_index(x.index)
# basedata['Power Min (kW)'] = x['chgMin_kW']
# basedata['Power Max (kW)'] = x['chgMax_kW']
# basedata['Energy Max (kWh)'] = x['eMax_kWh']
# basedata['Energy Min (kWh)'] = x['eMin_kWh']
# basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
# vc.runWithVC(shortname = ID, description = "user constraints for fr based on run 154 for 0-23h. no RA",
#              Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
#              NSR_active='yes',DA_active = 'yes', RA_active='no', RA_dispmode = 0, FR_active = 'no',User_active = 'yes', User_price = y)
#
