from vc_wrap import SvetObject
from combine_runs import ConstraintObject

iso_name = "pjm"
Scenario_time_series_filename = "/Users/zhenhua/Desktop/price_data/hourly_timeseries_pjm_2019.csv"
Finance_customer_tariff_filename = "/Users/zhenhua/Desktop/price_data/tariff_data/original_documents/caiso_pge_b20_2020.csv"

# value stacking, should be the best scenario
baseline = SvetObject(SVet_absolute_path="/Applications/storagevet2v101/StorageVET-master-git/",
                      default_params_file="Model_Parameters_2v1-0-2_default_03-2021.csv",
                      shortname="{} DA on".format(iso_name),
                      description=iso_name,
                      Scenario_n="24",
                      Scenario_no_export="1",
                      Scenario_time_series_filename=Scenario_time_series_filename,
                      Finance_customer_tariff_filename=Finance_customer_tariff_filename,
                      DCM_active='no',
                      retailTimeShift_active='no',
                      DA_active='yes',
                      SR_active='no',
                      NSR_active='no',
                      FR_active="no",
                      FR_CombinedMarket="1"
                      )
baseline.run_storagevet()
