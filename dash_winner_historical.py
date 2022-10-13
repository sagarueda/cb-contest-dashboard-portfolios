# Import libraries
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import pandas as pd

from load_data import getContestData, load_json, load_historical_csv,load_historical_csv2, getContestData2
from load_data import historical_ranking_slicer_by_id_contest,points_calculator
from load_data import total_best_enrolled_in_contest,re_ranking_contest,add_time_intops,add_max_time_intops, portfolios_points


# Load the dataset
#avocado = pd.read_csv('avocado-updated-2020.csv')
filepath3 = 'data/historical_contest.csv'
historical_contest = load_historical_csv2(filepath3)
add_time_intops(historical_contest)
add_max_time_intops(historical_contest)
historical_contest['points'] = points_calculator(historical_contest)
top_entry = 10
wide_df = re_ranking_contest(historical_contest, top_entry)

# Create the Dash app
app = Dash()

# Set up the app layout
geo_dropdown = dcc.Dropdown(options=wide_df['id_contest'].unique(),
                            value=12)

app.layout = html.Div(children=[
    html.H1(children='Historical Winner - Dashboard'),
    geo_dropdown,
    dcc.Graph(id='price-graph')
])


# Set up the callback function
@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id=geo_dropdown, component_property='value')
)
# plotting_topN(wide_df,width=1200,height=900, ranking='points',title="Top 10 by contest")
def update_graph(selected_geography):
    filtered = wide_df[wide_df['id_contest'] == selected_geography]
    filtered = filtered.sort_values('points', ascending = True)
    line_fig = px.bar(filtered,
                       x='points', y='username',
                       #color='points',
                       title=f'Winners of contest {selected_geography}')
    line_fig.update_xaxes(range=[100, 122]) 
    return line_fig


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)