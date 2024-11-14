# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Load the dataset
df = pd.read_csv(r'D:\Construct Week Project\Data-Dynamos_37\pollution_us_2000_2016.csv')

# Streamlit app setup
st.title("US Air Quality Analysis (2000-2016)")
st.write("This dashboard provides insights into air quality across regions, helping policymakers and agencies understand pollution levels by location and season.")

# Step 1: Initial Overview by Region
st.header("1. Initial Overview by Region")

# Mean pollutant levels by State and County
state_avg_pollution = df.groupby('State')[['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean']].mean()
county_avg_pollution = df.groupby(['State', 'County'])[['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean']].mean()
country_avg_pollution = df[['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean']].mean().to_frame().T

# Display Top 5 counties and states for each pollutant
st.subheader("Top Polluted Counties")
for pollutant, df_p in {
    "NO2 Mean": county_avg_pollution[['NO2 Mean']].sort_values(by='NO2 Mean', ascending=False).head(5),
    "O3 Mean": county_avg_pollution[['O3 Mean']].sort_values(by='O3 Mean', ascending=False).head(5),
    "SO2 Mean": county_avg_pollution[['SO2 Mean']].sort_values(by='SO2 Mean', ascending=False).head(5),
    "CO Mean": county_avg_pollution[['CO Mean']].sort_values(by='CO Mean', ascending=False).head(5),
}.items():
    st.write(f"Top 5 counties with highest average {pollutant} levels:", df_p)

# Country-level averages
st.write("Country-level average pollutant levels:", country_avg_pollution)

# Step 2: Heatmap of Pollutant Levels by State
st.header("2. Heatmap of Pollutant Levels by State")
st.subheader("NO2 Levels Heatmap")

fig_no2 = px.choropleth(
    state_avg_pollution.reset_index(),
    locations='State',
    locationmode="USA-states",
    color='NO2 Mean',
    color_continuous_scale="Viridis",
    scope="usa",
    title="Average NO2 Levels by State"
)
st.plotly_chart(fig_no2)

# Step 3: Top Polluted Counties by Pollutant
st.header("3. Top Polluted Counties by Pollutant")
st.write("Identifying counties with the highest pollution levels can pinpoint areas most affected by industrialization and urban traffic.")

# Display Top 10 Counties for each pollutant
for pollutant, top_counties in {
    "NO2 Mean": county_avg_pollution.sort_values(by='NO2 Mean', ascending=False).head(10),
    "O3 Mean": county_avg_pollution.sort_values(by='O3 Mean', ascending=False).head(10),
    "SO2 Mean": county_avg_pollution.sort_values(by='SO2 Mean', ascending=False).head(10),
    "CO Mean": county_avg_pollution.sort_values(by='CO Mean', ascending=False).head(10)
}.items():
    st.write(f"Top 10 counties with highest average {pollutant} levels:", top_counties)

# Step 4: Comparative Box Plots by Region
st.header("4. Comparative Box Plots by Region")
st.write("Distribution of NO2 levels by state")
plt.figure(figsize=(12, 6))
sns.boxplot(x='State', y='NO2 Mean', data=df)
plt.title("NO2 Levels Distribution by State")
plt.xticks(rotation=90)
st.pyplot(plt)

# Step 5: Correlation of Pollutants within Regions
st.header("5. Correlation of Pollutants within Regions")
st.write("Correlation matrix of pollutants at the state level")
st.write(state_avg_pollution.corr())

# Step 6: Seasonal Analysis by Region
st.header("6. Seasonal Analysis by Region")
st.write("Analyzing seasonal variation of pollution levels by state")

# Define seasons
df['Date Local'] = pd.to_datetime(df['Date Local'])
df['Season'] = df['Date Local'].dt.month.apply(lambda x: 
    "Winter" if x in [12, 1, 2] else 
    "Spring" if x in [3, 4, 5] else 
    "Summer" if x in [6, 7, 8] else "Fall"
)
seasonal_state_avg = df.groupby(['State', 'Season'])[['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean']].mean()
st.write(seasonal_state_avg)

# Step 7: Detecting High-Pollution Days for Each Region
st.header("7. Detecting High-Pollution Days for Each Region")
daily_max_pollutants = df.groupby(['Date Local', 'State'])[['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean']].max()
high_pollution_days = daily_max_pollutants[daily_max_pollutants > daily_max_pollutants.quantile(0.95)]
st.write("High pollution days (95th percentile):", high_pollution_days)

