#coding:utf-8
import sys
import glob
import csv

# v2 では同一ゲーム内の同一 CO をカウントしないように設定した

args = sys.argv
path_list = glob.glob(str(args[1])+'/*')

lib = {}
lib_jud = {}
agent_name = set()
agent_all = [0] * 15
agent_all_dict = {}
cnt = 0

# 各々のファイルパスを読み込み
for path in path_list:
    # ファイル読み込み
    with open(path) as f:
        # ファイル内の log の全部を取得して，それらを一行ずつ処理する
        # (ex) 1,talk,9,1,3,DIVINED Agent[05] HUMAN
        talk_all = f.readlines()
        for i in talk_all:
            log = i.split(",")
            # 0 日目の'status' で役職を取得することができる
            # (ex) 0,status,5,POSSESSED,ALIVE,HALU
            if(log[1] == "status" and int(log[0]) == 0):
                # agent_all では エージェントの ID_num-1 のインデックスにエージェントの名前と真の役職を格納している
                # agent_name では　全てのエージェントの名前を set 変数に格納している
                agent_all[int(log[2])-1] = str(log[5].replace("\n", "")) + " " + log[3]
                agent_name.add(str(log[5].replace("\n", "")))

                if log[5].replace("\n", "") not in agent_all_dict.keys():
                    agent_all_dict[log[5].replace("\n", "")] = {}
                if log[3] not in agent_all_dict[log[5].replace("\n", "")].keys():
                    agent_all_dict[log[5].replace("\n", "")][log[3]] = 0
                agent_all_dict[log[5].replace("\n", "")][log[3]] += 1


            if(log[1] == "talk"):
                if (len(log[5]) >= 10):
                    if(log[5][0:9] == "COMINGOUT"):
                        w = log[5].split()
                        w[1] = agent_all[int(w[1][6:8])-1]
                        l = w[1].split()
                        key_name = l[1][0]+w[2][0]

                        if key_name not in lib.keys():
                            lib[key_name] = {}
                        if l[0] not in lib[key_name].keys():
                            lib[key_name][l[0]] = 0

                        if key_name not in lib_jud.keys():
                            lib_jud[key_name] = {}
                        if l[0] not in lib_jud[key_name].keys():
                            lib_jud[key_name][l[0]] = 0

                        lib_jud[key_name][l[0]] += 1

                        if lib_jud[key_name][l[0]] == 1:
                            lib[key_name][l[0]] += 1

        roleTF = list(lib.keys())
        agent_n = list(agent_name)
        for roleTF_e in roleTF:
            for agent in agent_n:
                if roleTF_e not in lib_jud.keys():
                    lib_jud[roleTF_e] = {}
                if agent not in lib_jud[roleTF_e].keys():
                    lib_jud[roleTF_e][agent] = 0
                lib_jud[roleTF_e][agent] = 0



# 要は実装したいのは空の成分を作らない，空なら0にするってしたい
all_role = ['BODYGUARD', 'POSSESSED', 'WEREWOLF', 'VILLAGER', 'SEER', 'MEDIUM']
role_s = list(agent_all_dict.keys())
for agent in agent_name:
    for role in all_role:
        if agent not in agent_all_dict.keys():
            lib[agent] = {}
        if role not in agent_all_dict[agent].keys():
            lib[agent][role] = 0

# role_serve = []
# all_role_index = list(all_role)[:]
# all_role_index.insert(0,"-")
# role_serve.append(all_role_index)
#
# for agent in list(agent_name):
#     content = [agent]
#     for role in all_role:
#         if role != "-":
#             content.append(agent_all_dict[agent][role])
#     role_serve.append(content)
#
# with open('role_servance.csv', 'w') as file:
#   writer = csv.writer(file)
#   writer.writerows(role_serve)


roleTF = list(lib.keys())
agent_name = list(agent_name)

roleTF.insert(0,"-")

for roleTF_e in roleTF:
    for agent in agent_name:
        if roleTF_e not in lib.keys():
            lib[roleTF_e] = {}
        if agent not in lib[roleTF_e].keys():
            lib[roleTF_e][agent] = 0

grand = []
a = roleTF[:]
grand.append(a)

for i in range(len(agent_name)):
    b = [agent_name[i]]
    agent_name_tmp = agent_name[i]
    for j in roleTF:
        if j != "-":
            # print(roleTF)
            # print(j, agent_name_tmp)
            b.append(lib[j][agent_name_tmp])
    grand.append(b)

with open('data_v2.csv', 'w') as file:
  writer = csv.writer(file)
  writer.writerows(grand)
