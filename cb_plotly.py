# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 23:58:46 2022

@author: SaGaRueda
"""

#@title


from random import sample

import pandas as pd
import plotly
import plotly.graph_objs as go

from plotly import tools
import plotly.figure_factory as ff

def plotting_historical(data,axis_x,axis_y, width,height,tit,text_x = '',text_y = '',top_entries = 25):
    '''
    @param data: dataframe of data to be plotted
    @param axis_x: is the column of data which will be used to plot in the axis x
    @param axis_y: is the column of data which will be used to plot in the axis y
    @param width: is the weith of plot
    @param heihgt: is the height of plot
    @param title: a string to be used as title
    :return: a vertical bar plot in a .html file
    '''

    #colors = {item: 'rgb({}, {}, {})'.format(*sample(range(256), 3)) for item in data[axis_x].unique()}
    #data['color'] = data[axis_x].map(colors)    
    #color = #70E6FF
    frame = data

    # modify to get top 5, top 20 or any other
    frame = frame.sort_values(axis_x, ascending = False).iloc[:top_entries, :]
    
    ##2.3 Sort values in ascending order so that top bar corresponds to greatest value
    frame = frame.sort_values(axis_x, ascending = True)
    
    #layout
    layout = go.Layout(
            xaxis=dict(title=text_x,),
            yaxis=dict(title=text_y,

            ))

    #ticktext = ['#1', '#2', '#3', '#4', '#5', '#6','#7','#8','#9','#10']
    fig1 = go.Bar(
      x = frame[axis_x],
      y = frame[axis_y],
      marker_color = 'rgb(23,162,184)',#'rgb(162,234,235)',
      hoverinfo  = 'all',#'skip',#'none', # display Item name and Value when hovering over bar "all"
      textposition = 'inside', # position text outside bar
      texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
      orientation = 'h', # to have bar growing rightwards
      #ids = ticktext,
      legendgroup = 'hide'
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
            t=0.08*height,
            pad=4
        ),
        title={
            'text': tit,
            'y':0.96,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
            'family':"Arial",
            'size':25,
            'color':'#000000'
            }
        },

        #paper_bgcolor="LightSteelBlue",
    )
    fig.update_layout(
        yaxis = dict(
            tickfont = dict(size=15)),
        xaxis = dict(
            tickfont = dict(size=15)))
    
    #print(frame['axis_x'][0])
    #    print(max(list(data['axis_x'])))
    #print(0.8*(data['axis_x'].min()), 1.2*max(data['axis_x']))
    #min_val = data[axis_x][len(data[axis_x])-1]
    #max_val = data[axis_x][0]
    #fig.update_xaxes(range=[0.8*min_val, 1.5*max_val]) 
    
    fig.write_html("outputPlots/"+tit+".html", auto_open=True)
    #fig.write_html("path/to/file.html")
    
def plotting_contest_data(contest_info):
    data1 = "Number of contestant"
    data2 = "Number of different projects"
    data3 = "Number of top 10 in current contest"
    data4 = "Number of top 25 in current contest"
    

    table_data = [[data1, data2, data3, data4],
              [contest_info["N_total_contestant"],
               contest_info["N_total_projects"],
               contest_info["N_top10_current"],
               contest_info["N_top25_current"]],
     ]

    fig = ff.create_table(table_data, height_constant=120)

    fig.layout.margin.update({'t':50, 'b':100})
    fig.layout.update({'title': "Current contest information"},title_x=0.5)
    #"fig.update_layout(title_text='Your title', title_x=0.5)
        
    fig.write_html('contest_information.html', auto_open=True)
    #plotly.offline.plot(fig)    
    
    


def plotting_topN(data: pd.DataFrame, width: float = 800, height: float = 600, ranking: float = 'ranking', tit: str = "Top 10 by contest") -> None:
    '''
    @param data: dataframe of data to be plotted

    @param width: is the weith of plot
    @param heihgt: is the height of plot@
    @param ranking: is the ranking to be use as x in the plot
    @param axis_y: is the column of data which will be used to plot in the axis y
    @param title: a string to be used as title
    :return: a vertical bar plot in a .html file
    '''

    fig = go.Figure()

    for i in range(data['id_contest'].max()):
      
      frame = data[data['id_contest'] == i+1]
      frame = frame.sort_values(ranking, ascending = True)
    
      fig.add_trace(go.Bar(name="Contest "+str(i+1), x=frame[ranking], y=frame["username"],  
      hoverinfo='all',# display Item name and Value when hovering over bar
      textposition = 'inside', # position text outside bar
      texttemplate = '%{y}<br>%{x:.4s}', # display y field (Item name), line break and then the value with up to 4 digits
      orientation = 'h', # to have bar growing rightwards
      ))
      fig.update_layout(barmode='relative',#'stack', #relative
        autosize=False,
        width=width,
        height=height,
        margin=dict(
            l=0.005*width,
            r=0.005*width,
            b=0.005*height,
            t=0.04*height
        ),
        xaxis=dict(title=tit,
                   ),
        title={
            'text': "Top 10 by contest",
            'y':0.99    ,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        paper_bgcolor="LightSteelBlue",
    )
    #fig.update_xaxes(range=[120, 200])     
    
    plotly.offline.plot(fig)     

        
  
    
def dashboard_contest_data(contest_info, data,data1,kpi,kpi1,width,height,title):
    """Plotting cabecera"""

    info = ["Number of contestant","Number of different projects","Number of top 10 in current contest",
    "Number of top 25 in current contest"]  

    table_data = [info,
              [contest_info["N_total_contestant"],
               contest_info["N_total_projects"],
               contest_info["N_top10_current"],
               contest_info["N_top25_current"]],
     ]
    trace0 = ff.create_table(table_data, height_constant= 0.1*height)    

    trace0.layout.margin.update({'t':50, 'b':100})
    trace0.layout.update({'title': title },title_x=0.5)
    
    
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
  
    
    
    fig = tools.make_subplots(rows=1, cols=3, shared_xaxes=False)
    fig.append_trace(trace0, 1,1)    
    fig.append_trace(trace1, 1,2)
    fig.append_trace(trace2, 1,3)
    
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(
            l=0.005*width,
            r=0.005*width,
            b=0.005*height,
            t=0.1*height,
            pad=4
        ),
        title={
            'text': title,
            'y':0.97    ,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        #paper_bgcolor="LightSteelBlue",
    )

    plotly.offline.plot(fig)     



if __name__ == '__main__':
    """
    
    filepath = 'data/cb-contest-12-before-closing.json'
    filepath2 = 'data/cb-contest-11-historical-update.csv'

    data_contest_12 = load_json(filepath)
    contest_data = getContestData(data_contest_12)
   
    historical_ranking = load_historical_csv(filepath2)
    #@title Theis is the historic rank
    historic_ranking25 = get_historic_best(25, historical_ranking)
        
    historical_up_to_11 = historical_ranking_slicer_by_id_contest(11, historical_ranking)
    
    ranking = data_contest_with_historic(historical_up_to_11, contest_data)

    #Finding projects with the best 25 or best 10 contestant
    ranking25 = ranking[ranking["historic_rank_of_contest_gamers"] < 26 ]

    participants_ranking25 = ranking25[['username', 'id_user', 'historic_rank']]

    
    
    better_25_projects = project_from_best(ranking25)
    
    projects_hist_10 = better_25_projects[better_25_projects["historic_rank"]<11]

       
    
    width = 1400
    height = 900
    title2 = "Best historical"
    kpi1 = 'percentage'
    kpi2 = 'user_cumulated_points'

    plotting_historical4(projects_hist_10,historic_ranking25,kpi1,kpi2,width,height,title2)"""
    
