
from decimal import Decimal

def __locPercentile(n, p=0.90):
    
    '''
    @param n: integer for percentile location calculation from a population. total number of population
    @param p: default= 0.90, float to select percentile population location to return
    :return: int position of percentile p under as integer following the python round convention
    :business_rule: return number of contest participants who receives bonus score
    '''
    return round((1-p)*n)

def __rangeCalculation(numberOf_contest_participants, p=0.90):
    '''
    
    :@param numberOf_contest_participants: number of participants in a contest
    :@param p: percentile population location, default = 0.90
    :@return quantity of participants who receive third and fourth bonus range
    :business_rule: first and second bonus range are first 10 participants for all the contests
    
    '''
    range_for_percentile = __locPercentile(numberOf_contest_participants,p)
    ## punctuation for first 10 are keep for all contests
    range = (range_for_percentile - 10)/2
    return round(range)

def __bonusGrid(max_times_in_top):

    '''
    @param max_times_in_top: max number of times a bonus was given during all past contests 
    @return: dictionary = {key1: {key2: bonusValue}}
                        key1: string "rangen"
                        key2: int times the participant entered the top 90% in previous contests, (0-n)
                        bonusValue: bonus for that contest position and top 90% times.    
    '''

    score_level1 = [score for score in range(20, 100 + 1, 20)]
    score_level2 = [score for score in range(15, 100, 15)] #max number will be 90 
    score_level3 = [score for score in range(10, 100 + 1, 10)]
    score_level4 = [score for score in range(5, 100 + 1, 5)]

    score_list = [score_level1, score_level2, score_level3, score_level4]

    bonus_grid = {}
    bonus_grid["range1"]={}

    for n in range(max_times_in_top + 1):
        
        if n < len(score_list[0]):
            bonus_grid["range1"][n]= score_list[0][n]

        else:
            bonus_grid["range1"][n]= score_list[0][-1]
         
    bonus_grid["range2"]={}
    
    for n in range(max_times_in_top + 1):

        if n < len(score_list[1]):
            bonus_grid["range2"][n] = score_list[1][n]
        
        else:
            bonus_grid["range2"][n]= score_list[1][-1]
       
    bonus_grid["range3"]={}

    for n in range(max_times_in_top + 1):

        if n < len(score_list[2]):
            bonus_grid["range3"][n] = score_list[2][n]
        
        else:
            bonus_grid["range3"][n] = score_list[2][-1]

    bonus_grid["range4"]={}

    for n in range(max_times_in_top + 1):
        if n < len(score_list[3]):
            bonus_grid["range4"][n] = score_list[3][n]
        
        else:
            bonus_grid["range4"][n] = score_list[3][-1]
    
    return bonus_grid

def __bonusPerPositionAndTime(numberOf_contest_participants, max_times_in_top):
    
    '''
    @return: dictionary = {key1: {key2: bonusValue}}
                        key1: participant position (ranking) in a contest
                        key2: times the participant entered the top 90% in previous contests (0-n)
                        bonusValue: bonus for that contest position and top 90% times.
    
    '''
    
    positions = [n for n in range(1, __locPercentile(numberOf_contest_participants) + 1)]
    bonus_per_position_and_time = {}
    bonus_grid = __bonusGrid(max_times_in_top)

    for position in positions:
    
        if  (1 <= position <= 5):
            bonus_per_position_and_time[position] = bonus_grid["range1"]
        
        if (6 <= position <= 10):
            bonus_per_position_and_time[position] = bonus_grid["range2"]

        if (11 <= position <= (11 + __rangeCalculation(numberOf_contest_participants)) + 1):
            bonus_per_position_and_time[position] = bonus_grid["range3"]

        if (11 + __rangeCalculation(numberOf_contest_participants) + 1 <= position\
             <= __locPercentile(numberOf_contest_participants) + 1):
            bonus_per_position_and_time[position] = bonus_grid["range4"]

    return bonus_per_position_and_time

def __isBonusCandidate(contest_ranking_position, numberOf_contest_participants):
    """
    @param contest_ranking_position: ranking position of participant in the last contest to compute
    @return: Boolean True if user will receive bonus and False if not
    """

    if (contest_ranking_position > numberOf_contest_participants):
        raise Exception("ranking expected to be lower than the number of participants, got {}".format(contest_ranking_position))

    return contest_ranking_position <= (__locPercentile(numberOf_contest_participants,p=0.90))
  
def bonusCalculator(contest_ranking_position, numberOf_contest_participants, times_in_top, max_times_in_top):
    """
    @param timpes_in_top: number of times a participant received bonus in previous contests.
    @return: tuple with updated field times_in_top, and bonus value for a participant
    """
    if (contest_ranking_position > numberOf_contest_participants):
        raise Exception("ranking expected to be lower than the number of participants, got {}".format(contest_ranking_position))
    
    bonus_perPosition_andTimesInTop = __bonusPerPositionAndTime(numberOf_contest_participants, max_times_in_top)

    if __isBonusCandidate(contest_ranking_position, numberOf_contest_participants):
        return times_in_top + 1, bonus_perPosition_andTimesInTop[contest_ranking_position][times_in_top]

    else: #no bonus
        return times_in_top, 0

def contestBasePoints(contest_ranking_position, numberOf_contest_participants):

    """
    @return: compute base points for a contest
    """
    if (contest_ranking_position > numberOf_contest_participants):
        raise Exception("ranking expected to be lower than the number of participants, got {}".format(contest_ranking_position))
    
    contest_base_points = (1-((contest_ranking_position-1)/numberOf_contest_participants))*100
    return round(contest_base_points, 2)         

def contestPoints(contest_ranking_position, numberOf_contest_participants, times_in_top, max_times_in_top):

    """
    @return total points obtained by a participant in a contest
    """
    if (contest_ranking_position > numberOf_contest_participants):
        raise Exception("ranking expected to be lower than the number of participants, got {}".format(contest_ranking_position))

    _,bonus = bonusCalculator(contest_ranking_position, numberOf_contest_participants, times_in_top, max_times_in_top)

    contest_total_points = contestBasePoints(contest_ranking_position, numberOf_contest_participants)\
                             + bonus

    return round(contest_total_points, 2)

def first_contest(new_data_storage, first_contest_data, number_of_participants, max_times_in_top):
    """
    @param new_data_storage: data element where new historical data computed is stored 
    @param first_contest_data: data element where first contest data per participant is stores
    @return new_data_storage data element filled with first ever contest computed
    """
    for user_id in first_contest_data.keys():

        ranking_position = float(first_contest_data[user_id]['rank'])
        id_user = first_contest_data[user_id]['id_user']
        id_contest = 1 
        base_points = contestBasePoints(ranking_position, number_of_participants)
        times_in_top = 0
        total_contest_points = contestPoints(ranking_position, number_of_participants,times_in_top, max_times_in_top)
        contests_count = 1
        new_times_in_top, bonus = bonusCalculator(ranking_position, number_of_participants\
                                                ,times_in_top,max_times_in_top)

        user_cumulated_points = total_contest_points
        is_contest_participant = 1
    
        new_user_row = {'id_contest':id_contest, 'id_user':id_user, 'contest_base_points':base_points, 'bonus': bonus\
                        ,'contest_total_points': total_contest_points, 'user_cumulated_points': user_cumulated_points\
                        ,'contests_by_user_count':contests_count,'is_contest_participant':is_contest_participant\
                        ,'top_counter':new_times_in_top}   
            
        new_data_storage[id_user] = new_user_row

    return new_data_storage

def rankContestParticipants(userProcessedData):
    
    """
    @param userProcessedData: dictionary that contains the computed points and other fields 
    for the new contest to include in historical record.
    
    @return userProcessedData with new field `historic_rank` computed; historic_rank is assigned 
    based on participants ordered 'user_cumulated_points, from highest to lowest.

    business rule: tie between participants (exact `user_cumulated_point` value with two figure numbers)
    assigns same historical_rank.
    """

    ordered = userProcessedData.values()
    ordered = sorted(ordered, key= lambda d: d['user_cumulated_points'],reverse=True)
    i = 0
    old_data = None

    for data in ordered:
        if old_data == None or old_data['user_cumulated_points'] != data['user_cumulated_points']:
            i +=1
        
        data['historic_rank'] = i
        old_data = data
           
    return ordered

'''
if __name__ == '__main__':
    
    data= {1: {'user_cumulated_points': Decimal(34), 'col2': 'B'}, 2: {'user_cumulated_points': Decimal(20),'col2': 'D'}}
    print(rankContestParticipants(data))

print(contestPoints(45, 245, 1))
'''