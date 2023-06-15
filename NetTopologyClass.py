from helpers import log
import json
import re
import pprint
import copy
import code
from pyconfig import *
from datetime import datetime


class NetworkTopology:
    def __init__(self):
        self.visualization_dict = {'nodes': [], 'links': []}
        self.interfaces_dict = dict()
        self.neighborships = dict()
        try:
            with open('data/interface_stats.json') as json_file:
                self.interface_stats = json.load(json_file)
        except FileNotFoundError:
            self.interface_stats = dict()


    def classifyDeviceHostnameToGroup(self, s_device_name):
        group = "1"
        image = "img/devices/host.jpg"
        for node_pattern in NODE_HIERARCHY:
            pattern = re.compile(node_pattern[0])
            if pattern.match(s_device_name):
                group = node_pattern[1]
                image = node_pattern[2]
                break
        return group, image


    def addDevice(self, s_device_name):
        if not self.isDeviceDefined(s_device_name):
            group_number, image_name = self.classifyDeviceHostnameToGroup(s_device_name)
            self.visualization_dict['nodes'].append({"id": s_device_name, "group": group_number, "image": image_name})
            self.interfaces_dict[s_device_name] = []
            self.neighborships[s_device_name] = []
            return True
        else:
            return False


    def isDeviceDefined(self, s_device_name):
        for node in self.visualization_dict['nodes']:
            if node['id'] == s_device_name:
                return True
        return False


    def getLinkSpeedFromName(self, interface_name):
        speed = "1"
        for speed_pattern in LINK_SPEEDS:
            pattern = re.compile(speed_pattern[0])
            if pattern.match(interface_name):
                speed = speed_pattern[1]
        return speed


    def getDeviceInterfaceUtilizations(self, deviceid, interface_name):
        if deviceid not in self.interface_stats:
            return 0
        for interface in self.interface_stats[deviceid]['interfaces']:
            if interface['ifDescr'] == interface_name:
                if 'utilization' in interface:
                    return interface['utilization']
                else:
                    return 0


    def addLink(self, node_a, node_b, value, a_local_int_index, a_local_int_name, b_local_int_name):
        a_utilization = self.getDeviceInterfaceUtilizations(node_a, a_local_int_name)
        b_utilization = self.getDeviceInterfaceUtilizations(node_b, b_local_int_name)
        if a_utilization is None:
            a_utilization = 0
        if b_utilization is None:
            b_utilization = 0
        highest_utilization = max(a_utilization, b_utilization)
        for link in self.visualization_dict['links']:
            if link['source'] == node_a and link['target'] == node_b:
                if link['highest_utilization'] < highest_utilization:
                    link['highest_utilization'] = highest_utilization
                return False
            if link['source'] == node_b and link['target'] == node_a:
                link["target_interfaces"].append(a_local_int_name)
                link["target_interfaces_indes"].append(a_local_int_index)
                if link['highest_utilization'] < highest_utilization:
                    link['highest_utilization'] = highest_utilization
                return False
            if str(node_a) == str(node_b):
                return False
        if not self.isDeviceDefined(node_a):
            self.addDevice(node_a)
        if not self.isDeviceDefined(node_b):
            self.addDevice(node_b)
        self.visualization_dict['links'].append({"source": node_a,
                                                 "target": node_b,
                                                 "speed": value,
                                                 "highest_utilization": highest_utilization,
                                                 "source_interfaces": [a_local_int_name],
                                                 "source_interfaces_indes": [a_local_int_index],
                                                 "target_interfaces": [],
                                                 "target_interfaces_indes": []
                                                 })
        return True


    def dumpToJSON(self):
        with open('data/graph.json', 'w') as outfile:
            json.dump(self.visualization_dict, outfile, sort_keys=True, indent=4)
        with open('data/interfaces.json', 'w') as outfile:
            json.dump(self.interfaces_dict, outfile, sort_keys=True, indent=4)
        with open('data/interface_stats.json', 'w') as outfile:
            json.dump(self.interface_stats, outfile, sort_keys=True, indent=4)
        for device in self.interface_stats:
            for interface in self.interface_stats[device]['interfaces']:
                filename = 'data/stats/' + device + '_' + str(interface['index']) + ".json"
                with open(filename, 'w') as outfile:
                    json.dump(interface, outfile, sort_keys=True, indent=4)
        device_names_without_neighborships = []
        for k in self.neighborships:
            if len(self.neighborships[k]) == 0:
                device_names_without_neighborships.append(k)
        for k in device_names_without_neighborships:
            del self.neighborships[k]
        with open('data/neighborships.json', 'w') as outfile:
            json.dump(self.neighborships, outfile, sort_keys=True, indent=4)
        no_neighbor_interfaces = self.generateNoNeighborsInterfacesDict()
        empty_no_neighbor_keys = []
        for k in no_neighbor_interfaces:
            if len(no_neighbor_interfaces[k]) == 0:
                empty_no_neighbor_keys.append(k)
        for k in empty_no_neighbor_keys:
            del no_neighbor_interfaces[k]
        with open('data/no_neighbor_interfaces.json', 'w') as outfile:
            json.dump(no_neighbor_interfaces, outfile, sort_keys=True, indent=4)


    def getDeviceInterface(self, s_device_name, interface_index):
        for interface in self.interfaces_dict[s_device_name]:
            if interface['index'] == interface_index:
                return interface
        return


    def getDeviceInterfaceIndex(self, s_device_name, interface_name):
        for interface in self.interfaces_dict[s_device_name]:
            if str(interface['ifDescr']) == str(interface_name):
                return interface['index']
        return


    def addNeighborships(self, local_device_name, local_int_index, local_interface_name, neighbor_name,
                         neighbor_interface_name):
        for neighbor in self.neighborships[local_device_name]:
            if neighbor['local_int_index'] == local_int_index and neighbor['local_intf'] == local_interface_name and \
                    neighbor['neighbor'] == neighbor_name and neighbor['neighbor_intf'] == neighbor_interface_name:
                return False
        local_interface = self.getDeviceInterface(local_device_name, local_int_index)
        if local_interface == None:
            alternative_index = self.getDeviceInterfaceIndex(local_device_name, local_interface_name)
            local_int_index = alternative_index
        neighborship = {'local_int_index': local_int_index,
                        'local_intf': local_interface_name,
                        'neighbor': neighbor_name,
                        'neighbor_intf': neighbor_interface_name}
        self.neighborships[local_device_name].append(neighborship)


    def generateNoNeighborsInterfacesDict(self):
        no_neighbor_interfaces = dict()
        for device_a in self.interfaces_dict:
            no_neighbor_interfaces[device_a] = []
            for interface_a in self.interfaces_dict[device_a]:
                bool_interface_without_neighbor = True
                for device_b in self.neighborships:
                    if device_b == device_a:
                        for neighborship_of_device_a in self.neighborships[device_b]:
                            if neighborship_of_device_a['local_int_index'] == interface_a['index']:
                                bool_interface_without_neighbor = False
                if bool_interface_without_neighbor:
                    no_neighbor_interfaces[device_a].append(interface_a)
        return no_neighbor_interfaces

    def addDeviceInterface(self,
                           s_device_name,
                           interface_index_in_IFMIB,
                           ifDescr,
                           ifType,
                           ifMtu,
                           ifSpeed,
                           ifPhysAddress,
                           ifAdminStatus,
                           ifOperStatus
                           ):
        for ignored_iftype in IGNORED_IFTYPES:
            if ignored_iftype == str(ifType):
                return
        interface_dict = {
            'index': interface_index_in_IFMIB,
            'ifDescr': ifDescr,
            'ifType': ifType,
            'ifMtu': ifMtu,
            'ifSpeed': ifSpeed,
            'ifPhysAddress': ifPhysAddress,
            'ifAdminStatus': ifAdminStatus,
            'ifOperStatus': ifOperStatus
        }
        self.interfaces_dict[s_device_name].append(interface_dict)


    def addInterfaceStats(self,
                          deviceid,
                          INDEX,
                          ifDescr,
                          ifType,
                          ifOperStatus,
                          ifHCInOctets,
                          ifHCOutOctets,
                          ifHighSpeed
                          ):
        for ignored_iftype in IGNORED_IFTYPES:
            if ignored_iftype == str(ifType):
                return
        if ifOperStatus != "up":
            return
        now = datetime.now()
        print("Now: " + str(now))
        timestamp = int(datetime.timestamp(now))
        print("Timestamp: " + str(timestamp))
        if deviceid not in self.interface_stats:
            device_interfaces_stats = {
                "interfaces": [
                    {
                        "index": INDEX,
                        "ifDescr": ifDescr,
                        "last_timestamp": timestamp,
                        "last_ifHCInOctets": ifHCInOctets,
                        "last_ifHCOutOctets": ifHCOutOctets,
                        "stats": [

                        ]
                    }

                ]
            }

        else:

            device_interfaces_stats = self.interface_stats[deviceid]
            interface_found = False
            for interface in device_interfaces_stats['interfaces']:
                if interface['index'] == INDEX:
                    interface_found = True
                    device_interface_stats = interface
                    break
            if not interface_found:
                device_interface_stats = {
                    "index": INDEX,
                    "ifDescr": ifDescr,
                    "last_timestamp": timestamp,
                    "last_ifHCInOctets": ifHCInOctets,
                    "last_ifHCOutOctets": ifHCOutOctets,
                    "stats": [

                    ]
                }
                device_interfaces_stats['interfaces'].append(device_interface_stats)
            else:
                if len(device_interface_stats['stats']) > MAX_STATS_RECORDS:
                    device_interface_stats['stats'].pop(0)
                last_ifHCInOctets = int(device_interface_stats['last_ifHCInOctets'])
                last_ifHCOutOctets = int(device_interface_stats['last_ifHCOutOctets'])
                last_timestamp = int(device_interface_stats["last_timestamp"])
                if int(ifHCInOctets) >= last_ifHCInOctets and int(ifHCOutOctets) >= last_ifHCOutOctets:
                    delta_time = timestamp - last_timestamp
                    delta_ifHCInOctets = int(ifHCInOctets) - last_ifHCInOctets
                    delta_ifHCOutOctets = int(ifHCOutOctets) - last_ifHCOutOctets

                    InSpeed = int(delta_ifHCInOctets * 8 / 1024 / 1024 / delta_time)
                    OutSpeed = int(delta_ifHCOutOctets * 8 / 1024 / 1024 / delta_time)
                    utilization = int(max(InSpeed, OutSpeed) / int(ifHighSpeed) * 100)
                    device_interface_stats['utilization'] = utilization

                    device_interface_stats['stats'].append(
                        {
                            "time": now.strftime('%Y-%m-%d %H:%M:%S'),
                            "InSpeed": InSpeed,
                            "OutSpeed": OutSpeed
                        }
                    )
                device_interface_stats['last_ifHCInOctets'] = ifHCInOctets
                device_interface_stats['last_ifHCOutOctets'] = ifHCOutOctets
                device_interface_stats["last_timestamp"] = timestamp

        self.interface_stats[deviceid] = device_interfaces_stats
