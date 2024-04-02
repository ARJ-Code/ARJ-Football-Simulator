class Field:
    def __init__(self, rows = 40, columns = 24):
        self.rows = rows
        self.columns = columns
        self.grid = [["J" for _ in range(columns)] for _ in range(rows)]
        self.goal_A = [(0, columns // 2), (0, columns // 2 + 1)]
        self.goal_B = [(rows - 1, columns // 2), (rows - 1, columns // 2 -1),(rows - 1, columns // 2 + 2),(rows - 1, columns // 2 + 1)]

    def print_field(self):
        for row in self.grid:
            print(row)

    def place_player(self, player: str, row: int, column: int):
        self.grid[row][column] = (player)

    def erase_player(self, row: int, column: int):
        self.grid[row][column] = "J"

    def close_to_goal_A(self, row: int, column: int):
        return row < 4 and column < self.goal_A[1][1] +4 and column>self.goal_A[0][1] -4
    
    def close_to_goal_B(self, row: int, column: int):
        return row > self.rows - 5 and column < self.goal_B[1][1] +4 and column>self.goal_B[0][1] -4
    
    def move_player(self, rowfrom: int, columnfrom: int, rowto: int, columnto: int):
        self.place_player(self.grid[rowfrom][columnfrom], rowto, columnto)
        self.erase_player(rowfrom, columnfrom)

        