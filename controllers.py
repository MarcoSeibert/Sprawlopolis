import random
import tkinter as tk
from tkinter import ttk, Event
from tkinter.ttk import Label

import pywinstyles
from functools import partial
from math import sqrt, pi, exp
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

from globals import LEFT_MOUSE_BUTTON, CARD_SIZE
from models import ModelStart, ModelMain
from views import ViewStart, ViewMain, ViewLoading

path_to_switch = "Resources/ToggleSwitch.gif"
path_to_scale = "Resources/Difficulty.gif"
switch_delay = [20, 3, 100]
scale_delay = [35, 2, 125]


class ControllerStart:
    def __init__(self, model: ModelStart, view: ViewStart):
        self.model = model
        self.view = view
        self.combo = None
        self.map_index_to_base = {0: self.view.switch_sprawl, 1: self.view.switch_agro, 2: self.view.switch_naturo}
        self.map_index_to_exp = {1: self.view.switch_exp1, 2: self.view.switch_exp2, 3: self.view.switch_exp3,
                                 4: self.view.switch_exp4, 5: self.view.switch_exp5}

    def click_base(self, base_id: int):
        list_of_base_games = self.model.toggle_base(base_id)
        if not list_of_base_games:
            # Print warning and disable button and expansions
            self.view.label_note["text"] = "At least one base"
            self.combo = None
            self.view.button_play["state"] = tk.DISABLED
            self.view.button_play.unbind(LEFT_MOUSE_BUTTON)
            list_expansions = self.model.list_expansions
            frames_switch = get_frames_from_gif(path_to_switch)
            frames_switch.reverse()
            for exp_id, switch in self.map_index_to_exp.items():
                if exp_id in list_expansions:
                    play_gif(self.view, switch, frames_switch, False, switch_delay)
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
                    self.combo = "Combopolis_I"
                case [0, 2]:
                    self.view.label_note["text"] = "Using Combopolis II"
                    self.combo = "Combopolis_II"
                case [1, 2]:
                    self.view.label_note["text"] = "Using Combopolis III"
                    self.combo = "Combopolis_III"
                case [0, 1, 2]:
                    self.view.label_note["text"] = "Using Ultimopolis"
                    self.combo = "Ultimopolis"
            self.view.button_play["state"] = tk.NORMAL
            self.view.button_play.bind(LEFT_MOUSE_BUTTON, partial(self.view.on_play))
            # Disable expansions when using multiple base games
            list_expansions = self.model.list_expansions
            frames_switch = get_frames_from_gif(path_to_switch)
            frames_switch.reverse()
            for exp_id, switch in self.map_index_to_exp.items():
                if exp_id in list_expansions:
                    play_gif(self.view, switch, frames_switch, False, switch_delay)
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
            self.combo = None
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
        frames_switch = get_frames_from_gif(path_to_switch)
        for base_id, switch in self.map_index_to_base.items():
            if base_id in list_of_base_games and not switch.active:
                play_gif(self.view, switch, frames_switch, False, switch_delay)
                switch.active = True
            elif base_id not in list_of_base_games and switch.active:
                frames_switch.reverse()
                play_gif(self.view, switch, frames_switch, False, switch_delay)
                switch.active = False

    def click_exp(self, exp_id: int):
        list_expansions = self.model.toggle_exp(exp_id)
        if len(list_expansions) > 1:
            self.view.label_note["text"] = "Better only one exp"
        # Update the expansion toggles
        frames_switch = get_frames_from_gif(path_to_switch)
        for exp_id, switch in self.map_index_to_exp.items():
            if exp_id in list_expansions and not switch.active:
                play_gif(self.view, switch, frames_switch, False, switch_delay)
                switch.active = True
            elif exp_id not in list_expansions and switch.active:
                frames_switch.reverse()
                play_gif(self.view, switch, frames_switch, False, switch_delay)
                switch.active = False

    def click_diff(self, event: tk.Event):
        scale = event.widget
        y_click = event.y
        frames_scale = []
        match scale.value:
            case 0:
                scale.value = 1
                frames_scale = get_frames_from_gif("Resources/Difficulty01.gif")
                frames_scale.reverse()
            case 1:
                if y_click >= 96:
                    scale.value = 2
                    frames_scale = get_frames_from_gif("Resources/Difficulty12.gif")
                    frames_scale.reverse()
                else:
                    scale.value = 0
                    frames_scale = get_frames_from_gif("Resources/Difficulty01.gif")
            case 2:
                scale.value = 1
                frames_scale = get_frames_from_gif("Resources/Difficulty12.gif")
        play_gif(self.view, scale, frames_scale, False, scale_delay)
        self.model.difficulty = scale.value

    def click_play(self):
        self.view.master.start_game(self.model.list_base_games, self.model.list_expansions, self.model.difficulty,
                                    self.combo)


class ControllerMain:
    def __init__(self, model: ModelMain, view: ViewMain):
        self.model = model
        self.view = view
        self.number_of_decks = len(self.model.list_base_games)

        self.active_card_image = None
        self.starting_drag_position = (0, 0)
        self.drag_data = {"x": 0, "y": 0, "item": 0}

        self.view.master.bind("<Escape>", self.quit)

        self.image_approve = tk.PhotoImage(file="Resources/Approve.png", format="png")
        self.image_decline = tk.PhotoImage(file="Resources/Decline.png", format="png")
        self.image_turn = tk.PhotoImage(file="Resources/Turn.png", format="png")

        # For testing of the card mapping
        # self.deck = Deck("Ultimopolis", False)
        # for i, card in enumerate(self.deck.cards):
        #     self.temp= ttk.Label(self.view, image=card.front_image)
        #     self.temp.grid(column=0, row=i)
        #     self.temp = ttk.Label(self.view, image=card.back_image)
        #     self.temp.grid(column=1, row=i)
        #     self.temp = ttk.Label(self.view, text=i + 1)
        #     self.temp.grid(column=2, row=i)
        #     self.temp = ttk.Label(self.view, text=card.card_id)
        #     self.temp.grid(column=3, row=i)
        #     self.temp = ttk.Label(self.view, text=card.scoring_function)
        #     self.temp.grid(column=4, row=i)

        # add scoring cards to the grid
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        if self.number_of_decks == 3:
            self.scoring_card = ttk.Label(self.view.score_area)
            for i, card in enumerate(self.view.score_area.winfo_children()):
                card.grid(column=13, row=3 * i + 1, columnspan=2, rowspan=3)
        else:
            for i, card in enumerate(self.view.score_area.winfo_children()):
                card.grid(column=13, row=4 * i + 1, columnspan=2, rowspan=4)
        # add images to the cards
        for i, card in enumerate(self.view.score_area.winfo_children()):
            card.config(image=self.model.score_cards[i].back_image, background="#100001")
            pywinstyles.set_opacity(card, color="#100001")

        # add initial hand cards to the grid
        self.hand_card = ttk.Label(self.view.hand_area)
        self.hand_card = ttk.Label(self.view.hand_area)
        if self.number_of_decks != 2:
            # standard case = 3 cards
            self.hand_card = ttk.Label(self.view.hand_area)
            for i, card in enumerate(self.view.hand_area.winfo_children()):
                card.grid(column=1 + 2 * i, row=17, rowspan=2, columnspan=2)
        else:
            # Combopolis = 2 cards
            for i, card in enumerate(self.view.hand_area.winfo_children()):
                card.grid(column=1 + 3 * i, row=17, rowspan=2, columnspan=3)
        # add images to the cards
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.config(image=self.model.hand_cards[i].front_image, background="#000001")
            pywinstyles.set_opacity(card, color="#000001")
            card.bind(LEFT_MOUSE_BUTTON, self.play_card)

        # add decks to the grid
        self.next_card = ttk.Label(self.view.deck_area)
        match self.number_of_decks:
            case 1:
                self.next_card.grid(column=7, row=17, rowspan=2, columnspan=6)
            case 2:
                self.next_card = ttk.Label(self.view.deck_area)
                for i, card in enumerate(self.view.deck_area.winfo_children()):
                    card.grid(column=7 + 3 * i, row=17, rowspan=2, columnspan=3)
            case 3:
                self.next_card = ttk.Label(self.view.deck_area)
                self.next_card = ttk.Label(self.view.deck_area)
                for i, card in enumerate(self.view.deck_area.winfo_children()):
                    card.grid(column=7 + 2 * i, row=17, rowspan=2, columnspan=2)
        # add images to the cards
        images = [self.model.dict_of_decks[deck].cards[0].front_image for deck in self.model.dict_of_decks]
        cards_and_images = zip(self.view.deck_area.winfo_children(), images)
        for card, image in cards_and_images:
            card.configure(image=image, background="#000001")
            pywinstyles.set_opacity(card, color="#000001")

        # add bindings to drag canvas
        self.view.play_area.bind("<ButtonPress-2>", self.pick_up_canvas)
        self.view.play_area.bind("<ButtonRelease-2>", self.drop_canvas)
        self.view.play_area.bind("<B2-Motion>", self.drag_canvas)

        # add bindings to drag cards
        self.view.play_area.tag_bind("movable", "<ButtonPress-1>", self.pick_up_card)
        self.view.play_area.tag_bind("movable", "<ButtonRelease-1>", self.drop_card)
        self.view.play_area.tag_bind("movable", "<B1-Motion>", self.drag_card)

    def pick_up_canvas(self, event: Event):
        self.view.play_area.config(xscrollincrement=1)
        self.view.play_area.config(yscrollincrement=1)
        self.drag_data["x"], self.drag_data["y"] = (event.x, event.y)

    def drop_canvas(self, _):
        self.view.play_area.config(xscrollincrement=0)
        self.view.play_area.config(yscrollincrement=0)
        self.drag_data["x"], self.drag_data["y"] = (0, 0)

    def drag_canvas(self, event: Event):
        delta_x = self.drag_data["x"] - event.x
        delta_y = self.drag_data["y"] - event.y
        self.view.play_area.xview("scroll", delta_x, "units")
        self.view.play_area.yview("scroll", delta_y, "units")
        self.drag_data["x"], self.drag_data["y"] = (event.x, event.y)

    def pick_up_card(self, event: Event):
        x = self.view.play_area.canvasx(event.x)
        y = self.view.play_area.canvasy(event.y)
        self.drag_data["item"] = self.view.play_area.find_closest(x, y)[0]
        self.drag_data["x"] = x
        self.drag_data["y"] = y
        self.show_buttons(False)

    def drop_card(self, event: Event):
        grid_x_pix = self.view.play_area.canvasx(event.x, 100)
        grid_y_pix = self.view.play_area.canvasy(event.y, 73.5)
        self.view.play_area.coords(self.drag_data["item"], grid_x_pix, grid_y_pix)
        self.drag_data["item"] = 0
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.show_buttons(True, grid_x_pix, grid_y_pix)

    def drag_card(self, event: Event):
        x = self.view.play_area.canvasx(event.x)
        y = self.view.play_area.canvasy(event.y)
        delta_x = x - self.drag_data["x"]
        delta_y = y - self.drag_data["y"]
        self.view.play_area.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = x
        self.drag_data["y"] = y

    def play_card(self, event: Event):
        self.active_card_image = event.widget.cget("image")[0]
        pywinstyles.set_opacity(event.widget, value=0.5, color="#000001")
        self.view.play_area.create_image(3000, 1323, image=self.active_card_image, tag="movable")
        # for card in self.hand_cards:
        #     card.unbind(LEFT_MOUSE_BUTTON)

    def quit(self, _):
        # TODO ask if intentional (Are you sure?)
        self.view.master.destroy()

    def show_buttons(self, param: bool, grid_x_pix: int = 0, grid_y_pix: int = 0):
        if param:
            self.view.play_area.create_image(grid_x_pix - CARD_SIZE[0] / 2, grid_y_pix - CARD_SIZE[1] / 2,
                                             image=self.image_approve, tags=("canvas_buttons", "approve"))
            self.view.play_area.create_image(grid_x_pix - CARD_SIZE[0] / 2, grid_y_pix,
                                             image=self.image_turn, tags=("canvas_buttons", "turn"))
            self.view.play_area.create_image(grid_x_pix - CARD_SIZE[0] / 2, grid_y_pix + CARD_SIZE[1] / 2,
                                             image=self.image_decline, tags=("canvas_buttons", "decline"))
        else:
            self.view.play_area.delete("canvas_buttons")


class ControllerLoading:
    def __init__(self, view: ViewLoading):
        self.view = view

    def play_animation(self, list_base_games: list[str]):
        view = self.view
        label = self.view.label_image
        frames = get_frames_from_gif("Resources/Loading.gif")
        play_gif(view, label, frames, True, False)
        show_text(view, list_base_games)


def get_frames_from_gif(img: PhotoImage):
    with Image.open(img) as gif:
        index = 0
        frames = []
        while True:
            try:
                gif.seek(index)
                frame = ImageTk.PhotoImage(gif)
                frames.append(frame)
            except EOFError:
                break
            index += 1
        return frames


def display_next_frame(view, frame: PhotoImage, label: Label, frames: list[PhotoImage], loop: bool,
                       variable_delay: bool,
                       restart: bool = False):
    if restart:
        try:
            label.config
        except tk.TclError:
            return
        # start over after restart
        play_gif(view, label, frames, loop, variable_delay)
        return
    try:
        label.config(image=frame)
    except tk.TclError:
        return


def smooth(x: int, m: float, l: float, s: float, a: float) -> int:
    # Using a normal distribution to get smooth animations
    return int(l - a / (s * sqrt(2 * pi)) * exp(-0.5 * ((x - m) / s) ** 2))


def play_gif(view, label: Label, frames: list[PhotoImage], loop: bool, variable_delay: bool):
    frame = None
    label.image = None
    # delay for scheduling later frames
    total_delay = 0
    # delay between frames
    delay_frames = 40
    # scheduling event for every frame
    for i, frame in enumerate(frames):
        if variable_delay:
            m = (len(frames) - 1) / 2
            l = variable_delay[0]
            s = variable_delay[1]
            a = variable_delay[2]
            delay_frames = smooth(i, m, l, s, a)
        view.after(total_delay, display_next_frame, view, frame, label, frames, loop, variable_delay)
        total_delay += delay_frames
    # schedule restart after all frames are done
    if loop:
        view.after(total_delay, display_next_frame, view, frame, label, frames, loop, variable_delay, True)
    else:
        label.image = frame
        label.config(image=label.image)


def show_text(view, list_base_games: list[str]):
    label = view.label_text
    text_blocks = []
    text_blocks_sprawl = ["Loading urban sprawl...", "Constructing infrastructure...", "Writing city blueprints...",
                          "Preparing construction crews...", "Analyzing zoning laws...",
                          "Reading city council approvals...", "Prepping for urban challenges..."]
    text_blocks_agro = ["Cultivating farmland...", "Preparing the harvest...", "Planning rural landscape...",
                        "Loading livestock data...", "Laying out orchards...", "Setting up trellises...",
                        "Adapting for agricultural challenges..."]
    text_blocks_naturo = ["Charting waterways...", "Setting up riverside campsites...", "Planning forest preserves...",
                          "Loading mountain climbing routes...", "Packing for meadow picnics...",
                          "Lake reflections loading...", "Constructing lakeside cabins..."]
    if 0 in list_base_games:
        text_blocks.extend(text_blocks_sprawl)
    if 1 in list_base_games:
        text_blocks.extend(text_blocks_agro)
    if 2 in list_base_games:
        text_blocks.extend(text_blocks_naturo)
    random.shuffle(text_blocks)
    # delay for scheduling later texts
    total_delay = 0
    # delay between texts
    delay_frames = 750
    # scheduling event for every texts
    for text in text_blocks:
        view.after(total_delay, change_text, label, text)
        total_delay += delay_frames


def change_text(label: Label, text: str):
    label.config(text=text)
