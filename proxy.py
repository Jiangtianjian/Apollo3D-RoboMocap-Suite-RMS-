import getopt
import socket
import struct
import sys
import time

import sexp_parser as parser
import monitor_cmd
import worldModel


def deal_param(argv):
    agentNum = 1
    host = '127.0.0.1'  # default
    serverPort = 3100  # proxy<->server default
    agentPort = 3000  # agent<->proxy
    monitorPort = 3200  # proxy->monitor default
    try:
        opts, args = getopt.getopt(argv, "hs:a:")
    except getopt.GetoptError:
        print('proxy.py -s <toServerPort> -a <toAgentPort>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('proxy.py -s <toServerPort> -a <toAgentPort>')
            sys.exit()
        elif opt == '-s':
            serverPort = arg
        elif opt == '-a':
            agentPort = arg
    return agentNum, host, serverPort, agentPort, monitorPort


def proxy_init(agentAddress, serverAddress, monitorAddress):
    toAgent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    toAgent.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    toServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    toMonitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    toAgent.bind(agentAddress)
    toAgent.listen(1)
    print("waiting……")
    toAgentSocket, toAgentAddress = toAgent.accept()
    print("connect to agent!")
    toAgentSocket.settimeout(10)

    toServer.connect(serverAddress)
    print("connect to server!")
    toServer.settimeout(10)

    toMonitor.connect(monitorAddress)
    print("connect to Monitor!")
    toMonitor.settimeout(10)

    return toAgentSocket, toServer, toMonitor


def deal_agentList(agentList):  # msg from agent
    filtered_list = [sublist for sublist in agentList if 'say' not in sublist[0]]  

    return filtered_list


def deal_serverList(serverList):  # msg from server
    return serverList


def set_joint(joint, val):
    msg = ['O', [joint, str(val)]]
    return msg


angles = [0] * 20
speed = [0] * 20
last_speed = [0] * 20
last_angles = [0] * 20

# !remember:open syn mode
if __name__ == '__main__':
    agentList, serverList = [], []
    agentNum, host, serverPort, agentPort, monitorPort = deal_param(sys.argv[1:])

    agentAddress = (host, agentPort)
    serverAddress = (host, serverPort)
    monitorAddress = (host, monitorPort)

    agentConnect, serverConnect, monitorConnect = proxy_init(agentAddress, serverAddress, monitorAddress)
    agentType = 2
    world = worldModel.WorldModel(agentType)

    static_num = 0
    start_pt = 0
    start_shoot_sig = False
    has_begun_record = 0
    last_ball = [0, 0, 0]
    agent_started = False

    while True:

        try:  # agent -> proxy -> server
            agentRawData = agentConnect.recv(4096)
            if len(agentRawData) > 0:
                agentDecodeData = agentRawData.decode(encoding="unicode_escape")
                # agentHeader = agentRawData[:4]
                agentData = agentDecodeData[4:]
                agentList = parser.sexp_decode(agentData)
                agentList = deal_agentList(agentList)
                agentEncodeData = parser.sexp_encode(agentList)
                msgLen = socket.htonl(len(agentEncodeData))
                agentPrefix = struct.pack('<I', msgLen)
                sendToServer = agentPrefix + agentEncodeData.encode(encoding="unicode_escape")
                serverConnect.sendall(bytes(sendToServer))
        except Exception as err:
            print("agent ERROR:")
            print(err)
            exit(1)

        try:  # server -> proxy -> agent
            serverRawData = serverConnect.recv(4096)
            if len(serverRawData) > 0:
                serverDecodeData = serverRawData.decode(encoding="unicode_escape", errors="ignore")
                # serverHeader = serverRawData[:4]
                serverData = serverDecodeData[4:]
                serverList = parser.sexp_decode(serverData)
                serverList = deal_serverList(serverList)
                serverEncodeData = parser.sexp_encode(serverList)
                msgLen = socket.htonl(len(serverEncodeData))
                serverPrefix = struct.pack('<I', msgLen)
                sendToAgent = serverPrefix + serverEncodeData.encode(encoding="unicode_escape")
                agentConnect.sendall(bytes(sendToAgent))
        except Exception as err:
            print("server ERROR:")
            print(err)
            exit(2)

        try:  # proxy -> monitor
            monitorCMD = monitor_cmd.reqFullState()
            # monitorCMD = monitor_cmd.setBallPos(5, 5, 0)
            msgLen = socket.htonl(len(monitorCMD))
            monitorPrefix = struct.pack('<I', msgLen)
            sendToMonitor = monitorPrefix + monitorCMD.encode(encoding="unicode_escape")
            monitorConnect.sendall(sendToMonitor)
        except Exception as err:
            print("monitor ERROR:")
            print(err)
            exit(3)

        world.updateWorld(serverList, agentList)

        if not agent_started:
            agent_start_time = time.time()
            agent_started = True

        # Get Parameters
        angles = list(world.perceptor_dict.values())
        angles = angles[2:]

        # Get Start-Record Signal
        if world.perceptor_dict['laj3'] > -70 and time.time() - agent_start_time > 3:
            start_shoot_sig = True

        if not start_shoot_sig:
            continue
        ball = world.worldModel_dict['ball']

        # Set sample rate
        sr = 0
        if start_shoot_sig:
            if static_num == sr:
                print("{} 0 0".format(str(sr)), end=' ')
                for angle in angles:
                    print(angle, end=' ')
                # Type 0,1,2,3 don't have toes
                if agentType!=4:
                    print('0 0')
                else:
                    print('')
                static_num = 0
            else:
                static_num = static_num + 1

        last_angles = angles.copy()
        last_speed = speed.copy()
        last_ball = ball.copy()