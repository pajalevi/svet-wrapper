from vc_wrap import SvetObject
from combine_runs import ConstraintObject

# Create a storagevet object
# Note: DA should be turned off due to double counting of enegry arbitrage
pjm_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                          default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                          shortname="PJM SR+NSR+FR on",
                          description="PJM",
                          Scenario_n="48",
                          Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_pjm_2020.csv",
                          DCM_active='no',
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
                          shortname="NYISO SR+NSR+FR on",
                          description="NYISO",
                          Scenario_n="48",
                          Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_nyiso_2019.csv",
                          DCM_active='no',
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
                          shortname="ISONE SR+NSR+FR on",
                          description="ISONE",
                          Scenario_n="48",
                          Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_isone_2019.csv",
                          DCM_active='no',
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
                          shortname="CAISO SR+NSR+FR on",
                          description="CAISO",
                          Scenario_n="48",
                          Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_2019.csv",
                          DCM_active='no',
                          retailTimeShift_active='no',
                          DA_active='yes',
                          SR_active='yes',
                          NSR_active='yes',
                          FR_active="yes",
                          FR_CombinedMarket="0"
                          )
caiso_baseline.run_storagevet()

ercot_baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                          default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                          shortname="ERCOT SR+NSR+FR on",
                          description="ERCOT",
                          Scenario_n="72",
                          Scenario_time_series_filename="/Users/zhenhua/Desktop/ISO_price_data/hourly_timeseries_ercot_2019.csv",
                          DCM_active='no',
                          retailTimeShift_active='no',
                          DA_active='yes',
                          SR_active='yes',
                          NSR_active='yes',
                          FR_active="yes",
                          FR_CombinedMarket="0"
                          )
ercot_baseline.run_storagevet()
