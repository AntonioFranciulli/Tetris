import gamelib
import csv
import tetris

ESPERA_DESCENDER = 12
ANCHO_INTERFAZ = 400
ALTO_INTERFAZ = 400
ANCHO_TABLERO = 180
ALTO_TABLERO = 360
MARGEN_VERTICAL = 20
MARGEN_LATERAL = 110
ANCHO_BOTON = 125 # Ancho en pixeles de la imagen que utilizo como botón
ALTO_BOTON = 63 # Alto en pixeles de la imagen que utilizo como botón

# Funciones auxiliares
def buscar_pieza_en_grilla(n, grilla):
    """
    Esta función se encarga de buscar un elemento n dado por parámetro, dentro de la grilla actual, tambien dada por 
    parámetro, y devuelve las coordenadas X e Y de nuestra grilla en las que se encuentra dicho valor. 
    """
    resultado = []
    for fila in range(len(grilla)):
        for columna in range(len(grilla[fila])):
                posicion = columna, fila
                if grilla[fila][columna] == n:
                    resultado.append(posicion)
     
    return resultado 


# Funciones Principales   
def guardar_partida(juego, siguiente_pieza, cambiar_pieza, puntaje):
    """
    Esta función se encarga de guardar el estado actual del juego, la siguiente pieza, si se debe cambiar la pieza o no y el puntaje que lleva el usuario.
    Cada variable se guardará en una linea del archivo "ultimapartida.txt".
    """
    with open("ultimapartida.txt", 'w') as file:
        partida = '{}\n{}\n{}\n{}'.format(juego, siguiente_pieza, cambiar_pieza, puntaje)
        file.write(partida)

def guardar_puntuaciones(tabla_de_puntuaciones, ruta):
    """
    Esta función se encarga de tomar la nueva tabla de puntuaciones actualizada según lo que sucedió en la última partida, y guarda la información en
    el archivo "puntajes.csv".
    """
    with open("puntajes.csv", 'w') as file:
        for i in range(len(tabla_de_puntuaciones)):
            nombre, puntaje = tabla_de_puntuaciones[i][0], tabla_de_puntuaciones[i][1]
            puntaje = '{},{}\n'.format(nombre, puntaje)
            file.write(puntaje)

def modificar_puntuaciones(puntajes_historicos, puntaje):
    """
    Esta función se encarga de, una vez finalizado el juego, tomar el puntaje que obtuvo el jugador y devuelve el estado actual de las puntuaciones
    historicas. 
    
    Si no había información de 10 jugadores o más, agregará el nombre y el puntaje del jugador a la lista. En el caso de que haya roto el
    record de alguno de los top 10, tomará su lugar en la lista. Si no pasa ninguna de estas cosas, el puntaje no se guardará.

    Otra posible implementación de esta función es una lista enlazada la cual sería más rapida a la hora de realizar los cambios. Sin embargo,
    como en este caso solo vamos a guardar los puntajes de los 10 mejores jugadores, es mucho menos engorroso realizar esta implementación.
    """
    if len(puntajes_historicos) < 10:
        nombre = gamelib.input('¿Cuál es tu nombre?')
        tupla = puntaje, nombre
        puntajes_historicos.append(list(tupla))
        puntajes_historicos.sort(key=lambda x:x[0], reverse=True)
        return puntajes_historicos
    elif len(puntajes_historicos) == 10:
        for i in range(len(puntajes_historicos)):
            if puntaje > puntajes_historicos[i][0]:
                nombre = gamelib.input('¿Cuál es tu nombre?')
                tupla = puntaje, nombre
                puntajes_historicos.append(list(tupla))
                puntajes_historicos.sort(key=lambda x:x[0], reverse=True)
                puntajes = puntajes_historicos[0:10]
                return puntajes
        return puntajes_historicos

def cargar_partida(ruta):
    """
    Esta función se encarga de revisar el archivo "ultimapartida.txt" y devuelve el estado del juego de la última partida guardada.
    """
    with open(ruta, 'r') as file:
        
        juego = file.readline()
        siguiente_pieza = file.readline()
        cambiar_pieza = file.readline()
        puntaje = file.readline()
        return eval(juego), eval(siguiente_pieza), eval(cambiar_pieza), eval(puntaje)

def iniciar_juego(ruta, x, y):
    """
    Esta función se encarga de tomar las coordenadas X e Y donde el usuario hizo click en la pantalla de incio del juego, para luego realizar la acción
    correspondiente al botón que haya presionado. 
    """
    
    x_click = int(x) 
    y_click = int(y) 

    #Verifico donde clickeó el usuario y realizo la acción correspondiente

    if (x_click >= 55 and x_click <= 180) and (y_click >= 280 and y_click <= 343):
        #Creo un nuevo juego inicial.
        juego, cambiar_pieza = tetris.crear_juego(tetris.generar_pieza()), False
        siguiente_pieza = tetris.generar_pieza()
        puntaje = 0
        return juego, siguiente_pieza, cambiar_pieza, puntaje
        
    elif (x_click >= 220 and x_click <= 345) and (y_click >= 280 and y_click <= 343):
        #Cargo la información de la última partida guardada.
        juego, siguiente_pieza, cambiar_pieza, puntaje = cargar_partida("ultimapartida.txt") 
        return juego, siguiente_pieza, cambiar_pieza, puntaje

def jugar_de_nuevo():
    #Creo un nuevo juego inicial.
    juego, cambiar_pieza = tetris.crear_juego(tetris.generar_pieza()), False
    siguiente_pieza = tetris.generar_pieza()
    puntaje = 0
    return juego, siguiente_pieza, cambiar_pieza, puntaje

def controles(posibles_controles, tecla, juego, cambiar_pieza, siguiente_pieza, puntaje):
    """
    Esta función recibe la tecla que fue presionada y un diccionario que contiene lo que hacen las distintas teclas al ser clickeadas.
    
    Se encarga de tomar la tecla clickeada por el usuario, revisa a que función hace referencia dicha tecla en dicho diccionario
    y devuelve cual es la accion que corresponde a la tecla presionada.
    """
    try:
        accion = posibles_controles[tecla]
        
        if accion == 'DERECHA':
            # El usuario movió la pieza hacia la derecha, verifico si dada su posición en la grilla puede hacerlo y de ser así, la muevo..
            if not tetris.hay_colision_lateral(juego, tetris.DERECHA):
                juego_con_pieza_movida = tetris.mover(juego, tetris.DERECHA)
                return juego_con_pieza_movida, siguiente_pieza, cambiar_pieza, puntaje
            return juego, siguiente_pieza, cambiar_pieza, puntaje

        elif accion == 'IZQUIERDA':
            # El jugador movió la pieza hacia la izquierda, verifico si dada su posición en la grilla puede hacerlo y de ser así, la muevo.
            if not tetris.hay_colision_lateral(juego, tetris.IZQUIERDA):
                juego_con_pieza_movida = tetris.mover(juego, tetris.IZQUIERDA)
                return juego_con_pieza_movida, siguiente_pieza, cambiar_pieza, puntaje
            return juego, siguiente_pieza, cambiar_pieza, puntaje

        elif accion == 'DESCENDER':
            # El jugador movió la pieza hacia la abajo para acelerar el descenso de la misma, 
            # lo cual le sumará 2 puntos a su puntaje por cada celda que decida mover hacia abajo.
            juego, descender_cambia_pieza = tetris.avanzar(juego, siguiente_pieza)
            puntaje += 2
            return juego, siguiente_pieza, descender_cambia_pieza, puntaje   

        elif accion == 'ROTAR':
            # El jugador rotó la pieza hacia su proxima rotación, verifico si dada su posición en la grilla puede hacerlo y de ser así, la muevo..
            juego_con_pieza_rotada = tetris.rotar_pieza(juego)
            return juego_con_pieza_rotada, siguiente_pieza, cambiar_pieza, puntaje

        elif accion == 'GUARDAR':
            # El jugador decidió guardar el estado de su actual partida.
            guardar_partida(juego, siguiente_pieza, cambiar_pieza, puntaje)
            return juego, siguiente_pieza, cambiar_pieza, puntaje

        elif accion == 'CARGAR':
            # El jugador decidió cargar la última partida que ha guardado para continuarla.
            juego, siguiente_pieza, cambiar_pieza, puntaje = cargar_partida("ultimapartida.txt")
            return juego, siguiente_pieza, cambiar_pieza, puntaje

    except KeyError:
        return juego, siguiente_pieza, cambiar_pieza, puntaje

    
# Funciones de dibujado
def dibujar_juego(juego):
    """
    Esta función se encarga de dibujar la grilla del juego, la superficie consolidada y la posición actual de la pieza.
    """

    #Dibujo los bordes del juego.
    gamelib.draw_polygon([0, 0, 0, ALTO_INTERFAZ, ANCHO_INTERFAZ, ALTO_INTERFAZ, ANCHO_INTERFAZ, 0], fill='black')
    gamelib.draw_polygon([MARGEN_LATERAL, MARGEN_VERTICAL, ANCHO_INTERFAZ-MARGEN_LATERAL, MARGEN_VERTICAL, ANCHO_INTERFAZ-MARGEN_LATERAL, ALTO_INTERFAZ-MARGEN_VERTICAL, MARGEN_LATERAL, ALTO_INTERFAZ-MARGEN_VERTICAL], outline='white', fill='black')
    
    #Dibujo columnas.
    for i in range(1, tetris.ANCHO_JUEGO):
        gamelib.draw_line(MARGEN_LATERAL+i*MARGEN_VERTICAL, MARGEN_VERTICAL+1, MARGEN_LATERAL+i*MARGEN_VERTICAL, ALTO_INTERFAZ-MARGEN_VERTICAL, fill='grey', width=1)
        
    #Dibujo filas.
    for i in range(1, tetris.ALTO_JUEGO):
        gamelib.draw_line(MARGEN_LATERAL+1, MARGEN_VERTICAL+i*MARGEN_VERTICAL, ANCHO_INTERFAZ-MARGEN_LATERAL, MARGEN_VERTICAL+i*MARGEN_VERTICAL, fill='grey', width=1)

    #Dibujo superficie consolidada.
    superficie_consolidada = buscar_pieza_en_grilla(2, juego[1])
    for i in range(len(superficie_consolidada)):
        x_celda = superficie_consolidada[i][0]
        y_celda = superficie_consolidada[i][1]
        gamelib.draw_polygon([MARGEN_LATERAL+1+MARGEN_VERTICAL*x_celda, MARGEN_VERTICAL+1+MARGEN_VERTICAL*y_celda, (MARGEN_LATERAL+MARGEN_VERTICAL)+MARGEN_VERTICAL*x_celda, MARGEN_VERTICAL+1+MARGEN_VERTICAL*y_celda, (MARGEN_LATERAL+MARGEN_VERTICAL)+MARGEN_VERTICAL*x_celda, (MARGEN_VERTICAL*2)+MARGEN_VERTICAL*y_celda, MARGEN_LATERAL+MARGEN_VERTICAL*x_celda, (MARGEN_VERTICAL*2)+MARGEN_VERTICAL*y_celda], fill = 'red')

    #Dibujo pieza en transito.
    pieza_en_transito = juego[0]
    for i in range(len(pieza_en_transito)):
        x_celda = pieza_en_transito[i][0]
        y_celda = pieza_en_transito[i][1]
        gamelib.draw_polygon([MARGEN_LATERAL+1+MARGEN_VERTICAL*x_celda, MARGEN_VERTICAL+1+MARGEN_VERTICAL*y_celda, (MARGEN_LATERAL+MARGEN_VERTICAL)+MARGEN_VERTICAL*x_celda, MARGEN_VERTICAL+1+MARGEN_VERTICAL*y_celda, (MARGEN_LATERAL+MARGEN_VERTICAL)+MARGEN_VERTICAL*x_celda, (MARGEN_VERTICAL*2)+MARGEN_VERTICAL*y_celda, MARGEN_LATERAL+MARGEN_VERTICAL*x_celda, (MARGEN_VERTICAL*2)+MARGEN_VERTICAL*y_celda], fill = 'blue')

def dibujar_puntaje(puntaje):
    """
    Esta función se encarga de mostrar el puntaje que lleva acumulado el jugador en pantalla.
    """
    #Dibujo puntaje:
    gamelib.draw_text('Puntaje:', 345, 140, size=12)
    gamelib.draw_text(puntaje, 345, 170, size=20)

def dibujar_pantalla_de_inicio():
    """
    Esta función se encarga de dibujar la pantalla de inicio del juego. A partir de ella, el jugador podrá iniciar una partida nueva o cargar la última partida guardada.
    """
    gamelib.draw_image('media/Tetris_logo.gif', 64, 30)
    gamelib.draw_text('Bienvenido', ANCHO_INTERFAZ//2, 250)

    #Dibujo los botones
    gamelib.draw_image('media/botonazul.gif',55, 280)
    gamelib.draw_text('Jugar', 115, 310)
    gamelib.draw_image('media/botonrosa.gif', 220, 280)
    gamelib.draw_text('Cargar', 285, 300)
    gamelib.draw_text('partida', 285, 320)

def dibujar_siguiente_pieza(siguiente_pieza):
    """
    Esta función se encarga de tomar la siguiente pieza que se colocará en el tetris y dibujarla pantalla. 
    """
    #Posicion inicial de la pieza
    x0, y0 = 25, 170
    
    #Ancho y alto de cada celda
    ANCHO = MARGEN_VERTICAL # Recordemos que margen vertical = 20
    ALTO = MARGEN_VERTICAL # Recordemos que margen vertical = 20

    #Dibujo siguiente pieza.
    gamelib.draw_text('Próxima', 55, 140, size=12)
    gamelib.draw_text('pieza:', 55, 155, size=12)
    for i in range(len(siguiente_pieza)):
        x = siguiente_pieza[i][0]
        y = siguiente_pieza[i][1]
        #gamelib.draw_rectangle(MARGEN_LATERAL+20*x_celda, ALTO_INTERFAZ-MARGEN_VERTICAL*1.5+MARGEN_VERTICAL*y_celda, 45+MARGEN_VERTICAL*x_celda, 190+MARGEN_VERTICAL*y_celda, outline = 'white', fill = 'green')
        gamelib.draw_polygon([x0+20*x, y0+ALTO*y, x0+ANCHO*x, y0+ALTO+ALTO*y, x0+ANCHO+ANCHO*x, y0+ALTO+ALTO*y,45+ANCHO*x, 170+ALTO*y], outline = 'white', fill = 'green')  #MARGEN_VERTICAL*2.25+MARGEN_VERTICAL*x_celda, ALTO_INTERFAZ-(MARGEN_VERTICAL*0.5)+MARGEN_VERTICAL*y_celda

def dibujar_game_over(puntaje, puntajes_historicos):
    """
    Esta función dibuja en pantalla un cartel que indica game over en pantalla una vez que ha terminado el juego.
    """
    POSICION_GAME_OVER = (ANCHO_INTERFAZ//2, (ALTO_INTERFAZ//4)-MARGEN_VERTICAL)
    POSICION_BOTON_1 = (55, 235)
    POSICION_TEXTO_BOTON_1 = (115, 267)
    POSICION_BOTON_2 = (220, 235)
    POSICION_TEXTO_BOTON_2 = (285, 257)
    MARGEN_VERTICAL_TITULO_TABLA = 50
    
    gamelib.draw_begin()
    gamelib.draw_polygon([0, 0, 0, ALTO_INTERFAZ, ANCHO_INTERFAZ, ALTO_INTERFAZ, ANCHO_INTERFAZ, 0], fill='black')
    gamelib.draw_text('GAME OVER', ANCHO_INTERFAZ//2, MARGEN_VERTICAL+(MARGEN_VERTICAL//2), size = 20, fill = 'red')
    gamelib.draw_text('Puntaje: {}'.format(puntaje), ANCHO_INTERFAZ//2, 2.5*MARGEN_VERTICAL+(MARGEN_VERTICAL//2), size = 18)
    gamelib.draw_text('Top 10:', ANCHO_INTERFAZ//2, MARGEN_VERTICAL_TITULO_TABLA+MARGEN_VERTICAL*2, size = 14, fill = 'white')
    gamelib.draw_end()   
    
    
    gamelib.draw_begin
    for i in range(len(puntajes_historicos)):
        jugador = '{} - {}\n'.format(puntajes_historicos[i][0], puntajes_historicos[i][1])
        gamelib.draw_text(jugador, ANCHO_INTERFAZ//2, ANCHO_INTERFAZ//3 + MARGEN_VERTICAL*i-5, size = 12)
    gamelib.draw_end()   
    
    gamelib.draw_begin
    gamelib.draw_image('media/botonazul.gif', (ANCHO_INTERFAZ//2) - (ANCHO_BOTON//2), (ANCHO_INTERFAZ//4)*3+MARGEN_VERTICAL)
    gamelib.draw_text('Volver', ANCHO_INTERFAZ//2, (ANCHO_INTERFAZ//4)*3+MARGEN_VERTICAL+MARGEN_VERTICAL)
    gamelib.draw_text('a jugar', ANCHO_INTERFAZ//2, (ANCHO_INTERFAZ//4)*3+MARGEN_VERTICAL*2+MARGEN_VERTICAL)
    gamelib.draw_end()   
    

#Función principal
def main(): 
    # Inicializar el estado del juego
    gamelib.resize(400, 400)
    gamelib.title("Tetris++")
    gamelib.play_sound('media/tetristheme.wav')
    
    posibles_controles = {} # Diccionario que contiene las distintas teclas que el juego debe interpretar y la acción asociada a dichas teclas.
    with open('teclas.txt') as teclas:
        for fila in teclas:
            if fila != "\n":
                fila = fila.strip().split(' = ')
                if fila[0] in posibles_controles:
                    posibles_controles[fila[0]].append(fila[1])
                else:
                    posibles_controles[fila[0]] = fila[1]

    timer_bajar = ESPERA_DESCENDER

    while gamelib.is_alive():

        gamelib.draw_begin()
        dibujar_pantalla_de_inicio()
        gamelib.draw_end() 

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()
        
        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break
        
        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            try:
                juego, siguiente_pieza, cambiar_pieza, puntaje = iniciar_juego('ultimapartida.txt', x, y)
                while gamelib.loop(fps=30):   
                    for event in gamelib.get_events():
                        if event.type == gamelib.EventType.KeyPress:
                            #El Usuario presionó una tecla, hago la acción correspondiente
                            tecla = event.key
                            juego, siguiente_pieza, cambiar_pieza, puntaje = controles(posibles_controles, tecla, juego, cambiar_pieza, siguiente_pieza, puntaje)
                            gamelib.draw_begin() 
                            dibujar_juego(juego)
                            gamelib.draw_end() 

                    #Si el juego no esta terminado, sigue el juego.
                    if tetris.terminado(juego) is False:
                        if cambiar_pieza is True:
                            siguiente_pieza = tetris.generar_pieza()
                            juego, cambiar_pieza = juego, False
                            
                        timer_bajar -= 1
                        if timer_bajar == 0:
                            timer_bajar = ESPERA_DESCENDER
                            # Descender la pieza automáticamente
                            juego, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
                            puntaje += 1

                        gamelib.draw_begin() 
                        dibujar_juego(juego)
                        dibujar_puntaje(puntaje)
                        dibujar_siguiente_pieza(siguiente_pieza)
                        gamelib.draw_end()

                    #Si el juego terminó, muestro los mejores puntajes y si se logró un nuevo record pregunto al usuario su nombre.
                    else: 
                        puntajes_historicos = [] # Lista de tuplas que contiene los mejores 10 puntajes que se han registrado en el juego.
                        with open('puntajes.csv', newline='') as archivo:
                            puntajes = csv.reader(archivo, delimiter=',')
                            for persona in puntajes:
                                tupla = int(persona[0]), persona[1]
                                puntajes_historicos.append(list(tupla))

                        puntajes_historicos.sort(key=lambda x:x[0], reverse=True)

                        puntajes = modificar_puntuaciones(puntajes_historicos, puntaje)
                        guardar_puntuaciones(puntajes, "puntajes.csv")
                        dibujar_game_over(puntaje, puntajes)

                        X_BOTON = (ANCHO_INTERFAZ//2) - (ANCHO_BOTON//2)
                        Y_BOTON = (ANCHO_INTERFAZ//4)*3 + MARGEN_VERTICAL

                        #Una vez en la pantalla final, espero para ver si el jugador quiere jugar nuevamente o cerrar el juego.
                        ev = gamelib.wait(gamelib.EventType.ButtonPress)
                        if ev.type == gamelib.EventType.ButtonPress:
                            x, y = ev.x, ev.y 
                            try:
                                if (x >= X_BOTON and x <= X_BOTON+ANCHO_BOTON) and (y >= Y_BOTON and y <= Y_BOTON+ALTO_BOTON):
                                    #Creo un nuevo juego inicial.
                                    juego, siguiente_pieza, cambiar_pieza, puntaje = jugar_de_nuevo()
                            except AttributeError:
                                pass

                        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
                            # El usuario presionó la tecla Escape, cerrar la aplicación.
                            break

            except TypeError:
                pass
            
gamelib.init(main)