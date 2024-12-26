from  flask import Flask,jsonify,render_template,request,send_from_directory
from flask_cors import CORS
#
import config_deal
from API import base_info_api
from API import status_api
import  log_make
import collection
import os.path



ipv4=config_deal.get_ipv4()

app=Flask(__name__)
CORS(app)
#base_info

@app.route('/api/baseinfo',methods=['GET'])
def base_info():
    log_make.api_use_log(f'API-[base-info] user IP:{request.remote_addr} URL:{request.path} Method:{request.method}')
    return jsonify(base_info_api.json_data())

@app.route('/api/status')
def status():

    return status_api.json_data()

@app.route('/api/status/disk')
def status_disk():

    return status_api.json_data_disk()

#log
@app.route('/api/error_log')
def error_log():
    json={
        "contect":collection.read_log_msg(50,config_deal.get_err_log())
    }
    log_make.api_use_log(f'API-[error_log] user IP:{request.remote_addr} URL:{request.path} Method:{request.method}')
    return jsonify(json)

@app.route('/api/api_log')
def api_log():
    json={
        "contect":collection.read_log_msg(50,config_deal.get_api_use_log())
    }
    log_make.api_use_log(f'API-[api_log] user IP:{request.remote_addr} URL:{request.path} Method:{request.method}')
    return jsonify(json)

@app.route('/api/visiter_log')  #访问
def visiter_log():
    json={
        "contect":collection.read_log_msg(50,config_deal.get_normal_log())
    }
    log_make.api_use_log(f'API-[visiter_log] user IP:{request.remote_addr} URL:{request.path} Method:{request.method}')
    return jsonify(json)

@app.route('/api/hardware_log')
def hardware_log():
    json={
        "contect":collection.read_log_msg(50,config_deal.get_hardware_log())
    }
    log_make.api_use_log(f'API-[hardware_log] user IP:{request.remote_addr} URL:{request.path} Method:{request.method}')
    return jsonify(json)


@app.route('/api/public_msg')
def public_msg():
    json={
        "contect":collection.read_log_msg(20,"src/public_msg.txt")
    }
    log_make.api_use_log(f'API-[public_message] user IP:{request.remote_addr} URL:{request.path} Method:{request.method}')
    return jsonify(json)


@app.route('/api/disk_stat_table')
def disk_stat_table():
    json={
        "contect":""
    }
    log_make.api_use_log(f'API-[disk_stat_table] user IP:{request.remote_addr} URL:{request.path} Method:{request.method}')
    return jsonify(json)


#文件共享

@app.route('/src/<path:filename>')
def shared_files(filename):
    # 设置共享文件的目录
    shared_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),  "src")
    return send_from_directory(shared_dir, filename)


@app.route('/download/<path:filename>')
def download_file(filename):
    # 设置共享文件的目录
    shared_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),  "src")

    # 发送文件
    return send_from_directory(shared_dir, filename)


@app.route('/api/status_d')
def dynamic_status():
    json={
        "contect":status_api.json_data()
    }




def API_START():
    app.run(host=ipv4,port=config_deal.get_master_port())

# if __name__ == '__main__':
#     API_START()
