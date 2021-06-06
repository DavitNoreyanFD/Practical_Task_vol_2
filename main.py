"""
module main.py main working module where imported websocketserver module
"""
import websocketserver
import  constants

if __name__ == '__main__':
    ip, prt = (constants.ip, constants.port)
    websocketserver.websocket_running_func(ip, prt )