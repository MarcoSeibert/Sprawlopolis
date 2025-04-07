from controllers import ControllerStart, ControllerMain
from models import ModelStart, ModelMain
from views import ViewStart, ViewMain
import tkinter as tk


class App(tk.Tk):
    def __init__(self, factor_x: float, factor_y: float):
        super().__init__()

        # get some measurements
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.window_width = int(screen_width / factor_x)
        self.window_height = int(screen_height / factor_y)
        self.offset_x = (screen_width - self.window_width) // 2
        self.offset_y = (screen_height - self.window_height) // 2

        # set up basic parameters
        self.title("Sprawlopolis")
        self.geometry(f"{self.window_width}x{self.window_height}+{self.offset_x}+{self.offset_y}")
        self.resizable(False, False)
        self.iconbitmap("Resources/Icon.ico")


class StartApp(App):
    def __init__(self):
        super().__init__(2, 2)

        # set up model
        model_start = ModelStart()

        # set up view
        view_start = ViewStart(self)
        view_start.grid(row=0, column=0, pady=10, padx=10)

        # set up controller
        controller_start = ControllerStart(model_start, view_start)
        view_start.set_controller(controller_start)

    def start_game(self, list_base_games, list_expansions, difficulty):
        self.destroy()
        app_game = MainApp(list_base_games, list_expansions, difficulty)
        app_game.focus_force()
        app_game.mainloop()


class MainApp(App):
    def __init__(self, list_base_games, list_expansions, difficulty):
        super().__init__(1, 1)
        self.attributes("-fullscreen", 1)
        # set up model
        model_main = ModelMain(list_base_games, list_expansions, difficulty)

        # set up view
        view_main = ViewMain(self)
        view_main.grid(row=0, column=0, pady=10, padx=10)

        # set up controller
        controller_main = ControllerMain(model_main, view_main)
        view_main.set_controller(controller_main)


if __name__ == "__main__":
    app_start = StartApp()
    app_start.mainloop()
