import mysql.connector as db
from pandas import isnull
from DataBase_connection import open_connection, close_connection

def __readUsersContests(connection, id_contest):

    '''
    @param id_contest: unique key that identifies a contest
    @return select of fields specified in sql_select_query from contest asked which is in table users_contests.
    '''
    try:

        cursor = connection.cursor(dictionary=True)
        sql_select_query = ('select id_user, `rank` from users_contests where id_contest = %s and `type` like "entry"')
        cursor.execute(sql_select_query, (id_contest,))
        
        return cursor.fetchall()
               
    finally:
        
        cursor.close()

def participantsCount(connection, id_contest):

    '''
    @return total number of participants in a contest.
    '''

    try:

        cursor = connection.cursor(dictionary=True)

        sql_query = 'select count(*) as total FROM users_contests where id_contest = %s and `type` like "entry"'
        cursor.execute(sql_query, (id_contest,))
        return cursor.fetchone()['total']
   
    finally:
        cursor.close()

def userContestDataTransformer(connection, id_contest):
    '''
    @return: list of dicts obtained from MySQL is indexed to a dictionary where:
        dictionary_key = id_user
        dictionary_values = MySQL data (other dictionary)

    '''
    data_to_transform = __readUsersContests(connection, id_contest)
    data_dictionary = {}

    for row in data_to_transform:
        data_dictionary[row['id_user']]=row

    return data_dictionary

def ScriptVariables(connection):

    '''
    @return the two last id_contests for automatic script running. The higher id is the last one: the contest to be computed in
    the historical. The second, is used to take from the historical, the group of users that are ever participated in a contest 
    '''
    try:

        cursor = connection.cursor(dictionary=True, buffered=True)
        sql_query= 'select distinct id_contest from cryptobirds.users_contests where `type` like "entry" order by id_contest desc'
        cursor.execute(sql_query)
        
        return cursor.fetchmany(2)
        
    finally:
        cursor.close()

'''
if __name__ == '__main__':

    try:

        import mysql.connector as db
        
        n=0
        print("step", str(n))
        print('Connected')
        connection = db.connect(user='root', passwd = '', host='127.0.0.1', database='cryptobirds', port=3307)
        n+=1
        print("step", str(n))
        print("\n\r")
        print(__readUsersContests(connection, 1))
        n+=1
        print("step", str(n))
        print("\n\r")
        users = userContestDataTransformer(connection, 7)
        print(users)
        n+=1
        print("\n\r")
        print("step", str(n))
        user_selected = users[5289]['id_user']
        print(isNewParticipant(connection, user_selected, 1))
        n+=1
        print("\n\r")
        print("step", str(n))
        print("script variables: ")
        print(ScriptVariables(connection))
        n+=1
        print("\n\r")
        print("step", str(n))
        print("participants count: ", participantsCount(connection, 1))
        print("\n\r")

    except db.Error as error:
            
        print("failed to connect to database: {}".format(error))

    finally:
        close_connection(connection)
        print("connection closed")

'''