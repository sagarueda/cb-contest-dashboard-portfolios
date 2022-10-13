# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 14:50:22 2022

@author: SaGaRueda
"""

from decimal import Decimal
from pyclbr import readmodule_ex
from DataBase_connection import open_connection, close_connection
from DataBase_user_contests import userContestDataTransformer, participantsCount, ScriptVariables
import sys
from DataBase_contests_historical_rank import contestsHistoricalRankingDataTransformer, insertContestHistoricalRank, getMaxTopCounter
from historical_score_1 import bonusCalculator, contestBasePoints, contestPoints, rankContestParticipants, first_contest
import os



def historicalUpdate(connection, contest_rank_by_idUser,number_of_contest_participants,historical_records, id_contest, max_top_counter):
    '''
    @param connection: the connection to the database
    @param contest_rank_by_idUser is the dictionary that include the rank or position of an user for the last contest
    @param number_of_contest_participants is the total number of contest participants
    @param historical_records is the historical record of participants taken from the last content registry
    @param id_contest, contest id for the update of the historical rank
    @param max_times_in_top: max number of times a bonus was given during all past contests 
    @return the new data generation for the historical rank when a new contest is included and inserted into the database
    '''
    new_historical_db_data = {}    
    
    if id_contest == 1:
        first_contest(new_historical_db_data, contest_rank_by_idUser, number_of_contest_participants,max_top_counter)

    else:

        #user contest participants (all users) with default data        

        for user_id in historical_records.keys():
        
            base_points = 0
            bonus = 0
            total_contest_points = 0
            user_cumulated_points = historical_records[user_id]['user_cumulated_points']
            contests_count = historical_records[user_id]['contests_by_user_count']
            is_contest_participant = 0
            times_in_top = historical_records[user_id]['top_counter']
            
            new_db_entry = {'id_contest':id_contest, 'id_user':user_id, 'contest_base_points':base_points, 'bonus': bonus\
                            ,'contest_total_points': total_contest_points, 'user_cumulated_points': user_cumulated_points\
                            ,'contests_by_user_count':contests_count,'is_contest_participant':is_contest_participant\
                            ,'top_counter':times_in_top}    

            new_historical_db_data[user_id] = new_db_entry

        #for participants in the last contest to update:
    
        for user_id in contest_rank_by_idUser.keys():

            ranking_position = contest_rank_by_idUser[user_id]['rank'] 
            id_user = contest_rank_by_idUser[user_id]['id_user']
            base_points = contestBasePoints(ranking_position, number_of_contest_participants) 

            is_new_participant = id_user not in historical_records

            if is_new_participant:
                
                times_in_top = 0
                user_cumulated_points = contestPoints(ranking_position, number_of_contest_participants,times_in_top, max_top_counter)
                contests_count = 1
                new_times_in_top, bonus = bonusCalculator(ranking_position, number_of_contest_participants\
                                        ,times_in_top, max_top_counter)
                total_contest_points = contestPoints(ranking_position, number_of_contest_participants\
                                                    ,times_in_top,max_top_counter)
                is_contest_participant = 1
                
                new_user_row = {'id_contest':id_contest, 'id_user':id_user, 'contest_base_points':base_points, 'bonus': bonus\
                            ,'contest_total_points': total_contest_points, 'user_cumulated_points': user_cumulated_points\
                            ,'contests_by_user_count':contests_count,'is_contest_participant':is_contest_participant\
                            ,'top_counter':new_times_in_top}   
                
                new_historical_db_data[id_user] = new_user_row

            else:                                                                                                                        
                times_in_top = historical_records[id_user]['top_counter']
                last_historical_points = float(historical_records[id_user]['user_cumulated_points'])
                user_contest_points = contestPoints(ranking_position, number_of_contest_participants,times_in_top, max_top_counter) 
                user_cumulated_points = user_contest_points + last_historical_points
                contests_count = historical_records[id_user]['contests_by_user_count'] + 1                                

                new_times_in_top,bonus = bonusCalculator(ranking_position, number_of_contest_participants\
                                                        ,times_in_top,max_top_counter)
                total_contest_points = contestPoints(ranking_position, number_of_contest_participants, times_in_top, max_top_counter)

                is_contest_participant = 1

                updated_row = {'id_contest':id_contest, 'id_user':id_user, 'contest_base_points':base_points, 'bonus': bonus\
                            ,'contest_total_points': total_contest_points, 'user_cumulated_points': user_cumulated_points\
                            ,'contests_by_user_count':contests_count,'is_contest_participant':is_contest_participant\
                            ,'top_counter':new_times_in_top}                  
                
                new_historical_db_data.update({id_user: updated_row })

    new_historical_db_data = rankContestParticipants(new_historical_db_data)    
    #insertContestHistoricalRank(connection, new_historical_db_data)
        
    return new_historical_db_data

if __name__ == '__main__':

    #============================================================================================================
    #README:
    #============================================================================================================
    #   for connection to the database, you have to set the ENVIRONMENT VARIABLES:
    #
    #   'MYSQL_USER'
    #   'MYSQL_PASSWORD'
    #   'MYSQL_DATABASE'
    #   'MYSQL_SERVER'
    #   'MYSQL_PORT'--> optional, just if you use a different port than the default
    #
    #   for update historical_rank table after last contest has finished, write in console:
    #     MODE=last python main.py
    #
    #   if you want to compute the historical for a different contest, or using another previous data
    #   (e.g because one of the contests don't want to be taken into account as a business desition)
    #   you have to specify MODE=manual and and two id_contests as arguments:
    #
    #   'old_contest' id, is one contest id (field `id_contest`) that exist in the table `historical_rank`. 
    #    This means any contest from where the historical rank has already been computed.
    #   'current_contest' id is the id of the contest for which you want to compute the historical data.
    #   
    #   EXAMPLE 1:
    #   MODE = manual python main.py 9 10 
    #   will compute the updated historical rank for contest 10, taking the previous participants points and data 
    #   from contest 9
    #
    #   EXAMPLE 2:
    #   MODE = manual python main.py 8 10 
    #   will compute the updated historical rank for contest 10, taking the previous participants points and data 
    #   from contest 8
    #
    #   EXAMPLE 3:
    #   you can compute user points from a contest without taking into account the historical data by adding 0 by
    #  'old_contest' id
    #   MODE= manual python main.py 0 10
    #==============================================================================================================

    connection = open_connection()
    mode = os.environ.get('MODE')
    args = sys.argv[1:]
    
    if mode == 'last': 

        contest_id_variables = ScriptVariables(connection)
        current_contest = contest_id_variables[0]['id_contest']
        old_contest = contest_id_variables[1]['id_contest']
     
    elif mode == 'manual':

        if len(args) != 2:
            raise Exception('arguments missed, see README section')
        
        current_contest = args[1]
        old_contest = args[0]
           
    contest_rank_by_idUser = userContestDataTransformer(connection, current_contest)
    number_of_contest_participants = participantsCount(connection,current_contest)
    historical_records = contestsHistoricalRankingDataTransformer(connection,  old_contest)
    historical_max_top = getMaxTopCounter(connection, old_contest)
    
    print(historicalUpdate(connection=connection, contest_rank_by_idUser=contest_rank_by_idUser\
                            ,number_of_contest_participants = number_of_contest_participants\
                            ,historical_records=historical_records,id_contest=current_contest, max_top_counter=historical_max_top))

    close_connection(connection)

    '''
    print('record elements: ', len(new_historical_db_data))  
    print('dictionary size: ', sys.getsizeof(historicalUpdate))  
    '''