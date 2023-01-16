from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]

# legal directions to move in.
DIRECTIONS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
]


def __coord_legal(coordinate: Tuple[int, int], board: Board) -> bool:
    """Checks if a coordinate is legal on the board.
    :param coordinate: tuple representing the coordinate.
    :param board: two dimensional list of strings representing the board.
    :return: True if the coordinate is legal, False otherwise."""
    x, y = coordinate
    return 0 <= x < len(board) and 0 <= y < len(board[0])


def __possibe_movements(tile: Tuple[int, int], board):
    """Finds all possible movements from a given tile.
    :param tile: tuple representing the tile.
    :param board: two dimensional list of strings representing the board.
    :return: list of tuples representing the possible movements."""
    possible_movements = []
    for x, y in DIRECTIONS:
        new_tile = (tile[0] + x, tile[1] + y)
        if __coord_legal(new_tile, board):
            possible_movements.append(new_tile)
    return possible_movements


def is_valid_path(
    board: Board, path: Path, words: Iterable[str]
) -> Optional[str]:
    """
    Checks if the path is valid and returns the word if it is.
    :param board: two dimensional list of strings representing the board
    :param path: list of tuples representing the path taken to form a word.
    :param words: list of strings representing the words that can be formed.
    :return: the word if the path is valid, None otherwise."""
    # Check if the path is empty.
    if len(path) == 0:
        return None

    # Check if the path uses a tile twice.
    if len(path) != len(set(path)):
        return None

    # Initialize the word with the first tile.
    if not __coord_legal(path[0], board):
        return None
    former_x, former_y = path[0]
    word = board[former_x][former_y]

    # Check if the rest of the path is legal.
    for x, y in path[1::]:
        if (x, y) not in __possibe_movements((former_x, former_y), board):
            return None
        word += board[x][y]
        former_x, former_y = x, y
        
    if word in words:
        return word

    return None


def __word_from_path(board: Board, path: Path) -> str:
    """Returns the word formed by a given path.
    :param board: two dimensional list of strings representing the board.
    :param path: list of tuples representing the path taken to form a word.
    :return: the word formed by the path."""
    return "".join([board[x][y] for x, y in path])


def __find_paths(
    n: int,
    board: Board,
    words: Iterable[str],
    tile: Tuple[int, int],
    use_tile_size: bool,
    current_path: Path = [],
) -> List[Path]:
    """Finds all paths of length n starting from a given tile.
    :param use_tile_size: changes the value of the parameter n.
    :param n: if use_tile_size is True, n is the length of the path, otherwise
    it is the length of the word.
    :param board: two dimensional list of strings representing the board.
    :param words: list of strings representing the words that can be formed.
    :param tile: tuple representing the tile to start from.
    :param current_path: list of tuples representing the path taken so far.
    :return: list of paths of length n starting from the given tile."""

    if use_tile_size:
        new_string_size = len(board[tile[0]][tile[1]])
    else:
        new_string_size = 1

    new_path = current_path + [tile]

    # If we got the entire word, Check if it is in the list of words.
    if n == new_string_size:
        # Get the new word:
        word = __word_from_path(board, new_path)
        if word in words:
            return [new_path]
        return []

    # If the tile has a string that is too long, we can't form an n sized word.
    if new_string_size > n:
        return []

    # Continue to search for paths.
    paths = []
    new_tiles = __possibe_movements(tile, board)
    for new_tile in new_tiles:

        # We can't return to a tile we already visited.
        if new_tile in current_path:
            continue
        # Add the new tile to the path.
        for path in __find_paths(
            n - new_string_size,
            board,
            words,
            new_tile,
            use_tile_size,
            new_path,
        ):
            paths.append(path)
    return paths


def find_length_n_paths(
    n: int, board: Board, words: Iterable[str]
) -> List[Path]:
    """Finds all paths of length n form every possible tile.
    :param n: the length of the path.
    :param board: two dimensional list of strings representing the board.
    :param words: list of strings representing the words that can be formed.
    :param tile: tuple representing the tile to start from.
    :return: list of paths of length n form every possible tile.
    """
    if n == 0:
        return []
    else:
        paths = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                paths += __find_paths(
                    n, board, words, (i, j), use_tile_size=False
                )
        return paths


def find_length_n_words(
    n: int, board: Board, words: Iterable[str]
) -> List[Path]:
    """Finds all paths that form a word of length n form every possible tile.
    :param n: the length of the word.
    :param board: two dimensional list of strings representing the board.
    :param words: list of strings representing the words that can be formed.
    :param tile: tuple representing the tile to start from.
    :return: list of paths that form a word of length n form every possible tile.
    """
    if n == 0:
        return []
    else:
        paths = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                paths += __find_paths(
                    n, board, words, (i, j), use_tile_size=True
                )
        return paths


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    Finds the paths that form the longest path.
    :param board: two dimensional list of strings representing the board.
    :param words: list of strings representing the words that can be formed.
    :return: list of the longest paths.
    """
    # Find the longest possible word in the dictionary.
    max_path_len = len(max(words, key=len))
    found_words_list = []
    tot_paths = []

    for n in range(max_path_len, 0, -1):
        paths = find_length_n_paths(n, board, words)
        for path in paths:
            # Check if the word was already found.
            word = __word_from_path(board, path)
            if word not in found_words_list:
                found_words_list.append(word)
                tot_paths.append(path)

    return tot_paths
