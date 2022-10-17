# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 23:58:46 2022

@author: SaGaRueda
"""
#@title functions to plot several kind of historic information from contest

from random import sample
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly import tools
import plotly.figure_factory as ff


def plot_bar_one_trace(frame, fig, idcontest, x_ax, y_ax, tit):
    """Plot one bar trace using data and the fig object"""

    fig.add_trace(go.Bar(name= tit + str(idcontest), x=frame[x_ax], y=frame[y_ax],
                         marker_color='rgb(23,162,184)',
                         hoverinfo='all',  # display Item name and Value when hovering over bar
                         textposition='inside',  # position text outside bar
                         texttemplate='%{y}<br>%{x:.4s}',
                         # display y field (Item name), line break and then the value with up to 4 digits
                         orientation='h',  # to have bar growing rightwards
                         ))
def varOutSiteOfRange(data,since_contest, until_contest):
    """ return True when any variable since_contest or until_contest are outside of the permite range, 0 and max value of contest"""
    return 0 > since_contest or since_contest > data['id_contest'].max() or 0>until_contest or until_contest > data['id_contest'].max()


def barPlot_historical_contestant(data: pd.DataFrame, since_contest: int = 1, until_contest: int = 12, x_ax: str = 'ranking',y_ax: str = "id_user", tit: str = "Puntos del concurso") -> None:
    '''
    @param data: dataframe of data to be plotted
    @param since_contest: It is the first contest you want ot plot since, if since_contest is in the range of [1-last] the plot shows an especific contest.
                            if since_contest = 0 then the plot correspond to the historical winner, in this case it show only one plot since historical to the until contest.
    @parm until_contest: It is the last contest you want to plot
    @param ranking: is the ranking to be use as x in the plot
    @param axis_y: is the column of data which will be used to plot in the axis y
    @param title: a string to be used as title
    :return: a vertical bar plot of winners from all contest since the first one, it is an interactive figure where you can click and see an especicif contest with its top of winners
    The vertical bar plot is in a stacked mode, so it is grouped on each contestant its points in different contest, here the axes x is the points per contest'''

    width = 1200.0
    height = 900.0
    fig = go.Figure()
    try:
        if varOutSiteOfRange(data, since_contest, until_contest): return print("'since' and 'until' variables are outside of range of contest")
        if since_contest>0:
            for i in range(since_contest,until_contest+1):
              frame = data[data['id_contest'] == i+1].sort_values(x_ax, ascending=True)
              plot_bar_one_trace(frame,fig,i,x_ax,y_ax, "Concurso")
        elif since_contest ==0:
            frame = data.sort_values(x_ax, ascending=True)
            plot_bar_one_trace(frame, fig,until_contest, x_ax, y_ax, "Historico")
        else:
            return print("Some parameters are incorrect try again")

        fig.update_layout(barmode='stack',  # group',# 'relative',#, #relative
                          autosize=False,
                          width=width,
                          height=height,
                          margin=dict(l=0.005 * width,r=0.005 * width,b=0.005 * height,t=0.04 * height ),
                          xaxis=dict(title='Puntos', ),
                          yaxis=dict(title="Participantes", ),
                          title={'text': tit,'y': 0.99,'x': 0.5,'xanchor': 'center','yanchor': 'top'},)

        fig.update_xaxes(range=[0.99*data[x_ax].min(),1.005*data[x_ax].max()])
    finally:
        plotly.offline.plot(fig)


def plotting_historical(data,axis_x,axis_y, tit,text_x = '',text_y = '',top_entries = 25):
    '''
    @param data: dataframe of data to be plotted
    @param axis_x: is the column of data which will be used to plot in the axis x
    @param axis_y: is the column of data which will be used to plot in the axis y
    @param width: is the width of plot
    @param heihgt: is the height of plot
    @param title: a string to be used as title
    :return: a vertical bar plot in a .html file
    '''

    #color = #70E6FF
    width = 1200.0
    height = 900.0
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
            }},
    )
    fig.update_layout(
        yaxis = dict(
            tickfont = dict(size=15)),
        xaxis = dict(
            tickfont = dict(size=15)))
    fig.write_html("outputPlots/"+tit+".html", auto_open=True)
    #fig.write_html("path/to/file.html")
    
def plotting_contest_data(contest_info,topEntry):
    data1 = "Number of contestant"
    data2 = "Number of different projects"
    data3 = "Number of top "+str(topEntry)+" in the current contest"

    table_data = [[data1, data2, data3],
              [contest_info["N_total_contestant"],
               contest_info["N_total_projects"],
               contest_info["N_topN_current"],
            ]]
    fig = ff.create_table(table_data, height_constant=120)
    fig.layout.margin.update({'t':50, 'b':100})
    fig.layout.update({'title': "Current contest information"},title_x=0.5, font=dict(
            color='rgb(23,162,184)'))

    #"fig.update_layout(title_text='Your title', title_x=0.5)
    """colorscale = [[0, '#000000'],
                  [.5, '#17A2B8'],
                  [1, '#cce5ff']]"""
        
    fig.write_html('contest_information.html', auto_open=True)


"""    
def dashboard_contest_data(contest_info, data,data1,kpi,kpi1,width,height,title):
    Plotting cabecera
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
    )
    plotly.offline.plot(fig)     
"""
"""
if __name__ == '__main__':
    
"""