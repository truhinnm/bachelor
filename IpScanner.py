import os
import platform
import threading
import socket
from datetime import datetime





def next_ip(ip_ad):
    ip_split = ip_ad.split('.')
    if ip_split[3] == '255':
        ip_split[3] = '0'
        if ip_split[2] == '255':
            ip_split[2] = '0'
            if ip_split[1] == '255':
                ip_split[1] = '0'
                ip_split[0] = str(int(ip_split[0])+1)
            else:
                ip_split[1] = str(int(ip_split[1])+1)
        else:
            ip_split[2] = str(int(ip_split[2])+1)
    else:
        ip_split[3] = str(int(ip_split[3])+1)
    return ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + '.' + ip_split[3]


def get_my_ip(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    s.connect((ip, 0))
    print(s.getsockname())
    return s.getsockname()[0]


def scan_ip(ip, ping_com, alive_ips):
    comm = ping_com + ip
    response = os.popen(comm)
    data = response.readlines()
    for line in data:
        if 'TTL' in line:
            print(ip, "--> Ping Ok")
            alive_ips.append(ip)
            break


def full_scan(my_ip, start_ip, last_ip):
    alive_ips = []
    net = get_my_ip(my_ip)
    print('You IP :', net)
    oc = platform.system()
    if oc == "Windows":
        ping_com = "ping -n 1 "
    else:
        ping_com = "ping -c 1 "

    t1 = datetime.now()
    print("Scanning in Progress:")
    curr_ip = start_ip
    iplist = []
    while curr_ip != last_ip:
        if curr_ip == net:
            curr_ip = next_ip(curr_ip)
            continue
        iplist.append(curr_ip)
        curr_ip = next_ip(curr_ip)

    for ip in iplist:
        potoc = threading.Thread(target=scan_ip, args=[ip, ping_com, alive_ips])
        potoc.start()

    potoc.join()
    t2 = datetime.now()
    total = t2 - t1
    print("Scanning completed in: ", total)
    return alive_ips


