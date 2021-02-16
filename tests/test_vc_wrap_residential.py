from vc_wrap import SvetObject
from combine_runs import ConstraintObject

# Create a storagevet object
# TODO: change the default params file (and update tariff name)
# Note: DA should be turned off due to double counting of enegry arbitrage
DCM_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                          default_params_file="Model_Parameters_2v1-0-2_default_EA.csv",
                          shortname="EA+DCM on",
                          description="test run",
                          Scenario_n="month",
                          Scenario_time_series_filename="/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv",
                          DCM_active='yes',
                          retailTimeShift_active='yes',
                          DA_active='no',
                          SR_active='no'
                          )
DCM_baseline.run_storagevet()

# DCM constraints
DCMconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                 shortname=DCM_baseline.shortname, baseline_runID=DCM_baseline.runID,
                                 app_hours=[0, 23],
                                 regulation_scenario=3,
                                 constraint_init=True)
DCMconstraint.set_DCM_user_constraints()

# DCM priority run based on baseline
DCMpriority = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                         default_params_file="Model_Parameters_2v1-0-2_default_EA.csv",
                         shortname=DCMconstraint.new_shortname,
                         description="DCM priority run using retail rates",
                         Scenario_n="month",
                         Scenario_time_series_filename=DCMconstraint.new_hourly_timeseries_path,
                         User_active="yes", User_price=DCMconstraint.values,
                         DCM_active='no',
                         retailTimeShift_active='yes',
                         SR_active='yes', NSR_active='yes', DA_active='no', RA_active='no', RA_dispmode=0,
                         FR_active="no", FR_CombinedMarket="0")
DCMpriority.run_storagevet()

# DCM only sanity check
DCMsanity = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                       default_params_file="Model_Parameters_2v1-0-2_default_EA.csv",
                       shortname=DCMconstraint.new_shortname + "_DCMonly",
                       description="DCM only only sanity check with user constraints",
                       Scenario_n="month",
                       Scenario_time_series_filename=DCMconstraint.new_hourly_timeseries_path,
                       User_active="yes", User_price=DCMconstraint.values,
                       DCM_active='no',
                       retailTimeShift_active='yes',
                       DA_active='no',
                       SR_active='no')
DCMsanity.run_storagevet()
