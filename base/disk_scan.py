import log_make
import psutil
import os
from  base import system_info

import json

jsonpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'disk_health.json'))

#扫描
def disk_scan():
    json=[]

    for partition in psutil.disk_partitions():
        json.append({
            'device': partition.device,
            'disk_standby':system_info.get_disk_standby_byos(partition.device),
            'disk_health':system_info.get_disk_health_byos(partition.device),
            'disk_temp':system_info.get_disk_temp_byos(partition.device),
        })



    disk_scanresult_save(json)
    log_make.api_hardware_log(f'Disk scan Successfully')



#存储
def disk_scanresult_save(scan_res):
    with open(jsonpath,'w')as file:
        json.dump(scan_res,file,indent=4,separators=(',', ': '))
    log_make.api_hardware_log(f'Disk Scan Results Saved Successfully!')


#从文件获取

def get_disk_stats(disk_lable):
    data = []
    json_read = []

    with open(jsonpath, 'r') as file:
        json_read = json.load(file)

    for disk in json_read:
        if disk['device'] == disk_lable:
            data.append({
                'disk_standby': disk['disk_standby'],
                'disk_health': disk['disk_health'],
                'disk_temp': disk['disk_temp'],
            })

    return data