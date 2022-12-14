import pandas as pd


def adding_name(data, projects):
    newdf = pd.merge(data, projects, on='id_project')
    newdf.rename(columns = {'slug_x': 'slug','name_x':'name'}, inplace=True)
    newdf = newdf[['id_project','slug','name','start_price','end_price','average_points','performance']]

    return newdf



def points_per_slug_calculator(top_winners_by_historical, data_contest):
    #It is used when calculating the ongoing contest based on the json file

    """Return a new data frame including a column with points per portfolio
    it is calculated based on the percentage and the frecuency when this portfolio is being choose by a contestant in the top historical"""
    
    data = project_from_best(data_contest_with_historic(top_winners_by_historical, data_contest))
    #print(data.head())
    percentage_sum = data.groupby(['id_project','slug','name','start_price','end_price'],as_index=False)['percentage'].sum()
   
    percentage_sum.rename(columns = {'percentage': 'puntos_totales'}, inplace=True)
    percentage_sum = percentage_sum.sort_values('puntos_totales', ascending=False)
    percent_dataframe = pd.DataFrame(percentage_sum)

    percent_dataframe["average_points"] = (percent_dataframe["puntos_totales"] / percent_dataframe
        ["puntos_totales"].sum()) * 100

    percent_dataframe["performance"] = percent_dataframe.apply(lambda row: round(100.0*(row.end_price - row.start_price)/row.start_price,2), axis=1)

    return percent_dataframe

def points_per_slug_calculator2(data,top_projects):

    """Return a new data frame including a column with points per portfolio
    it is calculated based on the percentage and the frecuency when this projects is being choose by a contestant in the top historical"""

    percentage_sum = data.groupby(['id_project','start_price','end_price'],as_index=False)['percentage'].sum()
   
    percentage_sum.rename(columns = {'percentage': 'puntos_totales'}, inplace=True)
    percentage_sum = percentage_sum.sort_values('puntos_totales', ascending=False).iloc[:int(top_projects), :]
    percent_dataframe = pd.DataFrame(percentage_sum)

    percent_dataframe["average_points"] = (percent_dataframe["puntos_totales"] / percent_dataframe
        ["puntos_totales"].sum()) * 100

    percent_dataframe["performance"] = percent_dataframe.apply(lambda row: round(100.0*(row.end_price - row.start_price)/row.start_price,2), axis=1)

    return percent_dataframe       



def best_users_from_contestN(users_contests_projects_all,N):
    #From the list of all historical contest return only the projects that were choose in the contest N
    return users_contests_projects_all[users_contests_projects_all['id_contest'] == N]


def best_topN_project(filtered,best_users_contestN,top_projects):
        
        best_projects_data = pd.merge(filtered,best_users_contestN, how = 'inner', on=["id_user",])
        best_projects_data.rename(columns = {'id_contest_y': 'id_contest'}, inplace=True)
        best_projects_data = best_projects_data[['id_contest','id_project', 'percentage', 'start_price', 'end_price']]
        
        better_N_projects = points_per_slug_calculator2(best_projects_data,top_projects).iloc[:int(top_projects), :]
        
        return better_N_projects



def get_historic_best(n_participants, historical_ranking):
    """
    @param n_participants: unique key that identifies a contest
    @param historical_ranking: data framde with historical data
        @return select of fields specified in sql_select_query from contest asked which is in table contests_historical_rank.
    '''Return best historical ranking data with the next parameters
    [username, id, historic_rank]"""
    historic_ranking_n_participants = historical_ranking[historical_ranking['historic_rank'] < n_participants + 1 ]
    historic_ranking_n_participants = historic_ranking_n_participants[["username", "id", "historic_rank" ,"user_cumulated_points"]]
    historic_ranking_n_participants.rename(columns = {"id_user" :"id"}, inplace=True)

    return historic_ranking_n_participants


def project_from_best(dfranking_n):
    # input can be a sliced ranking df or the hole df
    data = list()
    columns = ["id_user", "username", "historic_rank", "slug",  "id_project","percentage","name", 'start_price','end_price']
    for row in dfranking_n.iterrows():
        username = row[1]["username"]
        id_user= row[1]["id_user"]
        historic_rank= row[1]["historic_rank"]
        for index in range(len(row[1]['projects'])):
            id_project = row[1]['projects'][index]['id']
            slug = row[1]['projects'][index]['slug']
            name = row[1]['projects'][index]['name']
            percentage = row[1]['projects'][index]['percentage']
            start_price = row[1]['projects'][index]['start_price']
            end_price = row[1]['projects'][index]['end_price']
            data.append({"id_user": id_user, "username": username, "slug": slug, "id_project":id_project, "name":name,\
                "historic_rank": historic_rank, 'percentage': percentage, 'start_price': start_price,'end_price': end_price})

    projects_of_better = pd.DataFrame(columns = columns, data = data)

    return projects_of_better


def data_contest_with_historic(historical_ranking, contest_current_data):

    ranking = pd.merge(contest_current_data ,historical_ranking, on=["id"])

    ranking = ranking.sort_values(by='historic_rank', ascending=True)
    ranking.rename(columns = {'id_contest_x': 'id_current_contest', 'id_contest_y': 'id_historical_contest', 'username_x': 'username'}, inplace=True)
    ranking = ranking[['username' ,"id_user" ,"historic_rank" ,"projects" ,'id_current_contest' ,'id_historical_contest']]
    # to reorder best historical participants that they actually are participating in the on going contest:
    ranking['historic_rank_of_contest_gamers'] = ranking['historic_rank'].rank(method='min')
    
    return ranking

def projects_current_contests(contest_data):
    """return a list wich contains all the projects in the current contest"""

    slugs = []  # list to be completed
    for user_i in contest_data["projects"]:
        # se recorre los index de cada contestant
        for project in user_i:
            # se recorre cada proyecto del contestant
            slugs.append(project["slug"])

    return slugs


def info_current_contest(current_contest_data ,top_winners_by_historical):
    contest_info = {}
    contest_info["N_total_contestant"] = len(current_contest_data)
    contest_info["N_total_projects"] = N_projects_current_contests(current_contest_data)
    contest_info["N_topN_current"] = total_best_enrolled_in_contest(top_winners_by_historical, current_contest_data)
    return contest_info    

def N_projects_current_contests(contest_data):
    """Return the amount of different projects in the current contest"""
    return len(set(projects_current_contests(contest_data)))


def total_best_enrolled_in_contest(historical_ranking_data, contest_current_data):
    """Return the amount of contestant from the best historical are participating in the current contest"""
    return len(pd.merge(contest_current_data, historical_ranking_data, on=["id"]))    