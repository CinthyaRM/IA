import mysql.connector

class Puzzle8:

    def __init__(self):
        self.board = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
        self.blank = (1, 1)
        self.movimientos = 0
        self.movimientos_realizados = []

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="movimientos"
        )
        self.cursor = self.db.cursor()

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))

    def is_valid_move(self, move):
        new_blank = (self.blank[0] + move[0], self.blank[1] + move[1])
        return 0 <= new_blank[0] < 3 and 0 <= new_blank[1] < 3

    def make_move(self, move):
        move_mapping = {
            'arriba': (-1, 0),
            'abajo': (1, 0),
            'izquierda': (0, -1),
            'derecha': (0, 1)
        }
        
        if move in move_mapping:
            move_texto = move
            move = move_mapping[move]
            new_blank = (self.blank[0] + move[0], self.blank[1] + move[1])
            self.board[self.blank[0]][self.blank[1]], self.board[new_blank[0]][new_blank[1]] = self.board[new_blank[0]][new_blank[1]], self.board[self.blank[0]][self.blank[1]]
            self.blank = new_blank
            self.movimientos += 1
            self.movimientos_realizados.append(move_texto)

            # Guarda el movimiento en la base de datos
            self.guardar_movimiento(move_texto)

    def guardar_movimiento(self, movimiento):
        sql = "INSERT INTO movimientoss (movimiento) VALUES (%s)"
        val = (movimiento, )
        self.cursor.execute(sql, val)
        self.db.commit()

    def imprimir_estado_inicial_7(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 7:
                    print(f"Coordenadas iniciales del valor 7 ({i}, {j}).")

    def imprimir_estado_final_7(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 7:
                    print(f"Coordenadas finales del valor 7 ({i}, {j}).")

    def play(self):
        self.imprimir_estado_inicial_7()
        while True:
            self.print_board()
            move = input("Ingresa un movimiento (arriba/izquierda/abajo/derecha, s para salir): ")
            if move == 's':
                break
            elif move in ['arriba', 'abajo', 'izquierda', 'derecha']:
                self.make_move(move)
            else:
                print("Entrada no válida. Usa arriba/izquierda/abajo/derecha o s para salir.")

            if self.board == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                print("Puzzle resuelto:")
                self.print_board()
                print("¡Felicidades! Resolviste el rompecabezas☺")
                print(f"Costo total de los movimientos realizados: {self.movimientos}")
                self.imprimir_estado_final_7()
                break

    def imprimir_movimientos(self):
        print("Movimientos realizados:")
        for move in self.movimientos_realizados:
            print(move)

if __name__ == "__main__":
    puzzle = Puzzle8()
    puzzle.play()
