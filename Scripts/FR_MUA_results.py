from vc_wrap import SvetObject
from combine_runs import ConstraintObject
import copy
import itertools

path = "/Applications/storagevet2v101/StorageVET-master-git/"
#ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv"
# FR Iteration
#isos = ["caiso","pjm","ercot","isone","nyiso"]
#iso_FR = ["0","0","1","1","1",]
isos = ["caiso","isone","nyiso"]
iso_FR = ["0","1","1",]
senslist_names = ["Battery_daily_cycle_limit","Finance_npv_discount_rate"]
sens_list = [["1","2"],["0.11","0.08"]]
ts_ends = ["_2019.csv","_0.25_FR-prices.csv"]
ts_short = ["historical","low"]
t=1

for iso_iter in [0,2]:#range(len(isos)):
    # for t in range(len(ts_ends)):
    iso=isos[iso_iter]
    FR_combined = iso_FR[iso_iter]
    ts = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ iso + ts_ends[t]

    # set up baseline for this ISO
    FRonly = SvetObject(SVet_absolute_path=path,
                        shortname="FR_only_"+iso+"_FR"+ts_short[t],
                        description="FR only run, baseline for FR priority. " + iso,
                        Scenario_time_series_filename=ts,
                        FR_active="yes", FR_CombinedMarket=FR_combined,
                        DA_active="yes", RA_active="no",
                        Scenario_n="48", Scenario_end_year="2034",
                        Battery_ccost_kw="0", Battery_ccost_kwh="400",
                        Battery_fixedOM="7",
                        Battery_hp="0", Battery_daily_cycle_limit="2"
                        )
    baseline = SvetObject(SVet_absolute_path=path,
                          shortname="FR_only_" + iso+"_FR"+ts_short[t],
                          description="FR only run, baseline for FR priority. " + iso,
                          Scenario_time_series_filename=ts,
                          FR_active="yes", FR_CombinedMarket=FR_combined,
                          RA_active="no",
                          SR_active="yes", NSR_active="yes",
                          Scenario_n="48", Scenario_end_year="2034",
                          Battery_ccost_kw="0", Battery_ccost_kwh="400",
                          Battery_fixedOM="7",
                          Battery_hp="0", Battery_daily_cycle_limit="2")

    # run baseline and constraint for each sensitivity
    all_runs = list(itertools.product(*sens_list))
    name = "FR_"+ts_short[t] +"MUA_run_"
    for i in range(len(all_runs)):
        thisrun = copy.deepcopy(FRonly)
        # set params for constraint ref
        for j in range(len(all_runs[i])):
            thisrun.argument_list[senslist_names[j]]=all_runs[i][j]
        thisrun.shortname = name + iso + "_sens"+str(i)
        thisrun.description = name + iso + "_sens"+str(i)+" GSA sensitivity, check parameters"
        # run baseline
        thisrun.run_storagevet()
        # set constraints
        FRconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                        shortname=thisrun.shortname, baseline_runID=thisrun.runID,
                                        app_hours=[0,23],
                                        regulation_scenario=3,
                                        constraint_init=True)
        FRconstraint.set_FR_user_constraints()
        # run constrained
        FRpriority = SvetObject(SVet_absolute_path=path,
                                shortname=FRconstraint.new_shortname + "24h_" + iso+ "_sens" + str(i) + "_FR"+ts_short[t],
                                description="FR Priority run based on FR only. all hours_" + iso,
                                Scenario_time_series_filename=FRconstraint.new_hourly_timeseries_path,
                                User_active="yes", User_price=FRconstraint.values,
                                FR_active="no", RA_active="no",
                                SR_active="yes", NSR_active="yes",
                                Scenario_n="48", Scenario_end_year="2034",
                                Battery_ccost_kw="0", Battery_ccost_kwh="400",
                                Battery_fixedOM="7",
                                Battery_hp="0", Battery_daily_cycle_limit="2"
                                )
        # set params for constrained run
        for j in range(len(all_runs[i])):
            FRpriority.argument_list[senslist_names[j]] = all_runs[i][j]
        FRpriority.run_storagevet()

        # set params for baseline run
        base = copy.deepcopy(baseline)
        for j in range(len(all_runs[i])):
            base.argument_list[senslist_names[j]] = all_runs[i][j]
        base.shortname = name + iso + "_base_sens" + str(i)
        base.description = name + iso + "_sens" + str(i) + " GSA sensitivity, baseline"
        base.run_storagevet()