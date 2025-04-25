import random
from tkinter import PhotoImage

import pypdf
from PIL import Image, ImageDraw, ImageTk
from pypdf import PdfReader

from globals import BASE_GAME_MAP, CARD_SIZE, CARD_MAPS

try:
    from pnp_data import ScoringFunctions
except ModuleNotFoundError as e:
    print(e)
    print("Using dummy functions instead")
    from globals import ScoringFunctions


class ModelStart:
    def __init__(self):
        self.list_base_games = [0]
        self.list_expansions = []
        self.difficulty = 1

    def toggle_base(self, base_id: int):
        if base_id in self.list_base_games:
            self.list_base_games.remove(base_id)
        else:
            self.list_base_games.append(base_id)
        return self.list_base_games

    def toggle_exp(self, exp_id: int):
        if exp_id in self.list_expansions:
            self.list_expansions.remove(exp_id)
        else:
            self.list_expansions.append(exp_id)
        return self.list_expansions


def add_corners_and_border(image_raw, card_size: tuple[int, int]) -> PhotoImage:
    image_raw.convert("RGBA")
    image_rotated = image_raw.rotate(-90, expand=True)
    width, height = image_rotated.size
    radius = max(card_size) // 4
    border_width = radius // 2
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=255)
    image_rotated.putalpha(mask)
    border = Image.new("RGBA", (width + border_width * 2, height + border_width * 2), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.rounded_rectangle((0, 0, width + border_width * 2, height + border_width * 2), radius + border_width,
                                  fill=(0, 0, 0, 255))
    border.paste(image_rotated, (border_width, border_width), image_rotated)
    result = border.resize(card_size)
    return ImageTk.PhotoImage(result)


class Deck:
    def __init__(self, game: str, is_base: bool, list_of_expansion: list[str] = None):
        card_size = (200, 147)
        self.cards = []
        card_ids = []
        self.scoring_functions = ScoringFunctions()
        # load card images and scoring functions
        try:
            if is_base:
                file_name = f"{game}_base.pdf"
            else:
                file_name = f"{game}.pdf"
            fp = f"Resources/PnPs/{file_name}"
            reader = PdfReader(fp)
            for i, page in enumerate(reader.pages[1:]):
                for j, image_file_object in enumerate(page.images):
                    image = add_corners_and_border(image_file_object.image, CARD_SIZE)
                    index = i * 6 + j + 1
                    card_nr = CARD_MAPS[game][index]["card_id"]
                    side = CARD_MAPS[game][index]["side"]
                    card_id = f"{game}_{card_nr}"
                    if card_id in card_ids:
                        existing_card = next(card for card in self.cards if card.card_id == card_id)
                        existing_card.add_image(side, image)
                    else:
                        scoring_function = self.scoring_functions.id_to_function_map[game][card_nr]
                        card = Card(card_nr, game, side, image, scoring_function, None)
                        card_ids.append(card_id)
                        self.cards.append(card)
        except FileNotFoundError as ex:
            print(ex)
            print("Using default image instead")
            fp = "Resources/Fallback.jpg"
            image_raw = Image.open(fp)
            image = add_corners_and_border(image_raw, card_size)
            for j in range(1, 19):
                scoring_function = self.scoring_functions.id_to_function_map[game][j]
                card = Card(j, "None", "front", image, scoring_function, None)
                card.add_image("back", image)
                self.cards.append(card)

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop(0)


class Card:
    def __init__(self, card_nr: int, base_game: str, side: str, image: PhotoImage, scoring_function, blocks: list):
        self.card_id = f"{base_game}_{card_nr}"
        self.base_game = base_game
        self.front_image = None
        self.back_image = None
        self.scoring_function = scoring_function
        self.blocks = blocks
        if self.base_game == "Ultimopolis":
            self.points = 13
        else:
            self.points = card_nr

        self.add_image(side, image)

    def add_image(self, side: str, image: PhotoImage):
        if side == "front":
            self.front_image = image
        else:
            self.back_image = image


class Boardstate:
    def __init__(self):
        pass

    def add_card_to_board(self, card: Card, coords: tuple[int, int]):
        pass
        # print(self, card)


class ModelMain:
    def __init__(self, list_base_games: list[str], list_expansions: list[str], difficulty: int, combo: str):
        self.boardstate = Boardstate()
        self.list_base_games = list_base_games
        self.list_expansions = list_expansions
        self.difficulty = difficulty
        self.combo = combo
        self.dict_of_decks = {}
        self.score_cards = []
        self.hand_cards = []
        self.number_of_decks = len(self.list_base_games)

        # Create a deck for every game and put it into a dict
        for game_id in self.list_base_games:
            game_name = BASE_GAME_MAP[game_id]
            deck = Deck(game_name, True)
            self.dict_of_decks[game_name] = deck
        if self.combo:
            combo_deck = Deck(combo, False)
            self.dict_of_decks[combo] = combo_deck
        # If there is only one game, take it. Else take the combo game
        game = list(self.dict_of_decks.keys())[-1]

        # draw three (or four) scoring cards
        if self.number_of_decks == 1:
            # Playing with one base game needs three score cards from this deck
            for _ in range(3):
                self.score_cards.append(self.dict_of_decks[game].deal())
        else:
            # Playing with several base games needs one score card from each + from the combo
            for deck in self.dict_of_decks:
                self.score_cards.append(self.dict_of_decks[deck].deal())

        # draw first card and remove combo deck if available
        self.boardstate.add_card_to_board(self.dict_of_decks[game].deal(), (30, 18))
        if self.number_of_decks != 1:
            self.dict_of_decks.pop(game)

        # draw three (or two) initial hand cards
        if self.number_of_decks == 1:
            # Playing with one base game needs three hand cards from this deck
            for _ in range(3):
                self.hand_cards.append(self.dict_of_decks[game].deal())
        else:
            for deck in self.dict_of_decks:
                self.hand_cards.append(self.dict_of_decks[deck].deal())
