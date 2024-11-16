import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Title with custom color
st.markdown("<h1 style='color: #1E90FF;'>Air Quality Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #32CD32;'>Explore air quality data by pollutants, regions, and time periods.</h3>", unsafe_allow_html=True)

data = pd.read_csv("pollution_us_2000_2016.csv")

# Convert 'Date Local' to datetime
data['Date Local'] = pd.to_datetime(data['Date Local'], errors='coerce')

# Drop irrelevant column
if 'Unnamed: 0' in data.columns:
    data = data.drop(columns=['Unnamed: 0'])

missing_values = data.isnull().sum()
print("Missing values:\n", missing_values)

data['SO2 AQI'] = data.groupby('City')['SO2 AQI'].transform(lambda x: x.fillna(x.median()))
data['CO AQI'] = data.groupby('City')['CO AQI'].transform(lambda x: x.fillna(x.median()))

data['Date Local'] = pd.to_datetime(data['Date Local'], format='%Y-%m-%d')

outliers_columns = data[['NO2 AQI', 'O3 AQI', 'SO2 AQI','CO AQI']]

def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)  # First quartile (25%)
    Q3 = data[column].quantile(0.75)  # Third quartile (75%)
    IQR = Q3 - Q1  # Interquartile range

    # Define lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    print(f"Outliers in {column}:\n", outliers[column])

    # Optionally, return a DataFrame without outliers
    df_no_outliers = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    return df_no_outliers

# Apply the function to pollutant columns
outliers_NO2_AQI = detect_outliers_iqr(outliers_columns, 'NO2 AQI')
outliers_O3_AQI = detect_outliers_iqr(outliers_columns, 'O3 AQI')
outliers_SO2_AQI = detect_outliers_iqr(outliers_columns, 'SO2 AQI')
outliers_CO_AQI = detect_outliers_iqr(outliers_columns, 'CO AQI')

def replace_outliers_with_median(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    median_value = data[column].median()
    data.loc[:, column] = data[column].apply(lambda x: median_value if (x < lower_bound or x > upper_bound) else x)


# Apply replacement to pollutant columns
replace_outliers_with_median(outliers_columns, 'NO2 AQI')
replace_outliers_with_median(outliers_columns, 'O3 AQI')
replace_outliers_with_median(outliers_columns, 'SO2 AQI')
replace_outliers_with_median(outliers_columns, 'CO AQI')

# Dataset Overview with colored headline
st.markdown("<h3 style='color: #FFD700;'>Dataset Overview</h3>", unsafe_allow_html=True)
st.write(data.head().style.set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#1E90FF'), ('color', 'white'), ('font-size', '14px')]},
    {'selector': 'tbody td', 'props': [('background-color', '#F0F8FF'), ('color', 'black'), ('font-size', '12px')]}
]))

# Sidebar filters with custom colors
st.sidebar.markdown("<h4 style='color: #FFD700;'>Filters</h4>", unsafe_allow_html=True)

# Pollutant selection
st.sidebar.markdown("<h4 style='color: #1E90FF;'>Choose a Pollutant</h4>", unsafe_allow_html=True)
pollutant = st.sidebar.selectbox("Select Pollutant", ['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean'])

# Date range filter with default date handling
st.sidebar.markdown("<h4 style='color: #1E90FF;'>Date Range</h4>", unsafe_allow_html=True)
start_date = st.sidebar.date_input("Start Date", data['Date Local'].min().to_pydatetime().date())
end_date = st.sidebar.date_input("End Date", data['Date Local'].max().to_pydatetime().date())

# Filter data based on date range
data_filtered = data[(data['Date Local'] >= pd.to_datetime(start_date)) & (data['Date Local'] <= pd.to_datetime(end_date))]

# Temporal Trend Visualization
if pollutant in data_filtered.columns:
    st.markdown(f"<h3 style='color: #FFD700;'>Temporal Trend of {pollutant}</h3>", unsafe_allow_html=True)
    data_grouped = data_filtered.groupby("Date Local")[pollutant].mean().resample('ME').mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    data_grouped.plot(ax=ax, color='tab:blue', lw=2)
    ax.set_title(f"{pollutant} Levels Over Time", fontsize=16, color='darkorange')
    ax.set_xlabel("Date", fontsize=12, color='darkgreen')
    ax.set_ylabel("Pollutant Level", fontsize=12, color='darkgreen')
    ax.grid(True)
    ax.set_xticks(data_grouped.index[::max(len(data_grouped) // 6, 1)])
    ax.set_xticklabels(data_grouped.index.strftime('%Y-%m-%d')[::max(len(data_grouped) // 6, 1)], rotation=45)
    st.pyplot(fig)

# State filter
st.sidebar.markdown("<h4 style='color: #1E90FF;'>Select State</h4>", unsafe_allow_html=True)
state = st.sidebar.selectbox("Select State", data_filtered['State'].unique())

# Filter data by state
state_data = data_filtered[data_filtered['State'] == state]

if not state_data.empty:
    # Only show cities present in the filtered `state_data` DataFrame
    city_options = state_data['City'].dropna().unique()
    st.sidebar.markdown("<h4 style='color: #1E90FF;'>Select City</h4>", unsafe_allow_html=True)
    city = st.sidebar.selectbox("Select City", city_options)
else:
    st.sidebar.warning("No data available for the selected state. Please choose another state.")

# Choropleth map by county for the selected state
# st.markdown(f"<h3 style='color: #FF6347;'>Pollutant Levels in {state}</h3>", unsafe_allow_html=True)
# fig = px.choropleth(state_data,
#                     locations="County",
#                     locationmode="USA-states",
#                     color=pollutant,
#                     scope="usa",
#                     title=f"<span style='color: #FFD700;'>{pollutant} Levels by County in {state}</span>",
#                     template="plotly_dark")
# st.plotly_chart(fig)

# Plot most populated states
st.markdown(f"<h3 style='color: #FF6347;'>Top Pollutant Level states</h3>", unsafe_allow_html=True)
topstatesdata = data[["State", 'NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].groupby("State").median()
toptenstatesdata = topstatesdata.sort_values(by=['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI'], ascending=False)[:10]
fig, ax = plt.subplots()
toptenstatesdata.plot(kind="bar", ax=ax)
st.pyplot(fig)

# Filter data for the selected city
city_data = state_data[state_data['City'] == city]

# Groupby data using date local
city_data = city_data[['Date Local', 'NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI', 'NO2 1st Max Value', 'O3 1st Max Value', 'SO2 1st Max Value', 'CO 1st Max Value']].groupby("Date Local").median()

# AQI and Peak Values bar chart for selected city
st.subheader(f"AQI Levels and Peak Values for {city}")
fig, axs = plt.subplots(1, 2, figsize=(15, 5))

# AQI Line Chart
city_data[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].plot(kind="line", ax=axs[0])
axs[0].set_title("AQI Levels by Pollutant")
axs[0].set_xlabel("Date")
axs[0].set_ylabel("AQI Level")

# Max Value Line Chart
city_data[['NO2 1st Max Value', 'O3 1st Max Value', 'SO2 1st Max Value', 'CO 1st Max Value']].plot(kind="line", ax=axs[1])
axs[1].set_title("Peak Pollutant Levels")
axs[1].set_xlabel("Date")
axs[1].set_ylabel("Pollutant Level")
st.pyplot(fig)
