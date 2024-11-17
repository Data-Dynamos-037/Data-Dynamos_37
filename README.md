# Air Quality Analysis Dashboard 🌍

This project is a **Streamlit-based dashboard** for analyzing air quality data in the U.S. between 2000 and 2016. The dashboard provides insights into pollutant levels, missing values, outliers, temporal trends, and interactive visualizations.

---

## Features ✨

1. **Dataset Overview**:
   - Displays the dataset's head and missing values.
   - Handles missing values with median imputation grouped by city.

2. **Outlier Detection and Handling**:
   - Detects outliers in pollutant AQI columns using the IQR method.
   - Replaces outliers with the median values.

3. **Interactive Visualizations**:
   - Temporal trends of pollutants over time.
   - Seasonal pollutant trends.
   - AQI and peak values by city and state.
   - Choropleth maps of pollutant levels across U.S. states.

4. **User Inputs**:
   - Select pollutants, states, cities, and date ranges for focused analysis.
   - Dynamic filtering and visual updates based on user selections.

5. **Correlation Heatmap**:
   - Visualizes correlations between different pollutants.

---

## Tech Stack 🛠️

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: 
  - Matplotlib
  - Seaborn
  - Plotly Express
- **Data**: U.S. Air Quality dataset (`pollution_us_2000_2016.csv`)

---

## Installation 🔧

### Prerequisites

- Python 3.8 or higher
- Virtual Environment (optional but recommended)
- Required Python Libraries:
  - `streamlit`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `plotly`

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Data-Dynamos-037/Data-Dynamos_37/blob/main/main.py

2. Install dependencies 
    pip install -r requirements.txt
3. Run app
    streamlit run main.py

File structure
 ├── app.py                 # Main Streamlit app
├── pollution_us_2000_2016.csv # Dataset
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── images/
    └── image.png          # Logo for dashboard (optional)

# How to use
 Launch the app using streamlit run app.py.
## Explore the Dashboard:
Use the sidebar to select pollutants, date ranges, states, and cities.
View missing values, outliers, and their replacements.
Analyze temporal trends, correlations, and seasonal patterns.
## Visualize Data:
Interactive maps and charts for better insights.

## Sample Dataset
The dataset pollution_us_2000_2016.csv contains the following columns:
Location Information: State, County, City, Address
Pollutant Metrics: NO2 AQI, O3 AQI, SO2 AQI, CO AQI
Date Information: Date Local

# Known Issues
Ensure the dataset pollution_us_2000_2016.csv is present in the root directory.
The app is optimized for desktops; smaller screens may impact layou