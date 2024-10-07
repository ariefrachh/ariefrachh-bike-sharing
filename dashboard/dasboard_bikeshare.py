import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Dashboard Bike Sharing Washington DC in 2011/2012')

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)   

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date_days = day_df["dteday"].min()
max_date_days = day_df["dteday"].max()

min_date_hour = hour_df["dteday"].min()
max_date_hour = hour_df["dteday"].max()

with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    
        
    start_date, end_date = st.date_input(
        label='Time Range',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
    
    st.write("## Statistik Singkat")
    total_users = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) &
                         (day_df["dteday"] <= pd.to_datetime(end_date))]["cnt"].sum()
    
    st.metric(label="Total Pengguna", value=f"{total_users:,}")
    
    st.write("## Filter Season")
    season_options = day_df['season'].unique()
    selected_season = st.multiselect('Pilih Season', season_options, default=season_options)
    
    st.write("## Filter Hari Kerja")
    workingday_filter = st.radio(
        "Apakah hari kerja?",
        options=['Ya', 'Tidak'],
        index=0  # default value
    )
    
    st.write("## Pilih Jenis Plot")
    plot_type = st.selectbox(
        'Jenis Visualisasi',
        ['Scatterplot', 'Lineplot', 'Histogram']
    )
    
st.subheader('Usage Distribution per Hour and Day')

fig, ax = plt.subplots(figsize=(12, 8))
sns.histplot(data=hour_df, x='hr', weights='cnt', hue='weekday', multiple='stack', palette='viridis', bins=24, ax=ax)
plt.title('Usage Distribution per Hour and Day')
plt.xlabel('Hour (0-23)')
plt.ylabel('Total Users')
plt.legend(title='Day of the Week', labels=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
plt.tight_layout()
st.pyplot(fig)


st.subheader('Total Usage per Day Over Two Years')

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
fig, ax = plt.subplots(figsize=(20, 6))
sns.lineplot(x='dteday', y='cnt', data=hour_df, ax=ax)
ax.set_title('Total Usage per Day Over Two Years', fontsize=16)
ax.set_xlabel('Date')
ax.set_ylabel('Total Usage')
st.pyplot(fig)


st.subheader('The Effect of Wind Speed ​​on Bike Sharing Users')

sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 8))
sns.scatterplot(data=day_df, x='windspeed', y='cnt', color='blue', alpha=0.6, ax=ax)
sns.regplot(x='windspeed', y='cnt', data=day_df, scatter=False, color='black', ax=ax)
ax.set_title('The Effect of Windspeed on the Number of Bike Sharing Users', fontsize=16)
ax.set_xlabel('Windspeed (Normalized)', fontsize=12)
ax.set_ylabel('Total User', fontsize=12)
st.pyplot(fig)
