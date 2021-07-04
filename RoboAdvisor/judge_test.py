import pandas as pd
import numpy as np
import json
import csv

def generate_reply(file):

    answer_record = []
    
    ########################################
    ## TODO:generate different replies for evaluation
    ## form:{'user_id': 1707233852, '0': 150, '1': 'B', '2': 'A', '3':30, '4': '財富自由', '5': 'BCE', '6':'A', '7': 5, '8': 'C', '9':'B', '10':'A'}
    ## example:
    ## answer_record.append({'user_id': 1707233852, '0': 70, '1': 'B', '2': 'A', '3':70, '4': '財富自由', '5': 'BCE', '6':'A', '7': 5, '8': 'C', '9':'B', '10':'A'})
    answer_record.append({'user_id': 1707233852, '0': 150, '1': 'B', '2': 'A', '3':70, '4': '財富自由', '5': 'BCE', '6':'A', '7': 5, '8': 'C', '9':'B', '10':'A'})
    answer_record.append({'user_id': 1707233853, '0': 150, '1': 'B', '2': 'A', '3':70, '4': '財富自由', '5': 'BDE', '6':'A', '7': 5, '8': 'C', '9':'B', '10':'C'})
    ########################################
    key = answer_record[0].keys()
    with open(file, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, key)
        dict_writer.writeheader()
        dict_writer.writerows(answer_record)

def load_reply(file):
    
    try:
        dataframe = pd.read_csv(file, encoding='big5')
        # dataframe = pd.read_csv(file, encoding='utf-8')
        # dataframe = pd.read_csv(file)
        answer_record = dataframe.to_dict('records')
        # print("Load!")
        # print(answer_record)
        return answer_record
    except:
        print("No previous data!")
        return -1   

def risk_judge(answer_record,user_id):

    reply_set = None
    for d in answer_record:
        if d['user_id'] == user_id:
            reply_set = d.copy()
            break
    if reply_set == None:
        print("No user: "+str(user_id))
        return 0

    ############################
    ## TODO: Design judgement model
    # print(reply_set)
    answer_modify = []
    for i in range(len(reply_set)-1):
        if i == 0:
            if reply_set['0']*12 / reply_set['3'] < 0.1:
                answer_modify.append('A')
            elif reply_set['0']*12 / reply_set['3'] >= 0.1 and reply_set['0']*12 / reply_set['3'] < 0.3:
                answer_modify.append('B')
            elif reply_set['0']*12 / reply_set['3'] >= 0.3 and reply_set['0']*12 / reply_set['3'] < 0.5:
                answer_modify.append('C')
            elif reply_set['0']*12 / reply_set['3'] >= 0.5 and reply_set['0']*12 / reply_set['3'] < 0.7:
                answer_modify.append('D')
            elif reply_set['0']*12 / reply_set['3'] >= 0.7:
                answer_modify.append('E')
        elif i == 3:
            if reply_set[str(i)] <= 1:
                answer_modify.append('A')
            elif reply_set[str(i)] > 1 and reply_set[str(i)] <= 5:
                answer_modify.append('B')
            elif reply_set[str(i)] > 5 and reply_set[str(i)] <= 15:
                answer_modify.append('C')
            elif reply_set[str(i)] > 15 and reply_set[str(i)] <= 30:
                answer_modify.append('D')
            elif reply_set[str(i)] > 30:
                answer_modify.append('E')
        elif i == 5:
            max_ans = reply_set[str(i)][-1]
            answer_modify.append(max_ans)
        elif i == 7:
            if reply_set[str(i)] < 3:
                answer_modify.append('A')
            elif reply_set[str(i)] >= 3 and reply_set[str(i)] < 5:
                answer_modify.append('B')
            elif reply_set[str(i)] >= 5 and reply_set[str(i)] < 7:
                answer_modify.append('C')
            elif reply_set[str(i)] >= 7 and reply_set[str(i)] < 9:
                answer_modify.append('D')
            elif reply_set[str(i)] >= 9:
                answer_modify.append('E')
        elif i == 4:
            answer_modify.append('C')
        else:
            answer_modify.append(reply_set[str(i)])
    # print(answer_modify)
    score = []
    for i in range(len(answer_modify)):
        if i in [2, 8]:
            if answer_modify[i] == 'A':
                score.append(5)
            elif answer_modify[i] == 'B':
                score.append(4)
            elif answer_modify[i] == 'C':
                score.append(3)
            elif answer_modify[i] == 'D':
                score.append(2)
            elif answer_modify[i] == 'E':
                score.append(1)
        elif i in [0,1,3,5,7,9]:
            if answer_modify[i] == 'A':
                score.append(1)
            elif answer_modify[i] == 'B':
                score.append(2)
            elif answer_modify[i] == 'C':
                score.append(3)
            elif answer_modify[i] == 'D':
                score.append(4)
            elif answer_modify[i] == 'E':
                score.append(5)
        elif i in [6,10]:
            if answer_modify[i] == 'A':
                score.append(1)
            elif answer_modify[i] == 'B':
                score.append(3)
            elif answer_modify[i] == 'C':
                score.append(5)

    risk_level = 0
    if np.mean(score) < 1.5:
        risk_level = 1
    elif np.mean(score) >= 1.5 and np.mean(score) < 2:
        risk_level = 2
    elif np.mean(score) >= 2 and np.mean(score) < 3:
        risk_level = 3
    elif np.mean(score) >= 3 and np.mean(score) < 4:
        risk_level = 4
    elif np.mean(score) >= 4:
        risk_level = 5

    print(user_id, np.sum(score), np.mean(score), risk_level)
    ############################
    
    return risk_level

if __name__ == '__main__':

    reply_file = 'data_test.csv'
    generate_reply(reply_file)
    answer_record = load_reply(reply_file)
    
    risk_level_list = []
    risk_level_id = []
    for i, d in enumerate(answer_record):
        risk_level = risk_judge(answer_record, d['user_id'])
        risk_level_list.append(risk_level)
        risk_level_id.append(d['user_id'])

    # print("-"*20)
    # for i in range(len(risk_level_list)):
    #     print(risk_level_id[i], risk_level_list[i])