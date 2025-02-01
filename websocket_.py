from flask import Flask, jsonify, Blueprint
from flask_socketio import SocketIO,emit

from base import system_info

app = Flask(__name__)
app.config['SECRET_KEY']='cll'
socketio =SocketIO(app)

ws_bp=Blueprint('ws',__name__)


# eve


@socketio.on('connect', namespace='/time')
def handle_time_connect():
    print('Time WebSocket client connected')

@socketio.on('disconnect', namespace='/time')
def handle_time_disconnect():
    print('Time WebSocket client disconnected')

@socketio.on('request_time', namespace='/time')
def handle_time_request():

    current_time = system_info.get_time()
    unix_time = system_info.get_unix_time()
    emit('time_update', {'local_time': current_time, 'unixtime': f'{unix_time:.0f}'}, namespace='/time')

# 注册Blueprint
app.register_blueprint(ws_bp, url_prefix='/ws')

def start_ws_server():
    import config_deal
    ipv4 = config_deal.get_ipv4()
    socketio.run(app, host=ipv4, port=config_deal.get_ws_port())

if __name__ == '__main__':
    start_ws_server()