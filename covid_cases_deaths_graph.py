import pandas as pd
import plotly.graph_objects as go

# Load the data into a Pandas DataFrame
df = pd.read_csv('covid_data.csv', usecols=['submission_date', 'tot_cases', 'tot_death'])

# Convert the submission_date column to a datetime object and extract the year and month
df['submission_date'] = pd.to_datetime(df['submission_date'])
df['year-month'] = df['submission_date'].dt.strftime('%Y-%m')

# Group the data by year-month and sum the total cases and deaths
df = df.groupby('year-month').agg({'tot_cases': 'sum', 'tot_death': 'sum'}).reset_index()

# Create the line chart using Plotly Express
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['year-month'], y=df['tot_cases'], name='Total Cases'))
fig.add_trace(go.Scatter(x=df['year-month'], y=df['tot_death'], name='Total Deaths', yaxis='y2'))

# Set the y-axis title
fig.update_layout(title='Total COVID-19 Cases and Deaths in the US',
                yaxis=dict(title='Total Cases'),
                yaxis2=dict(title='Total Deaths', overlaying='y', side='right'))

# Show the line chart
fig.show()
