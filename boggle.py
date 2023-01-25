from boggle_board_randomizer import randomize_board
from GUI import GUI
from ex11_utils import is_valid_path, is_valid_partial_path

class Boggle:
    """
    Class for the Boggle game.
    This class is responsible for handling the game logic
    and for comunication between the logic and GUI.
    """

    def __init__(self, valid_words: list[str]):

        self.__valid_words = valid_words        
        self.__keep_playing = True
        self.__menu_screen_text = "Welcome to Boggle!\nDo you want to play a game?"

    def __setup_game(self) -> None:
        """
        Sets up the board.
        """
        # Create the board
        self.__board = randomize_board()

        # Create the GUI object
        self.__gui = GUI(self, self.__board)
        
        # Sets the game to a neutral state
        self.__words = []
        self.__score = 0

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
        if event_type == "quit_game":
            self.__keep_playing = False
            return True
        
        if event_type == "click_tile":

            y, x = event_data["y"], event_data["x"]
            self.__current_path.append((y, x))
            # Check if the tile is valid
            if not is_valid_partial_path(self.__board, self.__current_path):
                self.__current_path.pop()
                return False

            self.__update_current_word(
                                    self.__current_word +
                                    self.__board[y][x]
                                    )
            
            return True

        if event_type == "add_word":
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
        if not (self.__current_word == "" or self.__current_word in self.__words)\
                and is_valid_path(self.__board, self.__current_path, self.__valid_words) != None:
            # Add the word to the list of words
            self.__words.append(word)
            self.__gui.add_word(self.__current_word)
            # Update the score
            self.__score += len(self.__current_word) ** 2
            self.__gui.update_score(self.__score)

        # Clear the current word
        self.__update_current_word("")
        self.__current_path = []
        
    def play(self):
        
        while(self.__keep_playing):
            self.__setup_game()
            self.__gui.start_game(self.__menu_screen_text)
            self.__menu_screen_text = "Do you want to play again?"
        


if __name__ == "__main__":

    # Open boggle_dict.txt and read the words into a list
    with open("boggle_dict.txt", "r") as f:
        valid_words = f.read().split()
    game = Boggle(valid_words)
    game.play()
