import customtkinter as ctk
import markdown
from tkinterweb import HtmlFrame
import config

class HelpGUI(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(config.TEXT_HELP)
        ctk.set_appearance_mode(config.APPEARANCE_MODE)
        with open(config.FILENAME_README, encoding='utf-8') as file:
            self.markdown = markdown.markdown(file.read())
        self.frame = HtmlFrame(self, messages_enabled=False)
        self.frame.load_html(self.markdown)
        self.frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)