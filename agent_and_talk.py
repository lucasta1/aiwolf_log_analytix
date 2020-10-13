#coding:utf-8
import sys
import glob
import csv

args = sys.argv
path_list = glob.glob(str(args[1])+'/*')

lib = {}
lib_jud = {}
agent_name = set()
agent_all = [0] * 15
agent_all_dict = {}

agent_talk = {}

# 各々のファイルパスを読み込み
for path in path_list:
    # ファイル読み込み
    with open(path) as f:
        talk_all = f.readlines()
        for i in talk_all:
            log = i.split(",")
            if(log[1] == "status" and int(log[0]) == 0):
                agent_all[int(log[2])-1] = str(log[5].replace("\n", "")) + " " + log[3]
                agent_name.add(str(log[5].replace("\n", "")))

                if log[5].replace("\n", "") not in agent_all_dict.keys():
                    agent_all_dict[log[5].replace("\n", "")] = []

                if log[5].replace("\n", "") not in agent_talk.keys():
                    agent_talk[log[5].replace("\n", "")] = []
                agent_talk[log[5].replace("\n", "")].append("●"+agent_all[int(log[2])-1]+"\n")


            if(log[1] == "talk"):
                agent, _ = agent_all[int(log[4])-1].split()

                l = log[5].split()
                if l[0] == "Skip" or l[0] == "Over" or l[0] == "VOTE":
                    pass
                else:
                    if agent not in agent_talk.keys():
                        agent_talk[agent] = []
                    agent_talk[agent].append(log[5])
                # if agent not in agent_talk.keys():
                #     agent_talk[agent] = []
                # agent_talk[agent].append(log[5])


cnt = 0
for i in range(len(agent_name)):
    agent, _ = agent_all[i].split()
    cnt += 1
    file_name = "talk_agent_" + str(cnt)
    with open(agent + '.txt', 'a') as file:
        try:
            for j in agent_talk[agent]:
                with open(agent + '.txt', 'a') as file:
                    file.write(j)
        except:
            pass

# cnt = 0
# for j in range(len(agent_name)):
#     agent, _ = agent_all[j].split()
#     cnt += 1
#     file_name = "talk_agent_" + str(cnt)
#     with open(file_name + '.txt', 'a') as file:
#         file.write(agent_all[j]+"\n")
#     for j in agent_talk[agent]:
#         with open(file_name+'.txt', 'a') as file:
#             file.write(j)
