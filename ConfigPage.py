from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import re
from pyconfig import *
from network_mapper import main
from IpScanner import full_scan
from TopoVizClass import VisWindow


def check_ip(ip):
    valid_ip = re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)"
                        r"{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip)
    return valid_ip


def ip_scanner():
    print(ip_list)
    fst_ip = fst_ip_entry.get()
    last_ip = last_ip_entry.get()
    my_ip = my_ip_entry.get()
    if check_ip(fst_ip) and check_ip(last_ip) and check_ip(my_ip):
        if fst_ip < last_ip:
            scan_err_msg.set("Scanning...")
            scan_err_label['foreground'] = "yellow"
            new_list = full_scan(my_ip, fst_ip, last_ip)
            for ip in new_list:
                print(ip_list_box['values'])
                if ip not in ip_list_box['values']:
                    ip_list.append(ip)
                    if len(ip_list_box['values']) == 0:
                        ip_list_box['values'] += ip
                    else:
                        ip_list_box['values'] += (ip,)
            scan_err_msg.set("Alive IPs added to list")
            scan_err_label['foreground'] = "green"
            print(ip_list)
        else:
            scan_err_label['foreground'] = "red"
            scan_err_msg.set("Wrong range")
    else:
        scan_err_label['foreground'] = "red"
        scan_err_msg.set("Wrong IP Address")


def params_edit():
    if ifDescr.get() == 1:
        params_list[1][0][1] = 1
    else:
        params_list[1][0][1] = 0
    if ifType.get() == 1:
        params_list[1][1][1] = 1
    else:
        params_list[1][1][1] = 0
    if ifMTU.get() == 1:
        params_list[1][2][1] = 1
    else:
        params_list[1][2][1] = 0
    if ifSpeed.get() == 1:
        params_list[1][3][1] = 1
    else:
        params_list[1][3][1] = 0
    if ifPhysAddress.get() == 1:
        params_list[1][4][1] = 1
    else:
        params_list[1][4][1] = 0
    if ifAdminStatus.get() == 1:
        params_list[1][5][1] = 1
    else:
        params_list[1][5][1] = 0
    if ifOperStatus.get() == 1:
        params_list[1][6][1] = 1
    else:
        params_list[1][6][1] = 0
    if ifHCInOctets.get() == 1:
        params_list[1][7][1] = 1
    else:
        params_list[1][7][1] = 0
    if ifHCOutOctets.get() == 1:
        params_list[1][8][1] = 1
    else:
        params_list[1][8][1] = 0
    if ifHighSpeed.get() == 1:
        params_list[1][9][1] = 1
    else:
        params_list[1][9][1] = 0
    if lldpRemSysName.get() == 1:
        params_list[2][0][1] = 1
    else:
        params_list[2][0][1] = 0
    if lldpRemSysDesc.get() == 1:
        params_list[2][1][1] = 1
    else:
        params_list[2][1][1] = 0
    if lldpRemPortId.get() == 1:
        params_list[2][2][1] = 1
    else:
        params_list[2][2][1] = 0
    if lldpRemPortDesc.get() == 1:
        params_list[2][3][1] = 1
    else:
        params_list[2][3][1] = 0


def add_ip():
    new_ip = ip_entry.get()
    if check_ip(new_ip):
        if new_ip not in ip_list_box['values']:
            err_msg.set("")
            ip_list.append(new_ip)
            if len(ip_list_box['values']) == 0:
                ip_list_box['values'] += new_ip
            else:
                ip_list_box['values'] += (new_ip,)
        else:
            err_msg.set("Duplicate IP")
    else:
        err_msg.set("Non-valid IP")


def delete_ip():
    new_ip_list = []
    for ip in ip_list_box['values']:
        if ip != ip_list_box.get():
            new_ip_list.append(ip)
        else:
            ip_list.remove(ip_list_box.get())
    ip_list_box['values'] = new_ip_list
    ip_list_box.delete(0, 'end')
    ip_list_box.set("")


def start_scan():
    if comm_str_entry.get() != "":
        comm_msg.set("")
        comm_string.append(comm_str_entry.get())
        main()
        vis_window = VisWindow()
    else:
        comm_msg.set("Please, enter Community String")


# INITIATE WINDOW
root = Tk()
root.title("LocateTopology")
root.iconbitmap(default="img/app.ico")
root.geometry("700x1000")

container = ttk.Frame(root)
canvas = Canvas(container, width=650, height=1000)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
main_frame = ttk.Frame(canvas)
main_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=main_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# MAIN NAME
label = ttk.Label(master=main_frame, text="LOCATE TOPOLOGY v1", font=("Impact", 28))
label.pack()

# CONFIG FRAME
configframe = ttk.Frame(master=main_frame, borderwidth=1, relief=SOLID, padding=[8, 10])

ip_scan_label = ttk.Label(configframe, text="IP Scanner")
ip_scan_label.pack(anchor=NW)

scan_ip_frame = ttk.Frame(master=configframe, relief=SOLID, padding=[8, 10])
scan_ip_data_frame = ttk.Frame(master=scan_ip_frame, relief=SOLID, padding=[8,10])
fst_ip_label = ttk.Label(master=scan_ip_data_frame, text="Enter starting IP")
my_ip_label = ttk.Label(master=scan_ip_data_frame, text="Enter your IP")
last_ip_label = ttk.Label(master=scan_ip_data_frame, text="Enter last IP")
fst_ip_entry = ttk.Entry(scan_ip_data_frame)
last_ip_entry = ttk.Entry(scan_ip_data_frame)
my_ip_entry = ttk.Entry(scan_ip_data_frame)
my_ip_label.grid(column=0, row=0)
fst_ip_label.grid(column=0, row=1)
last_ip_label.grid(column=0, row=2)
my_ip_entry.grid(column=1, row=0)
fst_ip_entry.grid(column=1, row=1)
last_ip_entry.grid(column=1, row=2)
scan_ip_data_frame.pack(side=LEFT, padx=5, pady=5)
scan_ip_button = ttk.Button(master=scan_ip_frame, text="Scan", command=ip_scanner)
scan_err_msg = StringVar()
scan_err_label = ttk.Label(master=scan_ip_frame, foreground="red", textvariable=scan_err_msg, wraplength=250)
scan_err_label.pack(side=LEFT, padx=5, pady=5)
scan_ip_button.pack(side=RIGHT, padx=5, pady=5)


scan_ip_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

ip_label = ttk.Label(configframe, text="Enter IP")
ip_label.pack(anchor=NW)

add_ip_frame = ttk.Frame(master=configframe, relief=SOLID, padding=[8, 10])

ip_entry = ttk.Entry(add_ip_frame)
ip_entry.pack(side=LEFT)

err_msg = StringVar()
error_label = ttk.Label(master=add_ip_frame, foreground="red", textvariable=err_msg, wraplength=250)
error_label.pack(padx=5, pady=5, side=LEFT)

add_ip_button = ttk.Button(master=add_ip_frame, text="Add IP", command=add_ip)
add_ip_button.pack(side=RIGHT)

add_ip_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

ip_del_label = ttk.Label(configframe, text="Edit IP List")
ip_del_label.pack(anchor=NW)

del_ip_frame = ttk.Frame(master=configframe, relief=SOLID, padding=[8, 10])

ip_list_box = ttk.Combobox(master=del_ip_frame, state="readonly", values=ip_list)
ip_list_box.pack(side=LEFT)

del_ip_button = ttk.Button(master=del_ip_frame, text="Remove IP", command=delete_ip)
del_ip_button.pack(side=RIGHT)

del_ip_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

comm_str_label = ttk.Label(configframe, text="Enter Community String")
comm_str_label.pack(anchor=NW)
comm_str_frame = ttk.Frame(master=configframe, relief=SOLID, padding=[8, 10])

comm_str_entry = ttk.Entry(comm_str_frame)
comm_str_entry.pack(side=LEFT)

comm_msg = StringVar()
comm_label = ttk.Label(master=comm_str_frame, foreground="red", textvariable=comm_msg, wraplength=250)
comm_label.pack(padx=5, pady=5, side=LEFT)

comm_str_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

configframe.pack(anchor=NW, fill=X, padx=5, pady=5)

# PARAMS FRAME
checkboxframe = ttk.Frame(master=main_frame, borderwidth=1, relief=SOLID, padding=[8, 10])

checkboxframe.rowconfigure(0, weight=1)

# ip_mib_frame = ttk.Frame(master=checkboxframe, relief=SOLID, padding=[8, 10])
#
# ip_mib_label = ttk.Label(ip_mib_frame, text="Select IP data")
# ip_mib_label.pack(anchor=NW)
#
# ip_mib_frame.grid(column=0, row=0, sticky=NSEW, padx=6)

if_mib_frame = ttk.Frame(master=checkboxframe, relief=SOLID, padding=[8, 10])
if_mib_label = ttk.Label(if_mib_frame, text="Select interface data")
if_mib_label.pack(anchor=NW)

ifDescr = IntVar()
ifDescr_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface Description",
                                      variable=ifDescr, command=params_edit)
ifDescr_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifType = IntVar()
ifType_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface Type",
                                     variable=ifType, command=params_edit)
ifType_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifMTU = IntVar()
ifMTU_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface MTU",
                                    variable=ifMTU, command=params_edit)
ifMTU_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifSpeed = IntVar()
ifSpeed_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface Speed",
                                      variable=ifSpeed, command=params_edit)
ifSpeed_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifPhysAddress = IntVar()
ifPhysAddress_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface Physical Address",
                                            variable=ifPhysAddress, command=params_edit)
ifPhysAddress_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifAdminStatus = IntVar()
ifAdminStatus_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface Admin Status",
                                            variable=ifAdminStatus, command=params_edit)
ifAdminStatus_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifOperStatus = IntVar()
ifOperStatus_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface Oper Status",
                                           variable=ifOperStatus, command=params_edit)
ifOperStatus_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifHCInOctets = IntVar()
ifHCInOctets_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface HCInOctets",
                                           variable=ifHCInOctets, command=params_edit)
ifHCInOctets_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifHCOutOctets = IntVar()
ifHCOutOctets_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface HCOutOctets",
                                            variable=ifHCOutOctets, command=params_edit)
ifHCOutOctets_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

ifHighSpeed = IntVar()
ifHighSpeed_checkbutton = ttk.Checkbutton(master=if_mib_frame, text="Interface High Speed",
                                          variable=ifHighSpeed, command=params_edit)
ifHighSpeed_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

if_mib_frame.grid(column=1, row=0, sticky=NSEW, padx=6)

lldp_mib_frame = ttk.Frame(master=checkboxframe, relief=SOLID, padding=[8, 10])
lldp_mib_label = ttk.Label(lldp_mib_frame, text="Select LLDP data")
lldp_mib_label.pack(anchor=NW)

lldpRemSysName = IntVar()
lldpRemSysName_checkbutton = ttk.Checkbutton(master=lldp_mib_frame, text="LLDP Neighbour System Name",
                                             variable=lldpRemSysName, command=params_edit)
lldpRemSysName_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

lldpRemSysDesc = IntVar()
lldpRemSysDesc_checkbutton = ttk.Checkbutton(master=lldp_mib_frame, text="LLDP Neighbour System Description",
                                             variable=lldpRemSysDesc, command=params_edit)
lldpRemSysDesc_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

lldpRemPortId = IntVar()
lldpRemPortId_checkbutton = ttk.Checkbutton(master=lldp_mib_frame, text="LLDP Neighbour Port Id",
                                            variable=lldpRemPortId, command=params_edit)
lldpRemPortId_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

lldpRemPortDesc = IntVar()
lldpRemPortDesc_checkbutton = ttk.Checkbutton(master=lldp_mib_frame, text="LLDP Neighbour Port Description",
                                              variable=lldpRemPortDesc, command=params_edit)
lldpRemPortDesc_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

lldpLocPortId = IntVar()
lldpLocPortId_checkbutton = ttk.Checkbutton(master=lldp_mib_frame, text="LLDP Neighbour Local Port ID",
                                            variable=lldpLocPortId, command=params_edit)
lldpLocPortId_checkbutton.pack(anchor=NW, fill=X, padx=5, pady=5)

lldp_mib_frame.grid(column=2, row=0, sticky=NSEW, padx=6)

checkboxframe.pack(anchor=NW, fill=X, padx=5, pady=5)

run_button_style = ttk.Style().configure("RunStyle.TButton", background='#008000')
run_button = ttk.Button(master=main_frame, text="Start Scanning!", style="RunStyle.TButton", command=start_scan)
run_button.pack(anchor=N, padx=6, pady=6, ipadx=10, ipady=2)

container.pack(anchor=NW, fill=X, padx=5, pady=[5, 60])
canvas.pack(side=LEFT, fill="both", expand=True)
scrollbar.pack(side=RIGHT, fill="y")

root.mainloop()
