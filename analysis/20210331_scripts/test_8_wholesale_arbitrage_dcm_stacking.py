from vc_wrap import SvetObject
from combine_runs import ConstraintObject

# Create a storagevet object
# Note: DA should be turned off due to double counting of enegry arbitrage
pjm_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                          default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                          shortname="PJM RS+DCM on + stacking",
                          description="PJM",
                          Scenario_n="48",
                          Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_pjm_2020.csv",
                          Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/pjm_virginia_gs3_2019.csv",
                          DCM_active='yes',
                          retailTimeShift_active='no',
                          DA_active='yes',
                          SR_active='yes',
                          NSR_active='yes',
                          FR_active="yes",
                          FR_CombinedMarket="1"
                          )
pjm_baseline.run_storagevet()

nyiso_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                            default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                            shortname="NYISO RS+DCM on + stacking",
                            description="NYISO",
                            Scenario_n="48",
                            Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_nyiso_2019.csv",
                            Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/nyiso_no9_rate2_2021.csv",
                            DCM_active='yes',
                            retailTimeShift_active='no',
                            DA_active='yes',
                            SR_active='yes',
                            NSR_active='yes',
                            FR_active="yes",
                            FR_CombinedMarket="1"
                            )
nyiso_baseline.run_storagevet()

isone_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                            default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                            shortname="ISONE RS+DCM on + stacking",
                            description="ISONE",
                            Scenario_n="48",
                            Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_isone_2019.csv",
                            Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data//isone_t2_2020.csv",
                            DCM_active='yes',
                            retailTimeShift_active='no',
                            DA_active='yes',
                            SR_active='yes',
                            NSR_active='yes',
                            FR_active="yes",
                            FR_CombinedMarket="1"
                            )
isone_baseline.run_storagevet()

caiso_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                            default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                            shortname="CAISO RS+DCM on + stacking",
                            description="CAISO",
                            Scenario_n="48",
                            Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_2019.csv",
                            Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/caiso_pge_b20_2020.csv",
                            DCM_active='yes',
                            retailTimeShift_active='no',
                            DA_active='yes',
                            SR_active='yes',
                            NSR_active='yes',
                            FR_active="yes",
                            FR_CombinedMarket="1"
                            )
caiso_baseline.run_storagevet()

ercot_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                            default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                            shortname="ERCOT RS+DCM on + stacking",
                            description="ERCOT",
                            Scenario_n="48",
                            Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_ercot_2019.csv",
                            Finance_customer_tariff_filename="/Users/zhenhua/Desktop/ISO_price_data/tariff_data/ercot_oncor_2018.csv",
                            DCM_active='yes',
                            retailTimeShift_active='no',
                            DA_active='yes',
                            SR_active='yes',
                            NSR_active='yes',
                            FR_active="yes",
                            FR_CombinedMarket="1"
                            )
ercot_baseline.run_storagevet()
