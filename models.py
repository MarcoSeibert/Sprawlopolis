import random

from PIL import Image, ImageDraw, ImageTk
from pypdf import PdfReader

from globals import BASE_GAME_MAP, CARD_SIZE, CARD_MAPS


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


#
#
# def get_first_picture():
#    card_size = (200, 147)
#    fp = "Resources/PnPs/Sprawlopolis_base.pdf"
#    try:
#        reader = PdfReader(fp)
#        page = reader.pages[1]
#        first_image = None
#        for count, image_file_object in enumerate(page.images):
#            image = image_file_object.image
#            first_image = image.rotate(90, expand=True)
#            break
#    except FileNotFoundError:
#        first_image = Image.open("Resources/Fallback.jpg")

# image = add_corners_and_border(first_image, card_size)
# return image

class Deck:
    def __init__(self, base_game, _):
        card_size = (200, 147)
        self.cards = []
        self.card_ids = []
        game = BASE_GAME_MAP[base_game]
        try:
            file_name = f"{game}_base.pdf"
            fp = f"Resources/PnPs/{file_name}"
            reader = PdfReader(fp)
            for i, page in enumerate(reader.pages[1:]):
                for j, image_file_object in enumerate(page.images):
                    image_raw = image_file_object.image
                    image_rotated = image_raw.rotate(-90, expand=True)
                    image = add_corners_and_border(image_rotated, CARD_SIZE)
                    index = i * 6 + j + 1
                    card_id = CARD_MAPS[game][index]["card_id"]
                    side = CARD_MAPS[game][index]["side"]
                    if card_id in self.card_ids:
                        existing_card = next(card for card in self.cards if card.card_id == card_id)
                        existing_card.add_image(side, image)
                    else:
                        card = Card(image, card_id, side)
                        self.card_ids.append(card_id)
                        self.cards.append(card)
        except FileNotFoundError as e:
            print(e)
            print("Using default image instead")
            fp = "Resources/Fallback.jpg"
            image_raw = Image.open(fp)
            image = add_corners_and_border(image_raw, card_size)
            for j in range(18):
                card = Card(image, j, "front")
                card.add_image("back", image)
                self.cards.append(card)

class Card:
    def __init__(self, image, card_id, side):
        self.front_image = None
        self.back_image = None
        self.add_image(side, image)
        self.card_id = card_id

    def add_image(self, side, image):
        if side == "front":
            self.front_image = image
        else:
            self.back_image = image


class ModelMain:
    def __init__(self, list_base_games, list_expansions, difficulty):
        self.list_base_games = list_base_games
        self.list_expansions = list_expansions
        self.difficulty = difficulty
        self.list_of_decks = []
        for game in self.list_base_games:
            deck = Deck(game, self.list_expansions)
            self.list_of_decks.append(deck)
        self.score_cards = []
        for i in range(3):
            self.score_cards.append(i)
