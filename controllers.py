import tkinter as tk
from functools import partial
from math import sqrt, pi, exp

path_to_switch = "Resources/ToggleSwitch.gif"
path_to_scale = "Resources/Difficulty.gif"
left_mouse_button = "<Button-1>"


def smooth(x, m, a):
    return int(a - (1 / (sqrt(2 * pi) * 3) * exp(-((x - m) ** 2) / (2 * 3 ** 2)) * 75 + 18))


def animate(i, widget, frames, m, a):
    frame = frames[i]
    i += 1
    widget.configure(image=frame)
    if i == len(frames):
        widget.image = frame
        return
    widget.after(smooth(i, m, a), animate, i, widget, frames, m, a)


class ControllerStart:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.map_index_to_base = {0: self.view.switch_sprawl, 1: self.view.switch_agro, 2: self.view.switch_naturo}
        self.map_index_to_exp = {1: self.view.switch_exp1, 2: self.view.switch_exp2, 3: self.view.switch_exp3,
                                 4: self.view.switch_exp4, 5: self.view.switch_exp5}

    def click_base(self, base_id):
        list_of_base_games = self.model.toggle_base(base_id)
        if not list_of_base_games:
            # Print warning and disable button and expansions
            self.view.label_note["text"] = "At least one base"
            self.view.button_play["state"] = tk.DISABLED
            self.view.button_play.unbind(left_mouse_button)
            list_expansions = self.model.list_expansions
            frames_switch = [tk.PhotoImage(file=path_to_switch, format=f"gif -index {i}") for i in range(13)]
            frames_switch.reverse()
            for exp_id, switch in self.map_index_to_exp.items():
                if exp_id in list_expansions:
                    animate(0, switch, frames_switch, 6.5, 30)
                    switch.active = False
            self.view.label_exp1["text"] = ""
            self.view.label_exp2["text"] = ""
            self.view.label_exp3["text"] = ""
            self.view.label_exp4["text"] = ""
            self.view.label_exp5["text"] = ""
            self.view.switch_exp1["state"] = tk.DISABLED
            self.view.switch_exp2["state"] = tk.DISABLED
            self.view.switch_exp3["state"] = tk.DISABLED
            self.view.switch_exp4["state"] = tk.DISABLED
            self.view.switch_exp5["state"] = tk.DISABLED
            self.view.switch_exp1.unbind(left_mouse_button)
            self.view.switch_exp2.unbind(left_mouse_button)
            self.view.switch_exp3.unbind(left_mouse_button)
            self.view.switch_exp4.unbind(left_mouse_button)
            self.view.switch_exp5.unbind(left_mouse_button)
            self.model.list_expansions = []
        elif len(list_of_base_games) > 1:
            match sorted(list_of_base_games):
                case [0, 1]:
                    self.view.label_note["text"] = "Using Combopolis I"
                case [0, 2]:
                    self.view.label_note["text"] = "Using Combopolis II"
                case [1, 2]:
                    self.view.label_note["text"] = "Using Combopolis III"
                case [0, 1, 2]:
                    self.view.label_note["text"] = "Using Ultimopolis"
            self.view.button_play["state"] = tk.NORMAL
            self.view.button_play.bind(left_mouse_button, partial(self.view.on_button_click))
            # Disable expansions when using multiple base games
            list_expansions = self.model.list_expansions
            frames_switch = [tk.PhotoImage(file=path_to_switch, format=f"gif -index {i}") for i in range(13)]
            frames_switch.reverse()
            for exp_id, switch in self.map_index_to_exp.items():
                if exp_id in list_expansions:
                    animate(0, switch, frames_switch, 6.5, 30)
                    switch.active = False
            self.view.label_exp1["text"] = ""
            self.view.label_exp2["text"] = ""
            self.view.label_exp3["text"] = ""
            self.view.label_exp4["text"] = ""
            self.view.label_exp5["text"] = ""
            self.view.switch_exp1["state"] = tk.DISABLED
            self.view.switch_exp2["state"] = tk.DISABLED
            self.view.switch_exp3["state"] = tk.DISABLED
            self.view.switch_exp4["state"] = tk.DISABLED
            self.view.switch_exp5["state"] = tk.DISABLED
            self.view.switch_exp1.unbind(left_mouse_button)
            self.view.switch_exp2.unbind(left_mouse_button)
            self.view.switch_exp3.unbind(left_mouse_button)
            self.view.switch_exp4.unbind(left_mouse_button)
            self.view.switch_exp5.unbind(left_mouse_button)
            self.model.list_expansions = []
        else:
            self.view.label_note["text"] = ""
            self.view.button_play["state"] = tk.NORMAL
            self.view.switch_exp1["state"] = tk.NORMAL
            self.view.switch_exp2["state"] = tk.NORMAL
            self.view.switch_exp3["state"] = tk.NORMAL
            self.view.switch_exp1.bind(left_mouse_button, partial(self.view.on_click_exp, 1))
            self.view.switch_exp2.bind(left_mouse_button, partial(self.view.on_click_exp, 2))
            self.view.switch_exp3.bind(left_mouse_button, partial(self.view.on_click_exp, 3))
            self.view.button_play.bind(left_mouse_button, partial(self.view.on_button_click))
            self.view.label_exp2["text"] = "Points of Interest"
            match self.model.list_base_games[0]:
                case 0:
                    self.view.label_exp1["text"] = "Wrecktar"
                    self.view.label_exp3["text"] = "Construction Zones"
                    self.view.label_exp4["text"] = "Beaches"
                    self.view.label_exp5["text"] = "Roadwork"
                    self.view.switch_exp4.bind(left_mouse_button, partial(self.view.on_click_exp, 4))
                    self.view.switch_exp5.bind(left_mouse_button, partial(self.view.on_click_exp, 5))
                    self.view.switch_exp4["state"] = tk.NORMAL
                    self.view.switch_exp5["state"] = tk.NORMAL
                case 1:
                    self.view.label_exp1["text"] = "Invasion"
                    self.view.label_exp3["text"] = "Seasons"
                    self.view.label_exp4["text"] = "Harvest"
                    self.view.label_exp5["text"] = ""
                    self.view.switch_exp4.bind(left_mouse_button, partial(self.view.on_click_exp, 4))
                    self.view.switch_exp5.unbind(left_mouse_button)
                    self.view.switch_exp4["state"] = tk.NORMAL
                    self.view.switch_exp5["state"] = tk.DISABLED
                case 2:
                    self.view.label_exp1["text"] = "Nessie"
                    self.view.label_exp3["text"] = "Elevation"
                    self.view.label_exp4["text"] = ""
                    self.view.label_exp5["text"] = ""
                    self.view.switch_exp4.unbind(left_mouse_button)
                    self.view.switch_exp5.unbind(left_mouse_button)
                    self.view.switch_exp4["state"] = tk.DISABLED
                    self.view.switch_exp5["state"] = tk.DISABLED

        # Update base game toggles
        frames_switch = [tk.PhotoImage(file=path_to_switch, format=f"gif -index {i}") for i in range(13)]
        for base_id, switch in self.map_index_to_base.items():
            if base_id in list_of_base_games and not switch.active:
                animate(0, switch, frames_switch, 6.5, 30)
                switch.active = True
            elif base_id not in list_of_base_games and switch.active:
                frames_switch.reverse()
                animate(0, switch, frames_switch, 6.5, 30)
                switch.active = False

    def click_exp(self, exp_id):
        list_expansions = self.model.toggle_exp(exp_id)
        if len(list_expansions) > 1:
            # TODO Print warning on screen
            print("Better use only one expansion")

        # Update the expansion toggles
        frames_switch = [tk.PhotoImage(file=path_to_switch, format=f"gif -index {i}") for i in range(13)]
        for exp_id, switch in self.map_index_to_exp.items():
            if exp_id in list_expansions and not switch.active:
                animate(0, switch, frames_switch, 6.5, 30)
                switch.active = True
            elif exp_id not in list_expansions and switch.active:
                frames_switch.reverse()
                animate(0, switch, frames_switch, 6.5, 30)
                switch.active = False

    def click_diff(self, event):
        scale = event.widget
        y_click = event.y
        frames_scale = []
        match scale.value:
            case 0:
                scale.value = 1
                frames_scale = [tk.PhotoImage(file=path_to_scale, format=f"gif -index {i}") for i in range(13, 6, -1)]
            case 1:
                if y_click >= 96:
                    scale.value = 2
                    frames_scale = [tk.PhotoImage(file=path_to_scale, format=f"gif -index {i}") for i in
                                    range(6, -1, -1)]
                else:
                    scale.value = 0
                    frames_scale = [tk.PhotoImage(file=path_to_scale, format=f"gif -index {i}") for i in range(8, 15)]
            case 2:
                scale.value = 1
                frames_scale = [tk.PhotoImage(file=path_to_scale, format=f"gif -index {i}") for i in range(1, 8)]
        animate(0, scale, frames_scale, 4, 37)
        self.model.difficulty = scale.value
