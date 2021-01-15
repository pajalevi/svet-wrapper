"""
combine_runs.py

This function generates the inputs for a run that combines
constraints from multiple runs according to the given inputs.
It then runs StorageVET.

Zhenhua Zhang Jan 13 2021
"""

import pandas as pd
from wrapper_zhenhua.vc_wrap import SVetObject
import os
import vc_wrap as vc

SVet_Path = "/Applications/storagevet2v101/StorageVET-master-git/"
default_params_file = "Model_Parameters_2v1-0-2_default.csv"
runs_log_file = "Results/runsLog.csv"

# reg_scenario == 1, create reservations based on res_hours
# reg_scenario == 2, TODO
# reg_scenario == 3, create reservations based on previous dispatch


def combineRuns(runIDs, resTypes, resHours, regScenario,
SVet_Path = SVet_Path, default_params_file = default_params_file, runs_log_file = runs_log_file, test = False):
  """This function takes as input the type of regulatory scenario desired and three
  pieces of information regarding each run used to make the combined run: the run number,
  the resource type {“NSR”,”SR”,”RA1”,”RA0”,”DR1”,”DR0”…} and the hours in which a resource
  is given priority (e.g. [[6,16], [16,23]]), which may not overlap. It uses this information
  to run StorageVET with the desired combination of storage value stacking"""

  # check that runIDs, resTypes, and resHours are the same length

  # check for overlap in resHours & that each element has length 2

  # create empty matrix of user constraints
  # create placeholder for value

  # for each resource...
  for i in range(len(runIDs)):

    # ID folder:
    # read in runs log file
    runsLog = pd.read_csv(SVet_Path + runs_log_file)
    runsfilter = runsLog['runID']==runIDs[i]
    shortname = runsLog.loc[runsLog['runID'] == runIDs[i]]['shortname'].values[0]
    # id row with runID
    # id shortname

    # call appropriate read-in fn for that resource
    resultsPath = SVet_Path + "Results/output_run" + str(runIDs[i]) + "_" + shortname + "/"#"timeseries_results_runID" + str(runIDs[i]) + ".csv"

    resType_to_fn(resTypes[i],resultsPath,resHours[i], regScenario)

    # add outputs to user constraint matrix
    # select for most binding user constraints
    # add value to value placeholder

  # write new hourly_timseries input file

  # git commit if NOT test

  # run svet via vc_wrap


# function resource does the following
# read in timeseries of dispatch
# identify appropriate columns
# subset for desired hours
# translate output to appropriate limits
# also calculate value of that service

def resType_to_fn(resType,resultsPath,resHour,regScenario):
  switch_case = {
    "NSR": nsrFn,
    "SR": srFn
  }
  func = switch_case.get(resType) #get returns the value of the item associated with key
  func(resultsPath,resHour,regScenario) #TODO: define inputs
#end resType_to_fn


runID = 133
regScenario = 1
resHour = [14,20]
resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_NSR_only/"#"timeseries_results_runID" + str(runID) + ".csv"
def nsrFn(resultsPath, runID, resHour, regScenario):
  """create user constraints for nsr within window defined by resHour
  according to the logic of the regScenario """
  print("nsrFn called")

  # load parameter file for run
  params = pd.read_csv(resultsPath + "params_run" + str(runID) + ".csv")
  battpwr = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ch_max_rated'),'Value'].values[0])
  battpwrd = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'dis_max_rated'),'Value'].values[0])
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0])
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0])
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0])
  battcap = battcapmax * (maxsoc / 100)
  rte = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'rte'),'Value'].values[0])/100

  # nsr creates energy constraints, so we return only those
  # start by pre-filling output with dummy constraints that dont do anything - just replicate batt params
  output = pd.DataFrame(index = pd.date_range(start="1/1/2019",periods=8760,freq="h"), columns = ["chgMin_kW","chgMax_kW","eMin_kWh","eMax_kWh"])
  output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  output.loc[:,"eMax_kWh"] = battcap * (maxsoc/100)
  output.loc[:,"chgMin_kW"] = battpwr * -1
  output.loc[:,"chgMax_kW"] = battpwr

  # load timeseries - has prices, results
  timeseries = pd.read_csv(resultsPath + "timeseries_results_runID" + str(runID) + ".csv"  )
  timeseries["date"] = pd.to_datetime(timeseries['Start Datetime (hb)'])
  timeseries = timeseries.set_index('date')

  if regScenario == 1:
    ## create reservations based on resHours
    ### ID duration of NSR commitment & batt storage size -> calculate energy reservation requirement
    # chgMin is so that batt can reduce charging to provide NSR - since it's not possible to simulate the battery
    # charging at a set amount each hour for a large number of hours (as it would get full) we will just model
    # the reservation of SOC for NSR via discharging
    #TODO: account for different ch/disch, and CHARGING EFFICIENCY
    # dur = float(params.loc[(params['Tag'] == 'NSR') & (params['Key'] == 'duration'),'Value'].values[0])
    # if dur >1:
    #   nrgres = battpwr #here we convert from power (kW) to energy (kWh)
    # else:
    #   nrgres = battpwr * (1/dur)
    # ## insert into output during approppriate times
    # output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = nrgres + (battcapmax * minsoc/100)
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = (battcapmax * (minsoc / 100)) + battpwr#nrgres + (battcapmax * minsoc/100)
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = battcap - rte*battpwr
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = -1
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = 1

    # calculate value - multiply NSR price signal by battpwr for every active hour
    valueseries = timeseries.loc[:,"NSR Price Signal ($/kW)"] * battpwr
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])

  elif regScenario == 2:
    raise ValueError("regScenario 2 has not been coded yet")
  elif regScenario == 3:
    #create reservations based on previous dispatch
    # colnames = ['Non-spinning Reserve (Charging) (kW)','Non-spinning Reserve (Discharging) (kW)']
    # minres = timeseries['Non-spinning Reserve (Discharging) (kW)'] + (battcapmax * minsoc/100)
    # chgres = timeseries['Non-spinning Reserve (Charging) (kW)']
    # output.loc[:,'eMin_kWh'] = minres
    # output.loc[:,'chgMin_kW'] = chgres
    
    #avoid infeasibility: pwrmin and pwrmax must not be equal. (same for energy)
    sel = (timeseries['Non-spinning Reserve (Discharging) (kW)'] + timeseries['Non-spinning Reserve (Charging) (kW)']) >= battpwr*2
    timeseries.loc[sel,'Non-spinning Reserve (Discharging) (kW)'] = timeseries.loc[sel,'Non-spinning Reserve (Discharging) (kW)'] -1
      
    chgmin = -1*(battpwrd - timeseries['Non-spinning Reserve (Discharging) (kW)'])
    chgmax = battpwr - timeseries['Non-spinning Reserve (Charging) (kW)']
    nrgmin = (battcapmax * (minsoc / 100)) + timeseries['Non-spinning Reserve (Discharging) (kW)']
    nrgmax = battcap - rte*timeseries['Non-spinning Reserve (Charging) (kW)']
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = chgmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = chgmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = nrgmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = nrgmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]

    valueseries = timeseries.loc[:,"NSR Price Signal ($/kW)"] * (timeseries['Non-spinning Reserve (Discharging) (kW)'] + timeseries['Non-spinning Reserve (Charging) (kW)'])
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])
  else:
    raise ValueError("regScenario must be 1, 2 or 3")

  return(output, value)
#end nsrFn

# # runID = 107
runID = 132
# runID = 109
# regScenario = 1
# resHour = [14,20]
# # resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_4h_SR/"#"timeseries_results_runID" + str(runID) + ".csv"
resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_SR_only/"#"timeseries_results_runID" + str(runID) + ".csv"
# resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_0.5h_SR/"#"timeseries_results_runID" + str(runID) + ".csv"
def srFn(resultsPath, runID, resHour, regScenario):
  """create user constraints for sr within window defined by resHour
  according to the logic of the regScenario """
  print("srFn called")

  # load parameter file for run
  params = pd.read_csv(resultsPath + "params_run" + str(runID) + ".csv")
  battpwr = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ch_max_rated'),'Value'].values[0])
  battpwrd = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'dis_max_rated'),'Value'].values[0])
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0])
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0])
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0])
  battcap = battcapmax * (maxsoc / 100)
  rte = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'rte'),'Value'].values[0])/100

  # sr creates energy constraints, so we return only those
  # start by pre-filling output with dummy constraints that dont do anything - just replicate batt params
  output = pd.DataFrame(index = pd.date_range(start="1/1/2019",periods=8760,freq="h"), columns = ["chgMin_kW","chgMax_kW","eMin_kWh","eMax_kWh"])
  output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  output.loc[:,"eMax_kWh"] = battcap * (maxsoc/100)
  output.loc[:,"chgMin_kW"] = battpwr * -1
  output.loc[:,"chgMax_kW"] = battpwr

  # load timeseries - has prices, results
  timeseries = pd.read_csv(resultsPath + "timeseries_results_runID" + str(runID) + ".csv"  )
  timeseries["date"] = pd.to_datetime(timeseries['Start Datetime (hb)'])
  timeseries = timeseries.set_index('date')

  if regScenario == 1:
    ## create reservations based on resHours
    ### ID duration of sr commitment & batt storage size -> calculate energy reservation requirement
    #assumes ch and disch are equal
    #TODO: account for different ch/disch, and CHARGING EFFICIENCY
    # dur = float(params.loc[(params['Tag'] == 'SR') & (params['Key'] == 'duration'),'Value'].values[0])
    # if dur <= battcapmax/ch_max_rated:# >1: # assumes that ch and disch are equal!
      # nrgres = battpwr #here we convert from power (kW) to energy (kWh)
    # else:
      # nrgres = battpwr * (1/dur)
    ## insert into output during approppriate times
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = (battcapmax * (minsoc / 100)) + battpwr#nrgres + (battcapmax * minsoc/100)
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = battcap - rte*battpwr
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = -1
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = 1

    # calculate value - multiply SR price signal by battpwr for every active hour
    # TODO: does this account for both up and down regulation?
    valueseries = timeseries.loc[:,"SR Price Signal ($/kW)"] * battpwr
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])

  elif regScenario == 2:
    raise ValueError("regScenario 2 has not been coded yet")
  elif regScenario == 3:
    #create reservations based on previous dispatch
    # colnames = ['Non-spinning Reserve (Charging) (kW)','Non-spinning Reserve (Discharging) (kW)']
    # min res = timeseries['Spinning Reserve (Discharging) (kW)'] + (battcapmax * minsoc/100)
    # chgres = timeseries['Spinning Reserve (Charging) (kW)']
    #avoid infeasibility
    sel = (timeseries['Spinning Reserve (Discharging) (kW)'] + timeseries['Spinning Reserve (Charging) (kW)']) >= battpwr*2
    timeseries.loc[sel,'Spinning Reserve (Discharging) (kW)'] = timeseries.loc[sel,'Spinning Reserve (Discharging) (kW)'] -1

    chgmin = -1*(battpwrd - timeseries['Spinning Reserve (Discharging) (kW)'])
    chgmax = battpwr - timeseries['Spinning Reserve (Charging) (kW)']
    pwrmin = (battcapmax * (minsoc / 100)) + timeseries['Spinning Reserve (Discharging) (kW)']
    pwrmax = battcap - rte*timeseries['Spinning Reserve (Charging) (kW)']
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = chgmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = chgmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = pwrmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = pwrmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]

    valueseries = timeseries.loc[:,"SR Price Signal ($/kW)"] * (timeseries['Spinning Reserve (Discharging) (kW)'] + timeseries['Spinning Reserve (Charging) (kW)'])
    # this won't match the objective_values.csv values because those do not take into account model predictive control for SR in which last chunk of run is discarded
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])
  else:
    raise ValueError("regScenario must be 1, 2 or 3")

  return(output, value)
#end srFn

runID = 154
regScenario = 3
resHour = [14,20]
resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_FR_only2019/"
def frFn(resultsPath, runID, resHour, regScenario):
  """create user constraints for frequency regulation within window defined by resHour
  according to the logic of the regScenario """
  print("frFn called")

  # load parameter file for run
  params = pd.read_csv(resultsPath + "params_run" + str(runID) + ".csv")
  battpwr = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ch_max_rated'),'Value'].values[0])
  battpwrd = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'dis_max_rated'),'Value'].values[0])
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0])
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0])
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0])
  splitmktTF = bool(params.loc[(params['Tag'] == 'FR') & (params['Key'] == 'CombinedMarket'),'Value'].values[0])
  rte = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'rte'),'Value'].values[0])/100
  battcap = battcapmax * (maxsoc / 100)

  # start by pre-filling output with dummy constraints that dont do anything - just replicate batt params
  output = pd.DataFrame(index = pd.date_range(start="1/1/2019",periods=8760,freq="h"), columns = ["chgMin_kW","chgMax_kW","eMin_kWh","eMax_kWh"])
  output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  output.loc[:,"eMax_kWh"] = battcap * (maxsoc/100)
  output.loc[:,"chgMin_kW"] = battpwr * -1
  output.loc[:,"chgMax_kW"] = battpwr

  # load timeseries - has prices, results
  timeseries = pd.read_csv(resultsPath + "timeseries_results_runID" + str(runID) + ".csv"  )
  timeseries["date"] = pd.to_datetime(timeseries['Start Datetime (hb)'])
  timeseries = timeseries.set_index('date')

  if regScenario == 1:
    ## create reservations based on resHours
    ### ID duration of fr commitment & batt storage size -> calculate energy reservation requirement
    #TODO: account for different ch/disch, and CHARGING EFFICIENCY

    # output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = (battcapmax * (minsoc / 100)) + battpw #
    # output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = battcap - rte*battpwr
    # output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = -1
    # output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = 1
    # 
    # # calculate value - multiply FR price signal by battpwr for every active hour
    # valueseries_up = timeseries.loc[:,"Regulation Up Price Signal ($/kW)"] * battpwr
    # valueseries_d = timeseries.loc[:,"Regulation Down Price Signal ($/kW)"] * battpwr
    # ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    # value = sum(valueseries_up[ll],valueseries_d[ll])
    raise ValueError("regScenario 1 has not been coded yet")
  elif regScenario == 2:
    raise ValueError("regScenario 2 has not been coded yet")
  elif regScenario == 3:
    #create reservations based on previous dispatch
 
  # minimum charging (max discharging) behavior must make room for FR net discharging.
  # wait, minimum charging behavior must make room for max FR power response - this should be based on 'Regulation Down (Charging) (kW)' and 'Regulation Down (Discharging) (kW)'
    # regup is provided by charging less / discharging more. so, power levels must be high enough that they can be reduced for FR call
    chgmin = -1*(battpwrd - timeseries['Regulation Up (Discharging) (kW)'] - timeseries['Regulation Up (Charging) (kW)'])
    # regd is provided by charging more / discharging less. so, power levels must be low enough that they can be increased for FR up call
    chgmax = battpwr - timeseries['Regulation Down (Charging) (kW)'] - timeseries['Regulation Down (Discharging) (kW)']
    # timeseries['FR Energy Throughput Down (Discharging) (kWh)'] + timeseries['FR Energy Throughput Up (Charging) (kWh)'])
    # energy throuput is given - must have space for throuput. Can either do this with net for hour, or with worst case (disaggregate charge and discharge)
    # for simplicity we will do the net for hour for now
    # negative values for FR energy Throughput indicate charging. total effect on battery charge is net of actual charging and FR energy throughput
    # so, actual change in battery charge will be [initial SOC] + [batt chg * efficiency] - [batt discharge] + [FR energy throuput]
    # obviously power is linked to FR provision, and we *could* include that in the energy limitations, and this could make for a more OR LESS
    # constraining energy limitation. e.g. in the case of energy up provision, the battery is charging full steam, but also discharging quite a bit for FR
    # and the net of these makes for a less constrained energy limit
    # impt to note that FR energy throughput has already factored in charging efficiency
    nrgmax = battcap + timeseries['FR Energy Throughput (kWh)'] - chgmin * rte #TODO: sanity check the use of rte!!!
    nrgmin = (battcap * (minsoc/100)) + timeseries['FR Energy Throughput (kWh)'] - chgmax # positive throuput is discharging. chgmax is negative to indicate required discharging
    # nrgmin = battcap + timeseries['Spinning Reserve (Discharging) (kW)']
    # nrgmax = battcap - rte*timeseries['Spinning Reserve (Charging) (kW)']
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = chgmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = chgmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = nrgmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = nrgmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]

 
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    # valueseries = timeseries.loc[:,"SR Price Signal ($/kW)"] * (timeseries['Spinning Reserve (Discharging) (kW)'] + timeseries['Spinning Reserve (Charging) (kW)'])
    valueseries = ((timeseries.loc[:,"FR Energy Settlement Price Signal ($/kWh)"] * timeseries['FR Energy Throughput (kWh)']) +
                  (timeseries.loc[:,"Regulation Down Price Signal ($/kW)"] * (timeseries['Regulation Down (Charging) (kW)'] + timeseries['Regulation Down (Discharging) (kW)'])) +
                  (timeseries.loc[:,"Regulation Up Price Signal ($/kW)"] * (timeseries['Regulation Up (Charging) (kW)'] + timeseries['Regulation Up (Discharging) (kW)'])))
    value = sum(valueseries[ll])
  else:
    raise ValueError("regScenario must be 1, 2 or 3")

  return(output, value)

def ra0Fn(resultsPath, runID, resHour, regScenario, kwmo_value = 5):
  """create user constraints for RA dispmode 0 within window defined by resHour
  according to the logic of the regScenario """
  print("ra0Fn called")
  # load parameter file for run
  params = pd.read_csv(resultsPath + "params_run" + str(runID) + ".csv")
  battpwr = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ch_max_rated'),'Value'].values[0])
  battpwrd = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'dis_max_rated'),'Value'].values[0])
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0])
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0])
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0])
  battcap = battcapmax * (maxsoc / 100)
  rte = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'rte'),'Value'].values[0])/100
  ralength = minsoc = float(params.loc[(params['Tag'] == 'RA') & (params['Key'] == 'length'),'Value'].values[0])
  
  # Load hourly_timeseries so that we can edit this file to create our desired scenario
  basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
  basedata = basedata.set_index(pd.date_range(start="1/1/2019",periods=8760,freq="h"))
  basedata['Power Min (kW)'] = battpwr * -1
  basedata['Power Max (kW)'] = battpwr
  basedata['Energy Max (kWh)'] = battcap * (maxsoc/100)
  basedata['Energy Min (kWh)'] = battcap * (minsoc/100)


  # output = pd.DataFrame(index = pd.date_range(start="1/1/2019",periods=8760,freq="h"), columns = ["chgMin_kW","chgMax_kW","eMin_kWh","eMax_kWh"])
  # output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  # output.loc[:,"eMax_kWh"] = battcap * (maxsoc/100)
  # output.loc[:,"chgMin_kW"] = battpwr * -1
  # output.loc[:,"chgMax_kW"] = battpwr

  # load timeseries - has prices, results
  # timeseries = pd.read_csv(resultsPath + "timeseries_results_runID" + str(runID) + ".csv"  )
  # timeseries["date"] = pd.to_datetime(timeseries['Start Datetime (hb)'])
  # timeseries = timeseries.set_index('date')

  if regScenario == 1: #create energy reservations based on reshours & change prices
    # how do I prevent the batt from participating in other services during this window, except for energy arbitrage?
    # could change the prices of other services so that they are negative
    # can't really retain energy arbitrage and forego the others...
    #ok so what would 'RA only' look like? we've got the energy reservation... 

    basedata.loc[(basedata.index.hour == resHour[0]),'Energy Min (kWh)'] = battpwrd * ralength #SOC must be sufficient at beginning of each RA period
    basedata.loc[(basedata.index.hour >= resHour[0]) & (basedata.index.hour <= resHour[1]),'FR Price ($/kW)'] = 0
    basedata.loc[(basedata.index.hour >= resHour[0]) & (basedata.index.hour <= resHour[1]),'Reg Up Price ($/kW)'] = 0
    basedata.loc[(basedata.index.hour >= resHour[0]) & (basedata.index.hour <= resHour[1]),'Reg Down Price ($/kW)'] = 0
    basedata.loc[(basedata.index.hour >= resHour[0]) & (basedata.index.hour <= resHour[1]),'NSR Price ($/kW)'] = 0
    basedata.loc[(basedata.index.hour >= resHour[0]) & (basedata.index.hour <= resHour[1]),'SR Price ($/kW)'] = 0

    # calculate value - how is this done for RA rn? Ra capacity price ($/kW/mo) * mos * battpwr
    # I can do this in post-process

  elif regScenario == 2: # create onesided reservations based on reshours
    basedata.loc[(basedata.index.hour == resHour[0]),'Energy Min (kWh)'] = battpwrd * ralength #SOC must be sufficient at beginning of each RA period
 
  elif regScenario == 3: # create reservations based on prev dispatch
    raise ValueError("recScenario 3 doesn't exsit yet for RA")
  else:
    raise ValueError("regScenario must be 1, 2 or 3")

  output = basedata
  value = kwmo_value * battpwrd * 12
  return(output,value)
