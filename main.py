# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Display an image in the dashboard
st.image('image.png', width=200)

# Title and subtitle with custom styles
st.markdown("<h1 style='color: #1E90FF;'>Air Quality Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #32CD32;'>Explore Air Quality Data by Pollutants, Regions, and Time Periods.</h3>", unsafe_allow_html=True)

# Function to load and cache the dataset for better performance
@st.cache
def load_data():
    data = pd.read_csv("pollution_us_2000_2016.csv")  # Replace with your dataset path
    return data

# Load the dataset
data = load_data()

# Display dataset overview with custom-styled header
st.markdown("<h3 style='color: #FFD700;'>Dataset Overview</h3>", unsafe_allow_html=True)
st.write(data.head().style.set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#1E90FF'), ('color', 'white'), ('font-size', '14px')]},
    {'selector': 'tbody td', 'props': [('background-color', '#F0F8FF'), ('color', 'black'), ('font-size', '12px')]}
]))

# Drop irrelevant column if exists
if 'Unnamed: 0' in data.columns:
    data = data.drop(columns=['Unnamed: 0'])
    st.write("Dropped 'Unnamed: 0' column as it was irrelevant.")

# Handle missing values by displaying their count
missing_values = data.isnull().sum()
st.write("Missing values count per column:")
st.write(missing_values)

# Impute missing values in 'SO2 AQI' and 'CO AQI' columns with city-wise medians
data['SO2 AQI'] = data.groupby('City')['SO2 AQI'].transform(lambda x: x.fillna(x.median()))
data['CO AQI'] = data.groupby('City')['CO AQI'].transform(lambda x: x.fillna(x.median()))
st.write("Imputing missing values in 'SO2 AQI' and 'CO AQI' with groupby city median values.")

# Check and display updated missing values count
missing_values = data.isnull().sum()
st.write("Missing values count per column after imputation:")
st.write(missing_values)

# Convert 'Date Local' to datetime and drop rows with invalid dates
data['Date Local'] = pd.to_datetime(data['Date Local'], errors='coerce')
data = data.dropna(subset=['Date Local'])

# Detect and handle outliers using the IQR method
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    df_no_outliers = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    return outliers, df_no_outliers

def replace_outliers_with_median(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    median_value = data[column].median()
    data[column] = data[column].apply(lambda x: median_value if (x < lower_bound or x > upper_bound) else x)

# Apply outlier detection and replacement to selected columns
outliers_columns = data[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']]
for col in outliers_columns.columns:
    replace_outliers_with_median(data, col)

# Display the summary statistics
data_without_date = data.drop(columns=['Date Local'])
st.markdown("<h3 style='color: #FFD700;'>Summary Statistics</h3>", unsafe_allow_html=True)
st.write(data_without_date.describe())

# Sidebar for pollutant selection
st.sidebar.markdown("<h4 style='color: #1E90FF;'>Choose a Pollutant</h4>", unsafe_allow_html=True)
pollutant = st.sidebar.selectbox("Select Pollutant", ['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean'])

# Sidebar for date range filtering
st.sidebar.markdown("<h4 style='color: #1E90FF;'>Date Range</h4>", unsafe_allow_html=True)
start_date = st.sidebar.date_input("Start Date", data['Date Local'].min().to_pydatetime().date())
end_date = st.sidebar.date_input("End Date", data['Date Local'].max().to_pydatetime().date())

# Filter data based on date range
data_filtered = data[(data['Date Local'] >= pd.to_datetime(start_date)) & (data['Date Local'] <= pd.to_datetime(end_date))]

# Visualize pollutant trends over time
if pollutant in data_filtered.columns:
    st.markdown(f"<h3 style='color: #FFD700;'>Temporal Trend of {pollutant}</h3>", unsafe_allow_html=True)
    data_grouped = data_filtered.groupby("Date Local")[pollutant].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    data_grouped.plot(ax=ax, color='tab:blue', lw=2)
    ax.set_title(f"{pollutant} Levels Over Time", fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Pollutant Level", fontsize=12)
    st.pyplot(fig)

# Display top pollutant levels by state
top_states_data = data[['State', 'NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].groupby("State").median()
top_ten_states = top_states_data.sort_values(by='NO2 AQI', ascending=False).head(10)
fig, ax = plt.subplots()
top_ten_states.plot(kind='bar', ax=ax)
st.pyplot(fig)

# Correlation heatmap for pollutants
st.markdown("<h3 style='color: #FF6347;'>Pollutant Correlations</h3>", unsafe_allow_html=True)
correlation_data = data[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', ax=ax, linewidths=0.5)
st.pyplot(fig)

# Seasonal trends of pollutants
st.markdown("<h3 style='color: #1E90FF;'>Seasonal Trends of Pollutants</h3>", unsafe_allow_html=True)
data['Month'] = data['Date Local'].dt.month
seasonal_data = data.groupby('Month')[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].mean()
fig, ax = plt.subplots(figsize=(10, 6))
seasonal_data.plot(ax=ax, colormap='coolwarm', marker='o')
ax.set_title("Average Pollutant Levels by Month", fontsize=16)
ax.set_xlabel("Month")
ax.set_ylabel("Pollutant AQI")
st.pyplot(fig)
