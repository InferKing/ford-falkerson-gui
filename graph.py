from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
import tkinter.ttk as ttk
from file_manager import FileManager
from data_converter import DataConverter
import config


class GraphGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg=config.BG_COLOR)
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__lbl_style = ttk.Style()
        self.__lbl_style.configure(
            config.LBL_STYLE_TL_NAME,
            font='Arial 12',
            background=config.BG_COLOR
        )

        G = nx.DiGraph()
        data = DataConverter().json_to_graph(FileManager().load_file_data(config.FILENAME))
        G.add_edges_from([(edge[0], edge[1], {'capacity': capacity}) for edge, capacity in zip(data[0], data[1])])
        pos = nx.spring_layout(G, center=(0, 0))
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)

        nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=700, node_color="skyblue", font_size=10,
                font_color="black", edge_color='red')

        nx.draw_networkx_edge_labels(G, pos, edge_labels={key: value for key, value in zip(data[0], data[1])})

        self.ax.set_title(config.TEXT_APP_TITLE)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame2 = tk.Frame(self, bg=config.BG_COLOR)
        self.frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.lbl_flow = ttk.Label(self.frame2, text=config.TEXT_BODY_RESULT_FLOW, style=config.LBL_STYLE_TL_NAME)
        self.lbl_flow.pack(pady=10)

        self.lbl_path = ttk.Label(self.frame2, text=config.TEXT_BODY_RESULT_FLOW, style=config.LBL_STYLE_TL_NAME)
        self.lbl_path.pack(pady=10)

        ford_falkerson = nx.maximum_flow(G, "O", "Z")

        self.lbl_flow['text'] = config.TEXT_BODY_RESULT_FLOW + f': {ford_falkerson[0]}'
        self.lbl_path['text'] = config.TEXT_BODY_RESULT_PATH + f': {ford_falkerson[1]}'
