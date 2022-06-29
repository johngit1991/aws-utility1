# # import os
# # directory_path = "/ec2_key/ec2-key-pair1.ppk"
# # print(directory_path)
# # instance_config_file = os.path.join(os.getcwd(),*directory_path.split("/"))
# # folder_name = os.path.basename(directory_path)
# # print("My directory name is : " + instance_config_file)
# # print("My directory name is : " + folder_name)


# strA = ""

# # checking if string with space is empty
# # print("Check if the string is empty : ", end="")
# # if(len(strA)):
# #     print("The string is not empty")
# # else:
# #     print("The string is empty")


# a_file = open("log.txt", "w")
# text = "abc\n123"
# print(text, file=a_file)
# a_file.close()

# import sys
# from datetime import datetime
# f = open("log.txt","w")
# now = datetime.now()
# date = now.strftime("%d %B,%Y %H:%M:%S")
# print("----",date,"----\n")



# def custom_print(message_to_print, log_file='output.txt'):
#     print(message_to_print)
#     with open(log_file, 'a') as of:
#         date = datetime.now()
#         of.write(date + "|" + message_to_print + '\n')




# def logger():
#     restorepoint = sys.stdout
#     sys.stdout = open("./log.txt","a")
#     now = datetime.now()
#     date = now.strftime("%d %B,%Y %H:%M:%S")
#     print("----",date,"----\n")
#     print("----","CLOSED","----\n")
#     sys.stdout = restorepoint


# def logger():
#      f = open("./log.txt","a",encoding="utf-8")
#      now = datetime.now()
#      date = now.strftime("%d %B,%Y %H:%M:%S")
#      print("----",date,"----\n")


#      import sys
# from datetime import datetime

import sys
from datetime import datetime

date = datetime.now()
print(date.__str__()+' | ' + "hii" + '\n')