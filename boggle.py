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

    def event_from_gui(self, event_type: str, event_data: dict) -> None:
        """
        Handles events from the GUI.
        :param event_type: The type of event
        :param event_data: The data of the event
        :return: None

        note: 
        For click_tile event, event_data should be a dict with keys "x" and "y"
        representing the coordinates of the tile
        For add_word event, event_data should be None
        """
        if event_type == "click_tile":
            self.__update_current_word(
                                    self.__current_word +
                                    self.__board[event_data["x"]][event_data["y"]]
                                    )
            self.__gui.update_current_word(self.__current_word)

        if event_type == "add_word":
            self.__add_word(self.__current_word)
            print("DEBUG: words is ", self.__words)

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

        if self.__current_word == "" or self.__current_word in self.__words:
            return
        self.__words.append(word)
        self.__gui.add_word(self.__current_word)
        self.__update_current_word("")

    def play(self):
        self.__gui.mainloop()


if __name__ == "__main__":
    game = Boggle()
    game.play()
