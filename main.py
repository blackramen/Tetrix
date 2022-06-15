from random import * 
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T
)


def generar_pieza(pieza = None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
  if pieza is None:
    return PIEZAS[randrange(len(PIEZAS))]
  return PIEZAS[pieza]


def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_nueva = []
    for x, y in pieza:
      pieza_nueva.append((x + dx, y + dy))
    return tuple(pieza_nueva)


def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    generar_pieza(). Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
  grilla = crear_grilla(ANCHO_JUEGO, ALTO_JUEGO)
  pieza_actual = trasladar_pieza(pieza_inicial,5,0)
  terminado = False
  return grilla, pieza_actual, terminado

def crear_grilla(ancho, alto):
    tablero = []
    longitud = []
    for _ in range(ancho):
        longitud.append(0)
    for _ in range(alto):
        tablero.append(longitud)
    return tablero


def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return (len(juego[0][0]),len(juego[0]))
    

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """ 
    pieza_actual = []
    grilla = juego[0]
    for y in range (ALTO_JUEGO):
        for x in range (ANCHO_JUEGO):
            if grilla[y][x] == 1:
                pieza_actual.append((x,y)) 
    return pieza_actual
    

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    if juego[x][y] == 1:
      return True
    return False 

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    grilla = juego[0]
    pieza_movida = trasladar_pieza(juego[1], direccion, 0)
    for x, y in pieza_movida:
        if grilla[y][x] == 2:
            return juego[0], juego[1], juego[2]
    for i in range(len(pieza_movida)):
        if 0 >= pieza_movida[i][0] >= 8:
            return juego[0], juego[1], juego[2]        
    return grilla, pieza_movida, 

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.
    
    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    avanzar = trasladar_pieza(juego[1],0, 1)
    for x,y in avanzar:
      if 
    return # tupla (nuevo_estado, cambiar_pieza)
 
def terminado(juego):

    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """

    return "???"




from csv import list_dialects
from random import *
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T
)
def prueba1(matriz):
    piezaRandom = randrange(len(matriz))
    pieza = matriz[piezaRandom]
    return pieza

def prueba1_1(matriz):
    pieza = list(prueba1(matriz))
    pocicion1 = list(pieza[0])
    pocicion2 = list(pieza[1])
    pocicion3 = list(pieza[2])
    pocicion4 = list(pieza[3])
    lista = [pocicion1, pocicion2, pocicion3, pocicion4]
    return lista

def prueba1_2(matriz, dx, dy):
    lista = prueba1_1(matriz)
    acum = 0
    while acum == 0 or acum % 2 == 0:
        for i in range(0, 4):
            for x in range(0,1):
                lista[i][x] = lista[i][x] + dx
            #print(lista)
        acum += 1
    acum = 0
    while acum == 0 or acum % 2 == 0:
        for i in range(0, 4):
            for x in range(1,2):
                lista[i][x] = lista[i][x] + dy
            #print(lista)
        acum += 1

    return lista

def prueba1_3(matriz, dx, dy):
    pieza = tuple(prueba1_2(matriz, dx, dy))
    pocicion1 = tuple(pieza[0])
    pocicion2 = tuple(pieza[1])
    pocicion3 = tuple(pieza[2])
    pocicion4 = tuple(pieza[3])
    return pocicion1, pocicion2, pocicion3, pocicion4

def prueba2(matriz, dx, dy):
    res = prueba1_2(matriz, dx, dy)
    print(res)

def prueba3(alto, ancho):
    tablero = []
    altura = []
    longitud = []
    for i in range(alto):
        altura.append(0)
    for l in range(ancho):
        longitud.append(0)

    for j in range(alto):
        tablero.append(longitud)
    print(tablero)



    

    

def main():
    prueba2(PIEZAS, 4, 18)
    prueba3(ALTO_JUEGO, ANCHO_JUEGO)
main()


print("rometrolo")