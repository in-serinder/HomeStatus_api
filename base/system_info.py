import getpass
import os
import socket
import subprocess
import json
import platform
import GPUtil
import cpuinfo
import pyudev
import psutil

import collection
import config_deal
import log_make

from base import disk_scan

def get_usr():
    info=len(psutil.users())  #-Login:{getpass.getuser()
    return info

def get_os():
    if platform.system()=="Linux":
        info=f"{platform.release()} "
    else:
        info=f"{platform.system()}-{platform.version()}"
    return info

#cpu分两个
def get_cpu():
    info=((cpuinfo.get_cpu_info()['brand_raw']).replace("Intel(R)",'')).replace("CPU",'')
    # info=cpuinfo.get_cpu_info()
    return info

def get_cpu_usage(): #获取状态信息
    cpu_usage=psutil.cpu_percent(interval=1)
    return cpu_usage

def get_cpu_th():
    cpu_freq=psutil.cpu_freq()
    return (cpu_freq.current)/1000



def get_cpu_temp():
    info=psutil.sensors_temperatures().get('coretemp')
    if info>70:
        log_make.api_hardware_log(f" [Warning] The CPU temperature has currently exceeded 70℃--Current:{info}%")
    return info

def get_gpu():
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            log_make.api_hardware_log("GPU Not Found")
            return "NotFound"

        else:
            info = gpus[0].name
            if "NVIDIA" in info:
                info = info.replace("NVIDIA", "NV")
            return info
    except IndexError:
        log_make.api_hardware_log("GPU Not Found Or DATA ERROR")
        return "NotFound"

def get_memory():
    size_total=((psutil.virtual_memory().total/1024)/1024)
    size_used = ((psutil.virtual_memory().used / 1024) / 1024)
    if (size_used/size_total*100)>85:
        log_make.api_hardware_log(f" [Warning] Memory usage space is tight 85% | Current:{size_used/size_total:2f}%")
    info =f"{size_total:.1f}/{size_used:.1f}MB" if size_total<=1024 else f"{(size_total/1024):.1f}/{(size_used/1024):.1f}GB"
    return info

def get_swap():
    size_total=((psutil.swap_memory().total)/1024)/1024
    size_used=((psutil.swap_memory().used)/1024)/1024
    if (size_used/size_total*100)>85:
        log_make.api_hardware_log(f" [Warning] Swap Space usage space is tight 85% | Current:{size_used/size_total:2f}%")
    info =f"{size_total:.1f}/{size_used:.1f}MB" if size_total<=1024 else f"{(size_total/1024):.1f}/{(size_used/1024):.1f}GB"
    return info

def get_ip():
    ip=socket.gethostbyname(socket.gethostname())
    return ip


def get_process_num():
    info=len(psutil.pids())
    return info


def get_logis():
    return config_deal.get_log_isuse()



def is_usb_device(device):
    context = pyudev.Context()
    device = pyudev.Devices.from_device_file(context, device)
    if device.get('ID_BUS') == 'usb':
        return True
    return False

def get_disk_status():
    disk_status=[]
    disk_stats=[]
    for partition in psutil.disk_partitions():
        disk_usage=psutil.disk_usage(partition.mountpoint)
        devices=partition.device
        mountpoint=partition.mountpoint


        disk_stats=disk_scan.get_disk_stats(devices)[0]
        print('转移',devices,disk_stats)

        if is_usb_device(partition.device):
            devices=f"(USB) {partition.device}"
        total=(disk_usage.total/1024)
        used=(disk_usage.used/1024)    #kb
        usage_rate=(used/total)*100
        # print('\n调试分区',devices,'\n')
        # print('\n调试', disk_scan.get_disk_stats(devices)[0]['disk_standby'], '\n',
        #       disk_scan.get_disk_stats(devices)[0]['disk_temp'], '\n',
        #       disk_scan.get_disk_stats(devices)[0]['disk_health'])
        disk_status.append({
            'device':f"{devices} ({mountpoint})",   #容量格式化后输出
            'total_space':f"{total:.0f}KB" if total<=1024 else (f"{total/1024:.1f}MB" if total<=1048576 else f"{(total/1024)/1024:.1f}GB"),
            'use_space':f"{used:.0f}KB" if used<=1024 else (f"{used/1024:.1f}MB" if used<=1048576 else f"{(used/1024)/1024:.1f}GB"),
            'usage_rate':f"{usage_rate:.2f}",   #删除%
            'disk_standby':disk_stats['disk_standby'],    #莫名超出索引问题，调试未找出问题
            'disk_temp':disk_stats['disk_temp'],
            'disk_health':disk_stats['disk_health'],
        })

        if usage_rate>90 :
            log_make.api_hardware_log(f"Disk usage space is tight-{devices}-{usage_rate:.2f}%")
            log_make.make_log("src/public_msg.txt", f"-[Log] Warning Disk usage space is tight-{usage_rate:.2f}% in {mountpoint}")
    return disk_status

def get_disk_standby_byos(disk_lable):
    disk_standby=False
    res=os.popen(f'smartctl -n standby {disk_lable}').read()
    print(f'文件：{res}')
    if res.find('STANDBY')!=-1:
        disk_standby=True
        return disk_standby
    return disk_standby





def get_disk_temp_byos(disk_lable):
    disk_temp="none"
    # res=os.popen(f'smartctl -A {disk_lable} | grep Temperature' ).read()
    res=int(collection.get_command_output(f'smartctl -A {disk_lable} | grep "Temperature_Celsius" | awk \'{{print $10}}\''))
    # res2=res.find('(')
    # if res2!=-1:
    #     disk_temp=int(res[res2-4:res2-1])
        # disk_temp=res2[res2-1:res2+1]
        # return disk_temp

    disk_temp=res
    return disk_temp

def get_disk_health_byos(disk_lable):
    count=0
    # disk_overall_health=os.popen(f'smartctl -H {disk_lable} | grep "SMART overall-health self-assessment" | awk \'{{print $6}}\'').read()
    # disk_rea_sec_count=os.popen(f'smartctl -A {disk_lable} | grep "Reallocated_Sector_Ct" | awk \'{{print $10}}\'').read()
    # disk_uncorrect_count=os.popen(f'smartctl -A {disk_lable} | grep "Current_Pending_Sector" | awk \'{{print $10}}\'').read()
    # disk_pend_sector_count=os.popen(f'smartctl -A {disk_lable} | grep "Current_Pending_Sector" | awk \'{{print $10}}\'').read()
    # disk_temp=os.popen(f'smartctl -A {disk_lable} | grep "Temperature_Celsius" | awk \'{{print $10}}\'').read()


    disk_rea_sec_count=int(collection.get_command_output(f'smartctl -A {disk_lable} | grep "Reallocated_Sector_Ct" | awk \'{{print $10}}\''))
    disk_uncorrect_count=int(collection.get_command_output(f'smartctl -A {disk_lable} | grep "Current_Pending_Sector" | awk \'{{print $10}}\''))
    disk_pend_sector_count=int(collection.get_command_output(f'smartctl -A {disk_lable} | grep "Current_Pending_Sector" | awk \'{{print $10}}\''))
    disk_temp = int(collection.get_command_output(f'smartctl -A {disk_lable} | grep "Temperature_Celsius" | awk \'{{print $10}}\''))


    disk_overall_health=os.popen(f'smartctl -H {disk_lable} | grep "SMART overall-health self-assessment" | awk \'{{print $6}}\'').read()


    # print(f'数据{disk_rea_sec_count} \t {disk_uncorrect_count} \t {disk_pend_sector_count}')
    count=int(disk_rea_sec_count+disk_uncorrect_count+disk_pend_sector_count)+count

    if disk_temp > 35 :
        count=count+(disk_temp-35)
    if disk_overall_health == 'FAILED':
        count=count+50
    if disk_overall_health == 'UNKNOWN':
        count=count+10
    # 参照50
    return count