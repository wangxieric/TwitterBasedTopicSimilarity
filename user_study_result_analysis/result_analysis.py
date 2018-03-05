import json
import pickle
import operator
from scipy.stats import ranksums
import numpy as np

'''
    Trasform the json file into processable variable
'''
result = []
with open("result.json","r") as f:
    for line in f:
        result.append(json.loads(line))

methods = ['CS', 'WE', 'JS', 'HD']
choose_reason = {}
choose_reason[1] = 0
choose_reason[2] = 0
choose_reason[3] = 0
count_jud = 0
user_count = set()
for i in range(len(methods)):
    for j in range(i+1, len(methods)):
        # result_list
        result_list = {methods[i]: [], methods[j]: []}
        for row in result:
            # Construct the count for correspond method
            count = {methods[i]: 0, methods[j]: 0}
            tid = row['results']['judgments'][0]['unit_data']['tid']
            com_methods = [tid[6:8],tid[10:12]]
            count_either = 0
            if methods[i] in com_methods and methods[j] in com_methods:
                for judge in row["results"]["judgments"]:
                    count_jud += 1
                    if judge["data"]["choose_a_candidate_topic_which_is_similar_to_the_given_base_topic"] == \
                            "candidate_topic_1":
                        count[com_methods[0]] = count[com_methods[0]] + 1
                    elif judge["data"]["choose_a_candidate_topic_which_is_similar_to_the_given_base_topic"] == \
                            "candidate_topic_2":
                        count[com_methods[1]] = count[com_methods[1]] + 1
                    elif judge["data"]["choose_a_candidate_topic_which_is_similar_to_the_given_base_topic"] == \
                            "either_of_them":
                        count_either += 1
                    if "choose_reasons" in judge["data"].keys():
                        if judge["data"]["choose_reasons"] == "Easy (1)":
                            choose_reason[1] += 1
                        elif judge["data"]["choose_reasons"] == "Reasonable (2)":
                            choose_reason[2] += 1
                        elif judge["data"]["choose_reasons"] == "Hard (3)":
                            choose_reason[3] += 1
                    user_count.add(judge["worker_id"])
                if count[methods[i]] > count[methods[j]]:
                    result_list[methods[i]].append(1)
                    result_list[methods[j]].append(0)
                    print "i: " + str(tid)
                elif count[methods[i]] < count[methods[j]]:
                    result_list[methods[i]].append(0)
                    result_list[methods[j]].append(1)
                    print "j: " + str(tid)
                else:
                    result_list[methods[i]].append(0)
                    result_list[methods[j]].append(0)
        print methods[i], sum(result_list[methods[i]]) / float(len(result_list[methods[i]]))
        print methods[j], sum(result_list[methods[j]]) / float(len(result_list[methods[j]]))
        print methods[i] + " : ", result_list[methods[i]], "\n" + methods[j] + " : ", result_list[methods[j]], "\n"
        print ranksums(result_list[methods[i]], result_list[methods[j]])

for key in choose_reason:
    print key, choose_reason[key]

print len(user_count)
print count_jud
