import getpass
import socket
import subprocess
import json
import platform
import GPUtil
import cpuinfo
import pyudev
import psutil

import config_deal
import log_make


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
    for partition in psutil.disk_partitions():
        disk_usage=psutil.disk_usage(partition.mountpoint)
        devices=partition.device
        mountpoint=partition.mountpoint
        if is_usb_device(partition.device):
            devices=f"(USB) {partition.device}"
        total=(disk_usage.total/1024)
        used=(disk_usage.used/1024)    #kb
        usage_rate=(used/total)*100
        disk_status.append({
            'device':f"{devices} ({mountpoint})",   #容量格式化后输出
            'total_space':f"{total:.0f}KB" if total<=1024 else (f"{total/1024:.1f}MB" if total<=1048576 else f"{(total/1024)/1024:.1f}GB"),
            'use_space':f"{used:.0f}KB" if used<=1024 else (f"{used/1024:.1f}MB" if used<=1048576 else f"{(used/1024)/1024:.1f}GB"),
            'usage_rate':f"{usage_rate:.2f}"    #删除%
        })
        if usage_rate>90 :
            log_make.api_hardware_log(f"Disk usage space is tight-{devices}-{usage_rate:.2f}%")
            log_make.make_log("src/public_msg.txt", f"-[Log] Warning Disk usage space is tight-{usage_rate:.2f}% in {mountpoint}")
    return disk_status

