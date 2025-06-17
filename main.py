import keyboard, time, copy, random

class Pieza():

    # Representa todas las formas que puede tener la pieza
    FORMAS = {
        'I': [
            [(0,0), (1,0), (2,0), (3,0)],      # 0° horizontal
            [(2,-1), (2,0), (2,1), (2,2)],     # 90° vertical
            [(0,1), (1,1), (2,1), (3,1)],      # 180° horizontal (shifted)
            [(1,-1), (1,0), (1,1), (1,2)]      # 270° vertical (shifted)
        ],
        'O': [
            [(0,0), (1,0), (0,1), (1,1)],      # Siempre igual (cuadrado)
            [(0,0), (1,0), (0,1), (1,1)],
            [(0,0), (1,0), (0,1), (1,1)],
            [(0,0), (1,0), (0,1), (1,1)]
        ],
        'T': [
            [(0,0), (-1,1), (0,1), (1,1)],     # 0°
            [(0,0), (0,1), (1,0), (0,-1)],     # 90°
            [(0,0), (-1,0), (0,-1), (1,0)],    # 180°
            [(0,0), (0,1), (-1,0), (0,-1)]     # 270°
        ],
        'L': [
            [(0,0), (0,1), (0,2), (1,2)],      # 0°
            [(0,0), (1,0), (2,0), (0,1)],      # 90°
            [(0,0), (-1,0), (0,-1), (0,-2)],   # 180°
            [(0,0), (0,-1), (-1,-1), (-2,-1)]  # 270°
        ],
        'J': [
            [(0,0), (0,1), (0,2), (-1,2)],     # 0°
            [(0,0), (1,0), (2,0), (2,1)],      # 90°
            [(0,0), (1,0), (0,-1), (0,-2)],    # 180°
            [(0,0), (0,-1), (-1,-1), (-2,-1)]  # 270°
        ],
        'S': [
            [(0,1), (1,1), (-1,0), (0,0)],     # 0°
            [(0,0), (0,1), (1,1), (1,2)],      # 90°
            [(0,1), (1,1), (-1,0), (0,0)],     # 180° igual que 0°
            [(0,0), (0,1), (1,1), (1,2)]       # 270° igual que 90°
        ],
        'Z': [
            [(0,1), (-1,1), (0,0), (1,0)],     # 0°
            [(1,0), (1,1), (0,1), (0,2)],      # 90°
            [(0,1), (-1,1), (0,0), (1,0)],     # 180° igual que 0°
            [(1,0), (1,1), (0,1), (0,2)]       # 270° igual que 90°
        ]
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
        self.nueva_pieza(random.choice(['L','J','O','Z','S','T','I']))
        
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
    def puede_mover(self, dx, dy, rotar=False):
        # Intenta mover (y opcionalmente rotar) sin modificar realmente la pieza
        rotacion_actual = self.pieza_actual.rotacion
        if rotar:
            nueva_rotacion = (rotacion_actual + 1) % len(Pieza.FORMAS[self.pieza_actual.tipo])
            forma = Pieza.FORMAS[self.pieza_actual.tipo][nueva_rotacion]
        else:
            forma = Pieza.FORMAS[self.pieza_actual.tipo][rotacion_actual]

        for x0, y0 in forma:
            x = self.pieza_actual.x + dx + x0
            y = self.pieza_actual.y + dy + y0
            if not (0 <= x < self.width and 0 <= y < self.height):
                return False
            if self.piezas_quietas[y][x] != '':
                return False
        return True
    def controlar_teclas(self):
        nueva_rotacion = False
        if keyboard.is_pressed('up'):
            nueva_rotacion = True

        if self.puede_mover(1,0):
            if keyboard.is_pressed('right'):
                self.pieza_actual.mover([1,0])
        if self.puede_mover(-1,0):
            if keyboard.is_pressed('left'):
                self.pieza_actual.mover([-1,0])
        if self.puede_mover(1,0,True) and self.puede_mover(-1,0,True) and nueva_rotacion:
            self.pieza_actual.rotacion = (self.pieza_actual.rotacion + 1) % len(Pieza.FORMAS[self.pieza_actual.tipo])
               
    
    def loop(self):
        # Vaciar el tablero menos con las piezas quietas
        self.board = copy.deepcopy(self.piezas_quietas)

        self.controlar_teclas()

        # Si al aumentar la y uno más no se pasa, mueve la pieza 
        if self.puede_mover(0,1):
            self.pieza_actual.mover([0,1])
        # sino la añade a piezas quietas y crea una nueva pieza
        else:
            for x, y in self.pieza_actual.coordenadas():
                self.piezas_quietas[y][x] = []
            self.board = copy.deepcopy(self.piezas_quietas)
            self.nueva_pieza(random.choice(['L','J','O','Z','S','T','I']))

        for i, line in enumerate(self.board):
            if all(lugar != '' for lugar in line):
                del self.board[i]
                self.board.insert(0, ['' for _ in range(self.width)])
        # Coloca la pieza
        self.colocar_pieza(self.pieza_actual)

        # Mostrar el tablero actualizado
        self.mostrar_tablero()
        time.sleep(0.2)

partida = Tetris()
for i in range(1000):
    partida.loop()
