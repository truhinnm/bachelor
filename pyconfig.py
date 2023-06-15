ip_list = []
params_list = [
    [],
    [
        [('IF-MIB', 'ifDescr'), 0],
        [('IF-MIB', 'ifType'), 0],
        [('IF-MIB', 'ifMtu'), 0],
        [('IF-MIB', 'ifSpeed'), 0],
        [('IF-MIB', 'ifPhysAddress'), 0],
        [('IF-MIB', 'ifAdminStatus',), 0],
        [('IF-MIB', 'ifOperStatus'), 0],
        [('IF-MIB', 'ifHCInOctets'), 0],
        [('IF-MIB', 'ifHCOutOctets'), 0],
        [('IF-MIB', 'ifHighSpeed'), 0]
    ],
    [
        [('LLDP-MIB', 'lldpRemSysName'), 0],
        [('LLDP-MIB', 'lldpRemSysDesc'), 0],
        [('LLDP-MIB', 'lldpRemPortId'), 0],
        [('LLDP-MIB', 'lldpRemPortDesc'), 0]
    ],
    [('SNMPv2-MIB', 'sysName', 0)],
    [('SNMPv2-MIB', 'sysDescr', 0)]
]
comm_string = []

MAX_STATS_RECORDS = 2016

LINK_SPEEDS = [("^TwentyGigE*", "20"),
               ("^FortyGig*", "40"),
               ("^Ten-GigabitEthernet*", "10"),
               ("^GigabitEthernet*", "1")]

NODE_HIERARCHY = [
                  ('^AR', "3", "img/devices/router.jpg"),
                  ('^LSW', "2", "img/devices/switch.jpg")
                  ]

IGNORED_IFTYPES = [ "l3ipvlan", "softwareLoopback", "other"]