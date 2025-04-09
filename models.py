import random
from tkinter import PhotoImage

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


def add_corners_and_border(image_raw: Image, card_size: tuple[int, int]) -> PhotoImage:
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
    def __init__(self, game, _):
        card_size = (200, 147)
        self.cards = []
        self.card_ids = []
        self.scoring_functions = ScoringFunctions()
        # load card images and scoring functions
        try:
            file_name = f"{game}_base.pdf"
            fp = f"Resources/PnPs/{file_name}"
            reader = PdfReader(fp)
            for i, page in enumerate(reader.pages[1:]):
                for j, image_file_object in enumerate(page.images):
                    image = add_corners_and_border(image_file_object.image, CARD_SIZE)
                    index = i * 6 + j + 1
                    card_nr = CARD_MAPS["Sprawlopolis"][index]["card_id"]
                    side = CARD_MAPS["Sprawlopolis"][index]["side"]
                    card_id = f"{game}_{card_nr}"
                    if card_id in self.card_ids:
                        existing_card = next(card for card in self.cards if card.card_id == card_id)
                        existing_card.add_image(side, image)
                    else:
                        scoring_function = self.scoring_functions.id_to_function_map["Sprawlopolis"][card_nr]
                        card = Card(card_nr, game, side, image, scoring_function, None)
                        self.card_ids.append(card_id)
                        self.cards.append(card)
        except FileNotFoundError as ex:
            print(ex)
            print("Using default image instead")
            fp = "Resources/Fallback.jpg"
            image_raw = Image.open(fp)
            image = add_corners_and_border(image_raw, card_size)
            for j in range(18):
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
    def __init__(self, card_nr, base_game, side, image, scoring_function, blocks):
        self.card_id = f"{base_game}_{card_nr}"
        self.points = card_nr
        self.base_game = base_game
        self.front_image = None
        self.back_image = None
        self.scoring_function = scoring_function
        self.blocks = blocks

        self.add_image(side, image)

    def add_image(self, side, image):
        if side == "front":
            self.front_image = image
        else:
            self.back_image = image

class Boardstate:
    def __init__(self):
        pass

    def add_card_to_board(self, card):
        print(self, card)

class ModelMain:
    def __init__(self, list_base_games, list_expansions, difficulty):
        self.boardstate = Boardstate()
        self.list_base_games = list_base_games
        self.list_expansions = list_expansions
        self.difficulty = difficulty
        self.dict_of_decks = {}
        self.score_cards = []
        self.hand_cards = []
        self.number_of_decks = len(self.list_base_games)

        for game_id in self.list_base_games:
            game_name = BASE_GAME_MAP[game_id]
            deck = Deck(game_name, self.list_expansions)
            self.dict_of_decks[game_name] = deck

        if self.number_of_decks == 1:
            game = list(self.dict_of_decks.keys())[0]
        else:
            # todo adjust for combo
            game = list(self.dict_of_decks.keys())[0]

        # draw three (or four) scoring cards
        if self.number_of_decks == 1:
            for _ in range(3):
                self.score_cards.append(self.dict_of_decks[game].deal())
        else:
            match sorted(self.list_base_games):
                case [0, 1]:
                    # todo take goal cards from all three decks (2*base + combo)
                    for _ in range(3):
                        self.score_cards.append(self.dict_of_decks[game].deal())
                    print("Using Combopolis I")
                case [0, 2]:
                    print("Using Combopolis II")
                case [1, 2]:
                    print("Using Combopolis III")
                case [0, 1, 2]:
                    # todo take goal cards from all four decks (3*base + ultimo)
                    for _ in range(4):
                        self.score_cards.append(self.dict_of_decks[game].deal())
                    print("Using Ultimopolis = 4 cards")

        # draw three (or two) initial hand cards
        # todo make case for 3 with all three decks
        if self.number_of_decks == 1 or self.number_of_decks == 3:
            for _ in range(3):
                self.hand_cards.append(self.dict_of_decks[game].deal())
        # todo make case for 2 from both decks
        else:
            for _ in range(2):
                self.hand_cards.append(self.dict_of_decks[game].deal())

        # draw first card
        if self.number_of_decks == 1:
            self.boardstate.add_card_to_board(self.dict_of_decks[game].deal())
