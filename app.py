import streamlit as st
import pandas as pd

entry = 0
exit = 1
morning_time = pd.to_timedelta("10:00:00")
late_morning_time = pd.to_timedelta("12:00:00")
evening_time = pd.to_timedelta("18:00:00")
early_evening = pd.to_timedelta("15:00:00")
master_list = {1: "Vaibhavkrishna Bhosle",
                2: "Shivaji Bhosle",
                3: "Suvarna Bhosle",
                4: "Shreekant",
                5: "Shivappa",
                6: "Maheshwari Biradar",
                7: "Suvarna A",
                8: "Sachin",
                9: "Jameer Sir",
                10: "Vijaylaxmi Mam",
                11: "Suryakant Sir",
                12: "Kannada Mam",
                13: "Dattu Sir",
                14: "Sandeep Sir",
                16: "Pandit Sir",
                17: "Vishwanath Sir"}

def filter(start_date,end_date,emp_id,df):
    after_start_date = df["date"] >= pd.to_datetime(start_date)
    before_end_date = df["date"] < pd.to_datetime(end_date)
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
    final = final.drop(["emp_id_x","in_out_x","emp_id_y","in_out_y",],axis=1)

    return final

file = st.file_uploader("Upload", type={"dat"})
option = st.selectbox("Select Employee",("Vaibhavkrishna Bhosle", "Shivaji Bhosle","Suvarna Bhosle","Shreekant","Shivappa","Maheshwari Biradar","Suvarna A","Sachin","Jameer Sir","Vijaylaxmi Mam","Suryakant Sir","Kannada Mam","Dattu Sir","Sandeep Sir","Pandit Sir","Vishwanath Sir"))
st.write("You Selected: ", option)

for key,value in master_list.items():
    if str(option) == value:
        emp_id = key

st.write("You Selected: ", emp_id)

if file is not None:
    df = pd.read_csv(file , sep="\t",header=None)
    df.columns = ["emp_id","Date_Time","fingure","in_out","junk","junk_"]
    df1 = df.Date_Time.str.split(expand=True)
    df["date"] = pd.to_datetime(df1[0])
    format_str = '%H:%M:%S'
    df["time"] = pd.to_timedelta(df1[1])
    df = df.drop(["Date_Time","fingure","junk","junk_"],axis=1)

start_date = st.text_input("Start Date: ", "yyyy-mm-dd")
end_date = st.text_input("End Date: ", "yyyy-mm-dd")

if st.button("Run"):
    sudo = filter(start_date,end_date,emp_id,df)
    sudo = sudo.loc[sudo["duration"].notnull()]
    sudo["date"] = sudo.date.apply(str)
    
    sudo["time_x"] = sudo["time_x"].apply(str)
    in_time = sudo.time_x.str.split(expand = True)
    sudo["In Time"] = in_time[2]

    sudo["time_y"] = sudo["time_y"].apply(str)
    out_time = sudo.time_y.str.split(expand = True)
    sudo["Out Time"] = out_time[2]
    
    sudo["duration"] =sudo.duration.apply(str)
    time_only = sudo.duration.str.split(expand=True)
    sudo["Total Duration"] = time_only[2]

    final = sudo.drop(["duration","time_x","time_y"],axis=1)
    #print(final)
    st.write(final)

    st.write("Total Number of Days Present: "+str(final.count()[0]))

else :
    st.write("Nothing to process")

