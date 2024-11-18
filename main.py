import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  

# st.markdown("<h1 style='text-align: center;'><img src='image.png' width='150'></h1>", unsafe_allow_html=True)
st.image('image.png',width = 200)
# Title with custom color
st.markdown("<h1 style='color: #1E90FF;'>Air Quality Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #32CD32;'>Explore Air Quality Data by Pollutants, Regions, and Time Periods.</h3>", unsafe_allow_html=True)
@st.cache
def load_data():
    # Load and preprocess your dataset here
    data = pd.read_csv("sampled_dataset.csv")
    return data
data = load_data()



# Dataset Overview with colored headline
st.markdown("<h3 style='color: #FFD700;'>Dataset Overview</h3>", unsafe_allow_html=True)
st.write(data.head().style.set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#1E90FF'), ('color', 'white'), ('font-size', '14px')]},
    {'selector': 'tbody td', 'props': [('background-color', '#F0F8FF'), ('color', 'black'), ('font-size', '12px')]}
]))
# Drop irrelevant columns
if 'Unnamed: 0' in data.columns:
    data = data.drop(columns=['Unnamed: 0'])

missing_values = data.isnull().sum()

data['SO2 AQI'] = data.groupby('City')['SO2 AQI'].transform(lambda x: x.fillna(x.median()))
data['CO AQI'] = data.groupby('City')['CO AQI'].transform(lambda x: x.fillna(x.median()))


missing_values = data.isnull().sum()

data['Date Local'] = pd.to_datetime(data['Date Local'], errors='coerce')
data = data.dropna(subset=['Date Local'])



# Assuming 'data' is your DataFrame
outliers_columns = data[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']]

# Function to detect outliers using IQR method
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)  # First quartile (25%)
    Q3 = data[column].quantile(0.75)  # Third quartile (75%)
    IQR = Q3 - Q1  # Interquartile range

    # Define lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    
    # Create a DataFrame without outliers
    df_no_outliers = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    return outliers, df_no_outliers

# Function to replace outliers with median
def replace_outliers_with_median(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    median_value = data[column].median()
    data[column] = data[column].apply(lambda x: median_value if (x < lower_bound or x > upper_bound) else x)

# Sample dataset (replace with your actual dataset)
# data = pd.read_csv('your_dataset.csv')

# Assume you have a dataframe called outliers_columns with these columns
outliers_columns = data[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']]

# Detect outliers before replacement for each column and store them separately
outliers_NO2_AQI, data_NO2_AQI = detect_outliers_iqr(outliers_columns, 'NO2 AQI')
outliers_O3_AQI, data_O3_AQI = detect_outliers_iqr(outliers_columns, 'O3 AQI')
outliers_SO2_AQI, data_SO2_AQI = detect_outliers_iqr(outliers_columns, 'SO2 AQI')
outliers_CO_AQI, data_CO_AQI = detect_outliers_iqr(outliers_columns, 'CO AQI')

# Combine all outliers in one table before replacement
outliers_combined_before = pd.concat([outliers_NO2_AQI[['NO2 AQI']],
                                      outliers_O3_AQI[['O3 AQI']],
                                      outliers_SO2_AQI[['SO2 AQI']],
                                      outliers_CO_AQI[['CO AQI']]], axis=1)

# Replace outliers with median for each column
replace_outliers_with_median(outliers_columns, 'NO2 AQI')
replace_outliers_with_median(outliers_columns, 'O3 AQI')
replace_outliers_with_median(outliers_columns, 'SO2 AQI')
replace_outliers_with_median(outliers_columns, 'CO AQI')

# Combine all data after replacement into one table
data_combined_after = pd.concat([outliers_columns[['NO2 AQI']],
                                 outliers_columns[['O3 AQI']],
                                 outliers_columns[['SO2 AQI']],
                                 outliers_columns[['CO AQI']]], axis=1)

# Display Outliers Before Replacement in Streamlit


# Display Outliers After Replacement in Streamlit

data_without_date = data.drop(columns=['Date Local'])

# Show summary statistics for all columns except 'Date Local'

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

#Pollution Correlations

st.markdown("<h3 style='color: #FF6347;'>Pollutant Correlations</h3>", unsafe_allow_html=True)
correlation_data = data[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', ax=ax, linewidths=0.5)
ax.set_title("Correlation Heatmap", fontsize=16)
st.pyplot(fig)

#Seasonal Trends of pollutants by month
st.markdown("<h3 style='color: #1E90FF;'>Seasonal Trends of Pollutants</h3>", unsafe_allow_html=True)
data['Month'] = data['Date Local'].dt.month
seasonal_data = data.groupby('Month')[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].mean()
fig, ax = plt.subplots(figsize=(10, 6))
seasonal_data.plot(ax=ax, colormap='coolwarm', marker='o')
ax.set_title("Average Pollutant Levels by Month", fontsize=16)
ax.set_xlabel("Month")
ax.set_ylabel("Pollutant AQI")
st.pyplot(fig)

# Pollutant levels for selected state
st.markdown("<h3 style='color: #FF6347;'>Pollutant Levels for each state</h3>", unsafe_allow_html=True)
pollutant_options = ['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']

# Add a selectbox with a unique key
pollutant_map = st.selectbox("Select a pollutant to visualize:", pollutant_options, key="pollutant_map_selectbox")

state_pollutant_pivot = data.pivot_table(
    index="State",
    values=pollutant_map,
    aggfunc="mean"
).sort_values(by=pollutant_map, ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    state_pollutant_pivot,
    cmap="YlGnBu",
    annot=True,
    fmt=".1f",
    ax=ax
)
plt.title(f"Heatmap of {pollutant_map} Levels Across States")
st.pyplot(fig)

#Heat Map of selected pollutant levels
st.markdown("<h3 style='color: #FF6347;'>Heat Map for Pollutant levels</h3>", unsafe_allow_html=True)
state_pollutant_avg = data.groupby('State')[pollutant_map].mean().reset_index()

top_states = state_pollutant_avg.nlargest(10, pollutant_map)

fig_top_states = px.bar(
    top_states,
    x=pollutant_map,
    y='State',
    orientation='h',
    title=f"Top 10 States with Highest {pollutant_map} Levels",
    labels={pollutant_map: f'{pollutant_map} Level'},
    color=pollutant_map,
    color_continuous_scale='Inferno'
)
st.plotly_chart(fig_top_states)



# Create a bar chart for average levels by state
fig_bar = px.bar(
    state_pollutant_avg,
    x='State',
    y=pollutant_map,
    title=f"Average {pollutant_map} Levels by State",
    labels={'State': 'State', pollutant_map: f'{pollutant_map} Level'},
    color=pollutant_map,
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig_bar)

#Line chart for selected pollutant trends by state
st.markdown("<h3 style='color: #FF6347;'>Line Chart for Pollutant Trends by State</h3>", unsafe_allow_html=True)
# Filter for specific states (optional)
selected_states = st.multiselect("Select states to visualize:", data['State'].unique())

if selected_states:
    filtered_data = data[data['State'].isin(selected_states)]

    fig_line = px.line(
        filtered_data,
        x="Date Local",
        y=pollutant_map,
        color="State",
        title=f"Trends of {pollutant_map} Levels in Selected States",
        labels={"Date Local": "Date", pollutant_map: f"{pollutant_map} Level"}
    )
    st.plotly_chart(fig_line)
else:
    st.warning("Please select at least one state to visualize trends.")

# Footer section
st.markdown("---")  # Add a horizontal line to separate the footer
st.markdown(
    """
    <style>
        .footer {
            position: relative;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            padding: 10px 0;
            color: #6c757d;
            text-align: center;
            font-size: 14px;
            border-top: 1px solid #e9ecef;
        }
        .footer h4 {
            margin: 0;
            font-size: 16px;
            color: #343a40;
        }
        .footer p {
            margin: 5px 0 0;
        }
    </style>
    <div class="footer">
        <h4>Team Members</h4>
        <p>Ashish (Team Lead) | Priyanka | Gangavaram | Waswi</p>
    </div>
    """,
    unsafe_allow_html=True
)
