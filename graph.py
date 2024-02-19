from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from file_manager import FileManager
from data_converter import DataConverter
import tree_view_validator as tvv
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
import tkinter.ttk as ttk
import config
import customtkinter as ctk


class GraphGUI(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.set_appearance_mode(config.APPEARANCE_MODE)

        self.G, self.pos, self.ax = None, None, None
        self.__display_options_select = {
            config.TEXT_OPTION_NO_ZERO: tvv.WithoutZeroData(),
            config.TEXT_OPTION_ANY: tvv.AnyData()
        }

        self.title(config.TEXT_APP_TITLE)
        self.resizable(False, False)
        self.frame = tk.Frame(self, bg=config.CANVAS_COLOR)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(30, 0))

        self.data = DataConverter().json_to_graph(FileManager().load_file_data(config.FILENAME_DATA))
        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)

        self.draw_graph()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)

        self.btn_redraw = ctk.CTkButton(self.frame, text=config.TEXT_BTN_REDRAW, command=self.draw_graph, bg_color='white')
        self.btn_redraw.place(x=20, rely=0.9)

        self.frame2 = tk.Frame(self, bg=self.cget('bg'))
        self.frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.lbl_flow = ctk.CTkLabel(self.frame2, text=config.TEXT_BODY_RESULT_FLOW)
        self.lbl_flow.pack(pady=7)

        self.ford_falkerson = nx.maximum_flow(self.G, config.TEXT_SOURCE, config.TEXT_STOCK)

        self.lbl_flow.configure(text=config.TEXT_BODY_RESULT_FLOW + f': {self.ford_falkerson[0]}')

        self.tree_data_preparer = tvv.TreeViewDataPreparer(tvv.AnyData())
        print(self.tree_data_preparer.prepare_data(self.ford_falkerson[1]))
        self.df = self.tree_data_preparer.prepare_data(self.ford_falkerson[1])

        self.tree = ttk.Treeview(self.frame2, padding=10, show='headings', columns=list(self.df.columns))
        self.vsb = ctk.CTkScrollbar(self.frame2, orientation='vertical', command=self.tree.yview)
        self.vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.vsb.set)

        for column in self.df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)

        self.__display_table()
        self.tree.pack(expand=True, fill=tk.BOTH, padx=(10, 5))

        self.display_options = ctk.CTkComboBox(self.frame2, values=config.TEXT_OPTION_VALUES,
                                               command=self.on_display_option_select, width=250)
        self.display_options.set(config.TEXT_OPTION_ANY)
        self.display_options.pack(pady=10)

    def on_display_option_select(self, event):
        selected_option = self.display_options.get()
        if selected_option not in self.__display_options_select:
            raise KeyError(f'Insert your option in dict {self.__display_options_select}')
        self.tree_data_preparer.strategy = self.__display_options_select.get(selected_option)
        self.df = self.tree_data_preparer.prepare_data(self.ford_falkerson[1])
        self.__display_table()

    def __display_table(self):
        self.tree.delete(*self.tree.get_children())
        for index, row in self.df.iterrows():
            self.tree.insert('', 'end', values=tuple(row))

    def draw_graph(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.G, self.pos = self.__create_graph()
        nx.draw(self.G, self.pos, ax=self.ax, with_labels=True, node_size=500, node_color="skyblue",
                font_size=9, font_color="black", edge_color='red', style='solid', node_shape='8')

        nx.draw_networkx_edge_labels(self.G, self.pos,
                                     edge_labels={key: value for key, value in zip(self.data[0], self.data[1])},
                                     label_pos=0.6,
                                     rotate=False)
        self.ax.set_title(config.TEXT_APP_TITLE)
        self.canvas.draw()

    def __create_graph(self):
        G = nx.DiGraph()
        G.add_edges_from(
            [(edge[0], edge[1], {'capacity': capacity}) for edge, capacity in zip(self.data[0], self.data[1])])
        pos = nx.spring_layout(G, k=len(self.data[1]))
        return G, pos
