import os
import datetime

import config_deal




def make_log(path,contect):
    if config_deal.get_log_isuse():
        if not os.path.exists(path):
            with open(path, "w") as file:
                file.write(f"{datetime.datetime.now().isoformat()[:-7]} Log Created\n")
                #first
            with open(path, "a") as file:
                file.write('[' + datetime.datetime.now().isoformat() + ']\t' + contect + '\n')
        else:
         with open(path,"a") as file:
            file.write('['+datetime.datetime.now().isoformat()+']\t'+contect+'\n')



def config_err(contect):
    make_log(config_deal.get_err_log(),contect)

def err_log(contect): #辨识度
    make_log(config_deal.get_err_log(), contect)


def api_use_log(contect):
    make_log(config_deal.get_api_use_log(), contect)

def api_hardware_log(contect):
    make_log(config_deal.get_hardware_log(), contect)

def api_normal_log(contect):    #不再前端显示
    make_log(config_deal.get_normal_log(), contect)





