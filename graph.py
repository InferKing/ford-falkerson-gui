from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
import tkinter.ttk as ttk
from file_manager import FileManager
from data_converter import DataConverter
import config
import customtkinter as ctk

class GraphGUI(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.set_appearance_mode(config.APPEARANCE_MODE)
        self.title(config.TEXT_APP_TITLE)
        self.resizable(False, False)
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.data = DataConverter().json_to_graph(FileManager().load_file_data(config.FILENAME_DATA))

        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)

        self.draw_graph()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.btn_redraw = ctk.CTkButton(self.frame, text=config.TEXT_BTN_REDRAW, command=self.draw_graph)
        self.btn_redraw.place(x=20, rely=0.9)

        self.frame2 = tk.Frame(self, bg=self.cget('bg'))
        self.frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.lbl_flow = ctk.CTkLabel(self.frame2, text=config.TEXT_BODY_RESULT_FLOW)
        self.lbl_flow.pack(pady=7)

        self.lbl_path = ctk.CTkLabel(self.frame2, text=config.TEXT_BODY_RESULT_FLOW)
        self.lbl_path.pack(pady=7, padx=10)

        ford_falkerson = nx.maximum_flow(self.G, config.TEXT_SOURCE, config.TEXT_STOCK)

        self.lbl_flow.configure(text=config.TEXT_BODY_RESULT_FLOW + f': {ford_falkerson[0]}')
        self.lbl_path.configure(text=config.TEXT_BODY_RESULT_PATH + f': {ford_falkerson[1]}')
    
    def draw_graph(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.G, self.pos = self.__create_graph()
        nx.draw(self.G, self.pos, ax=self.ax, with_labels=True, node_size=700, node_color="skyblue", font_size=10,
                font_color="black", edge_color='red')

        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels={key: value for key, value in zip(self.data[0], self.data[1])})
        self.ax.set_title(config.TEXT_APP_TITLE)
        self.canvas.draw()

    
    def __create_graph(self):
        G = nx.DiGraph()
        G.add_edges_from([(edge[0], edge[1], {'capacity': capacity}) for edge, capacity in zip(self.data[0], self.data[1])])
        pos = nx.spring_layout(G, k=len(self.data[1]))
        return G, pos

