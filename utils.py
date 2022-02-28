import pandas as pd
import numpy as np

def filter(start_date,end_date,emp_id,df):
    attendence = pd.date_range(start_date,end_date)
    after_start_date = df["date"] >= start_date
    before_end_date = df["date"] < end_date
    between_two_dates = after_start_date & before_end_date
    filtered_dates = df.loc[between_two_dates]
    filtered_dates=filtered_dates.reset_index()
    filtered_dates = filtered_dates.drop(["index"],axis=1)

    for key, value in filtered_dates.iterrows():
        if value[3] > early_evening:
            filtered_dates.iloc[key,1] = 1
    
    emp_attendence_morning = filtered_dates.loc[(filtered_dates["emp_id"] == emp_id) & (filtered_dates["in_out"] == entry)].drop_duplicates()
    emp_attendence_evening = filtered_dates.loc[(filtered_dates["emp_id"] == emp_id) & (filtered_dates["in_out"] == exit)].drop_duplicates()

    final = pd.merge(emp_attendence_morning,emp_attendence_evening,on="date",how='outer')
    final["duration"] = final["time_y"] - final["time_x"]
    final = final[final["emp_id_x"] == final.iloc[0,0]]
    final = final.drop(["emp_id_x","in_out_x","emp_id_y","in_out_y","time_x","time_y"],axis=1)

    return final


