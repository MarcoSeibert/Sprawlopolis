import tkinter as tk
import threading

from controllers import ControllerStart, ControllerMain, ControllerLoading
from models import ModelStart, ModelMain
from views import ViewStart, ViewMain, ViewLoading


class App(tk.Tk):
    def __init__(self, factor_x: float, factor_y: float, offset_factor_y=1):
        super().__init__()

        # get some measurements
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.window_width = int(screen_width / factor_x)
        self.window_height = int(screen_height / factor_y)
        self.offset_x = (screen_width - self.window_width) // 2
        self.offset_y = offset_factor_y * (screen_height - self.window_height) // 2

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
        super().__init__(1E6, 1E6, 0)
        self.attributes("-fullscreen", True)
        # set up loading screen
        self.withdraw()

        loading = Loading(self)
        process_thread = threading.Thread(target=self.start_up,
                                          args=[list_base_games, list_expansions, difficulty, loading])
        process_thread.start()
        loading.controller.play_animation(list_base_games)

    def start_up(self, list_base_games, list_expansions, difficulty, loading):
        # set up model
        model_main = ModelMain(list_base_games, list_expansions, difficulty)

        # set up view
        view_main = ViewMain(self)
        view_main.grid(row=0, column=0, pady=10, padx=10)

        # set up controller
        controller_main = ControllerMain(model_main, view_main)
        view_main.set_controller(controller_main)

        # close loading screen
        loading.destroy()
        self.deiconify()


class Loading(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, bg="white", highlightthickness=0, border=0, borderwidth=0)
        self.title("Loading")
        self.iconbitmap("Resources/Icon.ico")
        window_width = 500
        window_height = 250
        offset_x = (self.winfo_screenwidth() - window_width) // 2
        offset_y = (self.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{offset_x}+{offset_y}")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.focus_force()
        self.update()
        self.view = ViewLoading(self)
        self.view.grid(row=0, column=0)
        self.controller = ControllerLoading(self.view)


if __name__ == "__main__":
    app_start = StartApp()
    app_start.mainloop()
