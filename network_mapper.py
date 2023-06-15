import pprint
import argparse
import textwrap
import json
import quicksnmp
from pysnmp.hlapi import *
import code
import helpers
from helpers import log
from helpers import get_params_list
from NetTopologyClass import NetworkTopology
from pyconfig import *
import time


def main():
    topology_model = NetworkTopology()

    for device in ip_list:
        device = device.replace('\n', '')
        try:
            sSNMPHostname = quicksnmp.get(device, params_list[3], CommunityData(comm_string[0]))
        except RuntimeError as e:
            continue
        except (ValueError, TypeError):
            continue
        try:
            rawInterfacesTable = quicksnmp.get_table(device, get_params_list(params_list[1]),
                                                     CommunityData(comm_string[0]))
        except RuntimeError as e:
            continue
        except (ValueError, TypeError):
            continue
        try:
            rawTable = quicksnmp.get_table(device, get_params_list(params_list[2]),
                                           CommunityData(comm_string[0]))
        except RuntimeError as e:
            continue
        except (ValueError, TypeError):
            continue

        topology_model.addDevice(str(sSNMPHostname[0][1]))

        for row in rawInterfacesTable:
            oid = tuple(row[0][0])
            topology_model.addDeviceInterface(str(sSNMPHostname[0][1]),
                                              oid[-1],
                                              str(row[0][1]),
                                              str(row[1][1]),
                                              str(row[2][1]),
                                              str(row[3][1]),
                                              str(row[4][1].prettyPrint()),
                                              str(row[5][1]),
                                              str(row[6][1]))

            topology_model.addInterfaceStats(str(sSNMPHostname[0][1]),
                                             oid[-1],
                                             str(row[0][1]),
                                             str(row[1][1]),
                                             str(row[6][1]),
                                             str(row[7][1]),
                                             str(row[8][1]),
                                             str(row[9][1]))

        for row in rawTable:
            oid = tuple(row[0][0])
            local_in_index = oid[-2]
            local_interface_name = quicksnmp.get(device, [('LLDP-MIB', 'lldpLocPortId', local_in_index)],
                                                 CommunityData(comm_string[0]))
            local_in_index = topology_model.getDeviceInterfaceIndex(str(sSNMPHostname[0][1]),
                                                                    str(local_interface_name[0][1]))

            topology_model.addLink(str(sSNMPHostname[0][1]),
                                   str(row[0][1]),
                                   topology_model.getLinkSpeedFromName(str(row[2][1])),
                                   local_in_index,
                                   str(local_interface_name[0][1]),
                                   str(row[2][1])
                                   )
            topology_model.addNeighborships(str(sSNMPHostname[0][1]),
                                            local_in_index,
                                            str(local_interface_name[0][1]),
                                            str(row[0][1]),
                                            str(row[2][1]))
    topology_model.dumpToJSON()
    del topology_model

    return 0
