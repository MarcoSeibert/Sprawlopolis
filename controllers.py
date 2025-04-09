import tkinter as tk
from tkinter import ttk
import pywinstyles
from functools import partial
from math import sqrt, pi, exp

from PIL import Image

from globals import LEFT_MOUSE_BUTTON, BOLD_FONT, CARD_SIZE

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
        self.active_card_image = None
        self.model = model
        self.view = view
        self.starting_drag_position = (0, 0)
        self.drag_data = {"x": 0, "y": 0, "item": 0}
        self.view.master.bind("<Escape>", self.quit)
        self.number_of_decks = len(self.model.list_base_games)
        self.image_approve = tk.PhotoImage(file="Resources/Approve.png", format="png")
        self.image_decline = tk.PhotoImage(file="Resources/Decline.png", format="png")
        self.image_turn = tk.PhotoImage(file="Resources/Turn.png", format="png")

        # show scoring cards
        if self.number_of_decks != 3:
            # standard case = 3 goals
            for i, scoring_card in enumerate(self.model.score_cards):
                self.scoring_card = ttk.Label(self.view, image=scoring_card.back_image)
                self.scoring_card.grid(column=13, row=4 * i + 1, columnspan=2, rowspan=4)
                ttk.Label(self.view, text="0", font=BOLD_FONT).grid(column=15, row=4 * i + 1, columnspan=2, rowspan=4)
        else:
            # Ultimopolis = 4 goals
            for i, scoring_card in enumerate(self.model.score_cards):
                self.scoring_card = ttk.Label(self.view, image=scoring_card.back_image)
                self.scoring_card.grid(column=13, row=3 * i + 1, columnspan=2, rowspan=3)
                ttk.Label(self.view, text="0", font=BOLD_FONT).grid(column=15, row=3 * i + 1, columnspan=2, rowspan=3)

        # show initial hand cards
        self.hand_cards = []
        if self.number_of_decks != 2:
            # standard case = 3 cards
            self.first_card = ttk.Label(self.view, image=self.model.hand_cards[0].front_image)
            self.first_card.grid(column=1, row=17, rowspan=2, columnspan=2)
            self.first_card.bind(LEFT_MOUSE_BUTTON, self.play_card)
            self.hand_cards.append(self.first_card)
            self.second_card = ttk.Label(self.view, image=self.model.hand_cards[1].front_image)
            self.second_card.grid(column=3, row=17, rowspan=2, columnspan=2)
            self.second_card.bind(LEFT_MOUSE_BUTTON, self.play_card)
            self.hand_cards.append(self.second_card)
            self.third_card = ttk.Label(self.view, image=self.model.hand_cards[2].front_image)
            self.third_card.grid(column=5, row=17, rowspan=2, columnspan=2)
            self.third_card.bind(LEFT_MOUSE_BUTTON, self.play_card)
            self.hand_cards.append(self.third_card)
        else:
            # Combopolis = 2 cards
            self.first_card = ttk.Label(self.view, image=self.model.hand_cards[0].front_image)
            self.first_card.grid(column=1, row=17, rowspan=2, columnspan=3)
            self.second_card = ttk.Label(self.view, image=self.model.hand_cards[1].front_image)
            self.second_card.grid(column=4, row=17, rowspan=2, columnspan=3)

        # show decks
        match self.number_of_decks:
            case 1:
                # add indicator for decks
                self.view.deck_area.grid(column=7, row=17, columnspan=6, rowspan=2)
                self.view.deck_area.config(width=40)
                game = list(self.model.dict_of_decks.keys())[0]
                self.next_card = self.model.dict_of_decks[game].deal()
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image, background="#000001")
                self.next_card_image.grid(column=7, row=17, rowspan=2, columnspan=6)
                pywinstyles.set_opacity(self.next_card_image, color="#000001")

            case 2:
                # add indicator for decks
                self.view.deck_area.grid(column=7, row=17, columnspan=6, rowspan=2)
                self.view.deck_area.config(width=100)
                # todo show cards from the matching deck (for loop)
                game = list(self.model.dict_of_decks.keys())[0]
                self.next_card = self.model.dict_of_decks[game].deal()
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image, background="#000001")
                self.next_card_image.grid(column=7, row=17, rowspan=2, columnspan=3)
                pywinstyles.set_opacity(self.next_card_image, color="#000001")
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image, background="#000001")
                self.next_card_image.grid(column=10, row=17, rowspan=2, columnspan=3)
                pywinstyles.set_opacity(self.next_card_image, color="#000001")
            case 3:
                # add indicator for decks
                self.view.deck_area.grid(column=7, row=17, columnspan=6, rowspan=2)
                self.view.deck_area.config(width=120)
                # todo show cards from the matching deck
                game = list(self.model.dict_of_decks.keys())[0]
                self.next_card = self.model.dict_of_decks[game].deal()
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image, background="#000001")
                self.next_card_image.grid(column=7, row=17, rowspan=2, columnspan=2)
                pywinstyles.set_opacity(self.next_card_image, color="#000001")
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image, background="#000001")
                self.next_card_image.grid(column=9, row=17, rowspan=2, columnspan=2)
                pywinstyles.set_opacity(self.next_card_image, color="#000001")
                self.next_card_image = ttk.Label(self.view, image=self.next_card.front_image, background="#000001")
                self.next_card_image.grid(column=11, row=17, rowspan=2, columnspan=2)
                pywinstyles.set_opacity(self.next_card_image, color="#000001")

        # add first card to canvas
        self.temp_card = self.model.dict_of_decks["Sprawlopolis"].deal()
        self.view.play_area.create_image(3000, 1323, image=self.temp_card.front_image)

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
        x = self.view.play_area.canvasx(event.x)
        y = self.view.play_area.canvasy(event.y)
        self.drag_data["item"] = self.view.play_area.find_closest(x, y)[0]
        self.drag_data["x"] = x
        self.drag_data["y"] = y
        self.show_buttons(False)

    def drop_card(self, event):
        grid_x_pix = self.view.play_area.canvasx(event.x, 100)
        grid_y_pix = self.view.play_area.canvasy(event.y, 73.5)
        self.view.play_area.coords(self.drag_data["item"], grid_x_pix, grid_y_pix)
        # grid_x_int = grid_x_pix // 100
        # grid_y_int = grid_y_pix // 73.5
        # self.play_area.item config(self.drag_data["item"], tag="static")
        self.drag_data["item"] = 0
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.show_buttons(True, grid_x_pix, grid_y_pix)

    def drag_card(self, event):
        x = self.view.play_area.canvasx(event.x)
        y = self.view.play_area.canvasy(event.y)
        delta_x = x - self.drag_data["x"]
        delta_y = y - self.drag_data["y"]
        self.view.play_area.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = x
        self.drag_data["y"] = y

    def play_card(self, event):
        self.active_card_image = event.widget.cget("image")[0]
        pywinstyles.set_opacity(event.widget, value=0.5)
        self.view.play_area.create_image(3000, 1323, image=self.active_card_image, tag="movable")
        for card in self.hand_cards:
            card.unbind(LEFT_MOUSE_BUTTON)

    def quit(self, _):
        # TODO ask if intentional (Are you sure?)
        self.view.master.destroy()

    def show_buttons(self, param, grid_x_pix=0, grid_y_pix=0):
        if param:
            # print(grid_x_pix, grid_y_pix)
            self.view.play_area.create_image(grid_x_pix - CARD_SIZE[0] / 2, grid_y_pix - CARD_SIZE[1] / 2,
                                             image=self.image_approve, tag="canvas_buttons")
            self.view.play_area.create_image(grid_x_pix - CARD_SIZE[0] / 2, grid_y_pix,
                                             image=self.image_turn, tag="canvas_buttons")
            self.view.play_area.create_image(grid_x_pix - CARD_SIZE[0] / 2, grid_y_pix + CARD_SIZE[1] / 2,
                                             image=self.image_decline, tag="canvas_buttons")
