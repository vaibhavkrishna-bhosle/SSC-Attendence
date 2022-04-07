import streamlit as st
import pandas as pd
from datetime import timedelta

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
                15: "Veerendra J",
                16: "Pandit Sir",
                17: "Vishwanath Sir",
                18: "Pavan Sir",
                19: "Raheem Sir"}

def filter(start_date,end_date,emp_id,df):
    after_start_date = df["date"] >= pd.to_datetime(start_date)
    before_end_date = df["date"] < pd.to_datetime(end_date)
    between_two_dates = after_start_date & before_end_date
    filtered_dates = df.loc[between_two_dates]
    filtered_dates=filtered_dates.reset_index()
    filtered_dates = filtered_dates.drop(["index"],axis=1)

    filtered_dates = filtered_dates[filtered_dates["emp_id"] == emp_id]
    filtered_dates = filtered_dates.reset_index()
    filtered_dates = filtered_dates.drop(["index","emp_id"],axis=1)
    return filtered_dates

file = st.file_uploader("Upload", type={"dat"})
option = st.selectbox("Select Employee",("Vaibhavkrishna Bhosle", "Shivaji Bhosle","Suvarna Bhosle","Shreekant","Shivappa","Maheshwari Biradar","Suvarna A","Sachin","Jameer Sir","Vijaylaxmi Mam","Suryakant Sir","Kannada Mam","Dattu Sir","Sandeep Sir","Veerendra J","Pandit Sir","Vishwanath Sir","Pavan Sir","Raheem Sir"))
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
    df["time"] = pd.to_timedelta(df1[1])
    
    df = df.drop(["Date_Time","fingure","junk","junk_"],axis=1)

start_date = st.text_input("Start Date: ", "yyyy-mm-dd")
end_date = st.text_input("End Date: ", "yyyy-mm-dd")

if st.button("Run"):
    monthly_df = pd.DataFrame()
    filtered_dates = filter(start_date,end_date,emp_id,df)
    date_att = pd.to_datetime(filtered_dates["date"].unique()).strftime("%Y-%m-%d").tolist()
    date_cur = []
    in_time = []
    out_time = []
    on_break = []
    on_floor = []

    for dates in date_att:
        on_floor_time = timedelta()
        on_break_time = timedelta()


        temp = filtered_dates[filtered_dates["date"] == dates]
        temp = temp.reindex()

        if (temp.size/3) % 2 == 0:
            for i in range(0,int(temp.size/3),1):
                if i % 2 == 0:
                    temp["in_out"][i] = 0
                else:
                    temp["in_out"][i] = 1
            for i in range(1,int(temp.size/3)):
                if i % 2 == 1:
                    on_floor_time =on_floor_time + (temp["time"].iloc[i] - temp["time"].iloc[i-1])
                else:
                    on_break_time =on_break_time + (temp["time"].iloc[i] - temp["time"].iloc[i-1])

            date_cur.append(dates)
            in_time.append(min(temp["time"]))
            out_time.append(max(temp["time"]))
            on_floor.append(on_floor_time)
            on_break.append(on_break_time)
            print("Inserted")
        else:
            st.write("Error in data for date"+str(dates))
            date_cur.append(dates)
            in_time.append(min(temp["time"]))
            out_time.append(max(temp["time"]))
            on_floor.append(on_floor_time)
            on_break.append(on_break_time)


    monthly_df["Date"] = date_cur
    monthly_df["In Time"] =  in_time 
    monthly_df["Out Time"] = out_time
    monthly_df["On Floor"] = on_floor
    monthly_df["On Break"] = on_break
    monthly_df["Total on Campus"] = on_floor+on_break

    cols = monthly_df.columns
    monthly_df[cols[0]] = monthly_df[cols[0]]
    monthly_df[cols[1]] = monthly_df[cols[1]].astype(str).str[7:]
    monthly_df[cols[2]] = monthly_df[cols[2]].astype(str).str[7:]
    monthly_df[cols[3]] = monthly_df[cols[3]].astype(str).str[7:]
    monthly_df[cols[4]] = monthly_df[cols[4]].astype(str).str[7:]
    monthly_df[cols[5]] = monthly_df[cols[5]].astype(str).str[7:]
    
    #st.table(monthly_df)
    print("End of process")
    print(monthly_df)
    st.write(monthly_df)
    st.write("Total Number of Days Present: "+str(monthly_df.count()[0]))

else :
    st.write("Nothing to process")

