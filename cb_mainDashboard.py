# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 22:43:44 2022

@author: SaGaRueda
"""
from select import select
import numpy as np
import pandas as pd
from cb_loadData import getContestData, load_json
from cb_processingData import adding_name, points_per_slug_calculator, best_users_from_contestN,best_topN_project
from cb_DataBase_contests_queries import getContest_id, get_projects_name,contestsHistoricalRankingData,users_contests_projects
from cb_DataBase_connection import open_connection, close_connection
from dash import Dash, html, dcc, Input, Output
from graficosdash import get_bar_chart, get_table_rendimiento, get_table_retorno
import plotly.express as px
import plotly.graph_objects as go


#============================================================================================================
# Setting the parameters
#============================================================================================================
width_grap = 980.0 #Width of the main plot
height_grap = 400.0 #Width of the main plot

max_top_user = 50 #Maximun option to choose the top user to be taken into account
max_top_project  =50 #Maximun option to choose the top projects to show    
title_main = 'Proyectos con más presencia basado en el histórico'
title_box_contest = 'Número de concurso a analizar'
title_box_users = 'Seleccione el top de usuarios históricos'
title_box_projects = 'Seleccione el número de proyectos'
title_axis_x = 'Puntos'
title_axis_y = 'Proyectos' 
data1 = "Proyectos"
data2 = "Rendimiento [%]"   
color_bar_plot = 'rgb(23,162,184)'
axis_x = "average_points"#'puntos_totales'
axis_y = "name"
x_label = "name"
y_label = "performance"
axis_x = "average_points"#'puntos_totales'
axis_y = "name"
color_bar_plot = 'rgb(23,162,184)'
#Initial configuration for the three parameters
#
top_user_entry = 10 
selected_contest = 13
top_projects = 10

  

def contestDashApp(connection):
    '''
    @param conection: conector object to my sql database, based on the configuration enviromental variables that were setted as  server,user, pasword and db.
    You must configurate the env vars as next:
    db_user = os.environ.get('MYSQL_USER')
    db_password = os.environ.get('MYSQL_PASSWORD')
    db_name = os.environ.get('MYSQL_DATABASE')
    db_host = os.environ.get('MYSQL_SERVER')
    db_port = os.environ.get('MYSQL_PORT')
    
    This program return a dashboard containing three optional parameters
    @selected_contest: It is the number of contest you want to analyze the performance of each project.
    @top_user_entry: It is the number of best user you want to take into account.
    @top_projects:  It is the number of projects you want to see.
    '''


    #============================================================================================================
    #Extracting all contest information from MYSQL DATABASE: "id, "name"
    #============================================================================================================
    all_contest = getContest_id(connection) #It is the id and names of all contest contest.
    all_contest.rename(columns={"id": "id_contest"}, inplace=True)
    last_contest_id = all_contest['id_contest'].iloc[0]
    #============================================================================================================    


    #============================================================================================================
    #Extracting all projects names with their id from MYSQL DATABASE: id_project, slug, name, ticker
    #============================================================================================================
    projects_names = get_projects_name(connection) # Extracting the stickers names from projects tables from de database, it is to print a pretty name of the projects
    #============================================================================================================  
    

    #============================================================================================================
    #Extracting all users_contest_projects information from MYSQL DATABASE:
    # id_user, id_contest, id_project, percentage, start_price,end_price 
    #============================================================================================================    
    users_contests_projects_all = users_contests_projects(connection)
    #============================================================================================================
    

    #============================================================================================================
    #Extracting all Best_top_users from the first contest to the especific contest that we want to analyze -1.
    #============================================================================================================    
    filtered = contestsHistoricalRankingData(connection,top_user_entry, int(last_contest_id-1))
    #============================================================================================================      


    #============================================================================================================
    #In case the last contest_id is coincident with the current contest, 
    # it means there is a contest ongoing we can analyze the performance of each contest using
    # a json file wich contain the current contest information.
    #============================================================================================================
    # Este son datos del concurso actual, no está en la DB de MYSQL, se extrae como un dictionary
    filepath = 'data/cb-contest-13-before-closing26_10_22.json'  
    current_contest_data = getContestData(load_json(filepath))
    #============================================================================================================

    
    #============================================================================================================
    #Executing top_projects function return the top projects and a table with performance
    #============================================================================================================
    better_N_projects,table_projects = top_projects_performance(filtered,users_contests_projects_all,current_contest_data,projects_names,selected_contest,last_contest_id,top_projects)
    #============================================================================================================



    #============================================================================================================
    #Executing DASH PLOTLY Application
    #============================================================================================================
    app = Dash() #starting dash application
    # Set up the app layout
    historical_contest_a = dcc.Dropdown(options=all_contest['id_contest'],
                            value=13)
    dcc1 = dcc.Input(id="top_entry_id",
                    placeholder='Value...',
                    type='number', min=1, max=max_top_user, step=1,
                    value=10
                    )
    dcc2 = dcc.Input(id="top_projects_id",
            placeholder='Value...',
            type='number', min=1, max=max_top_project, step=1,
            value=10
            )


    #The main title
    app.layout = html.Div(children=[
        html.H1(children= title_main),
        html.Label(title_box_contest),
        historical_contest_a,
        
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children=title_box_users, className="menu-title"),
                    dcc1,
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children=title_box_projects
                        , className="menu-title"),
                        dcc2
                    ],
                ),

            ],
            className="menu",
        ),
        
        get_bar_chart(better_N_projects),
        get_table_rendimiento(table_projects), 
        get_table_retorno(),      

    ])

    # Set up the callback function for the interaction with the users
    @app.callback(
        #This function get the inputs parameters from the users who is interacting with the dashboard 
        [Output('Contest_graph','figure'),
        Output('table_of_projects','figure'),
        Output('table_of_projects2','figure'),],
        [Input(component_id = historical_contest_a, component_property='value'),
        Input(dcc1,component_property='value'),
        Input(dcc2,component_property='value'),
        ],
    )

    def update_graph(selected_contest,top_user_entry,top_projects_id):
        #============================================================================================================
        #Updating the top projects based on the best contestant from the historical: 
        # using three parameters: top_user_entry, selected_contest, top_projects
        #============================================================================================================
        '''
        @param selected_contest: The number of contest
        @param top_user_entry: It is the top users or contestant to be taken in to account.
        @param top_projects_id: The number of projects to shows in the dashboard
        '''
   
        print("Executing: ok ",selected_contest,top_user_entry,top_projects_id) #Just a printing to debug       


        #============================================================================================================
        #Filtering the best historical users since first contest to selected contest-1
        # xecuting top_projects function that return the top projects and a table with performance
        #============================================================================================================
        filtered = contestsHistoricalRankingData(connection,top_user_entry, selected_contest-1) #query to mysql"


        #============================================================================================================
        #Executing top_projects function that return the top projects and a table with performance
        #============================================================================================================
        better_N_projects,table_projects = top_projects_performance(filtered,users_contests_projects_all,current_contest_data,projects_names,selected_contest,last_contest_id,top_projects_id)     


        #============================================================================================================
        # Bar plot of projects
        #============================================================================================================
        line_fig1 = px.bar(better_N_projects,
                        x=axis_x, y=axis_y,                      
                        orientation = 'h',)                       
        line_fig1.update_layout(        
        autosize=False,
        width=width_grap,
        height=height_grap,
        margin=dict(
            l=40,  # left margin
            r=40,  # right margin
            b=10,  # bottom margin
            t=35,  # top margin                
            ),
            plot_bgcolor='lavender',
            xaxis=dict(title=title_axis_x,),
            yaxis=dict(title=title_axis_y,)),                
        line_fig1.update_traces(marker_color=color_bar_plot)

        #============================================================================================================
        # Table of performances of the projects
        #============================================================================================================        
        line_fig2 = go.Figure(layout = go.Layout(
        # retornal table layout
                margin=go.layout.Margin(
                    l=5,  # left margin
                    r=5,  # right margin
                    b=10,  # bottom margin
                    t=35  # top margin
                ))).add_trace(go.Table(
                                            #header=dict(values=list(table_projects.columns),
                                            header = dict(values=[data1, data2],
                                            fill_color='rgb(23,162,184)',
                                            align='left'),
                                            cells=dict(values=[table_projects.name, table_projects.performance],
                                            fill_color='lavender',
                                            align='right'),))

        top_rendimiento = "Rendimiento del portfolio de "+str(top_projects_id)+" proyectos"
        retorno_hip = "Retorno para un ingreso de $1000"
        rendimiento_portfolio = table_projects['performance'].mean(skipna = True) 
        
        #============================================================================================================
        # Table of retornos of the projects
        #============================================================================================================
 
        line_fig3 = go.Figure(layout = go.Layout(
                                        # retornal table layout
                                        margin=go.layout.Margin(
                                            l=5,  # left margin
                                            r=40,  # right margin
                                            b=10,  # bottom margin
                                            t=35  # top margin
                                        ))).add_trace(go.Table(
                                            #header=dict(values=list(table_projects.columns),
                                            header = dict(values=[top_rendimiento, retorno_hip],
                                            fill_color='rgb(23,162,184)',
                                            align='right'),
                                            cells=dict(values=[str(round(rendimiento_portfolio,2))+" %", str(round(1000*(1+rendimiento_portfolio/100),2))+" $"],
                                            fill_color='lavender',
                                            align='right'),),
                                            )                          

        return line_fig1,line_fig2,line_fig3


    app.run(debug=True) 



def top_projects_performance(filtered,users_contests_projects_all,current_contest_data,projects_names,selected_contest,last_contest_id,top_projects):
    '''This function return the top projects and a table of performance of each project
    @param filtered: best top users
    @param users_contests_projects_all: dataframe with all the historical contest information which contains each price (start and end) of each contest that each user had choose

    It is the number of contest you want to analyze the performance of each project.
    @top_user_entry: It is the number of best user you want to take into account.
    @top_projects:  It is the number of projects you want to see.'''    

    if selected_contest == last_contest_id:
        #We have to find the information from the json data wich correspond to the on going contest
        #This functions create a points per projects based in the number of times that project has been choosen and the weith or percentage each users has used for that project.
        #Also this functions return a data frame ordered per projects with the best points.
        better_N_projects = points_per_slug_calculator(filtered, current_contest_data)

    else:
        best_users_contestN = best_users_from_contestN(users_contests_projects_all,selected_contest+1)
        better_N_projects = best_topN_project(filtered,best_users_contestN,top_projects)
        better_N_projects = adding_name(better_N_projects,projects_names)


    better_N_projects = better_N_projects.sort_values(axis_x, ascending=False).iloc[:int(top_projects), :] 
    table_projects = better_N_projects[["name","performance"]]
    better_N_projects = better_N_projects.sort_values(axis_x, ascending=True)

    return better_N_projects,table_projects

if __name__ == "__main__":
    #============================================================================================================
    #README:
    #============================================================================================================
    #   for connection to the database, you have to set the ENVIRONMENT VARIABLES:
    #
    #   'MYSQL_USER'
    #   'MYSQL_PASSWORD'
    #   'MYSQL_DATABASE'
    #   'MYSQL_SERVER'
    #   'MYSQL_PORT'--> optional, just if you use a different port than the default
    #
    #
    #This program return a dashboard using dash library containing three interactive parameters
    #@selected_contest: It is the number of contest you want to analyze the performance of each project.
    #@top_user_entry: It is the number of best user you want to take into account.
    #@top_projects:  It is the number of projects you want to see.
    #
    #
    #   Plot 1:
    #   A bar plot of the best TOP_PROJECTS projects based on the portfolios of the best historical contestant which are in the current contest.
    #   The best projects were order by the total points per slug.
    #
    #   Table 1:
    #   A plot performance of each projects: each performance has been calculated as a [end_price-start_price]/end_price*100.
    # 
    #   Table 2:
    #   It is A table containing the information of a theorical portfolio based on th best project you choose.
    #   It also indicates your return your profit if as if you would be invested 1000 usd distribuited equitably in each project.
    #==============================================================================================================
    #   'MYSQL_USER' root
    #   'MYSQL_PASSWORD'  "yourkey"
    #   'MYSQL_DATABASE' cryptobirds
    #   'MYSQL_SERVER' localhost
    #   'MYSQL_PORT' 3306


    connection = open_connection()

    contestDashApp(connection)

    close_connection(connection)



