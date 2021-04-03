import pandas as pd
import numpy as np
import datetime

isone_data = pd.read_excel(
    "/Users/zhenhua/Desktop/ISO_price_data/isone_2019/5min_reserve_price_and_designation_2019.xlsx")

data_sr = isone_data.groupby(["month", "day", "hour"])['tmsr_dollar_per_MWh'].max().reset_index(drop=False)
data_sr["datetime (hs)"] = data_sr.apply(lambda x: datetime.datetime(year=2019, month=int(x["month"]),
                                                                     day=int(x["day"]), hour=int(x["hour"])),
                                         axis=1)
data_nsr = isone_data.groupby(["month", "day", "hour"])['tmnsr_dollar_per_MWh'].max().reset_index(drop=False)
data_nsr["datetime (hs)"] = data_nsr.apply(lambda x: datetime.datetime(year=2019, month=int(x["month"]),
                                                                       day=int(x["day"]), hour=int(x["hour"])),
                                           axis=1)

data_date = pd.DataFrame()
data_date["datetime (hs)"] = pd.date_range(start='2019-01-01', end='2020-01-01', freq='1H')

merged_data = data_date.merge(data_sr, left_on="datetime (hs)", right_on="datetime (hs)", how="left")
merged_data = merged_data.merge(data_nsr, left_on="datetime (hs)", right_on="datetime (hs)", how="left")

merged_data.to_csv("/Users/zhenhua/Desktop/ISO_price_data/isone_2019/hourly_2019.csv")
