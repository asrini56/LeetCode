"""
class Game:
    - board: Board
    - player1: Player
    - player2: Player
    - currentPlayer: Player
    - state: GameState        // IN_PROGRESS, WON, DRAW
    - winner: Player?

    + Game(player1, player2)
    + makeMove(player, column) -> bool
    + getCurrentPlayer() -> Player
    + getGameState() -> GameState
    + getWinner() -> Player?
    + getBoard() -> Board

class Board:
    - rows: int = 6
    - cols: int = 7
    - grid: DiscColor?[rows][cols]

    + Board()
    + getRows() -> int
    + getCols() -> int
    + canPlace(column) -> bool
    + placeDisc(column, color) -> int
    + isFull() -> bool
    + checkWin(row, column, color) -> bool
    + getCell(row, column) -> DiscColor?

class Player:
    - name: string
    - color: DiscColor

    + Player(name, color)
    + getName() -> string
    + getColor() -> DiscColor

enum GameState:
    IN_PROGRESS
    WON
    DRAW

enum DiscColor:
    RED
    YELLOW
"""

from enum import Enum
from typing import Optional, List

class GameState(Enum):
    IN_PROGRESS = 1
    WON = 2
    DRAW = 3

class DiscColor(Enum):
    RED = 1
    YELLOW = 2

class Player:
    def __init__(self, name: str, color: DiscColor):
        self._name = name
        self._color = color

    def get_name(self) -> str:
        return self._name

    def get_color(self) -> DiscColor:
        return self._color

class Board:
    def __init__(self, rows: int = 6, cols: int = 7):
        self.rows = rows
        self.cols = cols
        # Initialize the 2D grid with None (empty cells)
        self.grid: List[List[Optional[DiscColor]]] = [[None for _ in range(cols)] for _ in range(rows)]

    def get_rows(self) -> int:
        return self.rows

    def get_cols(self) -> int:
        return self.cols

    def can_place(self, column: int) -> bool:
        if column < 0 or column >= self.cols:
            return False
        # If the top cell of the column is empty, a disc can be dropped
        return self.grid[0][column] is None

    def place_disc(self, column: int, color: DiscColor) -> int:
        """Simulates gravity: drops the disc to the lowest available row in the column."""
        for r in range(self.rows - 1, -1, -1):
            if self.grid[r][column] is None:
                self.grid[r][column] = color
                return r
        raise ValueError(f"Column {column} is full.")

    def is_full(self) -> bool:
        return all(self.grid[0][c] is not None for c in range(self.cols))

    def get_cell(self, row: int, column: int) -> Optional[DiscColor]:
        return self.grid[row][column]

    def check_win(self, row: int, col: int, color: DiscColor) -> bool:
        """
        Optimized O(1) win checker that scans only the 4 axes passing 
        through the newly placed disc coordinate (row, col).
        """
        directions = [
            (0, 1),   # Horizontal (Left <-> Right)
            (1, 0),   # Vertical (Up <-> Down)
            (1, 1),   # Diagonal / (Top-Left <-> Bottom-Right)
            (1, -1)   # Diagonal \ (Bottom-Left <-> Top-Right)
        ]

        for dx, dy in directions:
            count = 1  # Count the current placed disc itself
            
            # Count in positive and negative directions along the axis
            count += self._count_direction(row, col, dx, dy, color)
            count += self._count_direction(row, col, -dx, -dy, color)

            if count >= 4:
                return True

        return False

    def _count_direction(self, start_row: int, start_col: int, dx: int, dy: int, color: DiscColor) -> int:
        count = 0
        r, c = start_row + dx, start_col + dy

        while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == color:
            count += 1
            r += dx
            c += dy

        return count

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.state = GameState.IN_PROGRESS
        self.winner: Optional[Player] = None

    def make_move(self, player: Player, column: int) -> bool:
        # Validate game state
        if self.state != GameState.IN_PROGRESS:
            return False

        # Validate turn order
        if self.current_player != player:
            return False

        # Validate column availability
        if not self.board.can_place(column):
            return False

        # Execute move (drop disc via gravity and get landing row)
        row = self.board.place_disc(column, player.get_color())

        # Evaluate win or draw conditions
        if self.board.check_win(row, column, player.get_color()):
            self.state = GameState.WON
            self.winner = player
        elif self.board.is_full():
            self.state = GameState.DRAW
        else:
            # Alternate turn
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

        return True

    def get_current_player(self) -> Player:
        return self.current_player

    def get_game_state(self) -> GameState:
        return self.state

    def get_winner(self) -> Optional[Player]:
        return self.winner

    def get_board(self) -> Board:
        return self.board
