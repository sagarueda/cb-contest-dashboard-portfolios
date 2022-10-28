
import pandas as pd

def getContest_id(connection):
    '''
    @param connection: connection to de DB
    @return the last ID_CONTEST wich is equivalent to the number of the last contest, for example at 15/10/2022 12 is the last contest
    '''
    try:
        cursor = connection.cursor(dictionary=True)
        sql_select_query = "select id, title from contests"
        cursor.execute(sql_select_query)
        result = cursor.fetchall()
        
        return pd.DataFrame(result).sort_values("id", ascending=False)

    finally:
        cursor.close()


def get_projects_name(connection):
    
    '''
    return a data frame with the name of all projects from the data base,
    '''    
    try:
        cursor = connection.cursor(dictionary=True)
        sql_query = ("SELECT id as id_project, slug, name, ticker FROM projects Where slug is not null and name is not null and ticker is not null")
        
        cursor.execute(sql_query)
        data_names = cursor.fetchall()
        return pd.DataFrame(data_names)

    finally:
        cursor.close()

def users_contests_projects(connection):
    '''
    return a data frame with the all projects from the data base,
    '''    
    try:
        cursor = connection.cursor(dictionary=True)
        sql_query = ("select id_user, id_contest, id_project, percentage, start_price,end_price from users_contests_projects inner join users_contests on users_contests_projects.id_user_contest = users_contests.id where start_price is not null and end_price is not null")
        
        cursor.execute(sql_query)
        data_projects = cursor.fetchall()
        return pd.DataFrame(data_projects)

    finally:
        cursor.close()  


def contestsHistoricalRankingData(connection,topEntry,id_lastcontest):

    '''
    @param connetion:
    @param topEntry: is the top 10 or top25 or topN that we wan to analize the historical
    @param id_lastcontest: is the last contest where we want to obtain the historical
    @return a dataFrame with the best historical until today, it contains just topentry rows, based on the user cumulated points
     username / id_contest |   id_user |   contest_total_points |   user_cumulated_points | is_contest_participant   |   historic_rank
       from the table contests_historical_rank where participant are under the top entry ranking'''
    try:
        cursor = connection.cursor(dictionary=True)
        #sql_select_query = "SELECT id_contest,id_user,contest_total_points,user_cumulated_points,is_contest_participant, " \
        #                   "historic_rank FROM contests_historical_rank where historic_rank <%s+1"
        sql_select_query_ = "SELECT users.username,users.id, contests_historical_rank.id_contest,contests_historical_rank.id_user, " \
                            "contests_historical_rank.user_cumulated_points," \
                            "contests_historical_rank.historic_rank FROM users inner join  contests_historical_rank on users.id = contests_historical_rank.id_user " \
                            "WHERE contests_historical_rank.id_contest = %s order by contests_historical_rank.user_cumulated_points desc limit %s"

        cursor.execute(sql_select_query_, (id_lastcontest,topEntry,))
        data_to_transform = cursor.fetchall()
          
        return pd.DataFrame(data_to_transform)

    finally:
        cursor.close()

"""
def one_project_performance(connection, project_id,id_contest):
    '''
    @param connetion: connector to the DB
    @param project_id: is the top 10 or top25 or topN that we wan to analize the historical
    @param id_contest: is the contest where we want to obtain the performance of project
    @return a performance float 0-100%'''

    try:
        cursor = connection.cursor(dictionary=True)
        query = ("select distinct users_contests_projects.start_price,users_contests_projects.end_price from users_contests_projects inner join users_contests on users_contests_projects.id_user_contest = users_contests.id where users_contests_projects.id_project = %s and users_contests_projects.start_price is not null and users_contests_projects.end_price is not null and users_contests.id_contest = %s")

        cursor.execute(query, (project_id,id_contest,))
        data_to_transform = cursor.fetchall()[0]
        #print(data_to_transform['start_price'],data_to_transform['end_price'])
        performance = performance_per(data_to_transform['start_price'],data_to_transform['end_price'])
        #print(str(performance)+" %")
        return performance

    finally:
        cursor.close()

def performance_per(x1,x2):
    return round(100.0*(x2-x1)/x1,2)

def projects_performance(connection, dataframe_projects,id_contest):
    '''
    @param connetion: connector to the DB
    @param project_id: is the top 10 or top25 or topN that we wan to analize the historical
    @param id_contest: is the contest where we want to obtain the performance of project
    @return a performance float 0-100%'''

    rend = [one_project_performance(connection,i,id_contest) for i in dataframe_projects['id_project']]
    #print(rend)

    dataframe_projects['performance'] = rend
    return dataframe_projects

def best_projects_id(connection, df_best_user,id_contest):
    '''
    @param connetion: connector to the DB
    @param dataframe_best_users: dataframe with the best contestant
    @param id_contest: is the contest where we want to obtain the performance of project
    @return a data frame with the best projects'''

    #select id_user, id_project, users_contests_projects.start_price,users_contests_projects.end_price
    rankingSchema = {'id_user': str, 'id_project': int, 'percentage':int, 'start_price': float, 'end_price': float}  # En project están la lista de portfolios elejidos?

    df = pd.DataFrame(columns=rankingSchema.keys()).astype(rankingSchema)

    try:
        cursor = connection.cursor(dictionary=True)
        for user in list(df_best_user['id_user']):
            
            query = ("select id_user, id_project, percentage, start_price,end_price from users_contests_projects inner join users_contests on users_contests_projects.id_user_contest = users_contests.id where id_user = %s and start_price is not null and end_price is not null and id_contest = %s+1; ")     
            cursor.execute(query, (user,id_contest,))
            best_project = cursor.fetchall()

            df = pd.concat([df,pd.DataFrame(best_project)],ignore_index=True)
        
        return df
    finally:
        cursor.close()"""

      


"""
if __name__ == '__main__':    

    from cb_loadData import getContestData, load_json
    from cb_processingData import adding_name, points_per_slug_calculator, info_current_contest,best_topN_project
    from cb_DataBase_contests_queries import contestsRankingData, getContest_id, get_projects_name,contestsHistoricalRankingData
    from cb_DataBase_connection import open_connection, close_connection
    from dash import Dash, html, dcc, Input, Output
    import plotly.express as px
    
    
    
    connection = open_connection()

    #contest_league_visualization(connection,top_entry,top_projects, last_project_id)
    top_user_entry = 10
    selected_contest = 11
    last_contest_id = 12 
    top_projects = 15
    #historical_winners_by_contest = contestsHistoricalRankingData(connection, top_entry,id_contest)
    axis_x ="user_cumulated_points"
    #print(len(filtered))
    #print(filtered.head())
    projects_names = get_projects_name(connection)    

    filepath = 'data/cb-contest-13-before-closing.json'  # Este son datos del concurso actual, no está en la DB de MYSQL, se extrae como un dictionary
    current_contest_data = getContestData(load_json(filepath))
    #print(current_contest_data.head())

    users_contests_projects_all = users_contests_projects(connection)
    #print(users_contests_projects_all)
    
    filtered = contestsHistoricalRankingData(connection,top_user_entry, selected_contest)
    #print(filtered)

     

    if selected_contest == last_contest_id:
        #We have to find the information from the json data wich correspond to the new contest
        better_N_projects = points_per_slug_calculator(filtered, current_contest_data)

    else:
        best_users_contestN = best_users_from_contestN(users_contests_projects_all,selected_contest+1)
        better_N_projects = best_topN_project(filtered,best_users_contestN,top_projects)
        better_N_projects = adding_name(better_N_projects,projects_names)
        
    print(better_N_projects)
    
    close_connection(connection)"""