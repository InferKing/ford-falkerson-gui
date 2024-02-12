from tkinter import ttk
from os import system
from vertex_name_generator import VertexNameGenerator
from data_converter import DataConverter
from file_manager import FileManager
from logger import LogMixin
from tkinter.messagebox import showerror
import config
import graph
import logging
import tkinter as tk
import customtkinter as ctk


class MainTabView(ctk.CTkTabview, LogMixin):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add(config.TEXT_TABVIEW_MAIN)
        self.add(config.TEXT_TABVIEW_HELP)
        self.set(config.TEXT_TABVIEW_MAIN)

        for ind in range(3):
            self.tab(self.get()).columnconfigure(ind, weight=1)

        self.title_lbl = ctk.CTkLabel(self.tab(self.get()), text=config.TEXT_BODY_TITLE, font=('Arial', 22))
        self.title_lbl.grid(columnspan=3, column=0, row=0, pady=15)

        # Separate window for fields
        self.canvas = tk.Canvas(self.tab(self.get()), highlightthickness=0, bg=master.cget('bg'))
        self.canvas.grid(column=0, columnspan=3, row=1)


        self.t1 = ctk.CTkLabel(self.canvas, text='12345', width=200)
        # self.scrollbar = ctk.CTkScrollbar(self.tab(self.get()), command=self.canvas.yview)
        # self.scrollbar.grid(sticky='nse', column=3, row=1)
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # self.frame = tk.Frame(self.canvas, padx=2, bg='red')
        self.canvas.create_window(0, 0, window=self.t1, anchor=tk.NW, width=300)
        self.update_canvas()
        # self.master.update()

        # self.update()
        # temp_frame = self.create_temp_frame()
        # self.origin_lbl = ctk.CTkLabel(temp_frame, text='Исток (O)')
        # self.origin_lbl.grid(column=0, row=2)
        # self.origin_entry = ctk.CTkEntry(temp_frame)
        # self.origin_entry.grid(column=1, row=2, **config.ENTRY_STYLE_DICT)
        #
        # self.add_vertex_btn = ctk.CTkButton(self.tab(self.get()), text=config.TEXT_ADD_VERTEX, command=self.add_vertex_gui)
        # self.add_vertex_btn.grid(column=0, row=2, **config.BTN_STYLE_DICT)
        #
        # self.remove_vertex_btn = ctk.CTkButton(self.tab(self.get()), text=config.TEXT_REMOVE_VERTEX, command=self.remove_vertex_gui)
        # self.remove_vertex_btn.grid(column=1, row=2, **config.BTN_STYLE_DICT)
        #
        # self.show_graph_btn = ctk.CTkButton(self.tab(self.get()), text=config.TEXT_TO_GRAPH, command=self.prepare_to_graph)
        # self.show_graph_btn.grid(column=2, row=2, columnspan=2, **config.BTN_STYLE_DICT)
        #
        # # self.help_btn = ctk.CTkButton(self, text=config.TEXT_HELP, command=lambda: system('start README.md'))
        # # self.help_btn.grid(column=0, row=3, columnspan=3, **config.BTN_STYLE_DICT)
        # # self.configure(menu=self.__menu)
        # self.__raw_data = []

    def remove_vertex_gui(self):
        if not self.__raw_data:
            return
        items = self.__raw_data.pop()
        for item in items:
            item.destroy()
        VertexNameGenerator.decrease_counter()
        self.update_canvas()
        self.logger.info('Widget deleted')

    def create_temp_frame(self):
        temp_frame = tk.Frame(self.frame, bg='green')
        for ind in range(3):
            temp_frame.columnconfigure(ind, weight=1)
        temp_frame.pack(expand=True, side=tk.TOP, fill=tk.BOTH)
        return temp_frame

    def add_vertex_gui(self):
        temp_frame = self.create_temp_frame()
        lbl = ctk.CTkLabel(temp_frame, text=VertexNameGenerator.get_vertex_name(), width=5)
        lbl.grid(column=0, row=0)
        entry = ctk.CTkEntry(temp_frame)
        entry.grid(column=1, row=0, **config.ENTRY_STYLE_DICT)

        self.__raw_data.append([lbl, entry, temp_frame])
        self.update_canvas()
        self.logger.info(f'Widget added with name {lbl.cget("text")}')

    def update_canvas(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def prepare_to_graph(self):
        new = list(map(lambda item: item[:-1], self.__raw_data))
        new.append([ttk.Label(text='O'), self.origin_entry])
        new.append([ttk.Label(text='Z'), ttk.Entry()])
        result = DataConverter().widget_to_json(new)
        if not result:
            self.logger.warning('DataConverter returned empty data')
            showerror('Ошибка', 'Данные в полях указаны неверно')
            return
        FileManager().save_file_data(config.FILENAME, result)
        self.show_graph_gui()

    def show_graph_gui(self):
        graph_window = graph.GraphGUI(self)
        graph_window.grab_set()
        self.logger.info('Graph window opened')


class MainGUI(ctk.CTk, LogMixin):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.title(config.TEXT_APP_TITLE)
        self.resizable(False, False)

        self.tab_view = MainTabView(self)
        self.tab_view.grid(row=0, column=0, padx=5, pady=5)


def main():
    app = MainGUI()
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename='app_logging.log',
        format='%(asctime)s %(levelname)s %(message)s',
        filemode='w'
    )
    main()
