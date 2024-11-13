import pandas as pd
df = pd.read_csv("pollution_us_2000_2016.csv")


# Outliers removal

outlier_columns = [
    'NO2 AQI', 'NO2 Mean', 'O3 AQI', 'O3 Mean',
    'SO2 AQI', 'SO2 Mean', 'CO AQI', 'CO Mean',
    'NO2 1st Max Value', 'O3 1st Max Value', 
    'SO2 1st Max Value', 'CO 1st Max Value'
]

# Function to detect outliers using IQR method
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers

# Function to handle outliers by replacing them with the column median
def handle_outliers_with_median(df, column):
    outliers = detect_outliers_iqr(df, column)
    median_value = df[column].median()  # Calculate median of the column
    df.loc[outliers.index, column] = median_value  # Replace outliers with median
    return df

detect_outliers_iqr(df, outlier_columns[0])[outlier_columns[0]]

# Apply the functions to each relevant column
for col in outlier_columns:
    print(f"Checking for outliers in '{col}' using IQR method.")
    
    iqr_outliers = detect_outliers_iqr(df, col)
    print(f"Outliers detected in '{col}' (IQR):\n", iqr_outliers)
   
    df = handle_outliers_with_median(df, col)

# check if outlier values are modified
df[outlier_columns[0]][10:15]

