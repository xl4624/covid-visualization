import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load the data into a Pandas DataFrame
df = pd.read_csv('covid_data.csv', usecols=[
    'submission_date', 'state', 'tot_cases', 'tot_death'])

# Convert the submission_date column to a datetime object and extract the year and month
df['submission_date'] = pd.to_datetime(df['submission_date'])
df['year_month'] = df['submission_date'].dt.strftime('%Y_%m')

# Filter the data to only include the first day of each month
df = df.loc[df['submission_date'].dt.day == 1]

# Group the data by state and year_month and sum the total cases
df = df.groupby(['state', 'year_month']).agg(
    {'tot_cases': 'sum', 'tot_death': 'sum'}).reset_index()


# Create the map using Plotly Express
fig = px.choropleth(df, locations='state', locationmode='USA-states',
                    color='tot_cases', scope='usa', animation_frame='year_month')

# Create a new trace for total deaths
deaths_trace = go.Choropleth(locations=df['state'], locationmode='USA-states',
                            z=df['tot_death'], colorscale='Reds', zmin=0, zmax=200000, colorbar_title='Total Deaths',
                            hovertemplate='State: %{location}<br>Total Deaths: %{z}', visible=False)

# Add the toggle button
fig.add_trace(deaths_trace)
fig.update_layout(updatemenus=[dict(
    type='buttons',
    showactive=True,
    buttons=[dict(
        label="Play",
        method="animate",
        args=[None, {"frame": {"duration": 1000, "redraw": False},
                    "fromcurrent": True, "transition": {"duration": 0}}]
    ),
        dict(
        label="Pause",
        method="animate",
        args=[[None], {"frame": {"duration": 0, "redraw": False},
                    "mode": "immediate", "transition": {"duration": 0}}]
    ),
        dict(
        label='Total Cases',
        method='update',
        args=[{'visible': [True, False]}, {'title': 'US COVID-19 Cases'}]
    ),
        dict(
        label='Total Deaths',
        method='update',
        args=[{'visible': [False, True]}, {'title': 'US COVID-19 Deaths'}]
    )
    ])],
    title='US COVID-19 Cases',
)

# Show the map
fig.show()
