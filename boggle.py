from boggle_board_randomizer import randomize_board
from GUI import GUI

class Boggle:
    """
    Class for the Boggle game.
    This class is responsible for handling the game logic
    and for comunication between the logic and GUI.
    """

    def __init__(self):

        self.__board = randomize_board()

        # Create the GUI object
        self.__gui = GUI(self, self.__board)

        self.__words = []

        self.__current_word = ""
        self.__current_path = []

    def event_from_gui(self, event_type: str, event_data: dict) -> bool:
        """
        Handles events from the GUI.
        :param event_type: The type of event
        :param event_data: The data of the event
        :return: True if the event was successful, False otherwise

        note: 
        For click_tile event, event_data should be a dict with keys "x" and "y"
        representing the coordinates of the tile
        For add_word event, event_data should be None
        """
        if event_type == "click_tile":
            # TODO: Check if the tile is valid i.e if it is adjacent to the last tile

            y, x = event_data["y"], event_data["x"]
            self.__update_current_word(
                                    self.__current_word +
                                    self.__board[y][x]
                                    )
            self.__current_path.append((y, x))
            
            return True

        if event_type == "add_word":
        # TODO: check if the word is valid
            self.__add_word(self.__current_word)
            return True
        
        return False

    def __update_current_word(self, string: str) -> None:
        """
        Updates the current word
        :param string: The new current word
        """
        self.__current_word = string
        # Update the current displayed word
        self.__gui.update_current_word(self.__current_word)
    
    def __add_word(self, word: str) -> None:
        """
        Adds the given word to the list of words
        :param word: The word to add
        """

        # Check if the word is valid
        if not (self.__current_word == "" or self.__current_word in self.__words):            
            self.__words.append(word)
            self.__gui.add_word(self.__current_word)

        self.__update_current_word("")
        self.__current_path = []

    def play(self):
        self.__gui.mainloop()


if __name__ == "__main__":
    game = Boggle()
    game.play()
