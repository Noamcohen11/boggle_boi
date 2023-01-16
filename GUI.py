from tkinter import *
from boggle_board_randomizer import randomize_board

class GUI:
    WIDTH = 800
    HEIGHT = 500

    def __init__(self):

        self.__master = Tk() # Create window
        self.__master.title("Boggle")
        self.__master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.__master.resizable(False, False)
        self.__canvas = Canvas(self.__master, width=self.WIDTH, height=self.HEIGHT) # Create canvas
        self.__canvas.pack()
        self.__board = randomize_board()
        self.__size = (len(self.__board), len(self.__board[0])) # Size of the board
        self.__tiles = self.__create_tiles(self.__size, self.__board)
        self.__current_word = ""
        self.__words = []
        self.__canvas.create_text(170, 90, text="", font=("Arial", 10), tags="current_word")
        self.__add_button = Button(self.__master, text="Add word", command=self.__add_word)
        # place button in top left corner
        self.__add_button.place(x=20, y=50)

    def __create_tiles(self, size: tuple, board: list[list[str]]):
        """Creates tiles for the board
        :param size: a tuple of the dimensions of the board
        :param board: The board
        :return: A list of the tiles
        """        
        tiles = []  # List of tiles
        min_size = min(size)
        tile_size = min(self.WIDTH, self.HEIGHT)*0.9/min_size # Size of each tile
        base = (self.WIDTH//2-tile_size*min_size/2 + 150, self.HEIGHT//2 - tile_size*min_size/2) # Top left corner of the grid
        print("DEBUG: board is ", board)
        for i in range(size[0]): # Create tiles
            for j in range(size[1]):
                x, y = base[0]+tile_size*j, base[1]+tile_size*i # Top left corner of tile
                # Create tile
                tile = self.__canvas.create_rectangle(0, 0, tile_size, tile_size, fill="white", outline="black", tags=f"tile_{i}_{j}")
                # Create text
                self.__canvas.create_text(x + tile_size/2, y+tile_size/2, text=board[i][j], font=("Arial", int(tile_size/2)), tags=f"tile_{i}_{j}")
                # Move tile to correct position
                self.__canvas.move(tile, base[0]+tile_size*j, base[1]+tile_size*i)
                # Bind click event to tile
                self.__canvas.tag_bind(f"tile_{i}_{j}", "<Button-1>", self.__click_tile)
                self.__canvas.tag_bind(f"tile_{i}_{j}", "<Button-3>", self.__click_tile)
                
                tiles.append(tile)
        return tiles # Return list of tiles

    def __click_tile(self, event): # Event handler for clicking a tile
        print("Clicked tile", event.widget.gettags(CURRENT)[0])
        loc = event.widget.gettags(CURRENT)[0].split("_")[1:]
        self.__update_current_word(self.__current_word + self.__board[int(loc[0])][int(loc[1])])

    def __update_current_word(self, string: str):
        self.__current_word = string
        self.__canvas.itemconfig("current_word", text=f"{string}")
        self.__canvas.itemconfig("current_word", text=f"{string}")

    def __add_word(self):
        if self.__current_word == "" or self.__current_word in self.__words:
            return
        self.__words.append(self.__current_word)        
        self.__canvas.create_text(170, 90, text=self.__current_word, font=("Arial", 10), tags=self.__current_word)
        self.__update_current_word("")
        for word in self.__words:
            self.__canvas.move(word, 0, 15)

    def mainloop(self):
        self.__master.mainloop()
    

if __name__ == "__main__":
    app = GUI()
    app.mainloop()