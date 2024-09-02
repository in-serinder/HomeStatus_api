import log_make
from base import system_info


def json_data():
    json_data = {
        "user":system_info.get_usr(),
        "os": system_info.get_os(),
        "cpu": system_info.get_cpu(),
        "gpu": system_info.get_gpu(),
        "mem": system_info.get_memory(),
        "swap": system_info.get_swap(),
        "ip": system_info.get_ip(),
        "process": system_info.get_process_num(),
        "log": system_info.get_logis(),
        "disk": system_info.get_disk_status()
    }
    # log_make.api_hardware_log("Hardware information obtained successfully")
    return json_data

