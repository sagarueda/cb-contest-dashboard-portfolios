# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 22:43:44 2022

@author: SaGaRueda
"""
import numpy as np
import pandas as pd
import sys
import os
from cb_loadData import getContestData, load_json
from cb_processingData import adding_name, points_per_slug_calculator, info_current_contest
from cb_plottingData import plotting_historical, plotting_contest_data, barPlot_historical_contestant
from cb_DataBase_contests_queries import contestsRankingData,contestsHistoricalRankingData, getLastContest_id, get_projects_name
from cb_DataBase_connection import open_connection, close_connection

def contest_league_visualization(connection,topUsersEntry,topProjects):
    '''
    @param connection: the connection to the database
    @param topUsersEntry: is the number of the best contestant that we want to use to process the historical contests
    @param topProjects: is the number of the best projects that is being to shows
    '''

    id_lastContest = getLastContest_id(connection)
    historical_winners_by_contest = contestsRankingData(connection, topUsersEntry)
    top_winners_by_historical = contestsHistoricalRankingData(connection, topUsersEntry, id_lastContest)

    #axis_x = "contest_total_points"
    #axis_y = "username"
    # barPlot_historical_contestant(historical_winners_by_contest,5,id_lastContest, axis_x,axis_y, "Top "+str(topUsersEntry)+ " by contest")

    axis_x2 = "user_cumulated_points"  # para ver el historico
    axis_y2 = "username"
    barPlot_historical_contestant(top_winners_by_historical, 0, id_lastContest, axis_x2, axis_y2, "Top " + str(topUsersEntry) + " histórico de los mejores concursantes")

    filepath = 'data/cb-contest-12-before-closing.json'   # Este son datos del concurso actual, no está en la DB de MYSQL, se extrae como un dict
    current_contest_data = getContestData(load_json(filepath))

    better_N_projects = points_per_slug_calculator(top_winners_by_historical, current_contest_data) #data frame of best projects per slug

    projects_names = get_projects_name(connection)
    better_N_projects = adding_name(better_N_projects,projects_names)

    #Plotting best projects
    title = "Top "+str(top_projects) + " de proyectos basado en los mejores concursantes"
    axis_x = "average_points"#'puntos_totales'
    axis_y = "prettyName"
    plotting_historical(better_N_projects,axis_x,axis_y, title, "Puntuación del proyecto", "Proyectos Block Chain",  topProjects)

    contest_info = info_current_contest(current_contest_data,top_winners_by_historical)

    #plotting contest info
    plotting_contest_data(contest_info,topUsersEntry)


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
    #   This program generates two plots and one table with the main information of the current contest.
    #   The main parameter is the number TOP_ENTRY which is the number of best contestant to be taken into account in the processing.
    #   In case you didn't enter eny top_entry, the program will use TOP_ENTRY = 10
    #   The output of the program are three .html containing this plots
    #
    #   PLOT 1:
    #   A bar plot of the TOP_ENTRY best historical contestant until today, ranked based on the acumulated total points, which was calculated based in the position in each contest a
    #   and with an extra bonus based in how many times the contestant arrived in the top contest.

    #
    #   Plot 2:
    #   A bar plot of the best TOP_PROJECTS projects based on the portfolios of the best historical contestant which are in the current contest.
    #   The best projects were order by the total points per slug.
    #
    #   Plot 3:
    #   It is A table containing the main information of the current contest

    #==============================================================================================================
    #   'MYSQL_USER' root
    #   'MYSQL_PASSWORD'  Amsterdam15!
    #   'MYSQL_DATABASE' cryptobirds
    #   'MYSQL_SERVER' localhost
    #   'MYSQL_PORT' 3306


    args = sys.argv[1:]
    if args is None:
        top_entry = 10
        top_projects = 10
    else:
        top_entry = int(args[0])
        top_projects = int(args[1])

    connection = open_connection()

    contest_league_visualization(connection,top_entry,top_projects)

    close_connection(connection)
