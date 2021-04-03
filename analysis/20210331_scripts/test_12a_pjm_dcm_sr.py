from vc_wrap import SvetObject
from combine_runs import ConstraintObject

# value stacking, should be the best scenario
pjm_all = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                     default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                     shortname="PJM DCM+SR+NSR on",
                     description="PJM",
                     Scenario_n="48",
                     Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_pjm_2020.csv",
                     Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/pjm_virginia_gs3_2019.csv",
                     DCM_active='yes',
                     retailTimeShift_active='yes',
                     DA_active='no',
                     SR_active='yes',
                     NSR_active='yes',
                     FR_active="no",
                     FR_CombinedMarket="1"
                     )
pjm_all.run_storagevet()

# use ths to determine monthly peak net load
pjm_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                          default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                          shortname="PJM DCM+SR on",
                          description="PJM",
                          Scenario_n="48",
                          Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_pjm_2020.csv",
                          Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/pjm_virginia_gs3_2019.csv",
                          DCM_active='yes',
                          retailTimeShift_active='yes',
                          DA_active='no',
                          SR_active='no',
                          NSR_active='no',
                          FR_active="no",
                          FR_CombinedMarket="1"
                          )
pjm_baseline.run_storagevet()

# DCM constraints
DCMconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                 shortname=pjm_baseline.shortname, baseline_runID=pjm_baseline.runID,
                                 app_hours=[0, 23],
                                 regulation_scenario=3,
                                 constraint_init=True)
DCMconstraint.set_DCM_user_constraints()

# determine sr constraints
pjm_all_w_dcm = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                           default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                           shortname=DCMconstraint.new_shortname,
                           description="PJM",
                           Scenario_n="48",
                           Scenario_time_series_filename=DCMconstraint.new_hourly_timeseries_path,
                           Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/pjm_virginia_gs3_2019.csv",
                           User_active="yes", User_price=DCMconstraint.values,
                           DCM_active='no',
                           retailTimeShift_active='yes',
                           DA_active='no',
                           SR_active='yes',
                           NSR_active='yes',
                           FR_active="no",
                           FR_CombinedMarket="1"
                           )
pjm_all_w_dcm.run_storagevet()

# SR has priority from 2-8pm
SRconstraint = ConstraintObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                                shortname=pjm_all_w_dcm.shortname, baseline_runID=pjm_all_w_dcm.runID,
                                app_hours=[14, 19],
                                regulation_scenario=3,
                                constraint_init=True)
SRconstraint.set_SR_user_constraints()

pjm_sr_priority = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                             default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                             shortname=SRconstraint.new_shortname,
                             description="PJM",
                             Scenario_n="48",
                             Scenario_time_series_filename=SRconstraint.new_hourly_timeseries_path,
                             Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/pjm_virginia_gs3_2019.csv",
                             User_active="yes", User_price=SRconstraint.values,
                             DCM_active='no',
                             retailTimeShift_active='yes',
                             DA_active='no',
                             SR_active='no',
                             NSR_active='yes',
                             FR_active="no",
                             FR_CombinedMarket="1"
                             )
pjm_sr_priority.run_storagevet()

pjm_sr_priority = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                             default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                             shortname=SRconstraint.new_shortname,
                             description="PJM",
                             Scenario_n="48",
                             Scenario_time_series_filename=SRconstraint.new_hourly_timeseries_path,
                             Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/pjm_virginia_gs3_2019.csv",
                             User_active="yes", User_price=SRconstraint.values,
                             DCM_active='yes',
                             retailTimeShift_active='yes',
                             DA_active='no',
                             SR_active='no',
                             NSR_active='yes',
                             FR_active="no",
                             FR_CombinedMarket="1"
                             )
pjm_sr_priority.run_storagevet()

