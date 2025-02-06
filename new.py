import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Add your logo image
st.image('image.png', width=200)

# Title and description
st.markdown("<h1 style='color: #1E90FF;'>Air Quality Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #32CD32;'>Explore Air Quality Data by Pollutants, Regions, and Time Periods.</h3>", unsafe_allow_html=True)

@st.cache
def load_data():
    data = pd.read_csv("sampled_dataset.csv")
    return data

# Load the dataset
data = load_data()

# Data Preprocessing
if 'Unnamed: 0' in data.columns:
    data = data.drop(columns=['Unnamed: 0'])

data['SO2 AQI'] = data.groupby('City')['SO2 AQI'].transform(lambda x: x.fillna(x.median()))
data['CO AQI'] = data.groupby('City')['CO AQI'].transform(lambda x: x.fillna(x.median()))
data['Date Local'] = pd.to_datetime(data['Date Local'], errors='coerce')
data = data.dropna(subset=['Date Local'])

# Detect and replace outliers
def replace_outliers_with_median(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    median_value = data[column].median()
    data[column] = data[column].apply(lambda x: median_value if (x < lower_bound or x > upper_bound) else x)

for col in ['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']:
    replace_outliers_with_median(data, col)

# Sidebar for pollutant and date range selection
st.sidebar.markdown("<h4 style='color: #1E90FF;'>Choose a Pollutant</h4>", unsafe_allow_html=True)
pollutant = st.sidebar.selectbox("Select Pollutant", ['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean'])

st.sidebar.markdown("<h4 style='color: #1E90FF;'>Date Range</h4>", unsafe_allow_html=True)
start_date = st.sidebar.date_input("Start Date", data['Date Local'].min().to_pydatetime().date())
end_date = st.sidebar.date_input("End Date", data['Date Local'].max().to_pydatetime().date())

# Filter data by date
data_filtered = data[(data['Date Local'] >= pd.to_datetime(start_date)) & (data['Date Local'] <= pd.to_datetime(end_date))]

# Temporal Trend Visualization
if pollutant in data_filtered.columns:
    st.markdown(f"<h3 style='color: #FFD700;'>Temporal Trend of {pollutant}</h3>", unsafe_allow_html=True)
    data_grouped = data_filtered.groupby("Date Local")[pollutant].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    data_grouped.plot(ax=ax, color='tab:blue', lw=2)
    ax.set_title(f"{pollutant} Levels Over Time", fontsize=16, color='darkorange')
    ax.set_xlabel("Date", fontsize=12, color='darkgreen')
    ax.set_ylabel("Pollutant Level", fontsize=12, color='darkgreen')
    ax.grid(True)
    st.pyplot(fig)

# State and city selection
st.sidebar.markdown("<h4 style='color: #1E90FF;'>Select State</h4>", unsafe_allow_html=True)
state = st.sidebar.selectbox("Select State", data_filtered['State'].unique())
state_data = data_filtered[data_filtered['State'] == state]

if not state_data.empty:
    city_options = state_data['City'].dropna().unique()
    st.sidebar.markdown("<h4 style='color: #1E90FF;'>Select City</h4>", unsafe_allow_html=True)
    city = st.sidebar.selectbox("Select City", city_options)
else:
    st.sidebar.warning("No data available for the selected state. Please choose another state.")

# Choropleth map for pollutant levels by state
st.markdown("<h3 style='color: #FF6347;'>Choropleth Map of Pollutants by State</h3>", unsafe_allow_html=True)
pollutant_state_data = data.groupby('State')[[pollutant]].mean().reset_index()
pollutant_state_map = px.choropleth(
    pollutant_state_data,
    locations="State",
    locationmode="USA-states",
    color=pollutant,
    color_continuous_scale="Viridis",
    scope="usa",
    title=f"Average {pollutant} Levels by State"
)
st.plotly_chart(pollutant_state_map, use_container_width=True)

# City-level AQI trends
city_data = state_data[state_data['City'] == city]
if not city_data.empty:
    city_data = city_data.groupby('Date Local')[
        ['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']
    ].median()
    st.subheader(f"AQI Levels in {city}")
    fig, ax = plt.subplots(figsize=(10, 6))
    city_data.plot(ax=ax, title=f"AQI Levels in {city}", marker='o', colormap='coolwarm')
    ax.set_ylabel("AQI Level")
    ax.grid(True)
    st.pyplot(fig)

# Top pollutant levels by state
st.markdown("<h3 style='color: #FF6347;'>Top Pollutant Level States</h3>", unsafe_allow_html=True)
topstatesdata = data.groupby("State")[
    ['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']
].median().sort_values(by=['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI'], ascending=False)
fig, ax = plt.subplots()
topstatesdata.head(10).plot(kind="bar", ax=ax)
st.pyplot(fig)

# Pollutant correlation heatmap
st.markdown("<h3 style='color: #FF6347;'>Pollutant Correlations</h3>", unsafe_allow_html=True)
correlation_data = data[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', ax=ax, linewidths=0.5)
ax.set_title("Correlation Heatmap", fontsize=16)
st.pyplot(fig)

# Seasonal trends by month
st.markdown("<h3 style='color: #1E90FF;'>Seasonal Trends of Pollutants</h3>", unsafe_allow_html=True)
data['Month'] = data['Date Local'].dt.month
seasonal_data = data.groupby('Month')[
    ['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']
].mean()
fig, ax = plt.subplots(figsize=(10, 6))
seasonal_data.plot(ax=ax, colormap='coolwarm', marker='o')
ax.set_title("Average Pollutant Levels by Month", fontsize=16)
ax.set_xlabel("Month")
ax.set_ylabel("Pollutant AQI")
st.pyplot(fig)


# Average AQI Levels by State and Pollutant
st.markdown("<h3 style='color: #FF4500;'>Average AQI Levels by State and Pollutant</h3>", unsafe_allow_html=True)

# Heatmap for Average AQI Levels
avg_aqi_data = data.groupby('State')[
    ['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']
].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(
    avg_aqi_data.set_index('State').transpose(),
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar_kws={'label': 'AQI Levels'}
)
ax.set_title("Heatmap of Average AQI Levels by State and Pollutant", fontsize=16)
ax.set_xlabel("States", fontsize=12)
ax.set_ylabel("Pollutants", fontsize=12)
st.pyplot(fig)

# Bar Graph for Average AQI Levels by Pollutant
st.markdown("<h3 style='color: #FFA500;'>Bar Graph of Average AQI Levels by Pollutant</h3>", unsafe_allow_html=True)

avg_aqi_overall = avg_aqi_data.mean().drop('State')
fig, ax = plt.subplots(figsize=(8, 6))
avg_aqi_overall.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title("Average AQI Levels by Pollutant", fontsize=16)
ax.set_ylabel("AQI Level", fontsize=12)
ax.set_xticklabels(avg_aqi_overall.index, rotation=45, fontsize=10)
st.pyplot(fig)
