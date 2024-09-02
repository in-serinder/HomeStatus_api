import threading
import time
import socket
import psutil
import collection
#细分获取,格式单位计算在前端

#流量
traffic_lock=threading.Lock #用于安全共享
i_list=[]




def get_cpu_temp():
    temp=psutil.sensors_temperatures().get('coretemp')
    for core_temp in temp:
        cpu_tmep = core_temp.current if temp else None  # 判空值
        all_temp=+cpu_tmep
    average_core_temp = all_temp/len(temp)
    return average_core_temp    #返回平均温度


def get_memory():
    memory=psutil.virtual_memory()    #mb
    list={"total":(memory.total/1024)/1024,
          "used":(memory.used/1024)/1024,
          "free":(memory.free/1024)/1024,
          "usage_rate":(memory.used/memory.total)*100
          }
    return list

def get_swap():
    swap=psutil.swap_memory()
    list={
        "total":(swap.total/1024)/1024,
        "used":(swap.used/1024)/1024,
        "free":(swap.free/1024)/1024,
        "usage_rate":(swap.used/swap.total)*100
    }
    return list

def get_network():
    # io_list=[]
    # net_io=psutil.net_io_counters(pernic=True)
    # print(i_list)
    # for interface,io in net_io.items():
    #     io_list.append({
    #         "interface":f"{interface}",
    #         "send_data":f"{collection.byte_upward_format(io.bytes_sent,'bit')}",
    #         "recv_data":f"{collection.byte_upward_format(io.bytes_recv,'bit')}",
    #         # "upload":f"{collection.byte_upward_format(i_list['upload'])}",
    #         # "download":f" "
    #     })
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host='127.0.0.1'
    port=880
    client.connect((host, port))
    data=client.recv(1024).decode()

    return data

def network_traffic_monitoring():   #线程锁住
    global i_list
    while True:
        net_io_current= psutil.net_io_counters(pernic=True)
        with traffic_lock: #共享
            i_list=[]
            for interface,io in net_io_rece.items():
                upload=net_io_current.bytes_sent-io.bytes_sent
                download=net_io_current.bytes_recv-io.bytes_recv    #对校后
                i_list.append({
                    "upload":upload,
                    "download":download
                })
        net_io_rece=net_io_current
        time.sleep(1)