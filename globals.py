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
                      3: {"card_id": 3, "side": "front"},
                      4: {"card_id": 4, "side": "front"},
                      5: {"card_id": 5, "side": "front"},
                      6: {"card_id": 6, "side": "front"},

                      7: {"card_id": 2, "side": "back"},
                      8: {"card_id": 1, "side": "back"},
                      9: {"card_id": 3, "side": "back"},
                      10: {"card_id": 4, "side": "back"},
                      11: {"card_id": 5, "side": "back"},
                      12: {"card_id": 6, "side": "back"},

                      13: {"card_id": 8, "side": "front"},
                      14: {"card_id": 7, "side": "front"},
                      15: {"card_id": 9, "side": "front"},
                      16: {"card_id": 10, "side": "front"},
                      17: {"card_id": 11, "side": "front"},
                      18: {"card_id": 12, "side": "front"},

                      19: {"card_id": 8, "side": "back"},
                      20: {"card_id": 7, "side": "back"},
                      21: {"card_id": 9, "side": "back"},
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

NATUROPOLIS_BASE_MAP = {1: {"card_id": 6, "side": "front"},
                        2: {"card_id": 5, "side": "front"},
                        3: {"card_id": 4, "side": "front"},
                        4: {"card_id": 3, "side": "front"},
                        5: {"card_id": 2, "side": "front"},
                        6: {"card_id": 1, "side": "front"},

                        7: {"card_id": 6, "side": "back"},
                        8: {"card_id": 1, "side": "back"},
                        9: {"card_id": 3, "side": "back"},
                        10: {"card_id": 2, "side": "back"},
                        11: {"card_id": 4, "side": "back"},
                        12: {"card_id": 5, "side": "back"},

                        13: {"card_id": 12, "side": "front"},
                        14: {"card_id": 11, "side": "front"},
                        15: {"card_id": 10, "side": "front"},
                        16: {"card_id": 9, "side": "front"},
                        17: {"card_id": 8, "side": "front"},
                        18: {"card_id": 7, "side": "front"},

                        19: {"card_id": 12, "side": "back"},
                        20: {"card_id": 11, "side": "back"},
                        21: {"card_id": 10, "side": "back"},
                        22: {"card_id": 9, "side": "back"},
                        23: {"card_id": 8, "side": "back"},
                        24: {"card_id": 7, "side": "back"},

                        25: {"card_id": 18, "side": "front"},
                        26: {"card_id": 17, "side": "front"},
                        27: {"card_id": 16, "side": "front"},
                        28: {"card_id": 15, "side": "front"},
                        29: {"card_id": 14, "side": "front"},
                        30: {"card_id": 13, "side": "front"},

                        31: {"card_id": 18, "side": "back"},
                        32: {"card_id": 17, "side": "back"},
                        33: {"card_id": 16, "side": "back"},
                        34: {"card_id": 13, "side": "back"},
                        35: {"card_id": 14, "side": "back"},
                        36: {"card_id": 15, "side": "back"}}

COMBOPOLIS_I_MAP = {1: {"card_id": 8, "side": "front"},
                    2: {"card_id": 7, "side": "front"},
                    3: {"card_id": 12, "side": "front"},
                    4: {"card_id": 13, "side": "front"},
                    5: {"card_id": 14, "side": "front"},
                    6: {"card_id": 15, "side": "front"},

                    7: {"card_id": 8, "side": "back"},
                    8: {"card_id": 12, "side": "back"},
                    9: {"card_id": 7, "side": "back"},
                    10: {"card_id": 15, "side": "back"},
                    11: {"card_id": 14, "side": "back"},
                    12: {"card_id": 13, "side": "back"}
                    }

COMBOPOLIS_II_MAP = {1: {"card_id": 13, "side": "front"},
                     2: {"card_id": 10, "side": "front"},
                     3: {"card_id": 14, "side": "front"},
                     4: {"card_id": 11, "side": "front"},
                     5: {"card_id": 15, "side": "front"},
                     6: {"card_id": 12, "side": "front"},

                     7: {"card_id": 15, "side": "back"},
                     8: {"card_id": 12, "side": "back"},
                     9: {"card_id": 14, "side": "back"},
                     10: {"card_id": 11, "side": "back"},
                     11: {"card_id": 13, "side": "back"},
                     12: {"card_id": 10, "side": "back"}
                     }

COMBOPOLIS_III_MAP = {1: {"card_id": 14, "side": "front"},
                      2: {"card_id": 11, "side": "front"},
                      3: {"card_id": 15, "side": "front"},
                      4: {"card_id": 12, "side": "front"},
                      5: {"card_id": 16, "side": "front"},
                      6: {"card_id": 13, "side": "front"},

                      7: {"card_id": 16, "side": "back"},
                      8: {"card_id": 13, "side": "back"},
                      9: {"card_id": 15, "side": "back"},
                      10: {"card_id": 12, "side": "back"},
                      11: {"card_id": 14, "side": "back"},
                      12: {"card_id": 11, "side": "back"}
                      }

ULTIMOPOLIS_MAP = {1: {"card_id": "b", "side": "front"},
                   2: {"card_id": "g", "side": "front"},
                   3: {"card_id": "p", "side": "front"},
                   4: {"card_id": "h", "side": "front"},
                   5: {"card_id": "s", "side": "front"},
                   6: {"card_id": "a", "side": "front"},

                   7: {"card_id": "b", "side": "back"},
                   8: {"card_id": "g", "side": "back"},
                   9: {"card_id": "p", "side": "back"},
                   10: {"card_id": "h", "side": "back"},
                   11: {"card_id": "s", "side": "back"},
                   12: {"card_id": "a", "side": "back"}
                   }

CARD_MAPS = {"Sprawlopolis": SPRAWLOPOLIS_BASE_MAP, "Agropolis": AGROPOLIS_BASE_MAP,
             "Naturopolis": NATUROPOLIS_BASE_MAP, "Combopolis_I": COMBOPOLIS_I_MAP, "Combopolis_II": COMBOPOLIS_II_MAP,
             "Combopolis_III": COMBOPOLIS_III_MAP, "Ultimopolis": ULTIMOPOLIS_MAP}


# Fallback class if PnP is not available
class ScoringFunctions:
    def __init__(self):
        self.id_to_function_map = {"Sprawlopolis": {}, "Agropolis": {}, "Naturopolis": {}}
        for i in range(1, 19):
            self.id_to_function_map["Sprawlopolis"][i] = lambda x: x
            self.id_to_function_map["Agropolis"][i] = lambda x: x
            self.id_to_function_map["Naturopolis"][i] = lambda x: x
            if i <= 6:
                self.id_to_function_map["Combopolis_I"][i] = lambda x: x
                self.id_to_function_map["Combopolis_II"][i] = lambda x: x
                self.id_to_function_map["Combopolis_III"][i] = lambda x: x
                self.id_to_function_map["Ultimopolis"][i] = lambda x: x

    def get_function_by_card_id(self, card_id: str):
        base_game = card_id.split("_")[0]
        card_nr = card_id.split("_")[1]
        return self.id_to_function_map[base_game][card_nr]
