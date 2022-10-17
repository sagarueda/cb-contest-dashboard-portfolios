import mysql.connector as db
import pandas as pd

from cb_DataBase_connection import open_connection, close_connection
from decimal import Decimal

def __readContestHistoricalRank(connection, id_contest):
    '''
    @param id_contest: unique key that identifies a contest
    @return select of fields specified in sql_select_query from contest asked which is in table contests_historical_rank.
    '''
    try:

        cursor = connection.cursor(dictionary=True)    
        sql_select_query = "select id_user, user_cumulated_points, top_counter, contests_by_user_count from contests_historical_rank where id_contest = %s"
        cursor.execute(sql_select_query, (id_contest,))
        result = cursor.fetchall()
    
        return result 

    finally:
        cursor.close()

def contestsHistoricalRankingDataTransformer(connection, id_contest):
    '''
    @return: list of dicts obtained from MySQL indexed to dictionary data type where:
        dictionary_key = id_user
        dictionary_values = MySQL data (other dictionary)
    '''
    data_to_transform = __readContestHistoricalRank(connection, id_contest)
    data_dictionary = {}
    for row in data_to_transform:
        data_dictionary[row['id_user']]=row
    return data_dictionary

def getLastContest_id(connection):
    '''
    @param connection: connection to de DB
    @return the last ID_CONTEST wich is equivalent to the number of the last contest, for example at 15/10/2022 12 is the last contest
    '''
    try:
        cursor = connection.cursor(dictionary=True)
        sql_select_query = "SELECT MAX(id_contest) FROM contests_historical_rank"
        cursor.execute(sql_select_query)
        result = cursor.fetchall()

        return int(result[0]['MAX(id_contest)'])

    finally:
        cursor.close()

def contestsRankingData(connection,topEntry):

    '''
    @param connetion: unique key that identifies a contest
    @param topEntry: es el top 10 or top25 que se quiere analizar del historico
    @return a dataFrame with: the quantity of top entries x Number of contest, it returns the top per contest not taking into account the cumulated points historical, just the top per contest.
     username / id_contest |   id_user |   contest_total_points |   user_cumulated_points | is_contest_participant   |   historic_rank
       from the table contests_historical_rank where participant are under the top entry ranking in all the contest historical '''
    try:
        cursor = connection.cursor(dictionary=True)
        #sql_select_query = "SELECT id_contest,id_user,contest_total_points,user_cumulated_points,is_contest_participant, " \
        #                   "historic_rank FROM contests_historical_rank where historic_rank <%s+1"
        sql_select_query_ = "SELECT users.username,users.id, contests_historical_rank.id_contest,contests_historical_rank.id_user, " \
                            "contests_historical_rank.contest_total_points,contests_historical_rank.user_cumulated_points,contests_historical_rank.is_contest_participant, " \
                            "contests_historical_rank.historic_rank FROM users inner join  contests_historical_rank on users.id = contests_historical_rank.id_user " \
                            "WHERE users.username IS NOT NULL and contests_historical_rank.historic_rank< %s +1"

        cursor.execute(sql_select_query_, (topEntry,))
        data_to_transform = cursor.fetchall()
        return pd.DataFrame(data_to_transform)

    finally:
        cursor.close()

def contestsHistoricalRankingData(connection,topEntry,id_lastcontest):

    '''
    @param connetion: unique key that identifies a contest
    @param topEntry: is the top 10 or top25 or topN that we wan to analize the historical
    @return a dataFrame with the best historical until today, it contains just topentry rows, based on the user cumulated points
     username / id_contest |   id_user |   contest_total_points |   user_cumulated_points | is_contest_participant   |   historic_rank
       from the table contests_historical_rank where participant are under the top entry ranking'''
    try:
        cursor = connection.cursor(dictionary=True)
        #sql_select_query = "SELECT id_contest,id_user,contest_total_points,user_cumulated_points,is_contest_participant, " \
        #                   "historic_rank FROM contests_historical_rank where historic_rank <%s+1"
        sql_select_query_ = "SELECT users.username,users.id, contests_historical_rank.id_contest,contests_historical_rank.id_user, " \
                            "contests_historical_rank.contest_total_points,contests_historical_rank.user_cumulated_points,contests_historical_rank.is_contest_participant, " \
                            "contests_historical_rank.historic_rank FROM users inner join  contests_historical_rank on users.id = contests_historical_rank.id_user " \
                            "WHERE users.username IS NOT NULL and contests_historical_rank.id_contest = %s order by contests_historical_rank.user_cumulated_points desc limit %s"

        cursor.execute(sql_select_query_, (id_lastcontest,topEntry,))
        data_to_transform = cursor.fetchall()
        return pd.DataFrame(data_to_transform)

    finally:
        cursor.close()


def getMaxTopCounter(connection, id_contest):
    '''
    @return max value in field `top_counter` from database 
    '''   
    try:

        cursor = connection.cursor(dictionary=True)
        sql_query = 'select ifnull(max(top_counter), 0) as max FROM contests_historical_rank where id_contest = %s'
        cursor.execute(sql_query, (id_contest,))

        return cursor.fetchone()['max']

    finally:
        cursor.close()




def get_projects_name(connection):
    
    '''
    return a data frame with the name of all projects from the data base,
    '''    
    try:
        cursor = connection.cursor(dictionary=True)
        sql_query = ("SELECT slug, name, ticker FROM projects Where slug is not null and name is not null and ticker is not null")
        cursor.execute(sql_query)
        data_names = cursor.fetchall()
        return pd.DataFrame(data_names)

    finally:
        cursor.close()

'''
if __name__ == '__main__':    

'''