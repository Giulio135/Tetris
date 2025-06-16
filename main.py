import keyboard
import time
import copy

class Pieza():

    # Representa todas las formas que puede tener la pieza
    FORMAS = {
        'I': [[(0,0), (1,0), (2,0), (3,0)]],
        'O': [[(0,0), (1,0), (0,1), (1,1)]],
        'T': [[(0,0), (-1,1), (0,1), (1,1)]],
        'L': [[(0,0), (0,1), (0,2), (1,2)]],
        'J': [[(0,0), (0,1), (0,2), (-1,2)]],
        'S': [[(0,1), (1,1), (-1,0), (0,0)]],
        'Z': [[(0,1), (-1,1), (0,0), (1,0)]]
    }

    def __init__(self, tipo, x, y):
        self.tipo = tipo
        self.rotacion = 0
        self.x = x
        self.y = y
    
    def coordenadas(self):
        ''' Devuelve las coordenadas actualizadas de la pieza'''
        # Almacena la forma de la pieza
        forma = Pieza.FORMAS[self.tipo][self.rotacion]
        # Actualiza las posiciones de la pieza con self.x y self.y
        return [(self.x + dx, self.y + dy) for dx, dy in forma]

    def mover(self, direccion):
        self.x += direccion[0]
        self.y += direccion[1]

class Tetris():
    def __init__(self):
        self.width = 10
        self.height= 20
        self.board = [['' for _ in range(self.width)] for _ in range(self.height)]
        self.piezas_quietas = copy.deepcopy(self.board)
        self.pieza_actual = None
        self.nueva_pieza('Z')
        
    def nueva_pieza(self, tipo):
        self.pieza_actual = Pieza(tipo, self.width // 2, y = 0)
    def colocar_pieza(self, pieza):
        for x, y in pieza.coordenadas():
            if 0 <= x < self.width and 0 <= y < self.height:
                self.board[y][x] = []
    def mostrar_tablero(self):
        for fila in self.board:
            print(fila)
        print('\n')
    def loop(self):
        # Vaciar el tablero menos con las piezas quietas
        self.board = copy.deepcopy(self.piezas_quietas)

        # Si al aumentar la y uno más no se pasa, mueve la pieza 
        if all(y + 1 < self.height for x, y in self.pieza_actual.coordenadas()):
            self.pieza_actual.mover([0,1])
        # sino la añade a piezas quietas y crea una nueva pieza
        else:
            for x, y in self.pieza_actual.coordenadas():
                self.piezas_quietas[y][x] = []
            self.board = copy.deepcopy(self.piezas_quietas)
            self.nueva_pieza('T')

        # Coloca la pieza
        self.colocar_pieza(self.pieza_actual)

        # Mostrar el tablero actualizado
        self.mostrar_tablero()
        time.sleep(0.2)

partida = Tetris()
for i in range(20):
    partida.loop()
