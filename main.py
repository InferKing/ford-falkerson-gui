import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from string import ascii_uppercase
import config


class GraphGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)


class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Ford Falkerson')
        self.geometry('450x300')
        self.minsize(300, 200)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.configure(bg=config.BG_COLOR)

        # Menu
        self.__menu = tk.Menu()
        self.__help_menu = tk.Menu(tearoff=0)
        self.__help_menu.add_command(label='Вызвать справку', command=self.show_help)
        self.__menu.add_cascade(label='Помощь', menu=self.__help_menu)

        # Styles and some configs
        # TODO: Expand the number of possible vertex names. Now only 26 are available.
        self.__vertex_names = tuple(ascii_uppercase)
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
            background=config.BG_COLOR
        )

        self.title_lbl = ttk.Label(self, text='Поиск максимального потока', style=config.H1_STYLE_NAME)
        self.title_lbl.grid(columnspan=2, column=0, row=0, pady=15)

        self.origin_lbl = ttk.Label(self, text='Исток (O)', style=config.LBL_STYLE_NAME)
        self.origin_lbl.grid(column=0, row=1)

        self.origin_entry = ttk.Entry(self)
        self.origin_entry.grid(column=1, row=1, sticky='ew', padx=20, pady=5)

        # self.stoke_lbl = ttk.Label(self, text='Сток (Z)', style=config.LBL_STYLE_NAME)
        # self.stoke_lbl.grid(column=0, row=2)
        #
        # self.stoke_entry = ttk.Entry(self)
        # self.stoke_entry.grid(column=1, row=2, sticky='ew', padx=20, pady=5)

        self.configure(menu=self.__menu)

    def add_vertex(self):
        pass

    def show_help(self):
        print('Ну допустим')
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
