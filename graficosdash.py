from select import select
import numpy as np
import pandas as pd
from cb_loadData import getContestData, load_json
from cb_processingData import adding_name, points_per_slug_calculator, best_users_from_contestN,best_topN_project
from cb_DataBase_contests_queries import getContest_id, get_projects_name,contestsHistoricalRankingData,users_contests_projects
from cb_DataBase_connection import open_connection, close_connection
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go

#============================================================================================================
# ======================== Plotly Graphs
#============================================================================================================


def get_bar_chart(better_N_projects):
    layout = go.Layout(
    #Best projects layout
    margin=go.layout.Margin(
        l=40,  # left margin
        r=40,  # right margin
        b=10,  # bottom margin
        t=35  # top margin
    ))

    title_axis_x = 'Puntos'
    title_axis_y = 'Proyectos'
    color_bar_plot = 'rgb(23,162,184)'
    axis_x = "average_points"#'puntos_totales'
    axis_y = "name"
    barChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Bar(x=better_N_projects[axis_x],
                                                                          y=better_N_projects[axis_y],
                                                                          marker=dict(color=color_bar_plot),
                                                                          orientation = 'h')).update_layout(
        title='Proyectos con mejor puntuación', plot_bgcolor='lavender',
        xaxis=dict(title=title_axis_x,),
        yaxis=dict(title=title_axis_y,
                )),
        style={'width': '50%', 'height': '50vh', 'display': 'inline-block'},
        id='Contest_graph'
        )
    return barChart



def get_table_rendimiento(better_N_projects):
    layout = go.Layout(
    #Best projects layout
    margin=go.layout.Margin(
            l=5,  # left margin
            r=5,  # right margin
            b=10,  # bottom margin
            t=35  # top margin

    ))
    color_bar_plot = 'rgb(23,162,184)'
    table = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Table(
                                            header=dict(values=list(better_N_projects.columns),
                                            fill_color=color_bar_plot,
                                            align='left'),
                                            cells=dict(values=[better_N_projects.name, better_N_projects.performance],
                                            fill_color='lavender',
                                            align='right')
                                            )),
        style={'width': '20%', 'height': '50vh', 'display': 'inline-block'},
        id='table_of_projects',
        )
    return table
         

def get_table_retorno():
    
    layout = go.Layout(
    # retornal table layout
    margin=go.layout.Margin(
                l=5,  # left margin
                r=40,  # right margin
                b=10,  # bottom margin
                t=35  # top margin
    ))

    top_rendimiento = "Rendimiento promedio top: "+str(10)
    retorno_hip = "Retorno de un ingreso de $1000"
    
    table = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Table(

        header = dict(values=[top_rendimiento, retorno_hip],
        fill_color='rgb(23,162,184)',
        align='right'),
        cells=dict(values=["",""],
        fill_color='lavender',
        align='right'),)),
        style={'width': '30%', 'height': '50vh', 'display': 'inline-block'},
        id='table_of_projects2',
        )
    return table 


  
