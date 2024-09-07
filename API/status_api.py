from base import system_info,dymic_ifno


def json_data():
    json={
        "cpu":[{
            "cpu_name": system_info.get_cpu(),
            "usage":system_info.get_cpu_usage(),
            "temp":dymic_ifno.get_cpu_temp(),
            "freq":f"{system_info.get_cpu_th():.2f}GHz"
        }],
        "mem":[
            {
                "total":f"{dymic_ifno.get_memory()['total']:.2f}MB" ,
                "used": f"{dymic_ifno.get_memory()['used']:.2f}MB",
                # "free":f"{dymic_ifno.get_memory()['free']:.2f}MB",
                "usage_rate":f"{dymic_ifno.get_memory()['usage_rate']:.2f}"
            }
        ],
        "swap":[
            {
                "total":f"{dymic_ifno.get_swap()['total']:.2f}MB" if dymic_ifno.get_swap()['total']<1024 else f"{dymic_ifno.get_swap()['total']/1024:.2f}GB",
                "used":f"{dymic_ifno.get_swap()['used']:.2f}" if dymic_ifno.get_swap()['used']<1024 else f"{dymic_ifno.get_swap()['used']/1024:.2f}GB",
                # "free":f"{dymic_ifno.get_swap()['free']:.2f}" if dymic_ifno.get_swap()['free']<1024 else f"{dymic_ifno.get_swap()['free']/1024:.2f}GB"
                "usage_rate": f"{dymic_ifno.get_swap()['usage_rate']:.2f}"
            }
        ],

        # "network":dymic_ifno.get_network(),
    }

    return json


def json_data_disk():
    json={
        "disk": system_info.get_disk_status(),
    }
    return json