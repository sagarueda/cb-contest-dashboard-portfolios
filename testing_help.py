# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:05:52 2022

@author: SaGaRueda
"""

import json
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib
import matplotlib.pyplot as plt
#import squarify
from IPython.display import display
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from load_data import getContestData, load_json, load_historical_csv

from load_data import get_historic_best
from load_data import getContestData, load_json, load_historical_csv, getContestData2
from cb_plotly import plotting_historical,plotting_historical2
from load_data import get_historic_best
from newcontestant import project_from_best, data_contest_with_historic
from newcontestant import historical_ranking_slicer_by_id_contest
from raceplotly.plots import barplot


#plotly.tools.set_credentials_file(username='sagarueda', api_key='sagaruedaplotly')


filepath = 'data/cb-contest-12-before-closing.json'
filepath2 = 'data/cb-contest-11-historical-update.csv'

data_contest_12 = load_json(filepath)
#print(json.dumps(data_contest_12, indent = 4))


contest_data = getContestData(data_contest_12)

historical_ranking = load_historical_csv(filepath2)


historical_up_to_11 = historical_ranking_slicer_by_id_contest(11, historical_ranking)

ranking = data_contest_with_historic(historical_up_to_11, contest_data)

#Finding projects with the best 25 or best 10 contestant
ranking25 = ranking[ranking["historic_rank_of_contest_gamers"] < 26 ]
ranking10 = ranking[ranking['historic_rank_of_contest_gamers'] < 11 ]
participants_ranking25 = ranking25[['username', 'id_user', 'historic_rank']]
participants_ranking10 = ranking10[['username', 'id_user', 'historic_rank']]


better_25_projects = project_from_best(ranking25)

projects_hist_25 = better_25_projects[better_25_projects["historic_rank"]<26]
#the best 10 are included in 25
projects_hist_10 = better_25_projects[better_25_projects["historic_rank"]<11]
    


#Plotting with bar the historical ranking 25
#plot parameters     
width = 800
height = 900
title2 = "Best projects based on the best 25 contestant"
kpi = 'historic_rank'

plotting_historical2(projects_hist_25,width,height,title2,kpi)


my_raceplot = barplot(projects_hist_25,
                      item_column='slug',
                      value_column='percetange',
                      time_column='index')

my_raceplot.plot(title = 'Best projects based on the best 25 contestant',
                 item_label = 'Top Projects',
                 value_label = 'Percentage',
                 frame_duration = 800)


#####
fig = make_subplots(rows=1, cols=2)

colors = {item: 'rgb({}, {}, {})'.format(*sample(range(256), 3)) for item in data[kpi].unique()}
data['color'] = data[kpi].map(colors)    

frame = data

top_entries = 40 # modify to get top 5, top 20 or any other
frame = frame.sort_values(kpi, ascending = False).iloc[:top_entries, :]

##2.3 Sort values in ascending order so that top bar corresponds to greatest value
frame = frame.sort_values(kpi, ascending = True)

#layout
layout = go.Layout(
        xaxis=dict(title=kpi,),
        yaxis=dict(#title='Contestant', )
                   )
        )


fig1 = go.Bar(
  x = frame['historic_rank'],
  y = frame['slug'],
  marker_color = frame['color'],      
  hoverinfo = 'all', # display Item name and Value when hovering over bar
  textposition = 'inside', # position text outside bar
  texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
  orientation = 'h' # to have bar growing rightwards
)

fig1.add_trace(row=1,cols=1)

colors = {item: 'rgb({}, {}, {})'.format(*sample(range(256), 3)) for item in data['user_cumulated_points'].unique()}
data['color'] = data['user_cumulated_points'].map(colors)    

frame = data

top_entries = 25 # modify to get top 5, top 20 or any other
frame = frame.sort_values('user_cumulated_points', ascending = False).iloc[:top_entries, :]

##2.3 Sort values in ascending order so that top bar corresponds to greatest value
frame = frame.sort_values('user_cumulated_points', ascending = True)

#layout
layout = go.Layout(
        xaxis=dict(title='Acumulated Points',),
        yaxis=dict(#title='Contestant', )
                   )
        )


fig2 = go.Bar(
  x = frame['user_cumulated_points'],
  y = frame['username'],
  marker_color = frame['color'],      
  hoverinfo = 'all', # display Item name and Value when hovering over bar
  textposition = 'inside', # position text outside bar
  texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
  orientation = 'h' # to have bar growing rightwards
)

fig2 = go.Figure(data=fig2, layout=layout)
fig2.add_trace(row=1,cols=2)    
  
fig2.update_layout(
    autosize=False,
    width=width,
    height=height,
    margin=dict(
        l=0.005*width,
        r=0.005*width,
        b=0.005*height,
        t=0.04*height,
        pad=4
    ),
    title={
        'text': title,
        'y':0.99    ,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor="LightSteelBlue",
)    

fig2.update_xaxes(range=[400, 750])    



plotly.offline.plot(fig)




    
def plotting_historical2(data,width,height,title,kpi):    
    """Return a plot in plotly html"""    
    colors = {item: 'rgb({}, {}, {})'.format(*sample(range(256), 3)) for item in data[kpi].unique()}
    data['color'] = data[kpi].map(colors)    

    frame = data

    top_entries = 40 # modify to get top 5, top 20 or any other
    frame = frame.sort_values(kpi, ascending = False).iloc[:top_entries, :]
    
    ##2.3 Sort values in ascending order so that top bar corresponds to greatest value
    frame = frame.sort_values(kpi, ascending = True)
    
    #layout
    layout = go.Layout(
            xaxis=dict(title=kpi,),
            yaxis=dict(#title='Contestant', )
                       )
            )
    

    fig1 = go.Bar(
      x = frame['historic_rank'],
      y = frame['slug'],
      marker_color = frame['color'],      
      hoverinfo = 'all', # display Item name and Value when hovering over bar
      textposition = 'inside', # position text outside bar
      texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
      orientation = 'h' # to have bar growing rightwards
    )
    
    fig = go.Figure(data=fig1, layout=layout)    
      
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(
            l=0.005*width,
            r=0.005*width,
            b=0.005*height,
            t=0.04*height,
            pad=4
        ),
        title={
            'text': title,
            'y':0.99    ,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        paper_bgcolor="LightSteelBlue",
    )    
    
      
    plotly.offline.plot(fig) #lo exporta en html   
    fig.write_html(title+'.html', auto_open=True)
    
    
def plotting_historical3(data,data1,kpi,kpi1,width,height,title):

    fig = make_subplots(rows=1, cols=2)
    
    colors = {item: 'rgb({}, {}, {})'.format(*sample(range(256), 3)) for item in data[kpi].unique()}
    data['color'] = data[kpi].map(colors)    

    frame = data

    top_entries = 40 # modify to get top 5, top 20 or any other
    frame = frame.sort_values(kpi, ascending = False).iloc[:top_entries, :]
    
    ##2.3 Sort values in ascending order so that top bar corresponds to greatest value
    frame = frame.sort_values(kpi, ascending = True)
    
    #layout
    layout = go.Layout(
            xaxis=dict(title=kpi,),
            yaxis=dict(#title='Contestant', )
                       )
            )
    

    fig1 = go.Bar(
      x = frame[kpi],
      y = frame['slug'],
      marker_color = frame['color'],      
      hoverinfo = 'all', # display Item name and Value when hovering over bar
      textposition = 'inside', # position text outside bar
      texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
      orientation = 'h' # to have bar growing rightwards
    )
    
    fig.add_trace(fig1,row=1,col=2)    
    
    colors = {item: 'rgb({}, {}, {})'.format(*sample(range(256), 3)) for item in data1[kpi1].unique()}
    data1['color'] = data1[kpi1].map(colors)    

    frame = data1

    top_entries = 25 # modify to get top 5, top 20 or any other
    frame = frame.sort_values(kpi1, ascending = False).iloc[:top_entries, :]
    
    ##2.3 Sort values in ascending order so that top bar corresponds to greatest value
    frame = frame.sort_values(kpi1, ascending = True)
    
    #layout
    layout = go.Layout(
            xaxis=dict(title=kpi1),
            yaxis=dict(#title='Contestant', )
                       )
            )
    

    fig2 = go.Bar(
      x = frame[kpi1],
      y = frame['username'],
      marker_color = frame['color'],      
      hoverinfo = 'all', # display Item name and Value when hovering over bar
      textposition = 'inside', # position text outside bar
      texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
      orientation = 'h' # to have bar growing rightwards
    )
    
    fig2 = go.Figure(data=fig2, layout=layout)
     
      
    fig2.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(
            l=0.005*width,
            r=0.005*width,
            b=0.005*height,
            t=0.04*height,
            pad=4
        ),
        title={
            'text': title,
            'y':0.99    ,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        paper_bgcolor="LightSteelBlue",
    )    
    
    fig2.update_xaxes(range=[400, 750])    
    fig.add_trace(fig2,row=1,col=2)   
    

    
    plotly.offline.plot(fig) 
    
    
def plotting_historical4(data,data1,kpi,kpi1,width,height,title):
    colors = {item: 'rgb({}, {}, {})'.format(*sample(range(256), 3)) for item in data[kpi].unique()}
    data['color'] = data[kpi].map(colors)   
    top_entries = 40 
    frame = data
    frame = frame.sort_values(kpi, ascending = False).iloc[:top_entries, :]
    frame = frame.sort_values(kpi, ascending = True)
    
    trace1 = go.Bar(
      x = frame[kpi],
      y = frame['slug'],
      marker_color = frame['color'],      
      hoverinfo = 'all', # display Item name and Value when hovering over bar
      textposition = 'inside', # position text outside bar
      texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
      orientation = 'h' # to have bar growing rightwards
    )
    colors = {item: 'rgb({}, {}, {})'.format(*sample(range(256), 3)) for item in data1[kpi1].unique()}
    data1['color'] = data1[kpi1].map(colors)    

    frame1 = data1

    top_entries = 25 # modify to get top 5, top 20 or any other
    frame1 = frame1.sort_values(kpi1, ascending = False).iloc[:top_entries, :]
    
    ##2.3 Sort values in ascending order so that top bar corresponds to greatest value
    frame1 = frame1.sort_values(kpi1, ascending = True)
    
    trace2 = go.Bar(
      x = frame1[kpi1],
      y = frame1['username'],
      marker_color = frame['color'],      
      hoverinfo = 'all', # display Item name and Value when hovering over bar
      textposition = 'inside', # position text outside bar
      texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
      orientation = 'h' # to have bar growing rightwards
    )
  
    
    
    fig = tools.make_subplots(rows=1, cols=2, shared_xaxes=False)
    
    fig.append_trace(trace1, 1,1)
    fig.append_trace(trace2, 1, 2)
    
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(
            l=0.005*width,
            r=0.005*width,
            b=0.005*height,
            t=0.04*height,
            pad=4
        ),
        title={
            'text': title,
            'y':0.99    ,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        paper_bgcolor="LightSteelBlue",
    )

    
    plotly.offline.plot(fig) 
    
    



