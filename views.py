import tkinter as tk
from functools import partial
from tkinter import ttk
from tkinter.constants import HORIZONTAL, VERTICAL

from PIL import ImageTk, Image, ImageDraw, ImageOps
from pypdf import PdfReader

trebuchet_ms = "Trebuchet MS"
left_mouse_button = "<Button-1>"

title_font = (trebuchet_ms, 35, "bold")
basic_font = (trebuchet_ms, 20)
bold_font = (trebuchet_ms, 20, "bold")


class MyLabel(ttk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False
        self.value = 0


class ViewStart(ttk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.controller = None

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
        self.button_play.bind("<Return>", partial(self.on_play))
        self.button_play.grid(column=0, row=6, columnspan=2)
        self.button_play.focus_set()
        self.label_note = ttk.Label(self, text="", font=basic_font, relief="sunken", width=18, anchor=tk.CENTER,
                                    background="WHITE")
        self.label_note.grid(column=0, row=7, columnspan=2)
        self.button_quit = ttk.Button(self, text="Quit!", style=my_button_style, command=self.on_quit)
        self.button_quit.grid(column=0, row=8, columnspan=2)
        self.button_quit.bind("<Return>", partial(self.on_quit))

    def set_controller(self, controller):
        self.controller = controller

    def on_quit(self, *args):
        self.master.destroy()

    def on_play(self, *args):
        if self.controller:
            self.controller.click_play()

    def on_click_base(self, base_id: int, *args):
        if self.controller:
            self.controller.click_base(base_id)

    def on_click_exp(self, exp_id: int, *args):
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


def add_corners_and_border(first_image, card_size):
    width, height = first_image.size
    radius = max(card_size) // 4
    border_width = radius // 2
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=255)
    first_image.putalpha(mask)
    border = Image.new("RGBA", (width + border_width * 2, height + border_width * 2), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.rounded_rectangle((0, 0, width + border_width * 2, height + border_width * 2), radius + border_width,
                                  fill=(0, 0, 0, 255))
    border.paste(first_image, (border_width, border_width), first_image)
    result = border.resize(card_size)
    return ImageTk.PhotoImage(result)


def get_first_picture():
    card_size = (200, 147)
    fp = "Resources/PnPs/Sprawlopolis_base.pdf"
    try:
        reader = PdfReader(fp)
        page = reader.pages[1]
        first_image = None
        for count, image_file_object in enumerate(page.images):
            image = image_file_object.image
            first_image = image.rotate(90, expand=True)
            break
    except FileNotFoundError:
        first_image = Image.open("Resources/Fallback.jpg")

    image = add_corners_and_border(first_image, card_size)
    return image


class ViewMain(ttk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.controller = None
        # Create menu bar
        menu_bar = tk.Menu(parent)
        file_menu = tk.Menu(menu_bar, tearoff=False, font=basic_font)
        file_menu.add_command(label="Back to menu")
        file_menu.add_command(label="Quit", command=self.quit, underline=0)
        menu_bar.add_cascade(label="Menu", menu=file_menu)
        parent.config(menu=menu_bar)

        # self.grid_columnconfigure(5, minsize=75)
        # self.grid_columnconfigure(6, minsize=75)
        self.grid_columnconfigure((12, 13), minsize=75)

        # insert title
        ttk.Label(self, text="Sprawlopolis digital", font=title_font).grid(column=0, row=0, columnspan=14)

        # insert play area
        self.play_area = tk.Canvas(self, width=1500, height=700, background="white", scrollregion=(0, 0, 3000, 3000))
        self.play_area.grid(column=1, row=1, columnspan=9, rowspan=6)
        ## add scrollbars
        self.hbar = ttk.Scrollbar(self, orient=HORIZONTAL)
        self.hbar.config(command=self.play_area.xview)
        self.hbar.grid(column=1, row=7, columnspan=9, sticky="we")
        self.vbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.vbar.config(command=self.play_area.yview)
        self.vbar.grid(column=0, row=1, rowspan=6, sticky="ns")
        self.play_area.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        self.first_image = get_first_picture()
        self.first_image_on_canvas = self.play_area.create_image(100, 100, image=self.first_image, tag="movable")

        # insert goals
        self.first_score_card = ttk.Label(self, image=self.first_image)
        self.first_score_card.grid(column=10, row=1, columnspan=2)
        ttk.Label(self, text="0", font=bold_font).grid(column=12, row=1, columnspan=2)
        self.second_score_card = ttk.Label(self, image=self.first_image)
        self.second_score_card.grid(column=10, row=2, columnspan=2)
        ttk.Label(self, text="0", font=bold_font).grid(column=12, row=2, columnspan=2)
        self.third_score_card = ttk.Label(self, image=self.first_image)
        self.third_score_card.grid(column=10, row=3, columnspan=2)
        ttk.Label(self, text="0", font=bold_font).grid(column=12, row=3, columnspan=2)

        # insert scorecard
        ## load images
        self.orange_block = add_corners_and_border(Image.open("Resources/Orange.png"), (50, 50))
        self.blue_block = add_corners_and_border(Image.open("Resources/Blue.png"), (50, 50))
        self.gray_block = add_corners_and_border(Image.open("Resources/Gray.png"), (50, 50))
        self.green_block = add_corners_and_border(Image.open("Resources/Green.png"), (50, 50))
        self.streets = add_corners_and_border(Image.open("Resources/Street.png"), (50, 50))
        ## add cells
        ### for blocks
        ttk.Label(self, image=self.orange_block).grid(column=10, row=4, sticky="e")
        self.orange_score = ttk.Label(self, text="0", font=bold_font)
        self.orange_score.grid(column=11, row=4)
        ttk.Label(self, image=self.blue_block).grid(column=10, row=5, sticky="e")
        self.blue_score = ttk.Label(self, text="0", font=bold_font)
        self.blue_score.grid(column=11, row=5)
        ttk.Label(self, image=self.gray_block).grid(column=12, row=4, sticky="e")
        self.gray_score = ttk.Label(self, text="0", font=bold_font)
        self.gray_score.grid(column=13, row=4)
        ttk.Label(self, image=self.green_block).grid(column=12, row=5, sticky="e")
        self.green_score = ttk.Label(self, text="0", font=bold_font)
        self.green_score.grid(column=13, row=5)
        ### for streets
        ttk.Label(self, image=self.streets).grid(column=10, row=6, sticky="e")
        self.street_score = ttk.Label(self, text="0", font=bold_font)
        self.street_score.grid(column=11, row=6)
        ### for goal
        ttk.Label(self, text="Goal Score:", font=bold_font).grid(column=10, row=8, columnspan=2)
        self.goal_score = ttk.Label(self, text="0", font=bold_font)
        self.goal_score.grid(column=12, row=8, sticky="w")
        ### for total
        ttk.Label(self, text="Total Score:", font=bold_font).grid(column=10, row=9, columnspan=2)
        self.total_score = ttk.Label(self, text="0", font=bold_font)
        self.total_score.grid(column=12, row=9, sticky="w")

        # insert hand
        self.first_card = ttk.Label(self, image=self.first_image)
        self.first_card.grid(column=1, row=8, rowspan=2)
        self.second_card = ttk.Label(self, image=self.first_image)
        self.second_card.grid(column=2, row=8, rowspan=2)
        self.third_card = ttk.Label(self, image=self.first_image)
        self.third_card.grid(column=3, row=8, rowspan=2)

        n = 3
        match n:
            case 1:
                self.next_card = ttk.Label(self, image=self.first_image)
                self.next_card.grid(column=4, row=8, rowspan=2, columnspan=6)

            case 2:
                self.next_card = ttk.Label(self, image=self.first_image)
                self.next_card.grid(column=4, row=8, rowspan=2, columnspan=3)
                self.next_card = ttk.Label(self, image=self.first_image)
                self.next_card.grid(column=7, row=8, rowspan=2, columnspan=3)

            case 3:
                self.next_card = ttk.Label(self, image=self.first_image)
                self.next_card.grid(column=4, row=8, rowspan=2, columnspan=2)
                self.next_card = ttk.Label(self, image=self.first_image)
                self.next_card.grid(column=6, row=8, rowspan=2, columnspan=2)
                self.next_card = ttk.Label(self, image=self.first_image)
                self.next_card.grid(column=8, row=8, rowspan=2, columnspan=2)

    def set_controller(self, controller):
        self.controller = controller

    def dummy(self):
        pass

    def quit(self):
        self.master.destroy()
