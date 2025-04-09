TREBUCHET_MS = "Trebuchet MS"
TITLE_FONT = (TREBUCHET_MS, 35, "bold")
BASIC_FONT = (TREBUCHET_MS, 20)
BOLD_FONT = (TREBUCHET_MS, 20, "bold")

LEFT_MOUSE_BUTTON = "<Button-1>"

CARD_SIZE = (200, 147)

BASE_GAME_MAP = {0: "Sprawlopolis", 1: "Agropolis", 2: "Naturopolis"}
SPRAWLOPOLIS_BASE_MAP = {1: {"card_id": 2, "side": "front"},
                         2: {"card_id": 1, "side": "front"},
                         3: {"card_id": 3, "side": "front"},
                         4: {"card_id": 4, "side": "front"},
                         5: {"card_id": 5, "side": "front"},
                         6: {"card_id": 6, "side": "front"},
                         7: {"card_id": 2, "side": "back"},
                         8: {"card_id": 3, "side": "back"},
                         9: {"card_id": 1, "side": "back"},
                         10: {"card_id": 6, "side": "back"},
                         11: {"card_id": 5, "side": "back"},
                         12: {"card_id": 4, "side": "back"},
                         13: {"card_id": 8, "side": "front"},
                         14: {"card_id": 7, "side": "front"},
                         15: {"card_id": 9, "side": "front"},
                         16: {"card_id": 10, "side": "front"},
                         17: {"card_id": 11, "side": "front"},
                         18: {"card_id": 12, "side": "front"},
                         19: {"card_id": 8, "side": "back"},
                         20: {"card_id": 9, "side": "back"},
                         21: {"card_id": 7, "side": "back"},
                         22: {"card_id": 12, "side": "back"},
                         23: {"card_id": 11, "side": "back"},
                         24: {"card_id": 10, "side": "back"},
                         25: {"card_id": 14, "side": "front"},
                         26: {"card_id": 13, "side": "front"},
                         27: {"card_id": 15, "side": "front"},
                         28: {"card_id": 16, "side": "front"},
                         29: {"card_id": 17, "side": "front"},
                         30: {"card_id": 18, "side": "front"},
                         31: {"card_id": 14, "side": "back"},
                         32: {"card_id": 15, "side": "back"},
                         33: {"card_id": 13, "side": "back"},
                         34: {"card_id": 18, "side": "back"},
                         35: {"card_id": 17, "side": "back"},
                         36: {"card_id": 16, "side": "back"}}
AGROPOLIS_BASE_MAP = {1: {"card_id": 2, "side": "front"},
                      2: {"card_id": 1, "side": "front"},
                      3: {"card_id": 3, "side": "front"}}
NATUROPOLIS_BASE_MAP = {1: {"card_id": 2, "side": "front"},
                        2: {"card_id": 1, "side": "front"},
                        3: {"card_id": 3, "side": "front"}}
CARD_MAPS = {"Sprawlopolis": SPRAWLOPOLIS_BASE_MAP, "Agropolis": AGROPOLIS_BASE_MAP,
             "Naturopolis": NATUROPOLIS_BASE_MAP}


class ScoringFunctions:
    def __init__(self):
        self.id_to_function_map = {"Sprawlopolis": {}, "Agropolis": {}, "Naturopolis": {}}
        self.id_to_function_map["Sprawlopolis"][1] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][2] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][3] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][4] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][5] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][6] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][7] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][8] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][9] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][10] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][11] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][12] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][13] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][14] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][15] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][16] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][17] = lambda x: x
        self.id_to_function_map["Sprawlopolis"][18] = lambda x: x

    def get_function_by_card_id(self, card_id):
        base_game = card_id.split("_")[0]
        card_nr = card_id.split("_")[1]
        return self.id_to_function_map[base_game][card_nr]
