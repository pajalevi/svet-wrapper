from vc_wrap import SvetObject
from combine_runs import ConstraintObject
from GSA_runs import iterate_financial_sensitivites
path = "/Applications/storagevet2v101/StorageVET-master-git/"

# runID ='979'
# run_shortname='RA_SCOM_200dayssens2'
# test_financial = SvetObject(SVet_absolute_path=path,
#                             shortname="fin_sensitivity_"+run_shortname,
#                             description="Test financial scenario with 20 year lifetime applied to run "+ runID,
#                             Scenario_end_year="2039")
# test_financial.new_financial_scenario(runID,run_shortname)


runIDs = range(860,979)
senslist_names1 = ["Battery_ccost_kwh","Finance_npv_discount_rate","Battery_fixedOM","User_price", "Scenario_end_year"]
senslist1 = [["400","450"],["0.14","0.11"],["40","77"],["3","6"],["2034","2039","2029"]] #TODO: make sure first value is default, and have iterate_sensitivities not run the first line
for r in runIDs:
    test_financial = SvetObject(SVet_absolute_path=path,
                                shortname="fin_sensitivity_on_runID" + str(r), #not used
                                description="Test financial scenario with 20 year lifetime applied to run " + str(runIDs)) # not used

    iterate_financial_sensitivites(test_financial,senslist_names1,senslist1,r)