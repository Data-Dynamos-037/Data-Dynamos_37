import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
df = pd.read_csv("pollution_us_2000_2016.csv")

df.drop(columns=['Unnamed: 0'], inplace=True)

missing_values = df.isnull().sum()
print("Missing values:\n", missing_values)

df['SO2 AQI'] = df.groupby('City')['SO2 AQI'].transform(lambda x: x.fillna(x.median()))
df['CO AQI'] = df.groupby('City')['CO AQI'].transform(lambda x: x.fillna(x.median()))

df['Date Local'] = pd.to_datetime(df['Date Local'], format='%Y-%m-%d')

outliers_columns = df[['NO2 AQI', 'O3 AQI', 'SO2 AQI','CO AQI']]

def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)  # First quartile (25%)
    Q3 = df[column].quantile(0.75)  # Third quartile (75%)
    IQR = Q3 - Q1  # Interquartile range

    # Define lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    print(f"Outliers in {column}:\n", outliers[column])

    # Optionally, return a DataFrame without outliers
    df_no_outliers = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df_no_outliers

# Apply the function to pollutant columns
outliers_NO2_AQI = detect_outliers_iqr(df, 'NO2 AQI')
outliers_O3_AQI = detect_outliers_iqr(df, 'O3 AQI')
outliers_SO2_AQI = detect_outliers_iqr(df, 'SO2 AQI')
outliers_CO_AQI = detect_outliers_iqr(df, 'CO AQI')

def replace_outliers_with_median(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    median_value = df[column].median()
    df[column] = df[column].apply(lambda x: median_value if (x < lower_bound or x > upper_bound) else x)

# Apply replacement to pollutant columns
replace_outliers_with_median(df, 'NO2 AQI')
replace_outliers_with_median(df, 'O3 AQI')
replace_outliers_with_median(df, 'SO2 AQI')
replace_outliers_with_median(df, 'CO AQI')

pollutants = ["NO2 AQI", "O3 AQI", "SO2 AQI", "CO AQI"]

city = st.selectbox("Select City", df['City'].unique())
pollutant = st.selectbox("Select Pollutant", pollutants)

filtered_data = df[df['City'] == city]
# Create a selectbox to choose the pollutant

# Check if 'Date Local' and selected 'pollutant' exist in filtered_data
st.write("Selected pollutant:", pollutant)

# Plot only if the selected pollutant exists in the DataFrame
if 'Date Local' in filtered_data.columns and pollutant in filtered_data.columns:
    fig, ax = plt.subplots()
    filtered_data.plot(x='Date Local', y=pollutant, ax=ax)
    st.pyplot(fig)
    ax.grid(True)
else:
    st.error(f"Columns 'Date Local' or '{pollutant}' not found in data.")