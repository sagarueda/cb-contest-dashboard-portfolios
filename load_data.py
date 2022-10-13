#@title
import json
import pandas as pd
from os import listdir
from os.path import isfile, join

from numpy.core.fromnumeric import choose
from random import sample
from historical_score_1 import contestPoints
# @title data loader
def getContestData(data):
    """return an scheme dataframe with full data"""
    rankingSchema = {'username': str, 'id_user_contest': int, 'id': int, 'id_contest': int,
                     'projects': list()}  # En project están la lista de portfolios elejidos?

    df = pd.DataFrame(columns=rankingSchema.keys()).astype(rankingSchema)

    for key in data['result']['winners']:
        df = df.append({'username': key['username'], 'id_user_contest': key['id_user_contest'],
                        'id': key['id'], 'id_contest': key['id_contest'], 'projects': key['projects']},
                       ignore_index=True)
    return df
# @title data loader
def getContestData2(data):
    """return an scheme dataframe with full data"""
    rankingSchema = {'username': str, 'id_user_contest': int, 'id': int, 'id_contest': int,
                     'projects': list()}  # En project están la lista de portfolios elejidos?

    df = pd.DataFrame(columns=rankingSchema.keys()).astype(rankingSchema)
    df_new_row = pd.DataFrame()
    
    for key in data['result']['winners']:
        
        df_new_row = pd.concat(df,{'username': key['username'], 'id_user_contest': key['id_user_contest'],
                        'id': key['id'], 'id_contest': key['id_contest'], 'projects': key['projects']},
                       ignore_index=True)
    return df_new_row

def load_json(filepath):
    """read a json file"""
#    file = open(filename, encoding="utf8")
    file = open(filepath,"r",encoding="utf8")
    data_contest = json.load(file)
    file.close()
    return data_contest


def load_historical_csv(filepath):
    """read a csv file"""
    historical = pd.read_csv(filepath, delimiter = ',', encoding="utf8")
    historical.rename(columns = {"id_user":"id"}, inplace=True)    
    return historical

def load_historical_csv2(filepath, delimiter = ';', encoding='ISO-8859-1'):
    """read a csv file"""
    historical = pd.read_csv(filepath, delimiter = delimiter,encoding=encoding)
 
    return historical
    


def get_historic_best(n_participants, historical_ranking):
    """Return best historical ranking data with the next parameters
    [username, id, historic_rank]"""
    historic_ranking_n_participants = historical_ranking[historical_ranking['historic_rank'] < n_participants + 1 ]
    historic_ranking_n_participants = historic_ranking_n_participants[["username", "id", "historic_rank","user_cumulated_points"]]
    historic_ranking_n_participants.rename(columns = {"id_user":"id"}, inplace=True)

    return historic_ranking_n_participants



def projects_current_contests(contest_data):
  """return a list wich contains all the projects in the current contest"""
    
  slugs = [] #list to be completed
  for user_i in contest_data["projects"]:
    #se recorre los index de cada contestant      
      for project in user_i:
        #se recorre cada proyecto del contestant          
          slugs.append(project["slug"])
       
  return slugs

def N_projects_current_contests(contest_data):
    """Return the amount of different projects in the current contest"""

    return len(set(projects_current_contests(contest_data)))

def data_contest_with_historic(historical_ranking, contest_data):
  
  ranking = pd.merge(contest_data,historical_ranking, on=["id"])
  ranking = ranking.sort_values(by='historic_rank', ascending=True)
  ranking.rename(columns = {'id_contest_x': 'id_current_contest', 'id_contest_y': 'id_historical_contest', 'username_x': 'username', 'id':'id_user'}, inplace=True)
  ranking = ranking[['username',"id_user","historic_rank","projects",'id_current_contest','id_historical_contest']]
  #to reorder best historical participants that they actually are participating in the on going contest:
  ranking['historic_rank_of_contest_gamers'] = ranking['historic_rank'].rank(method='min')

  return ranking


def total_best_enrolled_in_contest(historical_ranking_data, contest_data, number_of_best, want_to_print = True):

  ranking_hist = data_contest_with_historic(historical_ranking_data, contest_data)
  number_of_best_enrolled_in_contest = ranking_hist[ranking_hist["historic_rank"] < number_of_best + 1].shape[0]
  #ranking_hist is the df that contains 
  if want_to_print:

    print("="*100)
    print("there are {} users enrolled in current contest from the best historical {} users".format(str(number_of_best_enrolled_in_contest), str(number_of_best)))
    print("="*100)  
    
  return number_of_best_enrolled_in_contest



def re_ranking_contest(data,top_entry = 10):
  newdata = data[data['ranking'] < top_entry+1 ]
  return newdata


##new contestant

def historical_ranking_slicer_by_id_contest(id_contest, data):

  return data[data["id_contest"] == id_contest]


def data_contest_with_historic(historical_ranking, contest_data):
  
  ranking = pd.merge(contest_data,historical_ranking, on=["id"])
  ranking = ranking.sort_values(by='historic_rank', ascending=True)
  ranking.rename(columns = {'id_contest_x': 'id_current_contest', 'id_contest_y': 'id_historical_contest', 'username_x': 'username', 'id':'id_user'}, inplace=True)
  ranking = ranking[['username',"id_user","historic_rank","projects",'id_current_contest','id_historical_contest']]
  #to reorder best historical participants that they actually are participating in the on going contest:
  ranking['historic_rank_of_contest_gamers'] = ranking['historic_rank'].rank(method='min')

  return ranking

def project_from_best(dfranking_n):
  #input can be a sliced ranking df or the hole df
  data = list()
  columns = ["id_user", "username", "historic_rank", "slug", "percentage", 'start_price']
  for row in dfranking_n.iterrows():
  #print(row[1]['projects'])
    username = row[1]["username"]
    id_user= row[1]["id_user"]
    historic_rank= row[1]["historic_rank"]
    for index in range(len(row[1]['projects'])):
      slug = row[1]['projects'][index]['slug']
      percentage = row[1]['projects'][index]['percentage']
      start_price = row[1]['projects'][index]['start_price']
      data.append({"id_user": id_user, "username": username, "slug": slug, "historic_rank": historic_rank, 'percentage': percentage, 'start_price': start_price})

  projects_of_better = pd.DataFrame(columns = columns, data = data)
  
  return projects_of_better


def total_best_enrolled_in_contest(historical_ranking_data, contest_data, number_of_best, want_to_print = True):

  ranking_hist = data_contest_with_historic(historical_ranking_data, contest_data)
  number_of_best_enrolled_in_contest = ranking_hist[ranking_hist["historic_rank"] < number_of_best + 1].shape[0]
  #ranking_hist is the df that contains 
  if want_to_print:

    print("="*100)
    print("there are {} users enrolled in current contest from the best historical {} users".format(str(number_of_best_enrolled_in_contest), str(number_of_best)))
    print("="*100)  
    
  return number_of_best_enrolled_in_contest


def add_time_intops(data, topentry = 25):
    """ """
    aux = [1 if val<topentry+1 else 0 for val in data['ranking']]        
    data['time_intops'] = [aux[val] for val in range(len(aux))]
    

def add_max_time_intops(data, topentry = 25):
    """ """
    aux = [1 if val<topentry+1 else 0 for val in data['ranking']]        
    data['max_time_intops'] = [sum(aux[0:val+1]) for val in range(len(aux))]
    
    
def points_calculator(historical_contest):
    
    points =[]        
    for index in range(len(historical_contest)):
        contest_ranking_position = historical_contest['ranking'][index]
        Ncontest = historical_contest['id_contest'][index]
        numberOf_contest_participants = len(historical_contest[historical_contest['id_contest'] == Ncontest])
        #timpes_in_top: number of times a participant received bonus in previous contests.
        times_in_top = historical_contest['time_intops'][index]
        #param max_times_in_top: max number of times a bonus was given during all past contests 
        max_times_in_top = historical_contest['max_time_intops'][index]
        
        points.append(contestPoints(contest_ranking_position, numberOf_contest_participants, times_in_top, max_times_in_top)-20)  
    return points
        
def portfolios_points(data):
    """Return a new data frame including a column with points per portfolio
    it is calculated based on the percentage and the frecuency that this portfolio was choose by a contestant in the top historical"""

    percentage_sum = data.groupby('slug', as_index=False).percentage.sum()
    percentage_sum.rename(columns = {'percentage': 'puntos_totales'}, inplace=True)
    percentage_sum = percentage_sum.sort_values('puntos_totales', ascending=False)
    percent_dataframe = pd.DataFrame(percentage_sum)

    percent_dataframe["average_points"] = (percent_dataframe["puntos_totales"] / percent_dataframe["puntos_totales"].sum()) * 100
    percent_dataframe
    return percent_dataframe



def adding_name(data, projects):
    newdf = pd.merge(data, projects, on='slug')
    newdf["prettyName"] = [newdf['ticker'][i].upper() + "-" + newdf['name'][i] for i in range(len(newdf))]
    return newdf


