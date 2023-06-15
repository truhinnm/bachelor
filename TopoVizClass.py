from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import networkx as nx
import json


class VisWindow(Tk):
    def __init__(self):
        super().__init__()

        self.new_graph = nx.Graph()
        with open("data/interfaces.json", "r") as read_file:
            self.interfaces = json.load(read_file)
        with open("data/graph.json", "r") as read_file:
            self.graph = json.load(read_file)

        self.title("Topology Window")
        self.iconbitmap(default="img/app.ico")
        self.geometry("1200x700")

        self.vis_main_frame = ttk.Frame(master=self, relief=SOLID, borderwidth=1)
        self.vis_main_frame.pack(anchor=NW, expand=True, fill=BOTH)
        self.vis_main_frame.pack_propagate(False)
        self.vis_main_frame.grid_rowconfigure(0, weight=1)
        self.vis_main_frame.grid_columnconfigure(0, weight=3)
        self.vis_main_frame.grid_columnconfigure(1, weight=1)

        self.vis_topo_frame = ttk.Frame(master=self.vis_main_frame, relief=SOLID, borderwidth=1)
        self.vis_topo_frame.grid(column=0, row=0, sticky=NSEW)
        self.vis_topo_frame.grid_propagate(False)

        self.vis_data_frame = ttk.Frame(master=self.vis_main_frame, relief=SOLID, borderwidth=1)
        self.vis_data_frame.grid(column=1, row=0, sticky=NSEW)
        self.vis_data_frame.grid_propagate(False)
        self.vis_data_frame.grid_columnconfigure(0, weight=1)
        self.vis_data_frame.grid_rowconfigure(0, weight=1)

        self.device_data = Text(master=self.vis_data_frame, wrap="none", width=400, height=600, state=DISABLED)
        self.device_data.tag_configure("main_name", font="Helvetica 14 bold")
        self.device_data.tag_configure("int_name", font="Helvetica 12 bold")
        self.device_data.tag_configure("param_name", font="Helvetica 10 bold")
        self.device_data.tag_configure("value_name", font="Helvetica 10")
        self.device_data.grid(column=0, row=0, sticky=NSEW)

        self.ys = ttk.Scrollbar(master=self.vis_data_frame, orient="vertical", command=self.device_data.yview)
        self.ys.grid(column=1, row=0, sticky=NS)
        self.xs = ttk.Scrollbar(master=self.vis_data_frame, orient="horizontal", command=self.device_data.xview)
        self.xs.grid(column=0, row=1, sticky=EW)
        self.device_data["yscrollcommand"] = self.ys.set
        self.device_data["xscrollcommand"] = self.xs.set

        fig, ax = self.draw_graph(self.new_graph)

        self.h = ttk.Scrollbar(master=self.vis_topo_frame, orient=HORIZONTAL)
        self.v = ttk.Scrollbar(master=self.vis_topo_frame, orient=VERTICAL)
        self.box_canvas = Canvas(master=self.vis_topo_frame, scrollregion=(0, 0, 800, 800),
                                 bg="white", yscrollcommand=self.v.set, xscrollcommand=self.h.set)
        self.h["command"] = self.box_canvas.xview
        self.v["command"] = self.box_canvas.yview

        self.box_canvas.grid(column=0, row=0, sticky=NSEW)
        self.h.grid(column=0, row=1, sticky=EW)
        self.v.grid(column=1, row=0, sticky=NS)

        self.vis_topo_frame.grid_columnconfigure(0, weight=1)
        self.vis_topo_frame.grid_rowconfigure(0, weight=1)

        self.topo_canvas = FigureCanvasTkAgg(fig, master=self.box_canvas)
        self.toolbar = NavigationToolbar2Tk(self.topo_canvas, self.box_canvas)
        self.topo_canvas.draw()
        self.box_canvas.create_window(0, 0, anchor=NW, window=self.topo_canvas.get_tk_widget(), width=800, height=600)

        self.toolbar.update()

    def draw_graph(self, new_graph, **kwargs):

        for i in self.graph['nodes']:
            img = mpimg.imread(i['image'])
            new_graph.add_node(i['id'], image=img, source=i['id'])
        for i in self.graph['links']:
            new_graph.add_edge(i['source'], i['target'])
        plt.clf()
        sel = None
        for key, val in kwargs.items():
            if key == 'selected' and val is not None:
                sel = val
        pos = nx.planar_layout(new_graph)
        norm_list = {}
        sel_list = {}
        new_pos = {}
        for node, xy in pos.items():
            if node == sel:
                sel_list[node] = node
            else:
                norm_list[node] = node
            new_pos[node] = (xy[0], xy[1] - 0.06)
        nx.draw(new_graph, pos, width=3, with_labels=False)
        nx.draw_networkx_labels(new_graph, new_pos, norm_list, font_color='red', font_size=8)
        if len(sel_list) != 0:
            nx.draw_networkx_labels(new_graph, new_pos, sel_list, font_color='red', font_size=8, font_weight="bold")
        ax = plt.gca()
        fig = plt.gcf()
        fig.set_figheight(6)
        fig.set_figwidth(8)
        fig.canvas.mpl_connect('button_press_event', self.onclick)
        for n in new_graph.nodes():
            (x, y) = pos[n]
            imagebox = OffsetImage(new_graph.nodes[n]['image'], zoom=0.1)
            ab = AnnotationBbox(imagebox, (x, y), frameon=False)
            ax.add_artist(ab)
        return fig, ax

    def onclick(self, event):
        if event.button == 1:
            (x, y) = (event.xdata, event.ydata)
            pos = nx.planar_layout(self.new_graph)
            self.device_data.configure(state=NORMAL)
            for i in self.new_graph.nodes():
                node = pos[i]
                distance = pow(x - node[0], 2) + pow(y - node[1], 2)
                if distance < 0.015:
                    self.draw_graph(self.new_graph, selected=self.new_graph.nodes[i]['source'])
                    plt.draw()
                    self.device_data.delete("1.0", END)
                    for interface in self.interfaces:
                        if self.new_graph.nodes[i]['source'] == interface:
                            self.device_data.insert("1.0", self.new_graph.nodes[i]['source'], "main_name")
                            for data in self.interfaces[interface]:
                                if (data["ifDescr"] not in ["InLoopBack0", "NULL0", "Console9/0/0"]) and (
                                        data["ifOperStatus"] == "1"):
                                    self.device_data.insert(END, "\n" + data["ifDescr"] + ":", "int_name")
                                    for param_key, param_value in data.items():
                                        if param_key not in ["ifDescr", "ifType", "index"]:
                                            self.device_data.insert(END, "\n  "+param_key+" : ", "param_name")
                                            self.device_data.insert(END, param_value, "value_name")
            self.device_data.configure(state=DISABLED)

