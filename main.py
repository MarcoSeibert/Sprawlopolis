from controllers import ControllerStart
from models import ModelStart
from views import ViewStart
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()


        # get some measurements
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.window_width = screen_width // 2
        self.window_height = screen_height // 2
        self.offset_x = (screen_width - self.window_width) // 2
        self.offset_y = (screen_height - self.window_height) // 2

        # set up basic parameters
        self.title("Sprawlopolis")
        self.geometry(f"{self.window_width}x{self.window_height}+{self.offset_x}+{self.offset_y}")
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file="Resources/Icon.png"))

        # set up model
        model_start = ModelStart()

        # set up view
        view_start = ViewStart(self)
        view_start.grid(row=0, column=0, pady=10, padx=10)

        # set up controller
        controller_start = ControllerStart(model_start, view_start)
        view_start.set_controller(controller_start)

if __name__ == "__main__":
    app = App()
    app.mainloop()