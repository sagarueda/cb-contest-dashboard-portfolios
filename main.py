# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:05:52 2022

@author: SaGaRueda
"""
import numpy as np
import pandas as pd

from load_data import getContestData, load_json, load_historical_csv,load_historical_csv2, getContestData2
from load_data import get_historic_best, projects_current_contests,N_projects_current_contests
from load_data import project_from_best, data_contest_with_historic, adding_name
from load_data import historical_ranking_slicer_by_id_contest,points_calculator
from load_data import total_best_enrolled_in_contest,re_ranking_contest,add_time_intops,add_max_time_intops, portfolios_points
from cb_plotly import plotting_historical,plotting_contest_data, plotting_topN
from decimal import Decimal
from pyclbr import readmodule_ex
import sys
from historical_score_1 import bonusCalculator, contestBasePoints, contestPoints, rankContestParticipants, first_contest


def visualization_hist():

    filepath = 'data/cb-contest-12-before-closing.json'
    filepath2 = 'data/cb-contest-11-historical-update.csv'
    filepath3 = 'data/historical_contest.csv'
    filepath4 = 'data/projects_name.csv'

    data_contest_12 = load_json(filepath)
    contest_data = getContestData(data_contest_12)
   
    historical_ranking = load_historical_csv(filepath2)

    projects_names = load_historical_csv2(filepath4, delimiter = ',')

    #@title Theis is the historic rank
    historic_ranking25 = get_historic_best(25, historical_ranking)
    

    
    historical_up_to_11 = historical_ranking_slicer_by_id_contest(11, historical_ranking)
    
    ranking = data_contest_with_historic(historical_up_to_11, contest_data)

    #Finding projects with the best 25 or best 10 contestant
    ranking25 = ranking[ranking["historic_rank_of_contest_gamers"] < 26 ]
    ranking10 = ranking[ranking['historic_rank_of_contest_gamers'] < 11 ]
    participants_ranking25 = ranking25[['username', 'id_user', 'historic_rank']]
    participants_ranking10 = ranking10[['username', 'id_user', 'historic_rank']]
    
    
    contest_info = {}
    contest_info["N_total_contestant"] = len(contest_data)
    contest_info["N_total_projects"] = N_projects_current_contests(contest_data)
    contest_info["N_top10_current"] = total_best_enrolled_in_contest(historical_ranking, contest_data, 10, False)
    contest_info["N_top25_current"] = total_best_enrolled_in_contest(historical_ranking, contest_data, 25, False)
    #plotting contest info
    #plotting_contest_data(contest_info)
    
    
    better_25_projects = project_from_best(ranking25)
    
    projects_hist_25 = better_25_projects[better_25_projects["historic_rank"]<26]
    #the best 10 are included in 25
    projects_hist_10 = better_25_projects[better_25_projects["historic_rank"]<11]
    bestprojects_25 = portfolios_points(projects_hist_25)
    
    
    bestprojects_25 = adding_name(bestprojects_25,projects_names)

    #Plotting with bar the historical ranking 25
    #plot parameters     
    width = 800
    height = 900
    title = "Best historical since first contest"
    axis_x = "user_cumulated_points"
    axis_y = "username"
    
    #Plotting best projects
    title = "Top 10 de proyectos basado en los mejores concursantes"
    axis_x = "average_points"#'puntos_totales'
    axis_y = "prettyName"
    plotting_historical(bestprojects_25,axis_x,axis_y, width,height,title, "Puntuación del proyecto", "Proyectos Block Chain",  20)

    historical_contest = load_historical_csv2(filepath3)
    
    
    add_time_intops(historical_contest)    
    add_max_time_intops(historical_contest)        
    
   
    historical_contest ['points'] = points_calculator(historical_contest)    
        
    top_entry = 10
    wide_df = re_ranking_contest(historical_contest,top_entry)

    plotting_topN(wide_df,width=1200,height=900, ranking='points',tit="Top 10 by contest")
    



if __name__ == "__main__":
    
    visualization_hist()