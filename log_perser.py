#coding:utf-8
import sys
import glob

args = sys.argv
path_list = glob.glob(str(args[1])+'/*')
path_w = 'dtest_w.txt'

cnt = 1

# SS PS WS MM WM WV
# 6 種類の役職の特定

lib = {"SS":{}, "PS":{}, "WS":{}, "MM":{}, "WM":{}, "WV":{}}


for path in path_list:
    with open(path_w, mode='a') as f:
        f.write("------game "+str(cnt)+"------\n")
    cnt += 1
    agent_all = [0] * 15
    with open(path) as f:
        talk_all = f.readlines()
        for i in talk_all:
            log = i.split(",")
            if(log[1] == "status" and log[0] != 1):
                agent_all[int(log[2])-1] = str(log[5].replace("\n", "")) + "==" + log[3]
                #print("-----")
                if(log[3]=="SEER"):
                    seer_info = "●" + str(log[3]) + " == " + str(log[5].replace("\n", "")) + "\n"
                if(log[3] == "POSSESSED"):
                    possessed_info = "●" + str(log[3]) + " == " + log[5].replace("\n", "") + "\n"

            if(log[1] == "talk"):
                if (len(log[5]) >= 10):
                    if(log[5][0:9] == "COMINGOUT"):
                        w = log[5].split()
                        w[1] = agent_all[int(w[1][6:8])-1]
                        w.insert(0, "day"+str(log[0]))

                        w = str(w).replace("[", "")
                        w = str(w).replace("]", "")
                        w = str(w).replace(",", "")
                        w = str(w).replace("'", "")
                        w += "\n"

                        with open(path_w, mode='a') as f:
                            f.write(w)

        with open(path_w, mode='a') as f:
            f.write(seer_info)
            f.write(possessed_info)
