import pandas as pd
import plotly.express as px

# Load data from MapReduce function: avg_fare_by_passengers_count.py
fare_data = {
    "Passenger_Count": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Average_Fare": [11.216405, 11.838421, 11.540597, 11.766069, 11.208401, 12.126156, 31.788667, 29.981111, 36.993043]
}
fare_df = pd.DataFrame(fare_data)

# Creating a bar plot to visualize average taxi fare by passenger count
fig = px.bar(fare_df, x='Passenger_Count', y='Average_Fare', title='Average Taxi Fare by Passenger Count')
fig.show()
fig.write_image("average_fare_by_passenger_count.png")  # Save the bar plot as an image

# Load data from MapReduce function: total_fare_per_year.py
total_fare_per_year_data = {
    "Year": ["2013", "2010", "2014", "2011", "2012", "2015", "2009"],
    "Total_Fare": [109084889.27, 84908545.81, 106627238.25, 92350274.46, 99682239.46, 50227425.29, 85905561.20]
}
total_fare_per_year_df = pd.DataFrame(total_fare_per_year_data).sort_values(by="Year")

# Creating a bar plot to visualize total taxi fare per year
fig_bar = px.bar(total_fare_per_year_df, x='Year', y='Total_Fare', title='Total Taxi Fare per Year')
fig_bar.show()
fig_bar.write_image("total_fare_per_year.png")  # Save the bar plot as an image

# Creating a pie plot to show the percentage of total taxi fare per year
fig_pie = px.pie(total_fare_per_year_df, names='Year', values='Total_Fare', title='Percentage of Total Taxi Fare per Year')
fig_pie.update_layout(autosize=False, width=800, height=600)
fig_pie.show()
fig_pie.write_image("percentage_total_fare_per_year.png")  # Save the pie plot as an image

# Load the CSV data containing average fare by location
df = pd.read_csv('avg_fare_by_location.csv')

# Filter out coordinates outside New York City's typical geographical bounds
df = df[
    (df['Longitude'].between(-74.2557, -73.7004)) &
    (df['Latitude'].between(40.496, 40.915))
]

# Creating a scatter geo plot to visualize the average fare by location within New York City
fig = px.scatter_geo(df, lon='Longitude', lat='Latitude', color='Avg_Fare',
                     labels={"Avg_Fare": "Average Fare"},
                     title="Average Fare by Location in New York City",
                     color_continuous_scale=px.colors.sequential.Viridis,
                     center={"lat": 40.7128, "lon": -74.0060})  # Center on New York City
fig.show()
fig.write_image("nyc_avg_fare_by_location.png")  # Save the scatter plot as an image

