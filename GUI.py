from tkinter import *
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

    def __init__(self, game, board: list[list[str]]):

        # Create window
        self.__master = Tk() # Create window
        self.__master.title("Boggle")
        self.__master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.__master.resizable(False, False)

        # Create canvas
        self.__canvas = Canvas(self.__master, width=self.WIDTH, height=self.HEIGHT) # Create canvas
        self.__canvas.pack()

        self.__game = game

        # Create board
        self.__board = board
        self.__size = (len(self.__board), len(self.__board[0])) # Size of the board
        
        self.__tiles = self.__create_tiles(self.__size, self.__board)

        # Create current word placeholder and add word button
        self.__canvas.create_text(170, 90, text="", font=("Arial", 10), tags="current_word")
        self.__add_button = Button(self.__master, text="Add word", command=self.__click_add_button)
        self.__add_button.place(x=20, y=50)

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
        print("DEBUG: board is ", board)
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
            self.__canvas.itemconfig(f"tile_{y}_{x}", fill="#fc9790")
        
        

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
        self.__canvas.create_text(170, 90, text=word, font=("Arial", 10), tags="word")
        self.__canvas.move("word", 0, 15)

    def clear_board(self) -> None:
        """Clears the board"""
        for tile in self.__tiles:
            self.__canvas.itemconfig(tile, fill="white")

    def mainloop(self):
        """Starts the mainloop of the game"""
        self.__master.mainloop()
    

if __name__ == "__main__":
    print("Error: This file is not meant to be run directly.")