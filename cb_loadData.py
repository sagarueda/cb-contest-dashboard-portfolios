#@title data loader
import json
import pandas as pd


from numpy.core.fromnumeric import choose

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

