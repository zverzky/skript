import random

class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.positions = []

    def place_ship(self, positions):
        if len(positions) == self.length:
            self.positions = positions
            return True
        else:
            return False

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['O' for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, ship, positions):
        if self.is_valid_position(positions):
            for x, y in positions:
                self.grid[y][x] = 'S'
            ship.place_ship(positions)
            self.ships.append(ship)
            return True
        else:
            return False

    def is_valid_position(self, positions):
        for x, y in positions:
            if x < 0 or x >= self.size or y < 0 or y >= self.size or self.grid[y][x] == 'S':
                return False
        return True

    def is_empty_position(self, x, y):
        return self.grid[y][x] == 'O'

    def is_ship_position(self, x, y):
        return self.grid[y][x] == 'S'

    def display(self, hide_ships):
        for row in self.grid:
            print(' '.join(['X' if cell == 'S' and hide_ships else cell for cell in row]))
        print()

class Game:
    def __init__(self, size):
        self.size = size
        self.player_board = Board(size)
        self.computer_board = Board(size)

    def random_position(self, length):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        is_horizontal = random.choice([True, False])
        positions = []
        for i in range(length):
            if is_horizontal:
                positions.append((x + i, y))
            else:
                positions.append((x, y + i))
        return positions

    def setup_player_board(self):
        print("Let's setup your board!")
        for ship_name, ship_length in zip(['Carrier', 'Battleship', 'Submarine', 'Destroyer', 'Patrol Boat'], [5, 4, 3, 3, 2]):
            print(f"Placing {ship_name}...")
            positions = []
            while not positions:
                try:
                    x, y = map(int, input(f"Enter the coordinates for the {ship_name} (length {ship_length}): ").split(','))
                    orientation = input("Enter orientation (h for horizontal, v for vertical): ")
                    if orientation == 'h':
                        positions = [(x + i, y) for i in range(ship_length)]
                    elif orientation == 'v':
                        positions = [(x, y + i) for i in range(ship_length)]
                    else:
                        print("Invalid orientation! Please enter 'h' or 'v'.")
                        positions = []
                    if not all(0 <= x < self.size and 0 <= y < self.size for x, y in positions):
                        print("Ship out of bounds! Please enter different coordinates.")
                        positions = []
                except ValueError:
                    print("Invalid input! Please enter in the format 'x,y'.")
            while not self.player_board.place_ship(Ship(ship_name, ship_length), positions):
                print("Invalid position! Ship overlaps with existing ships or is out of bounds.")
                positions = []
                while not positions:
                    try:
                        x, y = map(int, input(f"Re-enter the coordinates for the {ship_name} (length {ship_length}): ").split(','))
                        orientation = input("Re-enter orientation (h for horizontal, v for vertical): ")
                        if orientation == 'h':
                            positions = [(x + i, y) for i in range(ship_length)]
                        elif orientation == 'v':
                            positions = [(x, y + i) for i in range(ship_length)]
                        else:
                            print("Invalid orientation! Please enter 'h' or 'v'.")
                            positions = []
                        if not all(0 <= x < self.size and 0 <= y < self.size for x, y in positions):
                            print("Ship out of bounds! Please enter different coordinates.")
                            positions = []
                    except ValueError:
                        print("Invalid input! Please enter in the format 'x,y'.")

    def setup_computer_board(self):
        print("Setting up computer's board...")
        for ship_name, ship_length in zip(['Carrier', 'Battleship', 'Submarine', 'Destroyer', 'Patrol Boat'], [5, 4, 3, 3, 2]):
            positions = self.random_position(ship_length)
            while not self.computer_board.place_ship(Ship(ship_name, ship_length), positions):
                positions = self.random_position(ship_length)

    def player_turn(self):
        print("Player's turn!")
        self.computer_board.display(True)
        while True:
            try:
                x, y = map(int, input("Enter the coordinates to attack: ").split(','))
                if not (0 <= x < self.size and 0 <= y < self.size):
                    print("Invalid coordinates! Please enter within the board size.")
                elif self.computer_board.is_ship_position(x, y):
                    print("Hit!")
                    self.computer_board.grid[y][x] = 'X'
                    for ship in self.computer_board.ships:
                        if (x, y) in ship.positions:
                            ship.positions.remove((x, y))
                            if not ship.positions:
                                print(f"You sunk the {ship.name}!")
                    if all(not ship.positions for ship in self.computer_board.ships):
                        print("Computer's ships are all sunk! You win!")
                        return
                    else:
                        break
                else:
                    print("Miss!")
                    self.computer_board.grid[y][x] = 'M'
                    break
            except ValueError:
                print("Invalid input! Please enter in the format 'x,y'.")

    def computer_turn(self):
        print("Computer's turn!")
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.player_board.is_ship_position(x, y):
                print(f"The computer attacks {x},{y} and hits your ship!")
                self.player_board.grid[y][x] = 'X'
                for ship in self.player_board.ships:
                    if (x, y) in ship.positions:
                        ship.positions.remove((x, y))
                        if not ship.positions:
                            print(f"The computer sunk your {ship.name}!")
                if all(not ship.positions for ship in self.player_board.ships):
                    print("Your ships are all sunk! Computer wins!")
                    return
                else:
                    break
            elif self.player_board.is_empty_position(x, y):
                print(f"The computer attacks {x},{y} and misses!")
                self.player_board.grid[y][x] = 'M'
                break

    def play(self):
        self.setup_player_board()
        self.setup_computer_board()
        while True:
            self.player_turn()
            self.computer_turn()

# Инициализация и запуск игры
game = Game(10)
game.play()
