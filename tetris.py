import os, sys
import random

#Variables Globales
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
VACIO = 0
PIEZA_EN_TRANSITO = 1
CONSOLIDADA = 2

#   Teniendo en cuenta lo que comentaste en las correcciones sobre que cosas como los diccionarios de puntajes, controles y teclas
#   convenía ponerlas dentro de la función main, se me ocurrio que tanto la lista de piezas como el diccionario de posibles rotaciones talvez convendría hacerlo,
#   pero no estoy seguro si esto sería eficiente ya que si por ejemplo pongo el diccionario de posibles rotaciones dentro de la funcion rotar, 
#   cada vez que llame a la funcion rotar se creará de nuevo el diccionario.
def pasar_str_a_tupla(pieza_str):
    """
    Esta función sirve para pasar las piezas almacenadas tanto en el archivo "piezas.txt" como las piezas almacenadas en el diccionario
    posibles_rotaciones. La función toma las coordenadas de una lista de tuplas que se encuentra en forma de string con el formato dado en el archivo piezas.txt
    y devuelve dichas coordenadas como una lista de tuplas.
    """
    pieza_str = (pieza_str.replace(";",",")).replace(" ","")
    
    temp = [] 
    for i in pieza_str.split(","):
        temp.append(i)
    
    resultado = [] 
    for i in range(len(temp)//2):
        x_celda = int(temp[i*2])
        y_celda = int(temp[i*2+1])
        celda = x_celda, y_celda
        resultado.append(celda)

    return resultado

PIEZAS = [] 
with open('piezas.txt') as piezas:
    for fila in piezas:
        fila = fila.split()         
        PIEZAS.append(tuple(pasar_str_a_tupla(fila[0])))

PIEZAS = (tuple(PIEZAS))

posibles_rotaciones = {} # Diccionario que contiene todas las posibles rotaciones que puede tener cada pieza.
with open('piezas.txt') as piezas:
    for fila in piezas:
        fila = fila.split()
        for i in range(len(fila)):
            if fila[i+1] == "#":
                posibles_rotaciones[fila[i]] = fila[0]
                break
            else:
                posibles_rotaciones[fila[i]] = fila[i+1]


#Funciones principales:

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    
    if pieza:
        return PIEZAS[pieza]
    else:
        return PIEZAS[random.randrange(len(PIEZAS))]

def trasladar_pieza(pieza_inicial, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    
    #Creo una funcion que permita trasladar cualquier tipo de pieza, incluso si la cantidad de celdas que ocupa dicha pieza
    #es distinta a la cantidad que tienen todas las piezas de tetris (4 celdas).
    pieza_trasladada = []
    for x, y in pieza_inicial:
        pieza_trasladada.append((x + dx, y + dy))
    
    #Convierto la lista resultante a una tupla de tuplas.
    return tuple(pieza_trasladada)

def rotar_pieza(juego):
    """
    Esta función toma una pieza dada por parámetro, la ordena, toma la primera posición de esa tupla ordenada y resta dicha primera posición a todas las tuplas para
    así trasladar toda la pieza al origen. Una vez que la pieza actual se encuentra en el origen, se busca la siguiente rotación en el diccionario "posibles rotaciones"
    y se traslada dicha rotación a la posición original de la pieza.
    """ 
    
    grilla = juego[1]
    pieza_ordenada = sorted(juego[0])
    pos1 = pieza_ordenada[0]
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -pos1[0], -pos1[1])
    siguiente_rotacion = buscar_rotacion(pieza_en_origen)
    nueva_posicion_pieza = trasladar_pieza(siguiente_rotacion, pos1[0], pos1[1])

    #for i in range(nueva_posicion_pieza)
    #Si la rotación es valida (no hay superficie consolidada en las celdas que ocupara la pieza rotada), devuelvo el nuevo estado del juego.
    if validez_rotacion(grilla, nueva_posicion_pieza):
        #Modifico la grilla del juego con la nueva posicion de la pieza.
        nueva_grilla = actualizar_grilla(0, juego[0], grilla)
        grilla_final = actualizar_grilla(1, nueva_posicion_pieza, nueva_grilla)
        return nueva_posicion_pieza, grilla_final
    return juego

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    
    columnas, filas = ANCHO_JUEGO, ALTO_JUEGO
    grilla = [[VACIO] * columnas for i in range(filas)] 
    pieza_actual = centrar_pieza(pieza_inicial)

    return pieza_actual, grilla

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return len(juego[1][0]), len(juego[1])

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    
    """
    
    return juego[0]
    
def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """

    # Recordemos que:
    # 0 = VACIO = Celda vacía.
    # 1 = PIEZA_EN_TRANSITO = Celda con fragmento de pieza en movimiento.
    # 2 = CONSOLIDADA = Celda con fragmento de superficie consolidada.

    if juego[1][y][x] == CONSOLIDADA:
        return True
    else:
        return False

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    pieza_actual = juego[0]
    grilla = juego[1]
    
    pieza_movida = []
    if validez_de_movimiento(pieza_actual, direccion, grilla) == True:
        pieza_movida.append(trasladar_pieza(pieza_actual, direccion, 0))
    else:
        pieza_movida.append(pieza_actual)
    
    return pieza_movida[0], grilla

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
    
    if terminado(juego) is True:
        return juego, False
    else:
        pieza = juego[0]
        siguiente_pieza_centrada = centrar_pieza(siguiente_pieza)
        grilla = juego[1]
        

        #Desciendo la pieza actual.
        pieza_descendida = trasladar_pieza(pieza, 0, 1)
        
        #Veo que sucede al descender la pieza. 
        if hay_colision(juego) is True: 
            # Elimino la pieza en transito de mi grilla.
            grilla = actualizar_grilla(VACIO, pieza, grilla)
            
            # Consolido las posiciones de pieza descendida.
            grilla = actualizar_grilla(CONSOLIDADA, pieza, grilla)
                
            # Verifico si al consolidar se han completado filas, y de ser así, las elimino y agrego la cantidad necesaria
            # de filas vacías en el inicio de la grilla.
            grilla = eliminar_filas(grilla)

            return (siguiente_pieza_centrada, grilla), True
             
        else:  
            # Elimino la posición actual de la pieza dentro de la grilla. 
            grilla = actualizar_grilla(VACIO, pieza, grilla)
                
            # Establezco la nueva posición de la pieza dentro de la grilla.
            grilla = actualizar_grilla(PIEZA_EN_TRANSITO, pieza_descendida, grilla)

            # Finalmente, devuelvo el el estado final del juego.
            return (pieza_descendida, grilla), False

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """

    pieza = juego[0]
    grilla = juego[1]


    # Creo una funcion que me permita verificar que todas las celdas que deberia ocupar la siguiente pieza
    # dentro de la grilla, esten desocupadas (que no contengan fragmentos de superficie consolidada). 
    for i in range(len(pieza)-1):
        celda = grilla[pieza[i][1]][pieza[i][0]]
        if celda == CONSOLIDADA:
            return True
    
    return False

    
#Funciones auxiliares: 

def centrar_pieza(pieza):
        """
        Esta función busca ubicar la posición de cada celda de la pieza,
        y devuelve valores dx y dy para trasladar la pieza en cuestión al centro de la grilla.
        """
        pieza_centrada = trasladar_pieza(pieza, (ANCHO_JUEGO//2), 0)
        return pieza_centrada
          
def agregar_un_valor_en_grilla(grilla, n, x, y):
    """
    Esta función se encarga de tomar un valor n dado por parametro y lo coloca en la posición x e y, tambien establecida por parámetro, dentro de la grilla.
    Finalmente, devuelve una nueva grilla con la modificación hecha.
    """
    
    grilla[y][x] = n
    grilla_nueva = []
    for filas in grilla:
        grilla_nueva.append(filas)
    return grilla_nueva

def validez_rotacion(grilla, pieza_rotada):
    """
    Esta es una función auxiliar que me permite verificar si la pieza puede ser rotada de la forma que el usuario pide, y de no ser así, devuelve la pieza a la posicion anterior a la rotacion.
    """
    
    for i in range(len(pieza_rotada)):
        celda = pieza_rotada[i]
        if celda[0] > ANCHO_JUEGO-1 or celda[0] < 0 or celda[1] < 0 or celda[1] > ALTO_JUEGO-1 or grilla[celda[1]][celda[0]] == CONSOLIDADA:
            return False      
    return True

def validez_de_movimiento(pieza, direccion, grilla):
    """
    Esta función se encarga de validar que un movimiento sea valido o no. Para que un movimiento sea valido, al mover una
    pieza tanto como a la derecha como a la izquierda, el resultado de dicho movimiento debe dejar a cada celda que compone
    a la pieza en una posición valida (dentro de la grilla) y donde no haya superficie consolidada.
    """
    
    resultado = []
    
    if direccion is DERECHA:
        for i in range(len(pieza)):
            celda = pieza[i]
            y, x = celda[1], celda[0]
            celda_en_grilla = grilla[y][x-1]
            if celda[0] < 0 or celda[0] > (ANCHO_JUEGO-2) or celda_en_grilla == CONSOLIDADA:
                return False    
        return True
         
    elif direccion is IZQUIERDA:
        for i in range(len(pieza)):
            celda = pieza[i]
            y, x = celda[1], celda[0]
            celda_en_grilla = grilla[y][x-1]
            if celda[0] < 1 or celda[0] > ANCHO_JUEGO or celda_en_grilla == CONSOLIDADA:
                return False    
        return True
 
def hay_colision(juego):
    """
    Esta función se encarga de tomar una pieza, la desciende una posición y verifica si al hacer ese movimiento, ocurre una colisión.

    Al mover nuestra pieza una celda hacia abajo pueden pasar 3 cosas:
        A) La pieza no colisiona con nada, por lo que el movimiento es valido.
        B) La pieza colisiona con superficie consolidada (intenta tomar una posición que ya esta ocupada por superficie)
        C) La pieza colisiona con el final de la grilla (intenta tomar una posición que no existe en la grilla, osea, cualquier Y >= ALTO_JUEGO).        

    A fines prácticos, como en las opciones B) y C) ocurre lo mismo hay una colisión, vamos a
    evaluar ambas posibilididades en la función, ya sea que la pieza colisionó con una superficie consolidada como
    si la pieza colisionó con el final de la grilla.
    """
    pieza = juego[0]
    grilla = juego[1]
    
    pieza_descendida = trasladar_pieza(pieza, 0, 1)

    # Busco que celdas contienen superficie en la grilla.
    superficie = []
    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            celda = grilla[i][j]
            posicion = j, i
            if celda == 2:
                superficie.append(posicion)

    # Veo si al descender la pieza, las coordenadas Y de alguna celda de la pieza se encuentran en el fondo de la grilla o si alguna celda de la pieza al ser descendida
    # tomaría el lugar de una celda de superficie. 

    
    for i in range(len(pieza_descendida)):
        if pieza_descendida[i][1] == (ALTO_JUEGO) or pieza_descendida[i] in superficie:
            return True
    return False

def hay_colision_lateral(juego, direccion):
    """
    Esta función se encarga de tomar una pieza, la mueve una posición hacia la derecha o izquierda y verifica si al hacer ese movimiento, ocurre una colisión.

    Al mover nuestra pieza una celda hacia abajo pueden pasar 3 cosas:
        A) La pieza no colisiona con nada, por lo que el movimiento es valido.
        B) La pieza colisiona con superficie consolidada (intenta tomar una posición que ya esta ocupada por superficie)
        C) La pieza colisiona con el final de la grilla (intenta tomar una posición que no existe en la grilla, osea, cualquier Y >= ALTO_JUEGO).        

    A fines prácticos, como en las opciones B) y C) ocurre lo mismo hay una colisión, vamos a
    evaluar ambas posibilididades en la función, ya sea que la pieza colisionó con una superficie consolidada como
    si la pieza colisionó con el final de la grilla.
    """
    pieza = juego[0]
    grilla = juego[1]
    
    pieza_trasladada = trasladar_pieza(pieza, direccion, 0)

    # Busco que celdas contienen superficie en la grilla.
    superficie = []
    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            celda = grilla[i][j]
            posicion = j, i
            if celda == CONSOLIDADA:
                superficie.append(posicion)

    # Veo si al descender la pieza, las coordenadas Y de alguna celda de la pieza se encuentran en el fondo de la grilla o si alguna celda de la pieza al ser descendida
    # tomaría el lugar de una celda de superficie. 

    
    for i in range(len(pieza_trasladada)):
        if pieza_trasladada[i] in superficie:
            return True
    return False

def eliminar_filas(grilla):
    """
    Esta función busca eliminar filas de la matriz donde cada celda que compone dicha fila contenga un fragmento de la superficie consolidada.
    """
    
    for i in range(len(grilla)):
        fila = grilla[i]
        fila_llena = ([CONSOLIDADA]*ANCHO_JUEGO)
        if fila == fila_llena:
            grilla.pop(i)
            grilla.insert(0, [VACIO]*ANCHO_JUEGO)
            
            
    return grilla

def actualizar_grilla(n, pieza, grilla):
    """
    Esta función está basada en agregar_un_valor_en_grilla, y sirve para actualizar el estado del juego dentro de la grilla. 
    
    La función recibe como parámetros la grilla a la que se le aplicarán los cambios, la pieza que será la tupla de coordenadas donde haremos 
    los cambios y un valor n que será el estado al cual se cambiarán las celdas que componen la pieza.

    Recordemos que el estado del juego se almacena en la grilla del juego, y cada celda de dicha grilla tiene 3 estados posibles:
    - 0 = Celda vacía.
    - 1 = Celda con fragmento de pieza en movimiento.
    - 2 = Celda con fragmento de superficie consolidada.

    Un ejemplo de su uso puede ser cuando queremos consolidar una pieza, trasaladar una pieza en transito una posición hacia abajo, entre otros usos.
    """
    for i in range(len(pieza)):
        agregar_un_valor_en_grilla(grilla, n, pieza[i][0], pieza[i][1])

    return grilla

def buscar_rotacion(pieza_en_origen):
    """
    Esta función toma una pieza dada por parámetro y verifica en el diccionario que contiene las posibles rotaciones de cada pieza (llamado "posibles_rotaciones")
    cual sería su siguiente rotación y devuelve dicha lista de tuplas. 
    """ 
    pieza = pasar_lista_de_tuplas_a_str(pieza_en_origen)
    siguiente_rotacion = posibles_rotaciones[pieza]
    resultado = pasar_str_a_tupla(siguiente_rotacion)
    
    return tuple(resultado)
        
def pasar_lista_de_tuplas_a_str(pieza):
    """
    Esta función vendría a ser la inversa de pasar_str_a_tupla (función auxiliar de Tetris.py), ya que toma una pieza dada por parámetro en la forma de lista de tuplas y la transforma
    en una string con el formato adecuado para que pueda ser comparado con los valores de el diccionario posibles_rotaciones.
    """
    resultado = ";".join("%s,%s" % tupla for tupla in pieza)
    
    return resultado 