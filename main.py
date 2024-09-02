import config_deal

import threading

from update_ import hardware_scan
from base import dymic_ifno
import log_make
import router_

from base import system_info
from API import base_info_api



config_deal.get_config()
log_make.api_normal_log(" Server Start ")
log_make.make_log("src/public_msg.txt",f"-[Log] Server Start")

check_disk=threading.Thread(target=hardware_scan.scan_start)
check_disk.start()

traffic_network=threading.Thread(target=dymic_ifno.network_traffic_monitoring)
traffic_network.start()

router_.API_START()

