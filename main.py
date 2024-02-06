import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from os import system
from vertex_name_generator import VertexNameGenerator
import config


class GraphGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)


class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Ford Falkerson')
        self.__min_size = (440, 390)
        self.geometry(f'{self.__min_size[0]}x{self.__min_size[1]}')
        self.minsize(self.__min_size[0], self.__min_size[1])
        # self.resizable(False, True)

        for ind in range(3):
            self.columnconfigure(ind, weight=1)
        self.configure(bg=config.BG_COLOR)

        # Menu
        self.__menu = tk.Menu()
        self.__help_menu = tk.Menu(tearoff=0)
        self.__help_menu.add_command(label='Вызвать справку', command=lambda: system('start README.md'))
        self.__menu.add_cascade(label='Помощь', menu=self.__help_menu)

        # Styles and some configs
        self.__h1_style = ttk.Style()
        self.__h1_style.configure(
            config.H1_STYLE_NAME,
            font='Arial 15',
            background=config.BG_COLOR
        )
        self.__lbl_style = ttk.Style()
        self.__lbl_style.configure(
            config.LBL_STYLE_NAME,
            font='Arial 11',
            background=config.BG_CANVAS_COLOR
        )

        self.title_lbl = ttk.Label(self, text='Поиск максимального потока', style=config.H1_STYLE_NAME)
        self.title_lbl.grid(columnspan=3, column=0, row=0, pady=15)

        # Separate window for fields
        self.canvas = tk.Canvas(self, bg=config.BG_CANVAS_COLOR)
        self.canvas.grid(column=0, columnspan=3, row=1)
        self.update()

        self.scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        self.scrollbar.grid(sticky='nse', column=3, row=1)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame = tk.Frame(self.canvas, padx=2)
        self.canvas.create_window(0, 0, window=self.frame, anchor=tk.NW, width=self.canvas.winfo_width())
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        temp_frame = self.create_temp_frame()
        self.origin_lbl = ttk.Label(temp_frame, text='Исток (O)', style=config.LBL_STYLE_NAME)
        self.origin_lbl.grid(column=0, row=2)
        self.origin_entry = ttk.Entry(temp_frame)
        self.origin_entry.grid(column=1, row=2, **config.ENTRY_STYLE_DICT)

        self.add_vertex_btn = ttk.Button(self, text='Добавить вершину', command=self.add_vertex_gui)
        self.add_vertex_btn.grid(column=0, row=2, **config.BTN_STYLE_DICT)

        self.remove_vertex_btn = ttk.Button(self, text='Удалить вершину', command=self.remove_vertex_gui)
        self.remove_vertex_btn.grid(column=1, row=2, **config.BTN_STYLE_DICT)

        self.show_graph_btn = ttk.Button(self, text='Перейти к графу', command=self.show_graph_gui)
        self.show_graph_btn.grid(column=2, row=2, columnspan=2, **config.BTN_STYLE_DICT)

        self.configure(menu=self.__menu)

        self.__raw_data = []

        # self.frame = tk.Frame(self)
        # self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #
        # self.fig = Figure(figsize=(5, 5))
        # self.ax = self.fig.add_subplot(111)
        #
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        # self.canvas.get_tk_widget().pack_forget()
        #
        # self.button = tk.Button(self, text="Draw Graph", command=self.show_graph_gui)
        # self.button.pack(side=tk.BOTTOM)

    def remove_vertex_gui(self):
        if not self.__raw_data:
            return
        items = self.__raw_data.pop()
        for item in items:
            item.destroy()
        VertexNameGenerator.decrease_counter()
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_temp_frame(self):
        temp_frame = tk.Frame(self.frame, bg=config.BG_CANVAS_COLOR)
        for ind in range(3):
            temp_frame.columnconfigure(ind, weight=1)
        temp_frame.pack(expand=True, side=tk.TOP, fill=tk.BOTH)
        return temp_frame

    def add_vertex_gui(self):
        temp_frame = self.create_temp_frame()
        lbl = ttk.Label(temp_frame, text=VertexNameGenerator.get_vertex_name(), style=config.LBL_STYLE_NAME, width=5)
        lbl.grid(column=0, row=0)
        entry = ttk.Entry(temp_frame)
        entry.grid(column=1, row=0, **config.ENTRY_STYLE_DICT)

        self.__raw_data.append((lbl, entry, temp_frame))
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def show_graph_gui(self):
        graph_window = GraphGUI(self)
        graph_window.grab_set()

    # def draw_graph(self):
    #     self.ax.clear()
    #
    #     G = nx.DiGraph()
    #     G.add_nodes_from([1, 2, 3, 4, 5])
    #     G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
    #
    #     pos = nx.spring_layout(G)
    #     nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=700, node_color="skyblue", font_size=10,
    #             font_color="black", edge_color='gray')
    #     self.ax.set_title("Ориентированный граф с Tkinter")
    #     self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    #     self.canvas.draw()


def main():
    app = MainGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
