import tkinter as tk
from functools import partial
from tkinter import ttk

from lib import MyLabel


class ViewStart(ttk.Frame):
    def __init__(self, parent:tk.Tk):
        super().__init__(parent)
        self.controller = None

        trebuchet_ms = "Trebuchet MS"
        left_mouse_button = "<Button-1>"

        title_font = (trebuchet_ms, 35, "bold")
        basic_font = (trebuchet_ms, 20)
        bold_font = (trebuchet_ms, 20, "bold")

        # set default parameters
        self.switch_off = tk.PhotoImage(file="Resources/ToggleSwitch.gif", format="gif -index 0")
        self.switch_on = tk.PhotoImage(file="Resources/ToggleSwitch.gif", format="gif -index 12")
        self.switch_normal = tk.PhotoImage(file="Resources/Difficulty.gif", format="gif -index 7")

        # creating frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # insert title
        ttk.Label(self, text="Sprawlopolis digital", font=title_font).grid(column=0, row=0, columnspan=6)

        # set up base game choice
        ttk.Label(self, text="Base game", font=bold_font).grid(column=0, columnspan=2, row=2, pady=(25, 10))

        ttk.Label(self, text="Sprawlopolis", font=basic_font).grid(column=0, row=3, sticky="E", pady=10)
        self.switch_sprawl = MyLabel(self, image=self.switch_on)
        self.switch_sprawl.bind(left_mouse_button, partial(self.on_click_base, 0))
        self.switch_sprawl.active = True
        self.switch_sprawl.grid(column=1, row=3)

        ttk.Label(self, text="Agropolis", font=basic_font).grid(column=0, row=4, sticky="E", pady=10)
        self.switch_agro = MyLabel(self, image=self.switch_off)
        self.switch_agro.bind(left_mouse_button, partial(self.on_click_base, 1))
        self.switch_agro.grid(column=1, row=4)

        ttk.Label(self, text="Naturopolis", font=basic_font).grid(column=0, row=5, sticky="E", pady=10)
        self.switch_naturo = MyLabel(self, image=self.switch_off)
        self.switch_naturo.bind(left_mouse_button, partial(self.on_click_base, 2))
        self.switch_naturo.grid(column=1, row=5)

        # set up expansion choices
        ttk.Label(self, text="Expansions", font=bold_font).grid(column=2, row=2, columnspan=2, pady=(25, 10))

        self.label_exp1 = ttk.Label(self, text="Wrecktar", font=basic_font, width=18, anchor="e")
        self.label_exp1.grid(column=2, row=3, sticky="E", pady=10, padx=25)
        self.switch_exp1 = MyLabel(self, image=self.switch_off)
        self.switch_exp1.bind(left_mouse_button, partial(self.on_click_exp, 1))
        self.switch_exp1.grid(column=3, row=3, sticky="W")

        self.label_exp2 = ttk.Label(self, text="Points of Interest", font=basic_font)
        self.label_exp2.grid(column=2, row=4, sticky="E", pady=10, padx=25)
        self.switch_exp2 = MyLabel(self, image=self.switch_off)
        self.switch_exp2.bind(left_mouse_button, partial(self.on_click_exp, 2))
        self.switch_exp2.grid(column=3, row=4, sticky="W")

        self.label_exp3 = ttk.Label(self, text="Construction Zones", font=basic_font)
        self.label_exp3.grid(column=2, row=5, sticky="E", pady=10, padx=25)
        self.switch_exp3 = MyLabel(self, image=self.switch_off)
        self.switch_exp3.bind(left_mouse_button, partial(self.on_click_exp, 3))
        self.switch_exp3.grid(column=3, row=5, sticky="W")

        self.label_exp4 = ttk.Label(self, text="Beaches", font=basic_font)
        self.label_exp4.grid(column=2, row=6, sticky="E", pady=10, padx=25)
        self.switch_exp4 = MyLabel(self, image=self.switch_off)
        self.switch_exp4.bind(left_mouse_button, partial(self.on_click_exp, 4))
        self.switch_exp4.grid(column=3, row=6, sticky="W")

        self.label_exp5 = ttk.Label(self, text="Roadwork", font=basic_font)
        self.label_exp5.grid(column=2, row=7, sticky="E", pady=10, padx=25)
        self.switch_exp5 = MyLabel(self, image=self.switch_off)
        self.switch_exp5.bind(left_mouse_button, partial(self.on_click_exp, 5))
        self.switch_exp5.grid(column=3, row=7, sticky="W")

        # set up difficulty
        ttk.Label(self, text="Difficulty", font=bold_font).grid(column=4, row=2, columnspan=2, padx=25, pady=(25, 10))
        ttk.Label(self, text="Easy\n\nStandard\n\nHard", font=basic_font).grid(column=5, row=3, sticky="W", rowspan=5)
        self.scale_difficulty = MyLabel(self, image=self.switch_normal)
        self.scale_difficulty.value = 1
        self.scale_difficulty.bind(left_mouse_button, partial(self.on_click_diff))
        self.scale_difficulty.grid(column=4, row=3, rowspan=5, sticky="E", padx=25)

        # set up buttons
        style_buttons = ttk.Style()
        my_button_style = "MyButton.TButton"
        style_buttons.configure(my_button_style, font=basic_font)
        self.button_play = ttk.Button(self, text="Play!", style=my_button_style)
        self.button_play.bind(left_mouse_button, partial(self.on_play))
        self.button_play.grid(column=0, row=6, columnspan=2)
        self.label_note = ttk.Label(self, text="", font=basic_font, relief="sunken", width=18, anchor=tk.CENTER,
                                    background="WHITE")
        self.label_note.grid(column=0, row=7, columnspan=2)
        ttk.Button(self, text="Quit!", style=my_button_style, command=self.on_quit).grid(column=0, row=8, columnspan=2)

    def set_controller(self, controller):
        self.controller = controller

    def on_quit(self):
        self.master.destroy()

    def on_play(self, *args):
        if self.controller:
            self.controller.click_play()

    def on_click_base(self, base_id:int, *args):
        if self.controller:
            self.controller.click_base(base_id)

    def on_click_exp(self, exp_id:int, *args):
        if self.controller:
            self.controller.click_exp(exp_id)

    def on_click_diff(self, *args):
        event = None
        for arg in args:
            # Check for left mouse button event
            if arg.type == tk.EventType("4") and arg.num == 1:
                event = arg
        if self.controller:
            self.controller.click_diff(event)


class ViewMain(ttk.Frame):
    def __init__(self, parent:tk.Tk):
        super().__init__(parent)
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller
