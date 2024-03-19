# %%
# import libraries
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
#load in the data 
gapminder = pd.read_csv('gdp_pcap.csv')
#display the data
gapminder.head(20)

# %%

# Melt the DataFrame to fix the rows and columns issue - the columns should be country, year, and gdp per capita 
data_melted = pd.melt(gapminder, id_vars='country', var_name='year', value_name='gdp')
#create a function to deal with the k issue in gdp percapita - need to get rid of ks and instead multiply number by 1000
def k(value):
    if 'k' in str(value):
        return float(value.replace('k', '')) * 1000
    else:
        return float(value)

# %%
#rename data to match later code 
gapminder=data_melted
#apply the function I created to the data 
gapminder['gdp'] = gapminder['gdp'].apply(k)

# %%
#check to make sure ks are gone
gapminder.head(500000)
#check data types
gapminder.dtypes

# %%

#convert year column to numeric 
gapminder['year'] = pd.to_numeric(gapminder['year'], errors='coerce')
#make a variable to include the unique year values 
year= gapminder['year'].unique()
year

# %%

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet
app = Dash(__name__, external_stylesheets=stylesheets) # initialize the app
server = app.server

#creating the layout 
app.layout = html.Div([ #parent div
    html.Div(html.H1("Gapminder Dataset Dashboard")), #header at top of dashboard
    #paragraph underneath header 
    html.Div(children="The Gapminder data set pulls in information from other sources such as the World Bank to display estimates of GDP per capita for all countries from the years 1800 to 2100. The values displayed for the years past the current year are estimates of GDP created using historical data. This dashboard includes three main components, a dropdown, slider, and graph, that allow the user to interact with the data. The dropdown allows the user to select one or multiple countries, the slider allows the user to select one of the years present in the dataset, and the line graph is an interactive graph that displays GDP per capita over time for each country. The user can hover over this graph to see the exact values for each country as well."),  # paragraph
    html.Div([
        html.Div([
            html.Label('Dropdown'),
            #creating the country dropdown
            dcc.Dropdown(
                options=[{'label': country, 'value': country} for country in gapminder['country'].unique()], #allows for unique countries to be options to be selected
                id='country-dropdown',
                placeholder='select a country', #text that will be in the dropbox before a country is selected
                multi=True
            ),
        ], className="six columns" #specifies that the dropdown should take up half the width of the page (there are 12 total columns)
        ),
        html.Div([
            #creating the year range slider
            dcc.RangeSlider(
                id='year-range-slider',
                min=gapminder['year'].min(), #the min of the slider is the min of the year values
                max=gapminder['year'].max(), #the max of the slider is the max of the year values
                step=20, #the x axis will go by steps of 20 years to make it less clustered
                 marks={str(year): str(year) for year in range(gapminder['year'].min(), gapminder['year'].max() + 1, 20)}, #allows for unique years to be displayed on the slider - counting by 20 so the numbers fit 
                value=[gapminder['year'].min(), gapminder['year'].max()] #the default range is the whole range of the data
            ),
        ], className="six columns" #specifies that the year range slider should take up half the width of the page (there are 12 total columns)
        ),
    ], className="row"
    ),
    html.Div(
        dcc.Graph(id = 'Gapminder-Graph') #place for the line graph
    )
])
#creating the callback
@app.callback(
    Output('Gapminder-Graph', 'figure'), #output is the line graph
    [Input('country-dropdown', 'value'), #the inputs are the country and year values from user input in the dropdown and slider
     Input('year-range-slider', 'value')]
)
#function to update the graph with the inputted values
def update_figure(selected_countries, selected_year_range):
    #creating a new dataframe based on the selected country (s) and year range
    filtered_df = gapminder[(gapminder['country'].isin(selected_countries)) & 
                             (gapminder['year'] >= selected_year_range[0]) & #allows the years in the filtered df to take on values greater than or equal to 
                             #the minimum selected year and less than or equal to the maximum selected year 
                              (gapminder['year'] <= selected_year_range[1])
                            ]
    #code for the line graph 
    fig = px.line(filtered_df, 
                  x='year', 
                  y='gdp',
                  color='country',
                  markers=True,
                  symbol='country',
                  title='GDP Per Capita for Each Country from 1800-2100',
                  labels={
                      "year": "Year",
                      "gdp": "GDP Per Capita (in thousands)",
                      "country": "Country"
                  })
    #updating the layout to make the transitions smoothe 
    fig.update_layout(transition_duration=500)
    return fig

# run app
if __name__ == '__main__':
    app.run()


