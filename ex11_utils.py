from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Tile = Tuple[int, int]
Path = List[Tile]

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


def __coord_legal(coordinate: Tile, board: Board) -> bool:
    """Checks if a coordinate is legal on the board.
    :param coordinate: tuple representing the coordinate.
    :param board: two dimensional list of strings representing the board.
    :return: True if the coordinate is legal, False otherwise."""
    x, y = coordinate
    return 0 <= x < len(board) and 0 <= y < len(board[0])


def __possibe_movements(tile: Tile, board) -> List[Tile]:
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


def __partial_words_set(
    words: Iterable[str], use_max_size=False, max_word_size: int = -1
) -> set[str]:
    """create a set of all partial words from dict

    Args:
        words (Iterable[str]): list of strings representing the words that can be formed.
        use_max_size (bool, optional): If True, only add
            partial words from words that are smaller than max_word_size
        max_word_size (int, optional): max word size to use. Defaulty not used.

    Returns:
        set[str]: set of all partial words.
    """
    partial_words = set()
    for word in words:
        if use_max_size and len(word) > max_word_size:
            continue
        partial_words.update({word[0:i] for i in range(len(word) + 1)})
    return partial_words


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
    partial_words: set,
    tile: Tile,
    use_tile_size: bool,
    save_undersized_words: bool,
    current_path: Path = [],
) -> List[Path]:
    """Finds all paths of length n starting from a given tile.
    :param use_tile_size: changes the value of the parameter n.
    :param save_undersized_words: if True, saves paths for words that are undersized.
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

    updated_path = current_path + [tile]
    # Get the new word:
    word = __word_from_path(board, updated_path)

    # If we got the entire word, Check if it is in the list of words.
    if n == new_string_size:
        if word in words:
            return [updated_path]
        return []
    # Check if the partial word we are building can form a word.
    if word not in partial_words:
        return []
    # If the tile has a string that is too long, we can't form an n sized word.
    if new_string_size > n:
        return []

    # Continue to search for paths.
    paths = []

    # if the word is in the list of words, but is undersized, we can still save it.
    if word in words and save_undersized_words:
        paths.append(updated_path)

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
            partial_words,
            new_tile,
            use_tile_size,
            save_undersized_words,
            updated_path,
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
        partial_words = __partial_words_set(words)
        for i in range(len(board)):
            for j in range(len(board[0])):
                paths += __find_paths(
                    n,
                    board,
                    words,
                    partial_words,
                    (i, j),
                    use_tile_size=False,
                    save_undersized_words=False,
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
        partial_words = __partial_words_set(
            words, use_max_size=True, max_word_size=n
        )
        for i in range(len(board)):
            for j in range(len(board[0])):
                paths += __find_paths(
                    n,
                    board,
                    words,
                    partial_words,
                    (i, j),
                    use_tile_size=True,
                    save_undersized_words=False,
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

    paths = []
    partial_words = __partial_words_set(
        words, use_max_size=True, max_word_size=max_path_len
    )
    for i in range(len(board)):
        for j in range(len(board[0])):
            paths += __find_paths(
                max_path_len,
                board,
                words,
                partial_words,
                (i, j),
                use_tile_size=False,
                save_undersized_words=True,
            )

    paths.sort(key=len, reverse=True)
    # Remove duplicates.
    for path in paths:
        # Check if the word was already found.
        word = __word_from_path(board, path)
        if word not in found_words_list:
            found_words_list.append(word)
            tot_paths.append(path)

    return tot_paths
