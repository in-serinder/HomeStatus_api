# import psutil

import config_deal

import threading

from update_ import hardware_scan
from base import dymic_ifno
import log_make
import router_
import websocket_

from base import system_info
from  base import disk_scan
from API import base_info_api






config_deal.get_config()


# 运行日志
log_make.api_normal_log(" Server Start ")
log_make.make_log("src/public_msg.txt",f"-[Log] Server Start")
# 磁盘健康检查
check_disk=threading.Thread(target=hardware_scan.scan_start)
check_disk.start()
# 流量监视
traffic_network=threading.Thread(target=dymic_ifno.network_traffic_monitoring)
traffic_network.start()
# ws路由
# websocket_router=threading.Thread(target=websocket_.start_ws_server())



# http路由
router_.API_START()



'''
调试
'''

# disk_scan.disk_scan()
# print(disk_scan.get_disk_stats('/dev/sde')[0]['disk_health'])

# for partition in psutil.disk_partitions():
#     # print(disk_scan.get_disk_stats(partition.device),'\n')
#     #
#     print(disk_scan.get_disk_stats(partition.device)[0]['disk_standby'],'\n')
#     print(disk_scan.get_disk_stats(partition.device)[0]['disk_temp'],'\n')
#     print(disk_scan.get_disk_stats(partition.device)[0]['disk_health'],'\n')


