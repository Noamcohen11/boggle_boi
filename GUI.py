from tkinter import *
from time import strftime, time
from boggle_board_randomizer import randomize_board
# from boggle import Boggle
class GUI:
    """
    Class for the GUI of the Boggle game.
    This class is responsible for creating and updating the GUI,
    as well as andling events from the GUI.
    """

    WIDTH = 800
    HEIGHT = 500
    END_TIME = 180
    MENU_SCREEN_TEXT = "Welcome to Boggle!\nDo you want to play a game?"

    def __init__(self, game, board: list[list[str]]):
        """Initializes the connection between the GUI and the game."""
        self.__game = game
        self.__board = board
        self.__num_words = 0
        self.__opening_screen_text = self.MENU_SCREEN_TEXT

    def __create_tiles(self, size: tuple, board: list[list[str]]) -> list:
        """Creates tiles for the board
        :param size: a tuple of the dimensions of the board
        :param board: The board
        :return: A list of the tiles
        """        
        tiles = []  # List of tiles
        min_size = min(size)
        tile_size = min(self.WIDTH, self.HEIGHT)*0.9/min_size # Size of each tile

        # Top left corner of the grid
        base = (
                self.WIDTH//2-tile_size*min_size/2 + 150,
                self.HEIGHT//2 - tile_size*min_size/2) 
        for i in range(size[0]): # Create tiles
            for j in range(size[1]):
                x, y = base[0]+tile_size*j, base[1]+tile_size*i # Top left corner of tile
                # Create tile
                tile = self.__canvas.create_rectangle(0, 0, tile_size, tile_size, fill="white", outline="black", tags=f"tile_{i}_{j}")
                # Create text
                self.__canvas.create_text(x + tile_size/2, y+tile_size/2, text=board[i][j], font=("Arial", int(tile_size/2)), tags=f"text_{i}_{j}")
                # Move tile to correct position
                self.__canvas.move(tile, base[0]+tile_size*j, base[1]+tile_size*i)
                # Bind click event to tile
                self.__canvas.tag_bind(f"tile_{i}_{j}", "<Button-1>", self.__click_tile)
                self.__canvas.tag_bind(f"text_{i}_{j}", "<Button-1>", self.__click_tile)
                
                tiles.append(tile)
        return tiles # Return list of tiles

    def __click_tile(self, event) -> None:
        """Handles click events on tiles.
        Calls the game's event_from_gui method with the event type "click_tile"
        and the coordinates of the tile as event data."""

        tile_tag = event.widget.gettags(CURRENT)[0]
        # Tile tag is in the format "tile_y_x" where y and x are the coordinates of the tile
        y, x = tile_tag.split("_")[1:]
        coordinate_dict = {
                            "y": int(y), 
                            "x": int(x)
                        }
        # Call game's event_from_gui method. If the method returns True, change the color of the tile
        if self.__game.event_from_gui(
                                    event_type="click_tile", 
                                    event_data=coordinate_dict
                                ):
            self.__canvas.itemconfig(f"tile_{y}_{x}", fill="#92cff0")
                
    def __click_add_button(self) -> None:
        """Handles click events on the add word button.
        Calls the game's event_from_gui method with the event type "add_word"
        """

        self.__game.event_from_gui(event_type="add_word", event_data=None)

    def update_current_word(self, string: str) -> None:
        """Updates the current word placeholder with the given string"""
        self.__canvas.itemconfig("current_word", text=f"{string}")
        if string == "":
            self.clear_board()

    def add_word(self, word: str) -> None:
        """Adds the given word to the list of words"""
        if self.__num_words % 2 == 0:
            self.__canvas.move("word", 0, 18)
            self.__canvas.create_text(100, 135, text=word, font=("Arial", 10), tags="word")

        else:
            self.__canvas.create_text(220, 135, text=word, font=("Arial", 10), tags="word")

        self.__num_words += 1

    def clear_board(self) -> None:
        """Clears the board"""
        for tile in self.__tiles:
            self.__canvas.itemconfig(tile, fill="white")

    def __update_clock(self) -> None:
        """Updates the clock"""
        new_time = time() - self.__start_time
        if new_time > self.__end_time:
            self.__root.destroy()

        self.__canvas.itemconfig("time", text=f"Time: {round(new_time)}")
        self.__root.after(1000, self.__update_clock)
        
    def update_score(self, score: int) -> None:
        """Updates the score
        :param score: The new score
        """
        self.__canvas.itemconfig("score", text=f"Score: {score}")
    
    def __menu_screen(self, text: str = "") -> None:
        """Shows the openeing screen"""

        self.__opening_screen = Tk()
        self.__opening_screen.title("Opening Screen")
        self.__opening_screen.geometry("600x300")
        self.__opening_screen.resizable(False, False)

        # Create opening screen text
        opening_screen_text = Label(
                                    self.__opening_screen,
                                    text=text,
                                    font=("Arial", 20)
                                    )
        
        # Create play button action i.e exit the opening screen and start the game
        play_button_action = lambda *args: self.__opening_screen.destroy() or self.__play_game()

        # Create quit button action i.e exit the opening screen
        quit_button_action = lambda *args: self.__opening_screen.destroy() or self.__game.event_from_gui("quit_game", None)

        # Create play and quit buttons
        play_button = Button(
                            self.__opening_screen,
                            text="Play",
                            height=3,
                            width=10,
                            bg="#8efaad",
                            command=play_button_action
                            )

        quit_button = Button(
                            self.__opening_screen,
                            text="Quit",
                            height=3,
                            width=10,
                            bg="#fc9790",
                            command=quit_button_action
                            )

        # Place the buttons on the screen
        opening_screen_text.pack()

        play_button.pack()
        play_button.place(relx=0.25, rely=0.5, anchor=CENTER)
        quit_button.pack()
        quit_button.place(relx=0.75, rely=0.5, anchor=CENTER)


        self.__opening_screen.mainloop()

    def start_game(self, text: str = "") -> None:
        """Starts the mainloop of the game"""        
        self.__menu_screen(text)

    def __play_game(self) -> None:
        """Starts the game"""

        self.__root = Tk() # Create window
        self.__root.title("Boggle")
        self.__root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.__root.resizable(False, False)

        
        # Create canvas
        self.__canvas = Canvas(self.__root, width=self.WIDTH, height=self.HEIGHT) # Create canvas
        self.__canvas.pack()


        # Create board
        self.__size = (len(self.__board), len(self.__board[0])) # Size of the board
        
        self.__tiles = self.__create_tiles(self.__size, self.__board)

        # Create current word placeholder and add word button
        self.__canvas.create_text(200, 70, text="", font=("Arial", 19, "bold"), tags="current_word")
        self.__add_button = Button(self.__root, text="Add word", font=("Arial", 10, "bold"), height=2, command=self.__click_add_button)
        self.__add_button.place(x=20, y=50)

        # Create a block for the words
        self.__canvas.create_rectangle(20, 100, 305, 400, fill="white", outline="black", tags="words_block")
        self.__canvas.create_text(155, 110, text="Words", font=("Arial", 10), tags="words_block")

        # Create a clock and a score
        self.__start_time = time()
        self.__end_time = self.END_TIME
        self.__canvas.create_text(50, 10, text="Time: 0", font=("Arial", 10), tags="time")
        self.__canvas.create_text(200, 10, text="Score: 0", font=("Arial", 10), tags="score")

        self.__update_clock()
        self.__root.mainloop()
    
if __name__ == "__main__":
    print("Error: This file is not meant to be run directly.")