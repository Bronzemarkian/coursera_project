# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

sites_df = spacex_df[['Launch Site']]
sites_df = sites_df.groupby(['Launch Site'], as_index=False).first()
sites_list = sites_df['Launch Site'].tolist()


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options = [{'label': 'All Sites', 'value': 'All'}] + [{'label': f'{site}', 'value': f'{site}'} for i, site in enumerate(sites_list)],
                                             # so add the all as default, but also iterate over a full list of options. Then add the list of libraries with a +
                                             value='All', #default value selected
                                             placeholder="place holder here",
                                             searchable=True
                                                 ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                #marks={0: '0', 100: '100'},
                                                value = [min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')) # this input is the input to the function it decorates
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'All':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Successfull Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index() # count instances of successes and failures
        success_counts.columns = ['class', 'count']  # rename for clarity
        
        fig = px.pie(success_counts, values='count', 
        names='class', 
        title=f'Total Success Launches for {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site, payload_range):

    if entered_site == 'All':
        fig = px.scatter(spacex_df,
                    x='Payload Mass (kg)',
                    y = 'class',
                    color = 'Booster Version',
                    title = 'Correlation between Payload and Success for all Sites',
                    range_x = payload_range
            )
        return fig
    
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df,
                    x='Payload Mass (kg)',
                    y = 'class',
                    color = 'Booster Version',
                    title = f'Correlation between Payload and Success for {entered_site}',
                    range_x = payload_range
            )
        return fig


""" Answer to the stated questions:

1. VAFB has the largest successfull launch.
2. KSC has the highest success rate of 76.9%
3. The plot doesnt display that, but seems highest about 2k-4k, and 4.5k-5.5k.
4. Again the plot doesnt display that, but seems to be 4k-4.5k.
5. Hard to see which has highest % of the boosters, what?

"""


# Run the app
if __name__ == '__main__':
    app.run()
