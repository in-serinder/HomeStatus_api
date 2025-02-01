import json
import os
import datetime

import log_make

json_data={
    "creat_date":datetime.datetime.now().isoformat(),
    "log_use":True,
    "api_use_log":"api_use.log",    #api使用时，记录访客和使用信息
    "err_log":"err.log",        #错误发生
    "normal_log":"log.log",     #普通log，资源刷新，公共信息刷新等等(不显示)
    "hardware_log":"hardware.log",
    "master_port":6324,
    "custom_port":True,
    "res_dir_port":6000,
    "base_info_api_port":6325,
    "log_api_port":6326,
    "public_msg_api_port":6327,
    "status_api":6328,
    "webinfo_api":6329,
    "disk_warn_threshold":90,
    "scan_time":4,
    "ipv4":'127.0.0.1'
}

config_file= "config.json"
file_data={}


def exist_config():
    if not os.path.exists(config_file):     #存在?
        with open("config.json", "w")as file:
            json.dump(json_data,file,indent=4)
    else:
        try:
            config_data=file_data
            #校验
            for key,value in json_data.items():
                if key not in config_data:
                    config_data[key]=value  #修复
        except FileNotFoundError:
            log_make.config_err("Json Config File Not Found")




def get_config():   #处理配置文件
    print("sdsd")
    global file_data
    exist_config()
    with open(config_file,"r")as file:
        file_data=json.load(file)




def get_log_isuse():
    return file_data['log_use']

#get存储位置
def get_api_use_log():
    try:
        return file_data['api_use_log']
        exist_config()
    except KeyError:
        log_make.config_err("JSON key value error---[api_use_log]")


def get_err_log():
    try:
        return file_data['err_log']
        exist_config()
    except KeyError:
        log_make.config_err("JSON key value error---[err_log]")


def get_normal_log():
    try:
        return file_data['normal_log']
        exist_config()
    except KeyError:
        log_make.config_err("JSON key value error---[normal_log]")


def get_hardware_log():
    try:
        return file_data['hardware_log']
        exist_config()
    except KeyError:
        log_make.config_err("JSON key value error---[hardware_log]")

def get_ipv4():
    # print("sdsda",file_data)
    try:
        exist_config()
        return file_data['ipv4']
    except KeyError:
        log_make.config_err("JSON key value error---[ipv4]")



#get_port
    # "res_dir_port":6324,
    # "base_info_api_port":6325,
    # "log_api_port":6326,
    # "public_msg_api_port":6327,
    # "status_api":6328,
    # "webinfo_api":6329

def custom_port():
    if file_data['custom_port']:
        return True
    else:
        return False


def get_master_port():  #主端口
    return file_data['master_port']

def get_res_dir_port():
    return file_data['res_dir_port'] if custom_port() else 6000

def get_base_info_api_port():
    return file_data['base_info_api_port'] if custom_port() else 6325

def get_log_api_port():
    return file_data['log_api_port'] if custom_port() else 6326

def get_public_msg_api_port():
    return file_data['public_msg_api_port'] if custom_port() else 6327

def get_status_api():
    return file_data['status_api'] if custom_port() else 6328

def get_webinfo_api():
    return file_data['webinfo_api'] if custom_port() else 6329


# 配置
def get_disk_warn_threshold():
    return file_data['disk_warn_threshold']


def get_scan_time():
    return file_data['scan_time']

