import tkinter as tk
from tkinter import ttk
from functools import partial
from math import sqrt, pi, exp

from globals import LEFT_MOUSE_BUTTON, BOLD_FONT

path_to_switch = "Resources/ToggleSwitch.gif"
path_to_scale = "Resources/Difficulty.gif"


def smooth(x: int, m: float, a: float) -> int:
    return int(a - (1 / (sqrt(2 * pi) * 3) * exp(-((x - m) ** 2) / (2 * 3 ** 2)) * 75 + 18))


def animate(i: int, widget: tk.Label, frames: list[tk.PhotoImage], m: float, a: float):
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

    def click_base(self, base_id: int):
        list_of_base_games = self.model.toggle_base(base_id)
        if not list_of_base_games:
            # Print warning and disable button and expansions
            self.view.label_note["text"] = "At least one base"
            self.view.button_play["state"] = tk.DISABLED
            self.view.button_play.unbind(LEFT_MOUSE_BUTTON)
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
            self.view.switch_exp1.unbind(LEFT_MOUSE_BUTTON)
            self.view.switch_exp2.unbind(LEFT_MOUSE_BUTTON)
            self.view.switch_exp3.unbind(LEFT_MOUSE_BUTTON)
            self.view.switch_exp4.unbind(LEFT_MOUSE_BUTTON)
            self.view.switch_exp5.unbind(LEFT_MOUSE_BUTTON)
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
            self.view.button_play.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_play))
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
            self.view.switch_exp1.unbind(LEFT_MOUSE_BUTTON)
            self.view.switch_exp2.unbind(LEFT_MOUSE_BUTTON)
            self.view.switch_exp3.unbind(LEFT_MOUSE_BUTTON)
            self.view.switch_exp4.unbind(LEFT_MOUSE_BUTTON)
            self.view.switch_exp5.unbind(LEFT_MOUSE_BUTTON)
            self.model.list_expansions = []
        else:
            self.view.label_note["text"] = ""
            self.view.button_play["state"] = tk.NORMAL
            self.view.switch_exp1["state"] = tk.NORMAL
            self.view.switch_exp2["state"] = tk.NORMAL
            self.view.switch_exp3["state"] = tk.NORMAL
            self.view.switch_exp1.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_click_exp, 1))
            self.view.switch_exp2.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_click_exp, 2))
            self.view.switch_exp3.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_click_exp, 3))
            self.view.button_play.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_play))
            self.view.label_exp2["text"] = "Points of Interest"
            match self.model.list_base_games[0]:
                case 0:
                    self.view.label_exp1["text"] = "Wrecktar"
                    self.view.label_exp3["text"] = "Construction Zones"
                    self.view.label_exp4["text"] = "Beaches"
                    self.view.label_exp5["text"] = "Roadwork"
                    self.view.switch_exp4.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_click_exp, 4))
                    self.view.switch_exp5.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_click_exp, 5))
                    self.view.switch_exp4["state"] = tk.NORMAL
                    self.view.switch_exp5["state"] = tk.NORMAL
                case 1:
                    self.view.label_exp1["text"] = "Invasion"
                    self.view.label_exp3["text"] = "Seasons"
                    self.view.label_exp4["text"] = "Harvest"
                    self.view.label_exp5["text"] = ""
                    self.view.switch_exp4.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_click_exp, 4))
                    self.view.switch_exp5.unbind(LEFT_MOUSE_BUTTON)
                    self.view.switch_exp4["state"] = tk.NORMAL
                    self.view.switch_exp5["state"] = tk.DISABLED
                case 2:
                    self.view.label_exp1["text"] = "Nessie"
                    self.view.label_exp3["text"] = "Elevation"
                    self.view.label_exp4["text"] = ""
                    self.view.label_exp5["text"] = ""
                    self.view.switch_exp4.unbind(LEFT_MOUSE_BUTTON)
                    self.view.switch_exp5.unbind(LEFT_MOUSE_BUTTON)
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

    def click_exp(self, exp_id: int):
        list_expansions = self.model.toggle_exp(exp_id)
        if len(list_expansions) > 1:
            self.view.label_note["text"] = "Better only one exp"
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

    def click_diff(self, event: tk.Event):
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

    def click_play(self):
        self.view.master.start_game(self.model.list_base_games, self.model.list_expansions, self.model.difficulty)


class ControllerMain:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.starting_drag_position = (0, 0)
        self.drag_data = {"x": 0, "y": 0, "item": 0}
        self.view.master.bind("<Escape>", self.quit)
        self.number_of_decks = len(self.model.list_base_games)

        # show scoring cards
        if self.number_of_decks != 3:
            # standard case = 3 goals
            for i, scoring_card in enumerate(self.model.score_cards):
                self.scoring_card = ttk.Label(self.view, image=scoring_card.back_image)
                self.scoring_card.grid(column=13, row=4 * i + 1, columnspan=2, rowspan=4)
                ttk.Label(self.view, text="0", font=BOLD_FONT).grid(column=15, row=4 * i + 1, columnspan=2, rowspan=4)
        else:
            # Ulimopolis = 4 goals
            for i, scoring_card in enumerate(self.model.score_cards):
                self.scoring_card = ttk.Label(self.view, image=scoring_card.back_image)
                self.scoring_card.grid(column=13, row=3 * i + 1, columnspan=2, rowspan=3)
                ttk.Label(self.view, text="0", font=BOLD_FONT).grid(column=15, row=3 * i + 1, columnspan=2, rowspan=3)

        # show initial hand cards
        if self.number_of_decks != 2:
            # standard case = 3 cards
            self.first_card = ttk.Label(self.view, image=self.model.hand_cards[0].front_image)
            self.first_card.grid(column=1, row=17, rowspan=2, columnspan=2)
            self.second_card = ttk.Label(self.view, image=self.model.hand_cards[1].front_image)
            self.second_card.grid(column=3, row=17, rowspan=2, columnspan=2)
            self.third_card = ttk.Label(self.view, image=self.model.hand_cards[2].front_image)
            self.third_card.grid(column=5, row=17, rowspan=2, columnspan=2)
        else:
            # Combopolis = 2 cards
            self.first_card = ttk.Label(self.view, image=self.model.hand_cards[0].front_image)
            self.first_card.grid(column=1, row=17, rowspan=2, columnspan=3)
            self.second_card = ttk.Label(self.view, image=self.model.hand_cards[1].front_image)
            self.second_card.grid(column=4, row=17, rowspan=2, columnspan=3)

        # show decks
        match self.number_of_decks:
            case 1:
                game = list(self.model.dict_of_decks.keys())[0]
                self.next_card = self.model.dict_of_decks[game].deal()
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image)
                self.next_card_image.grid(column=7, row=17, rowspan=2, columnspan=6)
            case 2:
                # todo show cards from the matching deck
                game = list(self.model.dict_of_decks.keys())[0]
                self.next_card = self.model.dict_of_decks[game].deal()
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image)
                self.next_card_image.grid(column=7, row=17, rowspan=2, columnspan=3)
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image)
                self.next_card_image.grid(column=10, row=17, rowspan=2, columnspan=3)
            case 3:
                # todo show cards from the matching deck
                game = list(self.model.dict_of_decks.keys())[0]
                self.next_card = self.model.dict_of_decks[game].deal()
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image)
                self.next_card_image.grid(column=7, row=17, rowspan=2, columnspan=2)
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image)
                self.next_card_image.grid(column=9, row=17, rowspan=2, columnspan=2)
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image)
                self.next_card_image.grid(column=11, row=17, rowspan=2, columnspan=2)

        # add first card to canvas
        self.temp_card = self.model.dict_of_decks["Sprawlopolis"].deal()
        self.view.play_area.create_image(3000, 1400, image=self.temp_card.front_image)

        # add bindings to drag canvas
        self.view.play_area.bind("<ButtonPress-2>", self.pick_up_canvas)
        self.view.play_area.bind("<ButtonRelease-2>", self.drop_canvas)
        self.view.play_area.bind("<B2-Motion>", self.drag_canvas)

        # add bindings to drag cards
        self.view.play_area.tag_bind("movable", "<ButtonPress-1>", self.pick_up_card)
        self.view.play_area.tag_bind("movable", "<ButtonRelease-1>", self.drop_card)
        self.view.play_area.tag_bind("movable", "<B1-Motion>", self.drag_card)

    def pick_up_canvas(self, event):
        self.view.play_area.config(xscrollincrement=1)
        self.view.play_area.config(yscrollincrement=1)
        self.drag_data["x"], self.drag_data["y"] = (event.x, event.y)

    def drop_canvas(self, _):
        self.view.play_area.config(xscrollincrement=0)
        self.view.play_area.config(yscrollincrement=0)
        self.drag_data["x"], self.drag_data["y"] = (0, 0)

    def drag_canvas(self, event):
        delta_x = self.drag_data["x"] - event.x
        delta_y = self.drag_data["y"] - event.y
        self.view.play_area.xview("scroll", delta_x, "units")
        self.view.play_area.yview("scroll", delta_y, "units")
        self.drag_data["x"], self.drag_data["y"] = (event.x, event.y)

    def pick_up_card(self, event):
        self.drag_data["item"] = self.view.play_area.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drop_card(self, event):
        grid_x_pix = self.view.play_area.canvasx(event.x, 100)
        grid_x_pix = max(grid_x_pix, 100)
        grid_y_pix = self.view.play_area.canvasy(event.y, 73.5)
        grid_y_pix = max(grid_y_pix, 73.5)
        self.view.play_area.coords(self.drag_data["item"], grid_x_pix, grid_y_pix)
        # grid_x_int = grid_x_pix // 100
        # grid_y_int = grid_y_pix // 73.5
        # self.play_area.item config(self.drag_data["item"], tag="static")
        self.drag_data["item"] = 0
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def drag_card(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.view.play_area.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def quit(self, _):
        # TODO ask if intentional (Are you sure?)
        self.view.master.destroy()

