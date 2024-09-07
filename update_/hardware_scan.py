import time

from base import system_info
from base import disk_scan
import config_deal
import log_make


def disk_warning():
    data=system_info.get_disk_status()

    for usage in data:
        if float(usage['usage_rate']) > config_deal.get_disk_warn_threshold():
            log_make.make_log("src/public_msg.txt", f"-[Log] Warning Disk usage space is tight-{usage['usage_rate']}% in {usage['device']}")





def scan_start():
    while True:
        disk_scan.disk_scan()
        disk_warning()
        time.sleep(config_deal.get_scan_time() *60 *60)