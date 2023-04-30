import pandas as pd
import plotly.express as px

# Load the data into a Pandas DataFrame
df = pd.read_csv('covid_data.csv', usecols=['submission_date', 'state', 'tot_death'])

# Convert the submission_date column to a datetime object and extract the year and month
df['submission_date'] = pd.to_datetime(df['submission_date'])
df['year-month'] = df['submission_date'].dt.strftime('%Y-%m')

# Filter the data to only include the first day of each month
df = df.loc[df['submission_date'].dt.day == 1]

# Group the data by state and year-month and sum the total deaths
df = df.groupby(['state', 'year-month']).agg({'tot_death': 'sum'}).reset_index()

# Create the map using Plotly Express
fig = px.choropleth(df, locations='state', locationmode='USA-states', color='tot_death', color_continuous_scale='Reds', scope='usa', animation_frame='year-month')

# Show the map
fig.show()
